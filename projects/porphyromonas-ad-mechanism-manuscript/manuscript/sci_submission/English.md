# Periodontitis oral smORFs yield micropeptides that occupy the AChE peripheral site: 22-task UniDL4BioPep scoring, docking, and 100-ns dynamics

## Abstract

Periodontitis has been tied to Alzheimer’s disease (AD) in clinical and experimental work, yet a peptide-level ligand that could act on a synaptic enzyme is still missing. Here we scored already-processed oral small open reading frames (smORFs) with UniDL4BioPep, docked twelve 7–9-residue peptides into human acetylcholinesterase (AChE, PDB 4EY6), and ran 100-ns molecular dynamics (MD) on apo AChE and three complexes. The healthy-labelled library (11,269,961 sequences) and the periodontitis-labelled library (11,721,988 sequences) were both passed through 22 UniDL4BioPep classifiers at ≥0.80. Only the periodontitis branch was then matched to oral genomic and metaproteomic catalogues. Blood–brain-barrier (BBB) hits numbered 1,095,861 (9.72%) in the healthy library and 1,125,832 (9.60%) in the periodontitis library. Intersection of the periodontitis BBB set with 33,786 unique, catalogue-supported peptides left 3,518 sequences; NTxPred2, mebipred and AnOxPePred reduced that list to twelve explicit peptides. All twelve carry a net positive charge at pH 7.4. Local AutoDock Vina (three runs) gave best poses between −8.25 and −9.60 kcal/mol. FLLHTTR, YLSLLQR and LLHPLRL contact the peripheral anionic site (PAS). Over 100 ns the FLLHTTR and YLSLLQR complexes stay more compact than apo AChE (backbone RMSD 0.1640 and 0.1625 nm versus 0.1897 nm). FLLHTTR keeps a dense hydrogen-bond net (7.03 ± 1.28); only YLSLLQR shrinks solvent-accessible surface area. These calculations outline a possible route in which oral micropeptides sit on the same PAS that accelerates amyloid-β (Aβ) assembly.

**Keywords:** Alzheimer’s disease; *Porphyromonas gingivalis*; periodontitis; smORF; micropeptide; acetylcholinesterase; peripheral anionic site; UniDL4BioPep; molecular docking; molecular dynamics

## Introduction

AD is not a single linear cascade. Amyloid, tau, cholinergic loss, immune activation and vascular injury run together [@scheltens2021alzheimer]. Amyloid biology still sits near the centre: APP processing yields Aβ40/Aβ42, oligomers injure synapses, and familial APP/PSEN alleles change Aβ length and amount [@selkoe2016amyloid]. Loss of basal-forebrain acetylcholine explains a large part of the cognitive picture, which is why AChE inhibitors remain in routine use [@hampel2018cholinergic]. Catalysis is not the whole story for this enzyme. AChE speeds Aβ fibril growth through the PAS, and AChE–Aβ particles are more toxic than free Aβ [@inestrosa1996ache]. A short hydrophobic PAS motif is enough to drive that chaperone effect [@deferrari2001motif]. The PAS is therefore a structural hinge between cholinergic failure and amyloid deposition.

Chronic periodontitis keeps a low-grade inflammatory load and lets microbial products leak into blood [@chalmers2025primer]. Oral activity is species- and site-specific, so 16S abundance cannot stand in for a molecular ligand [@belstrom2021periodontitis]. Gingipains and outer-membrane vesicles of *Porphyromonas gingivalis* are one well-mapped virulence pair [@guo2010gingipain; @ho2015omv]. Meta-analyses link periodontal disease to cognitive disorders, with effect sizes that move when case definitions change [@larvin2023periodontalcognition]. In an AD cohort, periodontitis tracked later decline [@ide2016periodontitis]. *P. gingivalis* and gingipains have been reported in AD brains [@dominy2019pgingivalis], and repeated oral infection in mice produces neuroinflammation and Aβ-related changes [@ilievski2018oral]. If a short oral peptide can sit on AChE, that exposure context becomes mechanistically useful [@hu2024mendelian].

Microbiome smORFs encode a large pool of uncharted small proteins [@sberro2019smallgenes; @durrant2021sorf]. Whether a 7–9-aa periodontitis peptide can occupy the Aβ-binding PAS is a structural question. Accelerated MD pulls Aβ onto the AChE surface and treats the enzyme as a nucleation centre [@lushchekina2017amd]. A 1-μs PAS-centred AChE–Aβ run stays bound, with the main residence at residues 344–361 [@atanasova2020md]. PAS-directed small molecules can block AChE-induced Aβ aggregation in the test tube [@bartolini2003pas]. PDB 4EY6 gives a 2.40 Å human AChE frame for docking [@cheung2012ache]. The aromatic gorge that joins the catalytic triad to the PAS was mapped earlier on *Torpedo* AChE [@kryger1999e2020].

We therefore asked three linked questions. First, after 22-task UniDL4BioPep scoring of both oral libraries, which periodontitis peptides remain once catalogue matching is applied? Second, do twelve 7–9-aa sequences from that funnel contact the PAS of human AChE? Third, do three of those complexes remain surface-bound for 100 ns without unfolding the enzyme?

## Materials and methods

### Study design

The work is computational. No new patients, specimens, sequencing runs or wet assays were added. Healthy and periodontitis tags are library labels; they are not peptide-level clinical diagnoses. Docking used local three-run AutoDock Vina poses. MD used 100-ns GROMACS trajectories of apo AChE and three peptide complexes.

