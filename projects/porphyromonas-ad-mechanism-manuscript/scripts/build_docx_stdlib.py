#!/usr/bin/env python3
"""Dependency-free Markdown-to-DOCX builder for the manuscript deliverables.

Supported Markdown: headings, paragraphs, simple emphasis/code spans, Pandoc-style
citation keys, pipe tables, numbered/bulleted items, and local PNG images. The standard
builder resolves citation keys to cached numbered text from a BibTeX file; genuine
Zotero fields require the separate Zotero/Better BibTeX bridge. The output is an OOXML
package that can be opened in Microsoft Word or LibreOffice. ZIP member metadata is
stable; passing ``--timestamp`` also fixes core metadata for byte-reproducible output.
Rendering is not performed here.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from html import escape
from pathlib import Path
import re
import struct
import zipfile

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
WP = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
PIC = "http://schemas.openxmlformats.org/drawingml/2006/picture"
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)


def zip_member(zf: zipfile.ZipFile, name: str, data: str | bytes) -> None:
    """Write a DOCX member with stable ZIP metadata for reproducible builds."""
    info = zipfile.ZipInfo(name, date_time=ZIP_TIMESTAMP)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    info.external_attr = 0o100644 << 16
    payload = data.encode("utf-8") if isinstance(data, str) else data
    zf.writestr(info, payload)


def x(text: str) -> str:
    return escape(text, quote=True)


def bibtex_doi_to_key(path: Path) -> dict[str, str]:
    """Return normalized DOI -> citekey mappings from a conventional BibTeX file."""
    text = path.read_text(encoding="utf-8")
    entries = re.finditer(
        r"(?ms)^@[A-Za-z]+\{([^,]+),(.*?)(?=^@[A-Za-z]+\{|\Z)",
        text,
    )
    mapping: dict[str, str] = {}
    for entry in entries:
        key, fields = entry.groups()
        doi = re.search(r"(?mi)^\s*doi\s*=\s*[\{\"]([^\}\"]+)", fields)
        if doi:
            normalized = doi.group(1).strip().lower().rstrip(".")
            if normalized in mapping and mapping[normalized] != key.strip():
                raise ValueError(f"Duplicate DOI in BibTeX: {normalized}")
            mapping[normalized] = key.strip()
    return mapping


def manuscript_citation_numbers(md_path: Path, bib_path: Path | None) -> dict[str, int]:
    """Map Pandoc citekeys to the manuscript's numbered reference-list entries."""
    text = md_path.read_text(encoding="utf-8")
    if "[@" not in text:
        return {}
    if bib_path is None:
        raise ValueError(f"Pandoc-style citations require --bibliography: {md_path}")
    doi_to_key = bibtex_doi_to_key(bib_path)
    mapping: dict[str, int] = {}
    reference_lines = re.findall(r"(?m)^(\d+)\.\s.*?doi:(10\.\d{4,9}/\S+)", text)
    for raw_number, raw_doi in reference_lines:
        doi = raw_doi.rstrip(".,;:)]}").lower()
        key = doi_to_key.get(doi)
        if key is None:
            raise ValueError(f"Reference DOI not found in BibTeX: {doi} ({md_path})")
        mapping[key] = int(raw_number)
    cited_keys = set(re.findall(r"@([A-Za-z0-9_.:+-]+)", text.split("## References", 1)[0].split("## 参考文献", 1)[0]))
    missing = sorted(cited_keys - set(mapping))
    if missing:
        raise ValueError(f"Cited keys are absent from the numbered reference list: {missing}")
    return mapping


def render_number_cluster(numbers: list[int]) -> str:
    """Render sorted citation numbers with consecutive values compressed to ranges."""
    values = sorted(set(numbers))
    groups: list[str] = []
    i = 0
    while i < len(values):
        start = values[i]
        end = start
        while i + 1 < len(values) and values[i + 1] == end + 1:
            i += 1
            end = values[i]
        groups.append(str(start) if start == end else f"{start}–{end}")
        i += 1
    return "[" + ",".join(groups) + "]"


