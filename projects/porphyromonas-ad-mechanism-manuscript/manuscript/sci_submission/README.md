# SCI submission rewrite (new folder)

Rewritten from `manuscript/sci_combined/` plus methods depth from `manuscript/full/`. This round also used `vendor_skills/` (nature-writing, nature-figure, humanizer, AIGC rewriter). See `../../vendor_skills/README.md`.

## What changed versus sci_combined

- Figure 1: screening cascade with large numerals (Okabe–Ito blue/green). SVG + PNG in `manuscript/figures/fig_screening_cascade.*`.
- Table 3: periodontitis minus healthy 22-task score-rate differences. Physicochemical Table 5 describes the twelve docking ligands only.
- Two separate PyMOL pose figures kept (Figures 3 and 4). Combined 12-pose overview removed.
- Each predictor (UniDL4BioPep, NTxPred2, mebipred, AnOxPePred) has its own methods subsection with architecture, training set and threshold.
- Source libraries are processed smORF strings from PRJNA678453; PRJEB65451 is a derived assembly, not a second cohort. Healthy library is scored only (no dereplication).
- Introduction expanded to seven paragraphs (AD, PAS, epidemiology including Hu 2024 MR, *P. gingivalis*, smORF mining, AChE–Aβ MD, study route). It ends with “Here we scored / docked / simulated”, not a question list.

## Files

- `English.md` / `English.docx`
- `Chinese.md` / `Chinese.docx`

Physicochemical source table: `source_materials/peptide_physicochemical_12.csv`.

## Rebuild

From the project root:

```bash
for language in English Chinese; do
  python3 scripts/build_docx_stdlib.py --clean-manuscript --allow-images \
    --timestamp 2026-08-23T00:00:00Z \
    --bibliography references/references.bib \
    --input "manuscript/sci_submission/${language}.md" \
    --output "manuscript/sci_submission/${language}.docx" \
    --title "${language}"
done
```

## Similarity / Turnitin / Apple Translate

This Linux environment cannot call Apple Translate. The AIGC-detector-rewriter skill forbids back-translation as the rewrite method. Prose was rewritten in place (English and Chinese separately) with humanizer + nature-writing. No detector score is claimed.

If you still want the Apple route that previously lowered a detector flag: on a Mac, open `English.docx`, run system Translate English → Chinese → English on **prose only**, and leave tables, numbers and figures untouched.