### Source libraries

Translated smORFs of 4–50 aa were taken as already-processed peptide strings. We did not reassemble reads or call genes de novo. The public source of the paired oral metagenomes and metatranscriptomes is PRJNA678453 [@belstrom2021periodontitis]. A derived MGnify third-party assembly, PRJEB65451 (metaSPAdes v3.15.3), exists for that BioProject; it is not a second clinical cohort. Library sizes were 11,269,961 healthy-labelled and 11,721,988 periodontitis-labelled sequences.

### UniDL4BioPep (22 tasks)

UniDL4BioPep was run first on both full libraries, which is the order used in recent microbiome peptide-antibiotic mining [@torres2024peptideantibiotics; @du2023unidl4biopep]. Each peptide is encoded by the pretrained ESM-2 checkpoint `esm2_t6_8M_UR50D` as a 320-dimensional contextual vector. A six-layer, task-specific convolutional network then produces a binary score. We applied 22 published heads: ACE inhibitory, DPP-IV inhibitory, Bitter, Umami, Antimicrobial, Antimalarial (alternative), Antimalarial (main), Quorum sensing, Anticancer (main), Anticancer (alternative), Anti-MRSA, TTCA, BBB (BBP), Anti-parasitic (APP), NeuroPred, Antibacterial, Antifungal, Antiviral, Toxicity, Antioxidant FRS, Allergenicity, and cell-penetrating peptide (CPP). The decision cut was ≥0.80 on every head. BBB (BBP) ≥0.80 is an operational “BBB-high” label, not measured transcytosis. Independent BBB peptide classifiers use other architectures and training sets, so their published AUCs do not transfer automatically to these very short oral strings [@gu2024bbb].

### Catalogue matching (periodontitis branch only)

After scoring, only periodontitis-labelled sequences were exact-matched to oral genomic and metaproteomic resources and collapsed to unique peptides. HOMD and eHOMD supply curated aerodigestive genomes [@chen2010homd; @escapa2018ehomd]. Salivary metaproteomes record peptides inside their own false-discovery framework [@belstrom2016metaproteomics]. Further oral metaproteomic sets add sequence observations from other clinical contexts [@jiang2022oralmetaproteomics; @yuan2025osample]. A match supports prior observation of the string; it does not prove expression in PRJNA678453 samples. The periodontitis library yielded 33,786 unique catalogue-supported peptides. Intersection with the 1,125,832 periodontitis BBB (BBP) hits recovered 3,518 sequences (3,446 of 5–30 aa; 72 of 31–50 aa). The healthy library was left at the 22-task score tables and was not dereplicated.

### NTxPred2

Peptides of 7–50 aa inside the 3,518-member set were scored with NTxPred2 [@rathore2025ntxpred2]. The peptide mode fine-tunes ESM2-t30 on neurotoxic versus non-neurotoxic sequences. A positive call is a model label, not electrophysiology.

### mebipred

Mebipred estimates general and ion-related metal-binding potential from engineered sequence features through a two-tier neural net [@aptekmann2022mebipred]. The cut used here was 0.50 for Cu-, Fe- and Zn-related output. The score is not a measured Kd or a coordination geometry.

### AnOxPePred

AnOxPePred is a one-dimensional convolutional multi-task net trained for free-radical scavenging (FRS) and chelation (CHEL) [@olsen2020anoxpepred]. Serial cuts were CHEL≥0.25, then CHEL≥0.25 with FRS<0.50, then CHEL≥0.25 with FRS<0.45. Agreement among UniDL4BioPep, NTxPred2, mebipred and AnOxPePred is triage, not orthogonal biology.

### Physicochemical descriptors

For the twelve unique 7–9-aa strings we recalculated length, histidine, cysteine and Arg+Lys counts, average molecular weight, isoelectric point, net charge at pH 7.4, Kyte–Doolittle GRAVY, Ikai aliphatic index, hydrophobic residue fraction (A, I, L, M, F, V, W, Y), and Boman index. Scales were applied to the amino-acid strings only; no experimental HPLC or CD was performed.

### Molecular docking

Human recombinant AChE (PDB 4EY6, 2.40 Å) was stripped of galantamine and crystal waters, chain breaks were repaired, and protonation was set at pH 7.4 [@cheung2012ache]. The twelve ligands ALLLHRC, FCLHLQLR, FLLHTTR, HLLTLKKHV, HLPLLHRCC, HVLLLRQCA, LLHLPKRTT, LLHPLRC, LLHPLRL, WLLVHLKK, YHHLLCRR and YLSLLQR were docked with AutoDock Vina, exhaustiveness 32 [@trott2010vina; @eberhardt2021vina]. The grid was centred on the PAS (Tyr72, Asp74, Thr75, Leu76, Trp286, His287, Tyr341) and covered the gorge neck (Phe295), the choline subsite (Trp86, Glu202, Tyr337) and the catalytic triad (Ser203, His447, Glu334). Each ligand was run three times. We report best-run affinity, three-run mean ± SD, hydrogen-bond count and PAS contact from the single best pose. Vina scores rank poses; they are not experimental free energies.

### Molecular dynamics

