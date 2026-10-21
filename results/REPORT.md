# RSM and ANN analysis of adsorption capacity: end-to-end report

**Project:** adsorption capacity (qe, mg/g) of 5 biochar materials
**Data:** 5 materials × 32 runs × 3 replicates = 480 laboratory measurements (`docs/RSM Data_Table.docx`)
**Where it ran:** Google Colab (CPU runtime), notebook `rsm_ann_analysis.ipynb`

---

## 1. Folder layout

```
suchithra/
├── docs/                         Documents you shared (inputs, never modified)
│   ├── RSM Data_Table.docx / .md   Data sheet and objectives
│   ├── voice.docx                  Experimenter's constraints (voice note)
│   ├── doubts.docx                 Notes from the first analysis
│   ├── s13369-022-07391-3.pdf      Nguyen et al. 2023 (RSM / CCRD reference)
│   └── Comparative assessment ... .pdf   Kumari et al. 2026 (ANN vs RSM reference)
├── rsm_ann_analysis.ipynb        v1 + v2 notebook (run in Google Colab)
├── rsm_ann_v3.ipynb              v3 notebook
└── results/
    ├── REPORT.md / REPORT.docx   This document
    ├── v1/      Version 1: RSM + ANN, the three goals
    ├── v2/      Version 2: v1 + accuracy-improvement methods
    └── v3/      Version 3: model selection by repeated stratified 5-fold CV
```

---

## 2. Objectives and constraints

**Objectives (from the data sheet)**
1. Optimise Concentration, Time, pH and Dosage for each of the 5 materials.
2. Find the best material using ANOVA.
3. Give the actual and predicted adsorption capacity for each material.

**Constraints (from the voice note)**
- The optimum pH must be **4–8**. A model optimum at pH 12 is not practical to recommend to farmers.
- The response is adsorption capacity qe. A low dose (about 10–25 mg) is expected to give the highest qe, because the same phosphate is spread over fewer grams.
- **Biochar is the control.** Its negative qe values are genuine lab results, showing that plain biochar does not adsorb. It is reported, not optimised.
- The values for repyrolysis 1:1 and 2:1 are nearly identical (94 of 96). The experimenter confirmed these are **genuine lab data**. *(An earlier note in `docs/doubts.docx` called this a copy-paste error; that was wrong.)*
- **No artificial data:** no values were added, changed, removed or synthesised in any version. The notebook checks this automatically.

---

## 3. The data and the experimental design

| Factor | Code | −2 | −1 | 0 | +1 | +2 |
|---|---|---|---|---|---|---|
| Concentration (ppm) | A (x1) | 10 | 25 | 50 | 75 | 100 |
| Time (min) | B (x2) | 60 | 120 | 180 | 240 | 360 |
| pH | C (x3) | 4 | 6 | 8 | 10 | 12 |
| Dosage (mg) | D (x4) | 10 | 20 | 50 | 100 | 150 |

The 32 runs per material are made up of:
- Runs 1–4: centre point (all factors at 0), 4 times.
- Runs 5–20: one factor changed at a time, at ±1 and ±2.
- Runs 21–28: 8 runs at ±1 with several factors changed together.
- Runs 29–32: 4 extreme corners at ±2.

**Notes on the design**
- This is not a full central composite design, so some interaction terms are partly confounded (for example Conc×Time and Conc×Dose correlate at 0.89). Interaction p-values should be read with care.
- Time and dose levels are not evenly spaced in real units, but they are coded −2 to +2.
- **Why the earlier analysis gave pH 12:** pH 12 appears only in runs 16, 30 and 31. Run 31 combines pH 12 with the highest concentration (100) and lowest dose (10). It is the highest-qe run for both repyrolysis materials and for BC:MgCO₃ 2:1. When pH alone is changed (runs 15 and 16), pH 12 gives *lower* qe than pH 4. So the "pH 12 optimum" comes from that corner run, not from a real pH effect.

---

## 4. Key terms

- **R²:** the share of the variation in qe that a model explains. 1 is perfect; 0 is no better than predicting the average; negative is worse than the average.
- **Adjusted R²:** R² with a penalty for unnecessary terms.
- **Predicted R²:** how well the model predicts a point that was left out. This is the honest measure of accuracy.
- **RMSE / MAE:** typical prediction error in mg/g. RMSE weights large errors more heavily.
- **ANOVA:** tests whether an effect is real or just noise. p < 0.05 means significant.
- **Lack of fit:** compares the model's error with the replicate scatter. Your replicates are very tight (about 2 mg/g), so this test flags almost any model. Nguyen et al. also reported a significant lack of fit.
- **Data leakage:** information from the test data reaching the model during training, which makes accuracy look better than it really is.

---

## 5. How leakage was prevented (both versions)

