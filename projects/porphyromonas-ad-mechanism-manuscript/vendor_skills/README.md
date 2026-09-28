# Skills used on `sci_submission` (this round)

Installed from GitHub into this folder (text only; large figure assets omitted) and applied to the manuscript.

| Skill | Source | What it was used for |
| --- | --- | --- |
| find-skills | local `~/.claude/skills/find-skills` | Search/install path; `npx skills find` returned no public match for academic rewrite, so the four user-named repos were cloned instead |
| nature-writing | [Yuan1z0825/nature-skills](https://github.com/Yuan1z0825/nature-skills) | Axes: `task=manuscript`, `paper_type=research`, `section=intro`, `language=en`, `journal=generic`. Intro rebuilt as problem → gap → route, not a question list |
| nature-shared / nature-introduction | same | Funnel ending is “Here we scored / docked / simulated”, not “we asked three questions” |
| nature-figure | same | Okabe–Ito blue/green, large numerals, min label 22–24 px, no overlapping boxes |
| nature-reviewer | same | One editorial audit (this environment cannot isolate three blind reviewers). Blocking: no sequence-level healthy vs periodontitis overlap map. Non-blocking: 100 ns ≠ 1 μs Atanasova |
| nature-polishing | same | Sentence-length mix; cut “not X but Y” openers |
| scientific-writing | [shaohuawen03-cyber/Auto-Empirical-Research-Skills](https://github.com/shaohuawen03-cyber/Auto-Empirical-Research-Skills) `04-K-Dense-AI-claude-scientific-writer` | Claim strength matched to computation-only evidence |
| humanizer | [blader/humanizer](https://github.com/blader/humanizer) | Removed staged closers, question-ending intro, “not the whole story” contrast |
| aigc-detector-rewriter | [Moonlit-Pages/AIGC-Detector-Rewriter-Skill](https://github.com/Moonlit-Pages/AIGC-Detector-Rewriter-Skill) | No back-translation. Expanded intro instead of compressing. Did **not** claim a detector score |
| turnitout-humanizer | [AhmadHassan-BTed/Turnitout-Humanizer](https://github.com/AhmadHassan-BTed/Turnitout-Humanizer) | Rule-based engine (no LLM). Applied its fact-lock: numbers, citations and tables unchanged. Did **not** run n-gram shattering on the manuscript (that would scramble SCI English). No detector score claimed |

## Apple Translate

This Linux sandbox cannot call macOS Translate. The AIGC skill also forbids back-translation as the rewrite method. Prose was rewritten in place (EN and ZH separately).

If you still want the Apple route that previously lowered a detector flag: on a Mac, open `English.docx`, Translate English → Chinese → English on **prose only**, leave tables, numbers and figures untouched.

## Nature-reviewer audit (single pass, not three-blind)

- Originality: peptide-level PAS occupancy from oral smORFs is a bounded computational case.
- Technical soundness: 22-task tables and Vina/MD numbers are internally consistent. Healthy vs periodontitis difference is a **rate table**, not unique sequences.
- Blocking gap: no row-wise overlap map, so the twelve docking peptides cannot be called periodontitis-specific.
- Readability: Fig. 1 now uses large numerals; intro ends with a research route, not questions.