def citation_text(raw: str, citation_numbers: dict[str, int]) -> str:
    keys = re.findall(r"@([A-Za-z0-9_.:+-]+)", raw)
    unknown = [key for key in keys if key not in citation_numbers]
    if unknown:
        raise ValueError(f"Unknown citation keys: {unknown}")
    return render_number_cluster([citation_numbers[key] for key in keys])


def png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()[:24]
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"Only PNG images are supported: {path}")
    return struct.unpack(">II", data[16:24])


def run_xml(text: str, *, bold=False, italic=False, code=False, size=None, color=None) -> str:
    if not text:
        return ""
    props = []
    if bold:
        props.append("<w:b/>")
    if italic:
        props.append("<w:i/>")
    if code:
        props.append('<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:eastAsia="等线"/>')
        props.append('<w:shd w:val="clear" w:color="auto" w:fill="F2F4F7"/>')
    if size:
        props.append(f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>')
    if color:
        props.append(f'<w:color w:val="{color}"/>')
    rpr = f"<w:rPr>{''.join(props)}</w:rPr>" if props else ""
    space = ' xml:space="preserve"' if text[:1].isspace() or text[-1:].isspace() else ""
    return f"<w:r>{rpr}<w:t{space}>{x(text)}</w:t></w:r>"


def inline_runs(text: str, *, base_size=None, citation_numbers: dict[str, int] | None = None) -> str:
    # Keep this intentionally conservative: no nested emphasis or Markdown links.
    token = re.compile(r"(\[@[^\]]+\]|\*\*.+?\*\*|(?<!\*)\*[^*]+?\*(?!\*)|`[^`]+?`)")
    out = []
    pos = 0
    for match in token.finditer(text):
        if match.start() > pos:
            out.append(run_xml(text[pos:match.start()], size=base_size))
        raw = match.group(0)
        if raw.startswith("[@"):
            if citation_numbers is None:
                raise ValueError("Citation markup found without a citation-number map")
            out.append(run_xml(citation_text(raw, citation_numbers), size=base_size))
        elif raw.startswith("**"):
            out.append(run_xml(raw[2:-2], bold=True, size=base_size))
        elif raw.startswith("*"):
            out.append(run_xml(raw[1:-1], italic=True, size=base_size))
        else:
            out.append(run_xml(raw[1:-1], code=True, size=base_size))
        pos = match.end()
    if pos < len(text):
        out.append(run_xml(text[pos:], size=base_size))
    return "".join(out)


def para_xml(text: str, style="Normal", *, align=None, indent=None, keep=False, page_break_before=False, base_size=None, citation_numbers=None) -> str:
    ppr = [f'<w:pStyle w:val="{style}"/>']
    if align:
        ppr.append(f'<w:jc w:val="{align}"/>')
    if indent:
        ppr.append(f'<w:ind w:left="{indent}" w:hanging="{indent}"/>')
    if keep:
        ppr.append("<w:keepNext/>")
    if page_break_before:
        ppr.append("<w:pageBreakBefore/>")
    return f"<w:p><w:pPr>{''.join(ppr)}</w:pPr>{inline_runs(text, base_size=base_size, citation_numbers=citation_numbers)}</w:p>"


def image_para(rel_id: str, path: Path, docpr_id: int, alt: str) -> str:
    width_px, height_px = png_size(path)
    max_cx = 6_150_000  # approximately 6.72 inches
    cx = max_cx
    cy = int(cx * height_px / width_px)
    max_cy = 7_600_000
    if cy > max_cy:
        cy = max_cy
        cx = int(cy * width_px / height_px)
    drawing = f"""
<w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0">
  <wp:extent cx="{cx}" cy="{cy}"/><wp:effectExtent l="0" t="0" r="0" b="0"/>
  <wp:docPr id="{docpr_id}" name="Figure {docpr_id}" descr="{x(alt)}"/>
  <wp:cNvGraphicFramePr><a:graphicFrameLocks noChangeAspect="1"/></wp:cNvGraphicFramePr>
  <a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
    <pic:pic><pic:nvPicPr><pic:cNvPr id="0" name="{x(path.name)}"/><pic:cNvPicPr/></pic:nvPicPr>
    <pic:blipFill><a:blip r:embed="{rel_id}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>
    <pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic>
  </a:graphicData></a:graphic>
</wp:inline></w:drawing></w:r>"""
    return f'<w:p><w:pPr><w:pStyle w:val="Figure"/><w:jc w:val="center"/><w:keepNext/></w:pPr>{drawing}</w:p>'


def make_sect_pr(orientation: str = "portrait", clean_manuscript: bool = False) -> str:
    header_footer_refs = (
        ""
        if clean_manuscript
        else '<w:headerReference w:type="default" r:id="rId4"/>'
        '<w:footerReference w:type="default" r:id="rId5"/>'
    )
    margin = 1440 if clean_manuscript else 1134
    line_pitch = 480 if clean_manuscript else 312
    if orientation == "landscape":
        pg_sz = '<w:pgSz w:w="16838" w:h="11906" w:orient="landscape"/>'
    else:
        pg_sz = '<w:pgSz w:w="11906" w:h="16838"/>'
    return (
        f'<w:sectPr>{header_footer_refs}{pg_sz}'
        f'<w:pgMar w:top="{margin}" w:right="{margin}" w:bottom="{margin}" w:left="{margin}" '
        'w:header="600" w:footer="600" w:gutter="0"/><w:cols w:space="720"/>'
        f'<w:docGrid w:linePitch="{line_pitch}"/></w:sectPr>'
    )


def is_table_caption_line(lines: list[str], idx: int) -> bool:
    line = lines[idx].rstrip()
    if not (line.startswith("**Table") or line.startswith("**表")):
        return False
    j = idx + 1
    while j < len(lines) and not lines[j].strip():
        j += 1
    if j < len(lines) and lines[j].strip().startswith("|"):
        return True
    return False


def has_more_tables_ahead(lines: list[str], idx: int) -> bool:
    j = idx
    while j < len(lines) and not lines[j].strip():
        j += 1
    if j < len(lines):
        line = lines[j].strip()
        if line.startswith("|") or is_table_caption_line(lines, j):
            return True
    return False


def table_xml(
    rows: list[list[str]],
    citation_numbers: dict[str, int] | None = None,
    base_size: int = 17,
    is_landscape: bool = False,
) -> str:
    """Build a journal-style three-line table: top, header-bottom, and final-bottom."""
    cols = max(len(r) for r in rows) if rows else 0
    rows = [r + [""] * (cols - len(r)) for r in rows]
    total = 13958 if is_landscape else 9360
    colw = max(500, total // cols) if cols else total
    grid = "".join(f'<w:gridCol w:w="{colw}"/>' for _ in range(cols))
    tr_xml = []
    for ri, row in enumerate(rows):
        cells = []
        for cell in row:
            header_rule = (
                '<w:tcBorders><w:bottom w:val="single" w:sz="8" '
                'w:space="0" w:color="000000"/></w:tcBorders>'
                if ri == 0 else ""
            )
            tcpr = (
                f'<w:tcPr><w:tcW w:w="{colw}" w:type="dxa"/>{header_rule}'
                '<w:vAlign w:val="center"/></w:tcPr>'
            )
            table_line = 240 if base_size >= 20 else 220
            ppr = f'<w:pPr><w:pStyle w:val="TableText"/><w:spacing w:before="0" w:after="0" w:line="{table_line}" w:lineRule="auto"/></w:pPr>'
            content = inline_runs(cell.strip(), base_size=base_size, citation_numbers=citation_numbers)
            cells.append(f'<w:tc>{tcpr}<w:p>{ppr}{content}</w:p></w:tc>')
        trpr = '<w:trPr><w:tblHeader/></w:trPr>' if ri == 0 else ""
        tr_xml.append(f'<w:tr>{trpr}{"".join(cells)}</w:tr>')
    borders = (
        '<w:top w:val="single" w:sz="12" w:space="0" w:color="000000"/>'
        '<w:left w:val="nil"/><w:bottom w:val="single" w:sz="12" '
        'w:space="0" w:color="000000"/><w:right w:val="nil"/>'
        '<w:insideH w:val="nil"/><w:insideV w:val="nil"/>'
    )
    tblpr = (
        '<w:tblPr><w:tblStyle w:val="ThreeLineTable"/><w:tblW w:w="5000" w:type="pct"/>'
        f'<w:tblLayout w:type="fixed"/><w:tblBorders>{borders}</w:tblBorders>'
        '<w:tblCellMar><w:top w:w="70" w:type="dxa"/><w:left w:w="80" w:type="dxa"/>'
        '<w:bottom w:w="70" w:type="dxa"/><w:right w:w="80" w:type="dxa"/>'
        '</w:tblCellMar></w:tblPr>'
    )
    return f'<w:tbl>{tblpr}<w:tblGrid>{grid}</w:tblGrid>{"".join(tr_xml)}</w:tbl>'


def split_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_separator(line: str) -> bool:
    cells = split_table_row(line)
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", c.replace(" ", "")) for c in cells)


def parse_markdown(
    md_path: Path,
    *,
    section_page_breaks: bool = True,
    bibliography: Path | None = None,
    reject_images: bool = False,
    journal_body: bool = False,
    landscape_tables: bool = False,
    clean_manuscript: bool = False,
):
    lines = md_path.read_text(encoding="utf-8").splitlines()
    citation_numbers = manuscript_citation_numbers(md_path, bibliography)
    body = []
    images: dict[Path, str] = {}
    image_order: list[Path] = []
    rel_counter = 10
    docpr_id = 1
    i = 0
    first_h2 = True
    current_h2 = ""
    current_orientation = "portrait"
    while i < len(lines):
        line = lines[i].rstrip()
        if not line:
            i += 1
            continue
        if line.startswith("<!-- PAGEBREAK -->"):
            body.append('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')
            i += 1
            continue
        image = re.fullmatch(r"!\[(.*?)\]\((.*?)\)", line.strip())
        if image:
            if reject_images:
                raise ValueError(f"Image markup is prohibited for clean manuscripts: {md_path}:{i + 1}")
            alt, raw_path = image.groups()
            img_path = (md_path.parent / raw_path).resolve()
            if img_path not in images:
                images[img_path] = f"rId{rel_counter}"
                image_order.append(img_path)
                rel_counter += 1
            body.append(image_para(images[img_path], img_path, docpr_id, alt))
            docpr_id += 1
            i += 1
            continue
        if landscape_tables and is_table_caption_line(lines, i):
            if current_orientation == "portrait":
                body.append(f'<w:p><w:pPr>{make_sect_pr("portrait", clean_manuscript)}</w:pPr></w:p>')
                current_orientation = "landscape"
            body.append(para_xml(line, "Caption", citation_numbers=citation_numbers))
            i += 1
            continue
        if line.startswith("|") and i + 1 < len(lines) and is_separator(lines[i + 1]):
            if landscape_tables and current_orientation == "portrait":
                body.append(f'<w:p><w:pPr>{make_sect_pr("portrait", clean_manuscript)}</w:pPr></w:p>')
                current_orientation = "landscape"
            rows = [split_table_row(line)]
            i += 2
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                rows.append(split_table_row(lines[i]))
                i += 1
            body.append(table_xml(rows, citation_numbers, base_size=20 if journal_body else 17, is_landscape=(landscape_tables and current_orientation == "landscape")))
            body.append('<w:p><w:pPr><w:spacing w:after="40"/></w:pPr></w:p>')
            if landscape_tables and not has_more_tables_ahead(lines, i):
                body.append(f'<w:p><w:pPr>{make_sect_pr("landscape", clean_manuscript)}</w:pPr></w:p>')
                current_orientation = "portrait"
            continue
        heading = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading:
            level = len(heading.group(1))
            text = heading.group(2).strip()
            style = f"Heading{min(level, 4)}"
            page_break = False
            if level == 2:
                current_h2 = text
                page_break = section_page_breaks and not first_h2
                first_h2 = False
            body.append(para_xml(text, style, keep=True, page_break_before=page_break, citation_numbers=citation_numbers))
            i += 1
            continue
        if re.match(r"^\d+\.\s+", line):
            body.append(para_xml(line, "Reference", indent="360", base_size=24 if journal_body else 18, citation_numbers=citation_numbers))
            i += 1
            continue
        if re.match(r"^[-*]\s+", line):
            body.append(para_xml("• " + re.sub(r"^[-*]\s+", "", line), "ListParagraph", indent="360", citation_numbers=citation_numbers))
            i += 1
            continue
        # Clean submission manuscripts use a two-character-equivalent (24 pt,
        # 480 twip) first-line indent for main-text paragraphs. Abstract text,
        # headings, keywords, captions, references, and tables remain flush left.
        style = "BodyText" if journal_body and current_h2 not in ("Abstract", "摘要") else "Normal"
        if line.startswith("**Table") or line.startswith("**表") or line.startswith("**Figure") or line.startswith("**图"):
            style = "Caption"
        elif line.startswith("**Article type") or line.startswith("**Draft status") or line.startswith("**文章类型") or line.startswith("**稿件状态") or line.startswith("**Bilingual"):
            style = "Note"
        elif line.startswith("**Keywords") or line.startswith("**关键词"):
            style = "Keywords"
        body.append(para_xml(line, style, citation_numbers=citation_numbers))
        i += 1
    return "".join(body), images, image_order


def legacy_styles_xml() -> str:
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="{W}">
  <w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="宋体" w:cs="Times New Roman"/><w:sz w:val="22"/><w:szCs w:val="22"/><w:lang w:val="en-US" w:eastAsia="zh-CN"/></w:rPr></w:rPrDefault>
  <w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="276" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr></w:pPrDefault></w:docDefaults>
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/><w:pPr><w:widowControl/></w:pPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:keepNext/><w:keepLines/><w:spacing w:before="240" w:after="180"/><w:jc w:val="center"/><w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:eastAsia="黑体"/><w:b/><w:color w:val="17365D"/><w:sz w:val="36"/><w:szCs w:val="36"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:keepNext/><w:keepLines/><w:spacing w:before="280" w:after="140"/><w:outlineLvl w:val="1"/></w:pPr><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:eastAsia="黑体"/><w:b/><w:color w:val="17365D"/><w:sz w:val="30"/><w:szCs w:val="30"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:keepNext/><w:spacing w:before="220" w:after="100"/><w:outlineLvl w:val="2"/></w:pPr><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:eastAsia="黑体"/><w:b/><w:color w:val="2F5597"/><w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading4"><w:name w:val="heading 4"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:keepNext/><w:spacing w:before="180" w:after="80"/><w:outlineLvl w:val="3"/></w:pPr><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:eastAsia="黑体"/><w:b/><w:color w:val="365F91"/><w:sz w:val="23"/><w:szCs w:val="23"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Note"><w:name w:val="Note"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:after="80"/><w:jc w:val="left"/></w:pPr><w:rPr><w:color w:val="5B6573"/><w:i/><w:sz w:val="19"/><w:szCs w:val="19"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Keywords"><w:name w:val="Keywords"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:after="160"/></w:pPr><w:rPr><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Caption"><w:name w:val="Caption"/><w:basedOn w:val="Normal"/><w:pPr><w:keepNext/><w:spacing w:before="60" w:after="120"/><w:jc w:val="left"/></w:pPr><w:rPr><w:i/><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Figure"><w:name w:val="Figure"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="120" w:after="60"/><w:jc w:val="center"/></w:pPr></w:style>
  <w:style w:type="paragraph" w:styleId="Reference"><w:name w:val="Reference"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:after="60" w:line="220" w:lineRule="auto"/><w:jc w:val="left"/></w:pPr><w:rPr><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="ListParagraph"><w:name w:val="List Paragraph"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:after="60"/></w:pPr></w:style>
  <w:style w:type="paragraph" w:styleId="TableText"><w:name w:val="Table Text"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:after="0"/><w:jc w:val="left"/></w:pPr><w:rPr><w:sz w:val="17"/><w:szCs w:val="17"/></w:rPr></w:style>
  <w:style w:type="table" w:styleId="ThreeLineTable"><w:name w:val="Three-Line Table"/><w:tblPr><w:tblBorders><w:top w:val="single" w:sz="12" w:color="000000"/><w:left w:val="nil"/><w:bottom w:val="single" w:sz="12" w:color="000000"/><w:right w:val="nil"/><w:insideH w:val="nil"/><w:insideV w:val="nil"/></w:tblBorders></w:tblPr></w:style>
</w:styles>'''


def styles_xml(journal_manuscript: bool = False) -> str:
    """Return conservative journal-submission styles for clean manuscripts."""
    if not journal_manuscript:
        return legacy_styles_xml()
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="{W}">
  <w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="宋体" w:cs="Times New Roman"/><w:sz w:val="24"/><w:szCs w:val="24"/><w:lang w:val="en-US" w:eastAsia="zh-CN"/></w:rPr></w:rPrDefault>
  <w:pPrDefault><w:pPr><w:spacing w:before="0" w:after="0" w:line="480" w:lineRule="auto"/><w:jc w:val="both"/><w:widowControl/></w:pPr></w:pPrDefault></w:docDefaults>
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/><w:pPr><w:spacing w:before="0" w:after="0" w:line="480" w:lineRule="auto"/><w:jc w:val="both"/><w:widowControl/></w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="BodyText"><w:name w:val="Body Text"/><w:basedOn w:val="Normal"/><w:next w:val="BodyText"/><w:qFormat/><w:pPr><w:ind w:firstLine="480"/><w:spacing w:before="0" w:after="0" w:line="480" w:lineRule="auto"/><w:jc w:val="both"/><w:widowControl/></w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:keepNext/><w:keepLines/><w:spacing w:before="240" w:after="120"/><w:jc w:val="left"/><w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="黑体"/><w:b/><w:color w:val="000000"/><w:sz w:val="30"/><w:szCs w:val="30"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:keepNext/><w:keepLines/><w:spacing w:before="240" w:after="120"/><w:jc w:val="left"/><w:outlineLvl w:val="1"/></w:pPr><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="黑体"/><w:b/><w:color w:val="000000"/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:keepNext/><w:keepLines/><w:spacing w:before="180" w:after="60"/><w:outlineLvl w:val="2"/></w:pPr><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="黑体"/><w:b/><w:i/><w:color w:val="000000"/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading4"><w:name w:val="heading 4"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:keepNext/><w:spacing w:before="120" w:after="0"/><w:outlineLvl w:val="3"/></w:pPr><w:rPr><w:i/><w:color w:val="000000"/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Note"><w:name w:val="Note"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:after="0" w:line="480" w:lineRule="auto"/></w:pPr><w:rPr><w:i/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Keywords"><w:name w:val="Keywords"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:after="120" w:line="480" w:lineRule="auto"/></w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Caption"><w:name w:val="Caption"/><w:basedOn w:val="Normal"/><w:pPr><w:keepNext/><w:spacing w:before="120" w:after="60" w:line="240" w:lineRule="auto"/><w:jc w:val="left"/></w:pPr><w:rPr><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Figure"><w:name w:val="Figure"/><w:basedOn w:val="Normal"/></w:style>
  <w:style w:type="paragraph" w:styleId="Reference"><w:name w:val="Reference"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:after="0" w:line="480" w:lineRule="auto"/><w:jc w:val="left"/></w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="ListParagraph"><w:name w:val="List Paragraph"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:after="0" w:line="480" w:lineRule="auto"/></w:pPr></w:style>
  <w:style w:type="paragraph" w:styleId="TableText"><w:name w:val="Table Text"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/><w:jc w:val="left"/></w:pPr><w:rPr><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr></w:style>
  <w:style w:type="table" w:styleId="ThreeLineTable"><w:name w:val="Three-Line Table"/><w:tblPr><w:tblBorders><w:top w:val="single" w:sz="12" w:color="000000"/><w:left w:val="nil"/><w:bottom w:val="single" w:sz="12" w:color="000000"/><w:right w:val="nil"/><w:insideH w:val="nil"/><w:insideV w:val="nil"/></w:tblBorders></w:tblPr></w:style>
</w:styles>'''


def build(
    md_path: Path,
    out_path: Path,
    title: str,
    *,
    clean_manuscript: bool = False,
    allow_images: bool = False,
    core_timestamp: str | None = None,
    bibliography: Path | None = None,
    landscape_tables: bool = False,
):
    body, images, image_order = parse_markdown(
        md_path,
        section_page_breaks=not clean_manuscript,
        bibliography=bibliography,
        reject_images=clean_manuscript and not allow_images,
        journal_body=clean_manuscript,
        landscape_tables=landscape_tables,
        clean_manuscript=clean_manuscript,
    )
    ns = f'xmlns:w="{W}" xmlns:r="{R}" xmlns:wp="{WP}" xmlns:a="{A}" xmlns:pic="{PIC}"'
    sect = make_sect_pr("portrait", clean_manuscript)
    document = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document {ns}><w:body>{body}{sect}</w:body></w:document>'

    rels = [
        ('rId1', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles', 'styles.xml'),
        ('rId2', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings', 'settings.xml'),
        ('rId3', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/fontTable', 'fontTable.xml'),
    ]
    if not clean_manuscript:
        rels.extend([
            ('rId4', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/header', 'header1.xml'),
            ('rId5', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer', 'footer1.xml'),
        ])
    for path in image_order:
        idx = image_order.index(path) + 1
        rels.append((images[path], 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/image', f'media/image{idx}.png'))
    rel_xml = ''.join(f'<Relationship Id="{rid}" Type="{typ}" Target="{target}"/>' for rid, typ, target in rels)
    doc_rels = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">{rel_xml}</Relationships>'

    header_footer_types = "" if clean_manuscript else (
        '<Override PartName="/word/header1.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/>'
        '<Override PartName="/word/footer1.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>'
    )
    content_types = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Default Extension="png" ContentType="image/png"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/><Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/><Override PartName="/word/fontTable.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.fontTable+xml"/>{header_footer_types}<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/><Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>'''
    root_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/></Relationships>'''
    settings = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:settings xmlns:w="{W}"><w:zoom w:percent="100"/><w:defaultTabStop w:val="720"/><w:characterSpacingControl w:val="doNotCompress"/><w:compat><w:compatSetting w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" w:val="15"/></w:compat></w:settings>'''
    fonts = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:fonts xmlns:w="{W}"><w:font w:name="Times New Roman"/><w:font w:name="Arial"/><w:font w:name="宋体"/><w:font w:name="黑体"/><w:font w:name="Consolas"/><w:font w:name="等线"/></w:fonts>'''
    header = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:hdr xmlns:w="{W}"><w:p><w:pPr><w:jc w:val="right"/><w:pBdr><w:bottom w:val="single" w:sz="4" w:space="4" w:color="B7C9E2"/></w:pBdr></w:pPr>{run_xml("Bilingual scientific-content draft | 中英文科学内容草案 | 2026-08-12", size=17, color="60758A")}</w:p></w:hdr>'''
    footer = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:ftr xmlns:w="{W}"><w:p><w:pPr><w:jc w:val="center"/></w:pPr>{run_xml("Page ", size=18, color="60758A")}<w:fldSimple w:instr="PAGE"><w:r><w:rPr><w:sz w:val="18"/><w:color w:val="60758A"/></w:rPr><w:t>1</w:t></w:r></w:fldSimple></w:p></w:ftr>'''
    now = core_timestamp or datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    administrative_metadata = "" if clean_manuscript else (
        "<dc:subject>Original research scientific-content draft</dc:subject>"
        "<dc:creator>Accountable authors to be supplied</dc:creator>"
        "<cp:lastModifiedBy>Arena.ai drafting workflow</cp:lastModifiedBy>"
    )
    core = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dc:title>{x(title)}</dc:title>{administrative_metadata}<dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created><dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified></cp:coreProperties>'''
    app = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"><Application>Dependency-free OOXML builder</Application><DocSecurity>0</DocSecurity><ScaleCrop>false</ScaleCrop><Company></Company><LinksUpToDate>false</LinksUpToDate><SharedDoc>false</SharedDoc><HyperlinksChanged>false</HyperlinksChanged><AppVersion>1.0</AppVersion></Properties>'''

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zip_member(zf, "[Content_Types].xml", content_types)
        zip_member(zf, "_rels/.rels", root_rels)
        zip_member(zf, "docProps/core.xml", core)
        zip_member(zf, "docProps/app.xml", app)
        zip_member(zf, "word/document.xml", document)
        zip_member(zf, "word/_rels/document.xml.rels", doc_rels)
        zip_member(zf, "word/styles.xml", styles_xml(journal_manuscript=clean_manuscript))
        zip_member(zf, "word/settings.xml", settings)
        zip_member(zf, "word/fontTable.xml", fonts)
        if not clean_manuscript:
            zip_member(zf, "word/header1.xml", header)
            zip_member(zf, "word/footer1.xml", footer)
        for idx, path in enumerate(image_order, start=1):
            zip_member(zf, f"word/media/image{idx}.png", path.read_bytes())
    print(out_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--title", default="Scientific manuscript")
    parser.add_argument(
        "--bibliography",
        type=Path,
        help="BibTeX authority used to resolve Pandoc-style citation keys to reference numbers.",
    )
    parser.add_argument(
        "--timestamp",
        dest="core_timestamp",
        help="Fixed W3C timestamp for reproducible core metadata, e.g. 2026-08-14T00:00:00Z.",
    )
    parser.add_argument(
        "--clean-manuscript",
        action="store_true",
        help=(
            "Omit header/footer parts, page-number fields, administrative core metadata, "
            "and automatic page breaks before top-level sections."
        ),
    )
    parser.add_argument(
        "--allow-images",
        action="store_true",
        help="Embed local PNG figures even when --clean-manuscript is set.",
    )
    parser.add_argument(
        "--landscape-tables",
        action="store_true",
        help="Render table pages in landscape orientation while keeping body text and figures in portrait.",
    )
    args = parser.parse_args()
    if args.core_timestamp:
        try:
            parsed_timestamp = datetime.fromisoformat(args.core_timestamp.replace("Z", "+00:00"))
        except ValueError:
            parser.error("--timestamp must be an ISO 8601/W3C date-time")
        if parsed_timestamp.tzinfo is None:
            parser.error("--timestamp must include a timezone, preferably Z")
    build(
        args.input.resolve(),
        args.output.resolve(),
        args.title,
        clean_manuscript=args.clean_manuscript,
        allow_images=args.allow_images,
        core_timestamp=args.core_timestamp,
        bibliography=args.bibliography.resolve() if args.bibliography else None,
        landscape_tables=args.landscape_tables,
    )


if __name__ == "__main__":
    main()