Four explicit-solvent systems were built in GROMACS with Amber99SB-ILDN and TIP3P water at 0.15 M NaCl [@abraham2015gromacs; @lindorfflarsen2010amber]: apo AChE (chain A) and the ALLLHRC, FLLHTTR and YLSLLQR complexes. Each box was triclinic with a 1.0 nm solute-to-wall buffer. Equilibration was 2,000 steps of steepest descent, 1.0 ns restrained NVT to 300 K, 1.0 ns restrained NPT, and 1.0 ns free NPT. Production was 100 ns (dt = 2.0 fs) at 300 K and 1.0 bar with LINCS, 1.2 nm cut-offs and particle-mesh Ewald. Frames were stored every 20 ps.

Metrics matched Figures 5–7: Cα RMSD, per-residue RMSF, SASA, Rg, DSSP occupancy, and intermolecular hydrogen bonds (`gmx hbond`; donor–acceptor ≤ 3.0 Å). Peptide self-fit RMSD and persistent contacts (7.0 Å) were stored as extras. Means ± SD use the last 20 ns (80–100 ns). The design follows the AChE–Aβ MD logic of Atanasova et al., at 100 ns rather than 1 μs [@atanasova2020md].

## Results

### Twenty-two UniDL4BioPep tasks on both libraries

Figure 1 summarises the cascade. Both libraries were scored at ≥0.80 on all 22 heads (Tables 1 and 2). Hit rates sit close to each other. Antimicrobial called 10,302,093/11,721,988 periodontitis sequences (87.89%) and 9,882,657/11,269,961 healthy sequences (87.69%). BBB (BBP) called 1,125,832 (9.60%) versus 1,095,861 (9.72%). Anti-parasitic (APP) and quorum sensing were the next largest heads; DPP-IV inhibitory was the smallest in both libraries. Labels overlap, so one peptide can sit in several rows. Because the two BBB rates differ by only 0.12 percentage points, BBB-high is not a periodontitis-specific stamp. Downstream docking used the periodontitis branch only.

**Table 1. UniDL4BioPep counts for the periodontitis-labelled library (11,721,988 smORFs; ≥0.80).**

| No. | Task | n | % |
| --- | --- | ---: | ---: |
| 1 | ACE inhibitory | 1,236,442 | 10.55 |
| 2 | DPP-IV inhibitory | 139,056 | 1.19 |
| 3 | Bitter | 1,831,185 | 15.62 |
| 4 | Umami | 3,100,811 | 26.45 |
| 5 | Antimicrobial | 10,302,093 | 87.89 |
| 6 | Antimalarial (alternative) | 695,608 | 5.93 |
| 7 | Antimalarial (main) | 2,010,724 | 17.15 |
| 8 | Quorum sensing | 4,491,507 | 38.32 |
| 9 | Anticancer (main) | 2,357,718 | 20.11 |
| 10 | Anticancer (alternative) | 2,015,652 | 17.20 |
| 11 | Anti-MRSA | 843,977 | 7.20 |
| 12 | TTCA | 2,666,759 | 22.75 |
| 13 | BBB (BBP) | 1,125,832 | 9.60 |
| 14 | Anti-parasitic (APP) | 5,462,493 | 46.60 |
| 15 | NeuroPred | 1,714,373 | 14.63 |
| 16 | Antibacterial | 2,597,877 | 22.16 |
| 17 | Antifungal | 2,960,118 | 25.25 |
| 18 | Antiviral | 3,275,203 | 27.94 |
| 19 | Toxicity | 1,714,299 | 14.62 |
| 20 | Antioxidant FRS | 2,521,106 | 21.51 |
| 21 | Allergenicity | 1,713,798 | 14.62 |
| 22 | Cell-penetrating peptide (CPP) | 925,627 | 7.90 |

**Table 2. UniDL4BioPep counts for the healthy-labelled library (11,269,961 smORFs; ≥0.80).**

| No. | Task | n | % |
| --- | --- | ---: | ---: |
| 1 | ACE inhibitory | 1,237,451 | 10.98 |
| 2 | DPP-IV inhibitory | 131,426 | 1.17 |
| 3 | Bitter | 1,840,368 | 16.33 |
| 4 | Umami | 3,094,287 | 27.46 |
| 5 | Antimicrobial | 9,882,657 | 87.69 |
| 6 | Antimalarial (alternative) | 703,632 | 6.24 |
| 7 | Antimalarial (main) | 1,954,667 | 17.34 |
| 8 | Quorum sensing | 4,161,825 | 36.93 |
| 9 | Anticancer (main) | 2,404,084 | 21.33 |
| 10 | Anticancer (alternative) | 1,979,643 | 17.57 |
| 11 | Anti-MRSA | 769,955 | 6.83 |
| 12 | TTCA | 2,618,849 | 23.24 |
| 13 | BBB (BBP) | 1,095,861 | 9.72 |
| 14 | Anti-parasitic (APP) | 5,517,278 | 48.96 |
| 15 | NeuroPred | 1,690,436 | 15.00 |
| 16 | Antibacterial | 2,658,234 | 23.59 |
| 17 | Antifungal | 3,128,057 | 27.76 |
| 18 | Antiviral | 3,362,295 | 29.83 |
| 19 | Toxicity | 1,725,268 | 15.31 |
| 20 | Antioxidant FRS | 2,643,538 | 23.46 |
| 21 | Allergenicity | 1,635,019 | 14.51 |
| 22 | Cell-penetrating peptide (CPP) | 1,029,770 | 9.14 |

![Figure 1. Screening cascade from oral smORF libraries to twelve peptides and three MD complexes.](../figures/fig_screening_cascade.png)

