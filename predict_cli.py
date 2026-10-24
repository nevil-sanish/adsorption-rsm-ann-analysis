#!/usr/bin/env python
"""Predict qe (mg/g) from the command line with the same models the website uses.

  python predict_cli.py --material "BC:MgCO3 1:1" --model v3 --conc 65 --time 190 --pH 8 --dose 10
  python predict_cli.py --material all --model v3 --conc 65 --time 190 --pH 8 --dose 10

Setup (the pinned versions matter: the saved models are scikit-learn pickles):
  pip install -r requirements.txt
"""
import argparse, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app'))
import predictor as P

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument('--material', default='all', help=f"'all' or one of: {', '.join(P.MATS)}")
ap.add_argument('--model', default='v3', choices=list(P.VERSIONS))
for k, (lo, hi) in P.RANGES.items(): ap.add_argument(f'--{k}', type=float, required=True, help=f'{lo} to {hi}')
a = ap.parse_args()
vals = dict(conc=a.conc, time=a.time, pH=a.pH, dose=a.dose)
errs = P.validate(**vals)
if errs: ap.error('; '.join(errs.values()))
if a.material != 'all' and a.material not in P.MATS: ap.error(f'unknown material; choose from {P.MATS}')
pred = P.predict(a.model, P.MATS, **vals)
for m, q in pred.items():
    if a.material in ('all', m): print(f'{m:<18} {q:8.2f} mg/g')
