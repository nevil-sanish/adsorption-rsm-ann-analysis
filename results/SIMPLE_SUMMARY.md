# Results in simple terms

**Study:** how much phosphate 5 materials can hold (adsorption capacity, written **qe**, in mg per gram)
**Analyses:** Version 1 (v1), Version 2 (v2) and Version 3 (v3, final)
**Data:** 480 lab measurements (5 materials × 32 experiments × 3 repeats). No values were changed or added.

---

## The short answer

- **Best material:** **BC:MgCO₃ 1:1** (biochar mixed with magnesium carbonate, 1:1).
- **Best conditions for it:** concentration **65 ppm**, time **190 minutes**, **pH 8**, dose **10 mg**.
- **Expected result:** about **90 mg/g** of phosphate held.
- **Prediction accuracy improved with each version.** The final model (v3) is about **90–94% accurate** on experiments it never saw.

---

## The 5 materials

| Material | What it is |
|---|---|
| Biochar | Plain biochar: the "control" used for comparison |
| Repyrolysis 1:1 | Biochar heated again, enriched (1:1) |
| Repyrolysis 2:1 | Biochar heated again, enriched (2:1) |
| BC:MgCO₃ 1:1 | Biochar with magnesium carbonate (1:1) |
| BC:MgCO₃ 2:1 | Biochar with magnesium carbonate (2:1) |

---

## Goal 1: the best conditions for each material

We tested 4 settings: **concentration, time, pH and dose**. A model found the combination that gives the highest qe for each material.

**Rule we followed:** pH must stay between **4 and 8**, because pH 12 is not practical for farmers.

| Material | Concentration | Time | pH | Dose | Expected qe |
|---|---|---|---|---|---|
| **BC:MgCO₃ 1:1** | 65 ppm | 190 min | 8 | 10 mg | **about 90 mg/g** |
| Repyrolysis 1:1 | 30 ppm | 160 min | 4.5 | 15 mg | about 50–60 mg/g |
| Repyrolysis 2:1 | 30 ppm | 150 min | 5 | 10 mg | about 50–55 mg/g |
| BC:MgCO₃ 2:1 | 100 ppm | 230 min | 8 | 15 mg | about 40–50 mg/g |
| Biochar | — | — | — | — | Not optimised: it does not hold phosphate |

**What this means**
- **A small dose (10–15 mg) works best** for every material. Less material per test means more phosphate held per gram, which matches what you saw in the lab.
- **pH 4–8 is enough.** Allowing pH up to 12 would improve results by less than 1 mg/g, so there is no reason to use high pH.
- The repyrolysis materials work best in **acidic water (pH 4.5–5)**. The magnesium carbonate materials work best at **pH 8**.
- **Next step:** run these conditions in the lab, 3 times each, to confirm.

*Why "about 90" and not a single number:* the simpler model (RSM) predicts 114 mg/g for BC:MgCO₃ 1:1. The more accurate models predict about 90, which matches the best value you actually measured (91.5 mg/g). So 90 is the realistic figure.

---

## Goal 2: which material is best

We used a statistical test (ANOVA) to check whether the materials really differ or the differences are just chance.

| Rank | Material | Average qe | Best qe measured | How well the model fits (out of 1.0) |
|---|---|---|---|---|
| **1** | **BC:MgCO₃ 1:1** | **40.7** | **91.5** | **0.96** |
| 2 | Repyrolysis 1:1 | 32.9 | 58.8 | 0.94 |
| 3 | Repyrolysis 2:1 | 32.6 | 54.4 | 0.94 |
| 4 | BC:MgCO₃ 2:1 | 20.9 | 51.1 | 0.74 |
| 5 | Biochar (control) | −2.1 | 4.2 | 0.79 |

**What this means**
- **BC:MgCO₃ 1:1 is clearly the best.** It holds the most phosphate, and the test shows it is truly better than every other material, not by chance.
- **All the enriched materials beat plain biochar by far.** Plain biochar holds almost nothing (its values are near zero or negative), which proves the enrichment is what works.
- **Repyrolysis 1:1 and 2:1 perform the same.** The ratio makes no difference for repyrolysis.
- **For magnesium carbonate, 1:1 is much better than 2:1.**
- **What matters most for the best material:** **dose** has the biggest effect, then **concentration**, then pH and time.

These results are the same in v1 and v2.

---

