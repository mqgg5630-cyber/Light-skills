#!/usr/bin/env python3
"""Dependency-free DOCX structural extractor for this manuscript project.

The extractor preserves body order, emits paragraph/table locators, records
styles and image relationships, and copies embedded media. It does not render
Word pages, evaluate fields, or read tracked changes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import zipfile
from pathlib import Path, PurePosixPath
import xml.etree.ElementTree as ET

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
REL = "http://schemas.openxmlformats.org/package/2006/relationships"
WP = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
PIC = "http://schemas.openxmlformats.org/drawingml/2006/picture"
CP = "http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
DC = "http://purl.org/dc/elements/1.1/"
DCTERMS = "http://purl.org/dc/terms/"

NS = {"w": W, "r": R, "rel": REL, "wp": WP, "a": A, "pic": PIC}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def q(ns: str, name: str) -> str:
    return f"{{{ns}}}{name}"


def attr(el: ET.Element | None, ns: str, name: str, default: str = "") -> str:
    return default if el is None else el.attrib.get(q(ns, name), default)


def paragraph_text(p: ET.Element) -> str:
    out: list[str] = []
    for el in p.iter():
        if el.tag in {q(W, "t"), q(W, "delText"), q(W, "instrText")}:
            out.append(el.text or "")
        elif el.tag == q(W, "tab"):
            out.append("\t")
        elif el.tag in {q(W, "br"), q(W, "cr")}:
            out.append("\n")
    return "".join(out).strip()


def paragraph_style(p: ET.Element, styles: dict[str, dict[str, object]]) -> dict[str, object]:
    ppr = p.find("w:pPr", NS)
    style_id = attr(ppr.find("w:pStyle", NS) if ppr is not None else None, W, "val")
    style = styles.get(style_id, {})
    outline_el = ppr.find("w:outlineLvl", NS) if ppr is not None else None
    outline = attr(outline_el, W, "val")
    if not outline:
        outline = str(style.get("outline", ""))
    numpr = ppr.find("w:numPr", NS) if ppr is not None else None
    num_id = attr(numpr.find("w:numId", NS) if numpr is not None else None, W, "val")
    ilvl = attr(numpr.find("w:ilvl", NS) if numpr is not None else None, W, "val")
    return {
        "style_id": style_id,
        "style_name": style.get("name", ""),
        "outline_level": int(outline) if outline.isdigit() else None,
        "numbering_id": num_id or None,
        "numbering_level": int(ilvl) if ilvl.isdigit() else None,
    }


def image_refs(p: ET.Element, relationships: dict[str, str]) -> list[dict[str, str]]:
    refs: list[dict[str, str]] = []
    alt_names = [
        (el.attrib.get("name", "") or el.attrib.get("descr", ""))
        for el in p.findall(".//wp:docPr", NS)
    ]
    for idx, blip in enumerate(p.findall(".//a:blip", NS)):
        rid = blip.attrib.get(q(R, "embed"), "")
        refs.append(
            {
                "relationship_id": rid,
                "target": relationships.get(rid, ""),
                "alt": alt_names[idx] if idx < len(alt_names) else "",
            }
        )
    return refs


def load_styles(zf: zipfile.ZipFile) -> dict[str, dict[str, object]]:
    if "word/styles.xml" not in zf.namelist():
        return {}
    root = ET.fromstring(zf.read("word/styles.xml"))
    styles: dict[str, dict[str, object]] = {}
    for style in root.findall("w:style", NS):
        style_id = attr(style, W, "styleId")
        name = attr(style.find("w:name", NS), W, "val")
        based_on = attr(style.find("w:basedOn", NS), W, "val")
        outline_el = style.find("w:pPr/w:outlineLvl", NS)
        outline = attr(outline_el, W, "val")
        styles[style_id] = {
            "name": name,
            "based_on": based_on,
            "outline": int(outline) if outline.isdigit() else None,
        }
    return styles


def load_relationships(zf: zipfile.ZipFile) -> dict[str, str]:
    name = "word/_rels/document.xml.rels"
    if name not in zf.namelist():
        return {}
    root = ET.fromstring(zf.read(name))
    return {
        rel.attrib.get("Id", ""): rel.attrib.get("Target", "")
        for rel in root.findall(q(REL, "Relationship"))
    }


def load_properties(zf: zipfile.ZipFile) -> dict[str, str]:
    name = "docProps/core.xml"
    if name not in zf.namelist():
        return {}
    root = ET.fromstring(zf.read(name))
    fields = {
        "title": q(DC, "title"),
        "subject": q(DC, "subject"),
        "creator": q(DC, "creator"),
        "description": q(DC, "description"),
        "created": q(DCTERMS, "created"),
        "modified": q(DCTERMS, "modified"),
        "last_modified_by": q(CP, "lastModifiedBy"),
    }
    return {key: (root.find(tag).text or "") for key, tag in fields.items() if root.find(tag) is not None}


def table_record(
    tbl: ET.Element,
    table_index: int,
    styles: dict[str, dict[str, object]],
) -> dict[str, object]:
    rows: list[list[str]] = []
    cell_details: list[dict[str, object]] = []
    for r_idx, tr in enumerate(tbl.findall("w:tr", NS), 1):
        row: list[str] = []
        for c_idx, tc in enumerate(tr.findall("w:tc", NS), 1):
            paras = tc.findall("w:p", NS)
            texts = [paragraph_text(p) for p in paras if paragraph_text(p)]
            text = " / ".join(texts)
            row.append(text)
            cell_details.append(
                {
                    "locator": f"table:{table_index},row:{r_idx},cell:{c_idx}",
                    "paragraphs": [
                        {
                            "text": paragraph_text(p),
                            **paragraph_style(p, styles),
                        }
                        for p in paras
                    ],
                }
            )
        rows.append(row)
    return {
        "type": "table",
        "locator": f"table:{table_index}",
        "rows": rows,
        "cells": cell_details,
    }


def safe_stem(path: Path) -> str:
    return re.sub(r"[^0-9A-Za-z._\-\u4e00-\u9fff]+", "_", path.stem).strip("_")


def extract(source: Path, out_dir: Path) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = safe_stem(source)
    media_dir = out_dir / "media" / stem
    media_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(source) as zf:
        styles = load_styles(zf)
        relationships = load_relationships(zf)
        properties = load_properties(zf)
        root = ET.fromstring(zf.read("word/document.xml"))
        body = root.find("w:body", NS)
        if body is None:
            raise ValueError("DOCX document body is missing")

        blocks: list[dict[str, object]] = []
        p_index = 0
        t_index = 0
        for block_index, child in enumerate(list(body), 1):
            if child.tag == q(W, "p"):
                p_index += 1
                blocks.append(
                    {
                        "type": "paragraph",
                        "block_index": block_index,
                        "locator": f"paragraph:{p_index}",
                        "text": paragraph_text(child),
                        **paragraph_style(child, styles),
                        "images": image_refs(child, relationships),
                    }
                )
            elif child.tag == q(W, "tbl"):
                t_index += 1
                rec = table_record(child, t_index, styles)
                rec["block_index"] = block_index
                blocks.append(rec)

        media: list[dict[str, object]] = []
        for name in sorted(zf.namelist()):
            if not name.startswith("word/media/") or name.endswith("/"):
                continue
            filename = PurePosixPath(name).name
            target = media_dir / filename
            with zf.open(name) as src, target.open("wb") as dst:
                shutil.copyfileobj(src, dst)
            media.append(
                {
                    "archive_path": name,
                    "output_path": str(target),
                    "size_bytes": target.stat().st_size,
                    "sha256": sha256(target),
                }
            )

    record = {
        "schema": "project.docx_extraction.v1",
        "source": str(source),
        "source_sha256": sha256(source),
        "limitations": [
            "Dependency-free XML extraction; pagination was not rendered.",
            "Tracked changes, comments, and field evaluation are not interpreted.",
            "Image semantics require separate visual review.",
        ],
        "properties": properties,
        "paragraph_count": p_index,
        "table_count": t_index,
        "media": media,
        "blocks": blocks,
    }

    json_path = out_dir / f"{stem}.structure.json"
    json_path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")

    md: list[str] = [
        f"# {source.name}",
        "",
        f"- Source SHA-256: `{record['source_sha256']}`",
        f"- Paragraphs: {p_index}",
        f"- Tables: {t_index}",
        f"- Embedded media: {len(media)}",
        "- Extraction note: body-order XML extraction; page boundaries are unavailable.",
        "",
    ]
    for block in blocks:
        if block["type"] == "paragraph":
            text = str(block["text"])
            if not text and not block["images"]:
                continue
            style_note = ", ".join(
                part
                for part in [
                    f"style={block['style_name'] or block['style_id']}" if (block["style_name"] or block["style_id"]) else "",
                    f"outline={block['outline_level']}" if block["outline_level"] is not None else "",
                ]
                if part
            )
            md.append(f"<!-- {block['locator']}{'; ' + style_note if style_note else ''} -->")
            if text:
                md.append(text)
            for image in block["images"]:
                md.append(f"[IMAGE target={image['target']} alt={image['alt']}]")
            md.append("")
        else:
            md.append(f"## [{block['locator']}]")
            rows = block["rows"]
            max_cols = max((len(row) for row in rows), default=0)
            if max_cols:
                normalized = [row + [""] * (max_cols - len(row)) for row in rows]
                md.append("| " + " | ".join(normalized[0]) + " |")
                md.append("| " + " | ".join(["---"] * max_cols) + " |")
                for row in normalized[1:]:
                    md.append("| " + " | ".join(row) + " |")
            md.append("")

    md_path = out_dir / f"{stem}.extracted.md"
    md_path.write_text("\n".join(md), encoding="utf-8")
    return md_path, json_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("sources", nargs="+", type=Path)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    for source in args.sources:
        md, js = extract(source, args.out_dir)
        print(f"{source.name}\t{md}\t{js}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