**Figure 1. Screening cascade.** UniDL4BioPep (22 tasks) was applied to both libraries. Catalogue matching and later filters were applied only to the periodontitis branch, ending in twelve 7–9-aa peptides for docking and three complexes for 100-ns MD.

### Periodontitis funnel to twelve sequences

Catalogue matching of the periodontitis library kept 33,786 unique peptides. Intersection with BBB-high gave 3,518 sequences. NTxPred2 scored 3,299/3,518 (93.77%) and called 923/3,299 (27.98%) positive. Later cuts left 111 mebipred-positive peptides, 15 with CHEL≥0.25, 12 with CHEL≥0.25 and FRS<0.50, and 8 with the stricter FRS<0.45 (Table 3). All 923 NTxPred2-positive peptides were ≤30 aa, so the metal/CHEL/FRS steps kept short peptides only.

**Table 3. Periodontitis branch after UniDL4BioPep scoring.**

| Stage | Rule | n | Denominator |
| --- | --- | ---: | ---: |
| Periodontitis smORFs | 4–50 aa | 11,721,988 | Library |
| BBB (BBP) | score ≥0.80 | 1,125,832 | 11,721,988 |
| Catalogue-supported unique peptides | Exact match | 33,786 | 11,721,988 |
| BBB-high ∩ catalogue-supported | Intersection | 3,518 | 1,125,832 ∩ 33,786 |
| Short (5–30 aa) | Length | 3,446 | 3,518 |
| Long (31–50 aa) | Length | 72 | 3,518 |
| NTxPred2 scored | 7–50 aa | 3,299 | 3,518 |
| NTxPred2-positive | Model label | 923 | 3,299 |
| mebipred-positive | ≥0.50 | 111 | — |
| CHEL-priority | CHEL≥0.25 | 15 | 111 |
| Main set | CHEL≥0.25 and FRS<0.50 | 12 | 111 |
| Stricter subset | CHEL≥0.25 and FRS<0.45 | 8 | — |

### Physicochemical profile of the twelve peptides

The twelve strings are unique 7–9-aa peptides of standard residues (Table 4). Eleven contain histidine; six contain cysteine; every sequence has at least one Arg or Lys. Molecular weights fall between 825.03 and 1,097.30 Da. Isoelectric points are alkaline (8.28–11.54). Net charge at pH 7.4 is positive for all twelve (0.85–2.08). GRAVY is positive for ten sequences, in line with leucine-rich cores; LLHLPKRTT (−0.36) and YHHLLCRR (−0.95) are the two hydrophilic exceptions. Aliphatic indices run from 97.5 (YHHLLCRR) to 222.9 (LLHPLRL). YLSLLQR is the only peptide without histidine. These numbers describe composition; they are not HPLC or CD measurements.

**Table 4. Composition and calculated physicochemical descriptors of the twelve 7–9-aa peptides.**

| Peptide | aa | MW (Da) | pI | z (pH 7.4) | GRAVY | AI | His | Cys | R+K |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| ALLLHRC | 7 | 825.03 | 9.00 | 0.92 | 1.14 | 181.4 | 1 | 1 | 1 |
| FCLHLQLR | 8 | 1029.26 | 9.00 | 0.92 | 0.69 | 146.2 | 1 | 1 | 1 |
| FLLHTTR | 7 | 887.04 | 11.09 | 1.04 | 0.19 | 111.4 | 1 | 0 | 1 |
| HLLTLKKHV | 9 | 1088.35 | 10.63 | 2.08 | 0.08 | 162.2 | 2 | 0 | 2 |
| HLPLLHRCC | 9 | 1091.35 | 8.28 | 0.85 | 0.43 | 130.0 | 2 | 2 | 1 |
| HVLLLRQCA | 9 | 1052.30 | 9.00 | 0.92 | 0.97 | 173.3 | 1 | 1 | 1 |
| LLHLPKRTT | 9 | 1078.32 | 11.54 | 2.04 | −0.36 | 130.0 | 1 | 0 | 2 |
| LLHPLRC | 7 | 851.07 | 9.00 | 0.92 | 0.66 | 167.1 | 1 | 1 | 1 |
| LLHPLRL | 7 | 861.09 | 11.09 | 1.04 | 0.84 | 222.9 | 1 | 0 | 1 |
| WLLVHLKK | 8 | 1036.32 | 10.63 | 2.04 | 0.46 | 182.5 | 1 | 0 | 2 |
| YHHLLCRR | 8 | 1097.30 | 9.91 | 1.96 | −0.95 | 97.5 | 2 | 1 | 2 |
| YLSLLQR | 7 | 892.06 | 9.89 | 0.99 | 0.04 | 167.1 | 0 | 0 | 1 |

### Docking to human AChE

All twelve ligands produced favourable Vina scores (Table 5, Figure 2). Best-run values ran from −8.25 to −9.60 kcal/mol; three-run means ran from −8.07 ± 0.16 to −9.44 ± 0.09 kcal/mol. Best-pose order was FLLHTTR (−9.60), YLSLLQR (−9.49), ALLLHRC (−9.29). Mean order put YLSLLQR first (−9.44 ± 0.09) and ALLLHRC second (−9.18 ± 0.11). FLLHTTR has the strongest single pose and the largest SD (−8.77 ± 1.41). Best poses made 3–10 hydrogen bonds (mean length 2.83–3.28 Å; Figures 3 and 4).