1. **Split by run condition, not by row:** the 3 replicates of a run are always together, on one side.
2. **Centre runs 1–4 count as one condition,** since their settings are identical.
3. **A condition is held out for all 5 materials at once.** The ANN learns from all materials together, so this stops it seeing the condition through another material.
4. **Stratified test draw (seed 42):** 1 run from each one-factor block (5–8, 9–12, 13–16, 17–20) and 2 from the factorial block (21–28). The test runs were **5, 12, 15, 18, 24 and 27**: 6 conditions, 90 measurements. Centre and extreme-corner runs always stay in training, so every test point lies inside the tested range.
5. **All tuning is done inside the training data** (grouped cross-validation): which RSM terms to keep, ANN size and regularisation, and input scaling. The test set is scored once.
6. **Leave-one-condition-out (LOCO):** every one of the 29 conditions is predicted by a model trained and tuned from scratch without it. Six test runs is a small sample, so LOCO gives a more stable estimate.

---

## 6. What was run in Google Colab

1. The notebook `rsm_ann_analysis.ipynb` was uploaded to Colab. It is saved in Google Drive, and the 480 lab rows are embedded in a hidden cell.
2. **Runtime → Run all** on a standard CPU runtime. All libraries come pre-installed in Colab: pandas, numpy, statsmodels, scipy, scikit-learn, matplotlib and openpyxl.
3. The last cell zips the `results/` folder and downloads it (`RSM_ANN_results.zip`). Its contents were copied into the version folders here.

| Version | Colab notebook (Google Drive) | Run time |
|---|---|---|
| v1 | https://colab.research.google.com/drive/1s1rngJQQXDMTjDQfb9LMWoo16Mpeg9Xr | about 20 min |
| v2 | https://colab.research.google.com/drive/1rWQat80Ue99-leizVeROoQOYSrzqOzYH?authuser=4 (Mercury account, T4) | about 30 min |
| v3 | https://colab.research.google.com/drive/1CM81nmv71kRFWK9tKOnDr6FDrYOdZraL?authuser=4 (Mercury account, T4) | running |

---

## 7. Version 1: baseline RSM and ANN (`results/v1/`)

### 7.1 What was done, step by step

| Step | Notebook section | What it does |
|---|---|---|
| 1 | Data | Loads the 480 measurements and marks centre runs 1–4 as one condition. |
| 2 | Model definitions | **RSM:** a full quadratic (4 linear + 4 squared + 6 interaction terms) per material, plus a *reduced* version that drops non-significant terms one at a time (p > 0.05) while keeping lower-order terms that a significant term depends on. **ANN:** one network for all materials (inputs: 4 coded factors + material as one-hot), 1 hidden layer with tanh activation and the L-BFGS solver; neurons {4, 8, 12} × L2 {0.001, 0.01, 0.1} chosen by 4-fold grouped CV; final model = average of 5 networks. |
| 3 | Train/test split | Stratified, leakage-free split (section 5). |
| 4 | Hold-out test | Models fitted on training data only, then scored once on the 6 unseen test runs. |
| 5 | LOCO | Each of the 29 conditions predicted by models fitted and tuned without it. |
| 6 | Final RSM (all data) | ANOVA tables and R², adjusted R², predicted R², and lack of fit for each material. |
| 7 | Goal 1 optimisation | Maximise qe with the reduced RSM. **pH is limited to 4–8** and the search is kept inside the tested design region (a leverage limit), so nothing is extrapolated far from the experiments. pH 4–12 is shown only for comparison. The ANN prediction at each optimum is given as a cross-check. |
| 8 | Validation plan | Optimum rounded to practical lab settings, with predicted qe and a 95% prediction interval. |
| 9 | Goal 2 | Two-way ANOVA (material × condition), Tukey HSD between materials, and a ranking table. |
| 10 | Goal 3 | Actual vs predicted for every run: RSM fitted, RSM unseen (LOCO) and ANN unseen (LOCO). |
| 11 | Plots | Actual-vs-predicted scatter, plus 6 response surfaces per material (other factors held at the optimum). |
| 12 | Export | Excel workbook and PNG files. |

### 7.2 Results

**Goal 2: the best material is BC:MgCO₃ 1:1**

| Rank | Material | Mean qe | Best observed qe | R² | Adj R² | Pred R² |
|---|---|---|---|---|---|---|
| 1 | BC:MgCO₃ 1:1 | 40.7 | 91.5 | 0.962 | 0.956 | 0.948 |
| 2 | Repyrolysis 1:1 | 32.9 | 58.8 | 0.943 | 0.936 | 0.932 |
| 3 | Repyrolysis 2:1 | 32.6 | 54.4 | 0.935 | 0.927 | 0.920 |
| 4 | BC:MgCO₃ 2:1 | 20.9 | 51.1 | 0.744 | 0.724 | 0.692 |
| 5 | Biochar (control) | −2.1 | 4.2 | 0.793 | 0.768 | 0.734 |

