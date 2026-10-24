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

## Predict from your own machine (same result as the website)

```
git clone <repo> && cd <repo>
pip install -r requirements.txt        # pinned versions; the saved models need them
python predict_cli.py --material "BC:MgCO3 1:1" --model v3 --conc 65 --time 190 --pH 8 --dose 10
```
`--material all` prints all five. `--model` is one of `v3`, `v2`, `v1-ann`, `v1-rsm`. It uses the same code (`app/predictor.py`) and model file (`app/models/bundle.joblib`) as the live site.