**Table 5. Three-run AutoDock Vina scores against human AChE (PDB 4EY6).**

| Peptide | H-bonds | Best | Mean ± SD (n=3) | PAS | Principal contacts |
| --- | ---: | ---: | --- | --- | --- |
| ALLLHRC | 3 | −9.29 | −9.18 ± 0.11 | No | Ser125, Ser203, Tyr124 |
| FCLHLQLR | 7 | −9.27 | −8.96 ± 0.48 | Yes | Ser203, Thr75, Tyr341 |
| FLLHTTR | 8 | −9.60 | −8.77 ± 1.41 | Yes | Asp74, Tyr72, His287 |
| HLLTLKKHV | 6 | −8.88 | −8.69 ± 0.20 | Yes | Tyr72, Phe346 |
| HLPLLHRCC | 4 | −8.35 | −8.28 ± 0.07 | No | Ser125, Tyr124, Tyr337 |
| HVLLLRQCA | 4 | −8.25 | −8.07 ± 0.16 | Yes | Thr75 |
| LLHLPKRTT | 3 | −9.01 | −8.89 ± 0.16 | Adjacent | Ser203, Val340 |
| LLHPLRC | 4 | −8.91 | −8.78 ± 0.11 | No | Ser125, Ser293 |
| LLHPLRL | 10 | −8.94 | −8.91 ± 0.05 | Yes | Trp286, Tyr341, His447 |
| WLLVHLKK | 4 | −8.94 | −8.64 ± 0.26 | No | Asn283, Gln279 |
| YHHLLCRR | 7 | −9.03 | −8.62 ± 0.43 | No | Trp86, Ser203 |
| YLSLLQR | 7 | −9.49 | −9.44 ± 0.09 | Yes | Tyr72, Thr75, Glu202 |

![Figure 2. Local AutoDock Vina scores of twelve candidate micropeptides.](../figures/fig5_docking_scores.png)

**Figure 2. Three-run Vina scores against human AChE (PDB 4EY6).** Blue circles, mean; whiskers, SD; orange diamonds, best run. Order follows best-run rank.

![Figure 3. Best poses of ALLLHRC, FCLHLQLR, FLLHTTR, HLLTLKKHV, HLPLLHRCC and HVLLLRQCA.](../figures/fig_docking_poses_A_F.png)

**Figure 3. Best docking poses, peptides 1–6 (A–F).** Peptide, orange; contacting residues, cyan. FLLHTTR (C) is the densest PAS pose.

![Figure 4. Best poses of LLHLPKRTT, LLHPLRC, LLHPLRL, WLLVHLKK, YHHLLCRR and YLSLLQR.](../figures/fig_docking_poses_G_L.png)

**Figure 4. Best docking poses, peptides 7–12 (G–L).** LLHPLRL (I) spans PAS Trp286/Tyr341 to catalytic His447. YLSLLQR (L) bridges PAS and the gorge mouth.

PAS contacts in the best pose were seen for FLLHTTR (Figure 3C), YLSLLQR (Figure 4L), FCLHLQLR, HVLLLRQCA, HLLTLKKHV and LLHPLRL (Figure 4I). ALLLHRC binds catalytic Ser203 with the shortest mean hydrogen bond (2.83 Å) rather than the outer PAS aromatics (Figure 3A). Three-run means separate ligands that stay strong across runs (YLSLLQR, ALLLHRC, LLHPLRL) from ligands whose best pose is better than the run average (FLLHTTR, FCLHLQLR, YHHLLCRR).

### 100-ns dynamics of apo AChE and three complexes

Production runs finished for apo AChE and the ALLLHRC, FLLHTTR and YLSLLQR complexes (Table 6, Figures 5–7). Each six-panel figure compares apo with one complex: RMSD (A), RMSF (B), SASA (C), Rg (D), last-20-ns DSSP (E) and intermolecular hydrogen bonds (F).

<!-- PAGEBREAK -->

![Figure 5. Apo AChE versus AChE–ALLLHRC, 100 ns.](../figures/fig_compare_mixed_ache_vs_alllhrc.png)

**Figure 5. Apo AChE versus AChE–ALLLHRC.** Panels A–F match Table 6. Complex RMSD (A) tracks apo; hydrogen bonds (F) fall from early occupancy to about two in the last 20 ns.

![Figure 6. Apo AChE versus AChE–FLLHTTR, 100 ns.](../figures/fig_compare_mixed_ache_vs_fllhttr.png)

**Figure 6. Apo AChE versus AChE–FLLHTTR.** After ~50 ns, complex RMSD (A) lies below apo. Hydrogen-bond counts (F) stay in the 6–10 range for the full 100 ns.

![Figure 7. Apo AChE versus AChE–YLSLLQR, 100 ns.](../figures/fig_compare_mixed_ache_vs_ylsllqr.png)

**Figure 7. Apo AChE versus AChE–YLSLLQR.** Late RMSD (A) is below apo. SASA (C) is the only complex that contracts relative to apo.

**Table 6. Last-20-ns metrics (mean ± SD) for apo AChE and three complexes.**

