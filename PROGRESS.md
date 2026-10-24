# Progress log: public dashboard and Render deployment

Updated after each step. Newest status first.

## Current status (2026-10-24)

| Item | State |
|---|---|
| Web app (predict page, results browser) | Done, tested locally and live |
| Live deployment | **https://adsorption-predictor.onrender.com** (Render, free plan, Singapore) |
| Deploys from branch | `main`. **Action needed:** in the Render dashboard open the service → Settings → Branch and set it to `main` (the old feature branch was deleted, so until then Render keeps serving the last build but cannot redeploy) |
| Repository public | **Not done yet.** GitHub blocked the change from the automated session. Do it by hand: repo → Settings → General → Danger Zone → Change visibility → Public |
| Work on `main` | Done. All commits are on `main` under the repo owner's name; the feature branch is deleted |

## What was built

1. **Models** (`scripts/train_models.py` → `app/models/bundle.joblib`): trained on all 480 measured rows with the same definitions as `results/v3/rsm_ann_v3.ipynb`.
   - v1 RSM (reduced quadratic, one per material), v1 ANN, v2 ANN + Gaussian Process ensemble, v3 ANN (Adam, early stopping).
   - No lab value is changed or synthesised. `app/data.csv` is the data table extracted from the notebook.
2. **Predict page** (`/`): enter concentration, time, pH and dose, choose a model version, and the page calls `/api/predict` live. It shows qe for all 5 materials, a table comparing every version, and a warning when versions disagree by 15 mg/g or more. Inputs outside the tested ranges (conc 10–100, time 60–360, pH 4–12, dose 10–150) are rejected.
3. **Results** (`/results`, `/results/v1|v2|v3`): accuracy table, then every file of each version: reports (rendered in the browser), Excel sheets (as tables), notebooks (read-only), plots, Word files (download).
4. **Deployment files**: `render.yaml`, `requirements.txt` (pinned versions, same ones used to train the models, so the pickle loads).

## Checks done

- All routes return 200; path traversal (`/files/..%2f...`) returns 404.
- Browser test: prediction updates, version switch re-runs, bad input shows an error, report images load.
- Live predictions equal local predictions (BC:MgCO₃ 1:1 at 65 ppm, 190 min, pH 8, 10 mg: v3 81.4, v2 89.5, v1 ANN 95.0, v1 RSM 113.8).

## Known issues and caveats

- v3 predicts 81.4 at the optimum here, while `V3_REPORT.md` says 68.2. The v3 ANN uses random early-stopping splits and a different scikit-learn version, so retraining gives a different network. Both sit inside the report's "expect 70–95 mg/g". The accuracy table on the site comes from the Colab runs, not from this retrained copy.
- v3 under-predicts the highest-qe (low dose) results; the site says so on the predict page.
- Render free plan sleeps after ~15 min idle; the first visit afterwards takes about 30–60 s.
- `docs/` holds two published journal PDFs and personal notes (`voice.docx`, `doubts.docx`). They become public with the repo (the website does not serve `docs/`).

## Commit history of this work

See `git log`. Each step below is its own commit.
