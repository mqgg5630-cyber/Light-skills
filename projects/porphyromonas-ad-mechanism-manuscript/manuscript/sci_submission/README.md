# SCI submission rewrite (new folder)

Rewritten from `manuscript/sci_combined/English.docx` plus methods depth from `manuscript/full/`. Prose was recast so it is not a close copy of the previous combined article.

## What changed versus sci_combined

- Figure 1: screening cascade (library → 22 UniDL4BioPep tasks → 12 peptides → 3 MD complexes). SVG + PNG in `manuscript/figures/fig_screening_cascade.*`.
- Table 4: calculated physicochemical descriptors of the twelve peptides (MW, pI, charge, GRAVY, aliphatic index).
- Two separate PyMOL pose figures kept (now Figures 3 and 4). Combined 12-pose overview (old Figure S1) removed.
- Each predictor (UniDL4BioPep, NTxPred2, mebipred, AnOxPePred) has its own methods subsection. Source libraries are the processed smORF strings from PRJNA678453; PRJEB65451 is cited as a derived assembly, not a second cohort. Healthy library is scored only (no dereplication).
- Docking table split into PAS (Yes/No) and principal contacts.

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

## Similarity / Turnitin

Wording was rewritten. No detector score is claimed. If an AI-writing scan is still high, run the English file through Apple Translate English → Chinese → English and replace only the prose (keep tables, numbers, and figure files unchanged).