| Metric | apo AChE | ALLLHRC | FLLHTTR | YLSLLQR |
| --- | --- | --- | --- | --- |
| Cα RMSD (nm) | 0.1897 ± 0.0090 | 0.1916 ± 0.0092 | 0.1640 ± 0.0080 | 0.1625 ± 0.0078 |
| Peptide self-fit RMSD (nm) | — | 0.2518 ± 0.0136 | 0.1752 ± 0.0111 | 0.0911 ± 0.0098 |
| RMSF mean (nm) | 0.0835 ± 0.0659 | 0.0876 ± 0.0581 | 0.0778 ± 0.0504 | 0.0771 ± 0.0498 |
| SASA (nm²) | 212.25 ± 2.89 | 217.47 ± 2.49 | 213.88 ± 2.36 | 209.71 ± 2.35 |
| Rg (nm) | 2.3045 ± 0.0056 | 2.3107 ± 0.0052 | 2.2967 ± 0.0047 | 2.3028 ± 0.0051 |
| Intermolecular H-bonds | — | 2.19 ± 0.80 | 7.03 ± 1.28 | 2.93 ± 1.14 |
| Persistent contact pairs | — | 7 | 7 | 7 |
| DSSP α-helix / β-sheet (%) | 33.44 / 17.35 | 33.66 / 16.76 | 32.92 / 17.52 | 33.31 / 17.02 |

Apo RMSD levels near 0.19 nm (Figures 5A–7A). ALLLHRC follows that control (complex 0.1916 nm). FLLHTTR and YLSLLQR drop below apo after 50–70 ns (0.1640 and 0.1625 nm), which reads as rigidification, not unfolding. Peptide self-fit RMSD is highest for ALLLHRC (0.2518 nm) and lowest for YLSLLQR (0.0911 nm). Catalytic-core RMSF stays low; mean RMSF is below apo for FLLHTTR and YLSLLQR. Rg remains 2.30–2.31 nm. SASA rises for ALLLHRC (217.47 nm²), sits near apo for FLLHTTR (213.88 nm²), and falls only for YLSLLQR (209.71 nm²; Figure 7C). Hydrogen-bond histories differ: ALLLHRC decays to 2.19 ± 0.80; FLLHTTR holds 7.03 ± 1.28 for the whole run (Figure 6F); YLSLLQR averages 2.93 ± 1.14. Helix (~33%) and sheet (~17%) overlay the apo bars. Each complex keeps seven persistent contact pairs. Centre-of-mass RDF peaks lie at 1.22 nm (ALLLHRC), 1.80 nm (FLLHTTR) and 1.62 nm (YLSLLQR), i.e. surface residence rather than bulk solvent.

## Discussion

### A possible PAS path from oral peptides to AD

AD pairs amyloid deposition with cholinergic failure [@selkoe2016amyloid; @hampel2018cholinergic]. Apart from hydrolysis, AChE promotes Aβ fibrils at the PAS, and AChE–Aβ complexes out-toxify free Aβ [@inestrosa1996ache]. A hydrophobic PAS motif is sufficient for that chaperone job [@deferrari2001motif], and PAS-directed ligands can suppress AChE-driven aggregation in biochemical assays [@bartolini2003pas]. Accelerated MD places Aβ on the AChE surface as a nucleation centre [@lushchekina2017amd]; a 1-μs trajectory keeps Aβ at the PAS, mainly at 344–361 [@atanasova2020md]. Periodontitis and *P. gingivalis* supply an exposure path [@dominy2019pgingivalis; @ilievski2018oral; @chalmers2025primer]. Docking and 100-ns runs indicate that periodontitis-derived micropeptides can occupy that same PAS. Four linked steps sketch a possible mechanism.

1. PAS recognition.  
   Best poses of the twelve peptides cluster at the PAS and gorge mouth (Figures 2–4). FLLHTTR anchors Asp74, Tyr72 and His287 (best-run −9.60 kcal/mol; Figure 3C). YLSLLQR touches PAS (Tyr72, Thr75) and the catalytic entrance (mean −9.44 ± 0.09 kcal/mol; Figure 4L). LLHPLRL spans Trp286/Tyr341 to His447 (Figure 4I). HLLTLKKHV reaches Tyr72 and Phe346 in the 344–361 Aβ residence zone. That geometry is the PAS Inestrosa identified as pro-fibrillar and Atanasova occupied with Aβ.

2. A lasting enzyme–peptide complex.  
   Over 100 ns the fold stays globular (RMSD 0.16–0.19 nm, Rg 2.30–2.31 nm, helix ~33% / sheet ~17%; Figures 5–7). FLLHTTR and YLSLLQR become more compact than apo in late RMSD, so the peptide sits on the surface and stiffens the protein rather than opening it. Intermolecular hydrogen bonds persist: FLLHTTR holds a dense polar net (7.03 ± 1.28; Figure 6F), YLSLLQR averages 2.93 ± 1.14, and ALLLHRC keeps seven contact pairs after early rearrangement. Lushchekina and Atanasova described a surface-bound, non-dissociating AChE–Aβ complex; the same pattern appears here for oral micropeptides.

3. Restricted acetylcholine access.  
   The PAS sits at the mouth of the 20-Å gorge that feeds the triad [@hampel2018cholinergic; @cheung2012ache]. Occupancy of Asp74/Tyr72/Trp286/Tyr341 can hinder substrate entry even while the catalytic core remains folded (low RMSF in panels B). The same pose that docks to the PAS therefore hits the cholinergic axis of AD.

