# Adsorption RSM vs ANN analysis

Response surface methodology (RSM) and artificial neural network (ANN) modelling of adsorption capacity (qe, mg/g) for 5 biochar materials: Biochar (control), Repyrolysis 1:1, Repyrolysis 2:1, BC:MgCO₃ 1:1 and BC:MgCO₃ 2:1. Each material has 32 runs with 3 replicates, and the factors are concentration, time, pH and dosage.

**Goals:** optimise the four factors for each material (pH limited to 4–8), find the best material by ANOVA, and compare actual vs predicted qe, with a leakage-free train/test evaluation.

| Path | Contents |
|---|---|
| `docs/` | Input documents: data sheet, voice-note constraints, notes, reference papers |
| `rsm_ann_analysis.ipynb` | Analysis notebook (run in Google Colab) |
| `results/REPORT.md`, `results/REPORT.docx` | Full end-to-end explanation of every run |
| `results/v1/` | Run 1: RSM + ANN, the three goals |
| `results/v2/` | Run 2: accuracy-improvement methods using the same data |

To reproduce, upload the notebook to https://colab.research.google.com and choose **Runtime → Run all**. No measured value is ever altered or synthesised.
