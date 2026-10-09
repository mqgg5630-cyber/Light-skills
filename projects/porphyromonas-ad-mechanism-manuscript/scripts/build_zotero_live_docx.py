#!/usr/bin/env python3
"""Build and audit a Zotero-live DOCX through Pandoc and Better BibTeX.

This is a strict implementation of the capability/probe sequence in
hajimi-kun/latex-to-word-workflow v3.0.0. It never substitutes formatted static
citation text when the live-field bridge is unavailable. The resulting file is
still a pre-refresh candidate: desktop Word with the Zotero add-in must refresh
its citation fields and insert/update the bibliography before acceptance.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT = ROOT / "quality_reports" / "zotero_live_status.json"
FILTER_URL = "https://retorque.re/zotero-better-bibtex/exporting/zotero.lua"
RPC = "http://127.0.0.1:23119/better-bibtex/json-rpc"


def cited_keys(text: str) -> list[str]:
    heading = "## References" if "## References" in text else "## 参考文献"
    body = text.split(heading, 1)[0]
    return list(dict.fromkeys(re.findall(r"@([A-Za-z0-9_.:+-]+)", body)))


def bbt_search(query: str) -> list[dict]:
    payload = json.dumps(
        {"jsonrpc": "2.0", "method": "item.search", "params": [query], "id": 1}
    ).encode()
    request = urllib.request.Request(
        RPC, data=payload, headers={"Content-Type": "application/json"}
    )
    with urllib.request.build_opener(urllib.request.ProxyHandler({})).open(
        request, timeout=5
    ) as response:
        result = json.load(response)
    if "error" in result:
        raise RuntimeError(result["error"])
    return result.get("result", [])


def obtain_filter(explicit: Path | None, directory: Path) -> Path:
    if explicit:
        if not explicit.is_file():
            raise FileNotFoundError(explicit)
        return explicit
    target = directory / "zotero.lua"
    with urllib.request.urlopen(FILTER_URL, timeout=30) as response:
        target.write_bytes(response.read())
    return target


def live_fields(path: Path) -> tuple[int, str]:
    with zipfile.ZipFile(path) as archive:
        xml = archive.read("word/document.xml").decode("utf-8", errors="replace")
    return xml.count("ADDIN ZOTERO_ITEM CSL_CITATION"), xml


def source_without_static_references(text: str) -> str:
    heading = "## References" if "## References" in text else "## 参考文献"
    body = text.split(heading, 1)[0].rstrip()
    # Zotero's Word add-in will insert the bibliography after Refresh. Keeping
    # the heading prevents accidental retention of a parallel static list.
    return body + "\n\n" + heading + "\n"


def write_report(path: Path, report: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--reference-doc", type=Path)
    parser.add_argument("--zotero-filter", type=Path)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--style", default="vancouver")
    args = parser.parse_args()

    source = args.input.resolve()
    output = args.output.resolve()
    report_path = args.report.resolve()
    text = source.read_text(encoding="utf-8")
    keys = cited_keys(text)
    pandoc = shutil.which("pandoc")
    diagnostics: list[str] = []
    if not keys:
        diagnostics.append("No Pandoc-style citation keys were found in the manuscript body.")

    bbt_connected = False
    bbt_first_key_found = False
    if keys:
        try:
            matches = bbt_search(keys[0])
            bbt_connected = True
            bbt_first_key_found = bool(matches)
            if not matches:
                diagnostics.append(f"Better BibTeX did not find the real key: {keys[0]}")
        except Exception as exc:
            diagnostics.append(f"Better BibTeX probe failed: {exc}")
    if not pandoc:
        diagnostics.append("Pandoc is not available on PATH.")

    report = {
        "schema": "local.zotero_live_status.v1",
        "input": str(source.relative_to(ROOT)) if source.is_relative_to(ROOT) else str(source),
        "requested_output": str(output.relative_to(ROOT)) if output.is_relative_to(ROOT) else str(output),
        "citation_key_count": len(keys),
        "first_citation_key": keys[0] if keys else None,
        "pandoc_available": bool(pandoc),
        "better_bibtex_connected": bbt_connected,
        "better_bibtex_first_key_found": bbt_first_key_found,
        "filter_source": str(args.zotero_filter) if args.zotero_filter else FILTER_URL,
        "diagnostics": diagnostics,
        "acceptance_state": "setup gate",
        "zotero_live_field_count": 0,
        "output_created": False,
    }
    if diagnostics:
        write_report(report_path, report)
        print(report_path)
        for message in diagnostics:
            print(message, file=sys.stderr)
        return 2

    with tempfile.TemporaryDirectory(prefix="zotero-live-") as raw_temp:
        temp = Path(raw_temp)
        try:
            zotero_filter = obtain_filter(args.zotero_filter.resolve() if args.zotero_filter else None, temp)
        except Exception as exc:
            report["diagnostics"].append(f"Official zotero.lua filter could not be obtained: {exc}")
            write_report(report_path, report)
            print(report_path)
            return 2

        metadata = f"---\nzotero:\n  csl-style: {args.style}\n---\n\n"
        probe_source = temp / "probe.md"
        probe_source.write_text(metadata + f"Probe citation [@{keys[0]}].\n", encoding="utf-8")
        probe_docx = temp / "probe.docx"
        probe_command = [
            pandoc, str(probe_source), "-f", "markdown+citations", "-t", "docx",
            f"--lua-filter={zotero_filter}", "-o", str(probe_docx),
        ]
        if args.reference_doc:
            probe_command.insert(-2, f"--reference-doc={args.reference_doc.resolve()}")
        probe = subprocess.run(probe_command, text=True, capture_output=True)
        report["probe_command"] = probe_command
        report["probe_returncode"] = probe.returncode
        report["probe_stderr"] = probe.stderr
        if probe.returncode != 0 or not probe_docx.is_file():
            report["diagnostics"].append("The one-citation semantic bridge probe failed.")
            write_report(report_path, report)
            print(report_path)
            return 2
        probe_fields, probe_xml = live_fields(probe_docx)
        report["probe_live_field_count"] = probe_fields
        report["probe_contains_expected_key"] = keys[0] in probe_xml
        if probe_fields != 1 or keys[0] not in probe_xml:
            report["diagnostics"].append(
                "The probe did not contain one ADDIN ZOTERO_ITEM CSL_CITATION field with the expected key."
            )
            write_report(report_path, report)
            print(report_path)
            return 2

        live_source = temp / "manuscript.md"
        live_source.write_text(metadata + source_without_static_references(text), encoding="utf-8")
        candidate = temp / "candidate.docx"
        command = [
            pandoc, str(live_source), "-f", "markdown+citations", "-t", "docx",
            f"--lua-filter={zotero_filter}", "-o", str(candidate),
        ]
        if args.reference_doc:
            command.insert(-2, f"--reference-doc={args.reference_doc.resolve()}")
        run = subprocess.run(command, text=True, capture_output=True)
        report["build_command"] = command
        report["build_returncode"] = run.returncode
        report["build_stderr"] = run.stderr
        if run.returncode != 0 or not candidate.is_file():
            report["diagnostics"].append("The full Zotero-live candidate build failed.")
            write_report(report_path, report)
            print(report_path)
            return 2
        fields, xml = live_fields(candidate)
        missing_keys = [key for key in keys if key not in xml]
        expected_clusters = len(re.findall(r"\[@[^\]]+\]", source_without_static_references(text)))
        report.update({
            "zotero_live_field_count": fields,
            "expected_citation_cluster_count": expected_clusters,
            "missing_citation_keys": missing_keys,
        })
        if fields != expected_clusters or missing_keys:
            report["diagnostics"].append("The full live-field audit did not match the source citation inventory.")
            write_report(report_path, report)
            print(report_path)
            return 2
        output.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(candidate, output)
        report["output_created"] = True
        report["acceptance_state"] = "pending user action"
        write_report(report_path, report)
        print(output)
        print(report_path)
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