4. Pathological chaperone activity.  
   Because the PAS is a documented pro-fibrillar site [@inestrosa1996ache; @deferrari2001motif], a heterologous peptide that stays there can lower the barrier for endogenous Aβ. FLLHTTR supplies a persistent polar net on the PAS (Figure 6F) that matches its docking pose (Figure 3C). YLSLLQR buries surface (SASA 209.71 versus 212.25 nm²; Figure 7C) and is the most rigid bound peptide (self-fit RMSD 0.0911 nm). Lushchekina’s nucleation-centre picture then maps onto these complexes: folded AChE presents a peptide-coated PAS on which Aβ oligomers can co-assemble. AChE–Aβ assemblies are already more synaptotoxic than free Aβ [@inestrosa1996ache]; a bacterial micropeptide on the same site is a possible route to hybrid nuclei.

### From the mouth to cortical AChE

Chronic periodontitis can move *P. gingivalis* products into blood through a broken epithelium, gingipains and vesicles [@guo2010gingipain; @ho2015omv]. Cytokines and proteases raise BBB leakiness, so short, leucine-rich, cationic peptides that scored BBB-high (a label that is almost as common in the healthy library) could reach interstitial fluid [@chalmers2025primer; @dominy2019pgingivalis]. PAS docking then gives a landing site on an enzyme that is both a cholinergic hydrolase and an amyloid chaperone. In this sketch the twelve sequences are pathogenic candidates because they occupy the experimentally mapped Aβ-binding PAS and remain bound for 100 ns, not because RMSD rises.

## Conclusions

Twelve 7–9-aa periodontitis micropeptides dock to human AChE. FLLHTTR, YLSLLQR and ALLLHRC stay on the surface for 100 ns without unfolding the enzyme. FLLHTTR forms the densest PAS hydrogen-bond net; YLSLLQR is the only complex that buries surface area. Read against the amyloid cascade [@selkoe2016amyloid], the cholinergic hypothesis [@hampel2018cholinergic], and the PAS chaperone experiments of Inestrosa, Lushchekina and Atanasova, the calculations support a possible mechanism in which oral pathogenic peptides occupy AChE, hinder acetylcholine access, and co-nucleate Aβ on the same PAS.

## References

