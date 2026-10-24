"""Tables and chart data for the comparison panels, read straight from the result workbooks (no retyped numbers)."""
import os
from functools import lru_cache
import pandas as pd

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'results')
TYPES = [('Linear', 'First order (linear)'), ('Interaction', 'Second order (two-factor interaction)'), ('Quadratic', 'Quadratic (squared)')]

def _x(v, f): return pd.read_excel(os.path.join(RESULTS, v, f), sheet_name=None)

@lru_cache(maxsize=1)
def load():
    v1, v3 = _x('v1', 'RSM_ANN_results.xlsx'), _x('v3', 'RSM_ANN_v3_results.xlsx')
    fit = v1['Fit summary']
    mats = list(fit.Material.unique())
    full, red = (fit[fit.Model == m].set_index('Material') for m in ('Full quadratic', 'Reduced'))
    rank, opt = v1['Material ranking'].set_index('Material'), v1['Optimum pH 4-8'].set_index('Material')
    anova = {}
    for name, df in v1.items():
        if name.startswith('ANOVA '): anova[mats[int(name.split()[1]) - 1]] = df[df['Term type'].notna()].set_index('Source')
    terms = [{'type': lab, 'rows': [{'term': s, 'p': {m: float(anova[m].loc[s, 'p-value']) for m in mats}} for s in anova[mats[0]].index[anova[mats[0]]['Term type'] == t]]} for t, lab in TYPES]
    sig_count = {m: int((anova[m]['Significant (p<0.05)'] == 'Yes').sum()) for m in mats}
    fits = [{'mat': m, 'r2': full.loc[m, 'R2'], 'adj': full.loc[m, 'Adj R2'], 'pred': full.loc[m, 'Pred R2'], 'r2_red': red.loc[m, 'R2'],
             'sig': sig_count[m], 'n': len(anova[m])} for m in mats]
    mats_tbl = [{'mat': m, 'rank': int(rank.loc[m, 'Unnamed: 0']), 'mean': rank.loc[m, 'Mean qe (all runs)'], 'best': rank.loc[m, 'Max observed qe'],
                 'rsm': opt.loc[m, 'RSM qe pred'], 'pi': (opt.loc[m, '95% PI low'], opt.loc[m, '95% PI high']), 'ann': opt.loc[m, 'ANN qe pred'],
                 'conc': opt.loc[m, 'Concentration (ppm)'], 'time': opt.loc[m, 'Time (min)'], 'pH': opt.loc[m, 'pH'], 'dose': opt.loc[m, 'Dosage (mg)']} for m in mats]
    mats_tbl.sort(key=lambda r: r['rank'])
    sel = v3['Model selection summary']
    models_cv = [{'model': r['Model'], 'r2': r['5-fold R2 mean'], 'rmse': r['5-fold RMSE mean']} for _, r in sel.iterrows()]
    ho, lo = v1['Hold-out test metrics'], v1['LOCO metrics']
    v3m = v3['Best vs baselines per material'].set_index('Material')
    per_mat = []
    for m in mats + ['ALL']:
        g = lambda d, mod: float(d[(d.Material == m) & (d.Model == mod)].R2.iloc[0])
        per_mat.append({'mat': m, 'ho': {'RSM': g(ho, 'RSM reduced'), 'ANN (v1)': g(ho, 'ANN'), 'ANN (v3)': float(v3m.loc[m, 'Hold-out R2 ANN Adam early-stop + conc/dose'])},
                        'lo': {'RSM': g(lo, 'RSM reduced'), 'ANN (v1)': g(lo, 'ANN'), 'ANN (v3)': float(v3m.loc[m, 'LOCO R2 ANN Adam early-stop + conc/dose'])}})
    return dict(mats=mats, fits=fits, terms=terms, materials=mats_tbl, models_cv=models_cv, per_mat=per_mat)