## Goal 3: actual vs predicted values

We checked how well the models predict qe. The fair test: we hid each experiment from the model, asked it to predict, and compared with the real lab value.

**Accuracy score:** 1.0 = perfect, 0 = useless. **Average error** is in mg/g (smaller is better).

| Material | Average real qe | v1 accuracy | v1 average error | **v2 accuracy** | **v2 average error** |
|---|---|---|---|---|---|
| **BC:MgCO₃ 1:1** | 40.7 | 0.80 | 5.3 | **0.87** | **5.0** |
| Repyrolysis 1:1 | 32.9 | 0.76 | 5.0 | 0.73 | **4.7** |
| Repyrolysis 2:1 | 32.6 | 0.64 | 5.8 | **0.72** | **4.6** |
| BC:MgCO₃ 2:1 | 20.9 | **0.58** | **4.9** | 0.43 | 5.3 |
| Biochar (control) | −2.1 | 0.23 | 2.5 | **0.57** | **1.8** |
| **All materials** | | **0.88** | | **0.89** | |

**Example: the best experiment of each material (real value vs prediction, with the experiment hidden from the model)**

| Material | Real qe | v1 predicted | v2 predicted |
|---|---|---|---|
| **BC:MgCO₃ 1:1** | **91.5** | 71.3 | **93.4** |
| Repyrolysis 1:1 | 58.8 | 58.4 | 51.3 |
| Repyrolysis 2:1 | 54.4 | 40.2 | 41.0 |
| BC:MgCO₃ 2:1 | 51.1 | 30.7 | 16.9 |
| Biochar | 4.2 | 8.5 | 1.4 |

**What this means**
- **The models predict qe with an average error of about 5 mg/g.** Repeating the same experiment in the lab already varies by about 2 mg/g, so this is reasonably close.
- **v2 is better overall,** and especially for the **best material**: its prediction for the top experiment (93.4) is very close to the real value (91.5).
- **BC:MgCO₃ 2:1 is the hardest to predict.** For that material, v1 does slightly better.
- **The simple model (RSM)** is good for explaining which factors matter (Goal 2) but not for predicting new conditions. The neural-network models (ANN) predict much better.

The complete table (every experiment, every material) is in `results/v2/RSM_ANN_results.xlsx`, sheet "Actual vs predicted".

---

## v1 vs v2: which is better?

| | v1 | v2 |
|---|---|---|
| Best conditions (Goal 1) | Same | Same |
| Best material (Goal 2) | Same | Same |
| Prediction accuracy (Goal 3) | Good (0.88) | **Slightly better (0.89), and much better for the best material** |
| Prediction model used | Neural network (ANN) | Neural network + Gaussian Process, averaged together |

**v2 is better.** It used only the same lab data, with no new or made-up values, but added a scientific hint: phosphate held depends on concentration ÷ dose.

---

---

## Version 3 (final): picking the best model fairly

v3 tested 14 models on the same data in a fair way, the standard "5-fold" test used in papers, and picked the most accurate one.

| | v1 | v2 | **v3 (final)** |
|---|---|---|---|
| Accuracy on unseen experiments | 0.92 | 0.93 | **0.94** |
| Accuracy, stricter check | 0.88 | 0.89 | **0.90** |
| Average error | 7.1 mg/g | 6.8 mg/g | **6.3 mg/g** |

- **Winner:** a neural network that stops training at the right moment ("early stopping") and is told that phosphate held depends on concentration ÷ dose.
- **Best material, BC:MgCO₃ 1:1:** accuracy rose from 0.80 (v1) to **0.91**.
- **Training longer does not help:** every network finished learning well before its limit.
- **One weakness:** the final model predicts a little **too low** for the very best results (low dose). So at the best conditions, expect about **70–95 mg/g**. The lab test will tell.

---

## Words used in this document

| Word | Simple meaning |
|---|---|
| qe (adsorption capacity) | How much phosphate (mg) one gram of material holds |
| Dose | How much material (mg) was used in the test |
| ANOVA | A test that checks whether differences are real or just chance |
| RSM | A simple equation-based model, standard in this type of study |
| ANN | A neural network: a computer model that learns patterns from the data |
| Gaussian Process | Another learning model that works well with small data |
| Accuracy (R²) | How well predictions match real values (1.0 = perfect) |
| Control | The plain material used for comparison (plain biochar) |
