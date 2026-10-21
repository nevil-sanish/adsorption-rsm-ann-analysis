# Adsorption RSM vs ANN analysis

Response surface methodology (RSM) and artificial neural network (ANN) modelling of adsorption capacity (qe, mg/g) for 5 biochar materials: Biochar (control), Repyrolysis 1:1, Repyrolysis 2:1, BC:MgCO₃ 1:1 and BC:MgCO₃ 2:1. Each material has 32 runs with 3 replicates, and the factors are concentration, time, pH and dosage.

**Goals:** optimise the four factors for each material (pH limited to 4–8), find the best material by ANOVA, and compare actual vs predicted qe, with a leakage-free train/test evaluation.

| Path | Contents |
|---|---|
| `docs/` | Input documents: data sheet, voice-note constraints, notes, reference papers |
| `results/v1/rsm_ann_analysis.ipynb` | v1 notebook (also contains the v2 sections; identical to `results/v2/rsm_ann_v2.ipynb`) |
| `results/REPORT.md`, `results/REPORT.docx` | Full end-to-end explanation of every run |
| `results/v1/` | Run 1: RSM + ANN, the three goals |
| `results/v2/` | Run 2: accuracy-improvement methods using the same data |
| `rsm_ann_v3.ipynb`, `results/v3/` | Run 3: best-model selection by repeated stratified 5-fold CV |

To reproduce, upload the notebook to https://colab.research.google.com and choose **Runtime → Run all**. No measured value is ever altered or synthesised.
