# Zotero-linked Word acceptance gate

The four manuscript Markdown sources now use Pandoc citation keys from
`references/references.bib`. The committed DOCX files contain automatically
resolved Vancouver-style numbered citation text, but they are **not described as
Zotero-live** because this build host does not expose Pandoc or a running Better
BibTeX JSON-RPC endpoint. Zotero Refresh cannot convert ordinary citation text
into live fields.

Follow this gate on a workstation with desktop Microsoft Word:

1. Install Pandoc, Zotero, the Zotero Word add-in, and Better BibTeX.
2. Import `references/references.bib` into Zotero and confirm that Better BibTeX
   retains the cited keys. Avoid duplicates.
3. Start Zotero and verify one real key:

   ```bash
   python scripts/test_better_bibtex.py scheltens2021alzheimer
   ```

4. Build a disposable Zotero-live candidate with the strict bridge. The script
   first creates and audits a one-citation probe; it stops rather than emitting
   a static substitute if the probe fails.

   ```bash
   python scripts/build_zotero_live_docx.py \
     --input manuscript/full/English.md \
     --output manuscript/full/English.zotero-candidate.docx \
     --reference-doc manuscript/full/English.docx \
     --report quality_reports/zotero_live_full_english.json
   ```

   Repeat for `full/Chinese.md`, `concise/English.md`, and
   `concise/Chinese.md`. Do **not** add `--citeproc`; the official Better BibTeX
   `zotero.lua` filter creates the `ADDIN ZOTERO_ITEM CSL_CITATION` fields.

5. Open each candidate in desktop Word. In the Zotero tab, set Document
   Preferences to an appropriate numbered biomedical style (for example,
   Vancouver), click **Refresh**, then use **Add/Edit Bibliography** after the
   References heading.
6. Save, close, reopen, and inspect all citation clusters and the complete
   bibliography. Confirm that Zotero can edit a citation without converting it
   to plain text.
7. Replace the neutral deliverable filename only after the Word/Zotero refresh
   is confirmed, and return the refreshed DOCX for an independent OpenXML audit.

Acceptance states are reported exactly as `setup gate`, `pending user action`,
`user-confirmed, unaudited`, or `returned file independently audited`. Visible
numbered text alone is never treated as proof of Zotero-live fields.