1. Scheltens P, De Strooper B, Kivipelto M, et al. Alzheimer’s disease. *Lancet*. 2021;397(10284):1577–1590. doi:10.1016/S0140-6736(20)32205-4.
2. Selkoe DJ, Hardy J. The amyloid hypothesis of Alzheimer’s disease at 25 years. *EMBO Mol Med*. 2016;8(6):595–608. doi:10.15252/emmm.201606210.
3. Hampel H, Mesulam MM, Cuello AC, et al. The cholinergic system in the pathophysiology and treatment of Alzheimer’s disease. *Brain*. 2018;141(7):1917–1933. doi:10.1093/brain/awy132.
4. Inestrosa NC, Alvarez A, Pérez CA, et al. Acetylcholinesterase accelerates assembly of amyloid-β-peptides into Alzheimer’s fibrils. *Neuron*. 1996;16(4):881–891. doi:10.1016/s0896-6273(00)80108-7.
5. De Ferrari GV, Canales MA, Shin I, et al. A structural motif of acetylcholinesterase that promotes amyloid β-peptide fibril formation. *Biochemistry*. 2001;40(35):10447–10457. doi:10.1021/bi0101392.
6. Chalmers JC, Hernandez-Kapila YL. The role of the oral microbiome, host response, and periodontal disease treatment in Alzheimer’s disease: a primer. *Periodontol 2000*. 2025;98(1):220–227. doi:10.1111/prd.12631.
7. Belstrøm D, Constancias F, Drautz-Moses DI, et al. Periodontitis associates with species-specific gene expression of the oral microbiota. *npj Biofilms Microbiomes*. 2021;7:76. doi:10.1038/s41522-021-00247-y.
8. Guo Y, Nguyen KA, Potempa J. Dichotomy of gingipains action as virulence factors. *Periodontol 2000*. 2010;54(1):15–44. doi:10.1111/j.1600-0757.2010.00377.x.
9. Ho MH, Chen CH, Goodwin JS, et al. Functional advantages of *Porphyromonas gingivalis* vesicles. *PLoS One*. 2015;10(4):e0123448. doi:10.1371/journal.pone.0123448.
10. Larvin H, Gao C, Kang J, et al. The impact of study factors in the association of periodontal disease and cognitive disorders. *Age Ageing*. 2023;52(2):afad015. doi:10.1093/ageing/afad015.
11. Ide M, Harris M, Stevens A, et al. Periodontitis and cognitive decline in Alzheimer’s disease. *PLoS One*. 2016;11(3):e0151081. doi:10.1371/journal.pone.0151081.
12. Dominy SS, Lynch C, Ermini F, et al. *Porphyromonas gingivalis* in Alzheimer’s disease brains. *Sci Adv*. 2019;5(1):eaau3333. doi:10.1126/sciadv.aau3333.
13. Ilievski V, Zuchowska PK, Green SJ, et al. Chronic oral application of a periodontal pathogen results in brain inflammation, neurodegeneration and amyloid beta production in wild type mice. *PLoS One*. 2018;13(10):e0204941. doi:10.1371/journal.pone.0204941.
14. Hu C, Li H, Huang L, et al. Periodontal disease and risk of Alzheimer’s disease: a two-sample Mendelian randomization. *Brain Behav*. 2024;14(4):e3486. doi:10.1002/brb3.3486.
15. Sberro H, Fremin BJ, Zlitni S, et al. Large-scale analyses of human microbiomes reveal thousands of small, novel genes. *Cell*. 2019;178(5):1245–1259.e14. doi:10.1016/j.cell.2019.07.016.
16. Durrant MG, Bhatt AS. Automated prediction and annotation of small open reading frames in microbial genomes. *Cell Host Microbe*. 2021;29(1):121–131.e4. doi:10.1016/j.chom.2020.11.002.
17. Lushchekina SV, Kots ED, Novichkova DA, Petrov KA, Masson P. Role of acetylcholinesterase in β-amyloid aggregation studied by accelerated molecular dynamics. *BioNanoScience*. 2017;7(2):396–402. doi:10.1007/s12668-016-0375-x.
18. Atanasova M, Dimitrov I, Ivanov S. Molecular dynamics simulations of acetylcholinesterase–beta-amyloid peptide complex. *Cybern Inf Technol*. 2020;20(6):140–154. doi:10.2478/cait-2020-0068.
19. Bartolini M, Bertucci C, Cavrini V, Andrisano V. β-Amyloid aggregation induced by human acetylcholinesterase: inhibition studies. *Biochem Pharmacol*. 2003;65(3):407–416. doi:10.1016/s0006-2952(02)01514-9.
20. Cheung J, Rudolph MJ, Burshteyn F, et al. Structures of human acetylcholinesterase in complex with pharmacologically important ligands. *J Med Chem*. 2012;55(23):10282–10286. doi:10.1021/jm300871x.
21. Chen T, Yu WH, Izard J, et al. The Human Oral Microbiome Database: a web accessible resource for investigating oral microbe taxonomic and genomic information. *Database (Oxford)*. 2010;2010:baq013. doi:10.1093/database/baq013.
22. Belstrøm D, Jersie-Christensen RR, Lyon D, et al. Metaproteomics of saliva identifies human protein markers specific for individuals with periodontitis and dental caries compared to orally healthy controls. *PeerJ*. 2016;4:e2433. doi:10.7717/peerj.2433.
23. Du Z, Ding X, Xu Y, Li Y. UniDL4BioPep: a universal deep learning architecture for binary classification in peptide bioactivity. *Brief Bioinform*. 2023;24(3):bbad135. doi:10.1093/bib/bbad135.
24. Rathore AS, Jain S, Choudhury S, Raghava GPS. A large language model for predicting neurotoxic peptides and neurotoxins. *Protein Sci*. 2025;34(8):e70200. doi:10.1002/pro.70200.
25. Aptekmann AA, Buongiorno J, Giovannelli D, et al. mebipred: identifying metal-binding potential in protein sequence. *Bioinformatics*. 2022;38(14):3532–3540. doi:10.1093/bioinformatics/btac358.
26. Olsen TH, Yesiltas B, Marin FI, et al. AnOxPePred: using deep learning for the prediction of antioxidative properties of peptides. *Sci Rep*. 2020;10:21471. doi:10.1038/s41598-020-78319-w.
27. Trott O, Olson AJ. AutoDock Vina: improving the speed and accuracy of docking with a new scoring function. *J Comput Chem*. 2010;31(2):455–461. doi:10.1002/jcc.21334.
28. Eberhardt J, Santos-Martins D, Tillack AF, Forli S. AutoDock Vina 1.2.0: new docking methods, expanded force field, and Python bindings. *J Chem Inf Model*. 2021;61(8):3891–3898. doi:10.1021/acs.jcim.1c00203.
29. Abraham MJ, Murtola T, Schulz R, et al. GROMACS: high performance molecular simulations through multi-level parallelism from laptops to supercomputers. *SoftwareX*. 2015;1–2:19–25. doi:10.1016/j.softx.2015.06.001.
30. Lindorff-Larsen K, Piana S, Palmo K, et al. Improved side-chain torsion potentials for the Amber ff99SB protein force field. *Proteins*. 2010;78(8):1950–1958. doi:10.1002/prot.22711.
31. Torres MDT, Brooks EF, Cesaro A, et al. Mining human microbiomes reveals an untapped source of peptide antibiotics. *Cell*. 2024;187(19):5453–5467.e15. doi:10.1016/j.cell.2024.07.027.
32. Escapa IF, Chen T, Huang Y, et al. New insights into human nostril microbiome from the expanded Human Oral Microbiome Database (eHOMD). *mSystems*. 2018;3(3):e00187-18. doi:10.1128/mSystems.00187-18.
33. Jiang X, Zhang Y, Wang H, et al. In-depth metaproteomics analysis of oral microbiome for lung cancer. *Research (Wash D C)*. 2022;2022:9781578. doi:10.34133/2022/9781578.
34. Yuan J, Cao Q, Chen M, et al. OSaMPle workflow for salivary metaproteomics analysis reveals dysbiosis in inflammatory bowel disease patients. *npj Biofilms Microbiomes*. 2025;11:63. doi:10.1038/s41522-025-00692-z.
35. Gu Y, Chen P, Wang B, et al. Prediction of blood-brain barrier penetrating peptides based on data augmentation with Augur. *BMC Biol*. 2024;22:86. doi:10.1186/s12915-024-01883-4.
36. Kryger G, Silman I, Sussman JL. Structure of acetylcholinesterase complexed with E2020 (Aricept): implications for drug design. *Structure*. 1999;7(3):297–307. doi:10.1016/s0969-2126(99)80040-9.