- **Two-way ANOVA:** the effect of material is highly significant (F = 6637, p < 0.001).
- **Tukey HSD:** every pair of materials differs significantly, **except repyrolysis 1:1 vs 2:1 (p = 1.0)**. The ratio has no effect for repyrolysis, while for MgCO₃ 1:1 is clearly better than 2:1.
- **Significant terms for BC:MgCO₃ 1:1:** all 4 linear terms; the squared terms Conc², pH² and Dose²; the interactions Conc×Time, Conc×pH, Conc×Dose and Time×Dose. Not significant: Time², Time×pH and pH×Dose. The other materials are in the Excel sheets "ANOVA 1–5".

**Goal 1: optimum conditions (pH 4–8), rounded for the lab**

| Material | Conc (ppm) | Time (min) | pH | Dose (mg) | RSM qe | 95% PI | ANN qe |
|---|---|---|---|---|---|---|---|
| BC:MgCO₃ 1:1 | 65 | 190 | 8.0 | 10 | 113.8 | 103.6–123.9 | 94.0 |
| Repyrolysis 1:1 | 30 | 160 | 4.5 | 15 | 61.4 | 53.9–68.9 | 48.0 |
| Repyrolysis 2:1 | 30 | 150 | 5.0 | 10 | 65.2 | 57.2–73.2 | 49.9 |
| BC:MgCO₃ 2:1 | 100 | 230 | 8.0 | 15 | 54.7 | 41.1–68.3 | 52.4 |

- **pH:** every optimum respects pH 4–8. For both MgCO₃ materials it sits at the upper limit (pH 8).
- **Dose:** 10–15 mg for every material, which matches the experimenter's observation.
- **Expected qe for BC:MgCO₃ 1:1:** RSM predicts about 114 and the ANN about 94; the best observed was 91.5. Expect the lab validation run to come out around 90–115 mg/g.

**Goal 3: accuracy on unseen data**

| Data the model is scored on | RSM R² | ANN R² | ANN RMSE | ANN MAE |
|---|---|---|---|---|
| Training fit | 0.74–0.96 | — | — | — |
| Hold-out test (6 unseen runs) | 0.727 | **0.918** | 4.35 | 2.65 |
| LOCO (all 29 conditions, unseen) | 0.540 | **0.878** | 7.05 | 4.72 |

RSM fits its own data well but predicts unseen conditions less well. The ANN is clearly more accurate on unseen data. The run-by-run table is in the Excel sheet "Actual vs predicted".

### 7.3 Files in `v1/`

| File | Contents |
|---|---|
| `RSM_ANN_results.xlsx` | Every table: fit summary; ANOVA per material; optimum at pH 4–8 and at 4–12; lab validation plan; material ranking; two-way ANOVA; Tukey; actual vs predicted; hold-out and LOCO metrics; split |
| `actual_vs_predicted.png` | Actual vs predicted scatter per material |
| `surface_<material>.png` | 6 response surfaces per material |

---

## 8. Version 2: accuracy improvements (`results/v2/`)

**Full details:** `results/v2/V2_REPORT.md` / `.docx`. Ran on a Colab T4 runtime (Mercury account); the models compute on the CPU.

v2 re-runs all of v1 unchanged and adds 8 methods that use only the existing data:
- a conc ÷ dose input
- a removal-space target
- weighted RSM
- a Gaussian Process
- monotonic boosting
- an RSM + ANN hybrid
- an ANN with conc/dose
- an ANN + GPR ensemble

| Model | Test R² | LOCO R² | LOCO RMSE (mg/g) |
|---|---|---|---|
| **Ensemble (ANN + GPR)** (best on LOCO) | 0.907 | **0.887** | **6.78** |
| **ANN + conc/dose** (best on test) | **0.927** | 0.882 | 6.94 |
| ANN (v1) | 0.918 | 0.876 | 7.11 |
| RSM reduced (v1) | 0.727 | 0.540 | 13.71 |

- **Accuracy improved modestly,** most of all for BC:MgCO₃ 1:1.
- **The removal-space target failed** on unseen extreme conditions and should not be used.
- **At the BC:MgCO₃ 1:1 optimum,** the more accurate models predict about 90 mg/g, against 114 from RSM.

---

## 9. How to reproduce

1. Open https://colab.research.google.com → **Upload notebook** → choose `rsm_ann_analysis.ipynb`.
2. **Runtime → Run all.** Results download as `RSM_ANN_results.zip`.
3. The random seed is fixed at 42, so the split and the results are reproducible.

## 10. Limitations

- **Small dataset:** 29 distinct conditions per material. Test metrics on 6 runs vary with the choice of runs, so report LOCO alongside them.
- **Design:** confounded interactions and uneven level spacing (section 3).
- **Measurement noise:** replicates differ by about 2 mg/g, so no model can predict more precisely than about 2 mg/g.
- **Validation:** the predicted optima should be confirmed by lab runs (3 replicates each) at the validation-plan settings.
