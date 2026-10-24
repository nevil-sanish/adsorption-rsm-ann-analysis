"""Loads the trained bundle and predicts qe for one condition with any model version."""
import os
import numpy as np, pandas as pd
from joblib import load

HERE = os.path.dirname(os.path.abspath(__file__))
B = load(os.path.join(HERE, 'models', 'bundle.joblib'))
MATS, LEVELS = B['mats'], B['levels']
KEYS = ['x1', 'x2', 'x3', 'x4']
RANGES = {'conc': (10, 100), 'time': (60, 360), 'pH': (4, 12), 'dose': (10, 150)}

# id -> (label, short description). "recommended" marks the final, most accurate model.
VERSIONS = {
    'v3': ('v3: ANN, Adam + early stopping', 'Final model. Most accurate on average (5-fold CV R² 0.903).'),
    'v2': ('v2: ANN + Gaussian Process ensemble', 'Better than v3 at the extreme low-dose, high-qe corner.'),
    'v1-ann': ('v1: ANN', 'First neural network (5-fold CV R² 0.859).'),
    'v1-rsm': ('v1: RSM (quadratic)', 'Equation-based model. Explains factor effects, but over/under-shoots on new conditions.'),
}

def _coded(df):
    for k, c in zip(KEYS, ['conc', 'time', 'pH', 'dose']):
        df[k] = np.interp(df[c], LEVELS[k], [-2, -1, 0, 1, 2])
    df['logR'] = np.log(df.conc / df.dose)
    return df

def _ann(model, df):
    onehot = pd.get_dummies(df.mat).reindex(columns=MATS, fill_value=0).astype(float)
    X = pd.concat([df[model['cols']].astype(float), onehot], axis=1).values
    return np.mean([n.predict(X) for n in model['nets']], axis=0)

def _rsm(df):
    out = np.empty(len(df))
    for i, (_, r) in enumerate(df.iterrows()):
        m = B['rsm'][r.mat]; v = m['params']['const']
        for t in m['terms']:
            if t.endswith('^2'): f = r[t[:-2]] ** 2
            elif '*' in t: a, b = t.split('*'); f = r[a] * r[b]
            else: f = r[t]
            v += m['params'][t] * f
        out[i] = v
    return out

def _gpr(df):
    out = np.empty(len(df))
    for i, (_, r) in enumerate(df.iterrows()):
        g = B['gpr'][r.mat]
        out[i] = g['gpr'].predict(g['scaler'].transform(pd.DataFrame([r[['x1', 'x2', 'x3', 'x4', 'logR']]])))[0]
    return out

def predict(version, mats, conc, time, pH, dose):
    """qe (mg/g) for each material in `mats`, under the chosen model version."""
    df = _coded(pd.DataFrame({'mat': mats, 'conc': float(conc), 'time': float(time), 'pH': float(pH), 'dose': float(dose)}))
    if version == 'v1-rsm': p = _rsm(df)
    elif version == 'v1-ann': p = _ann(B['ann_v1'], df)
    elif version == 'v2': p = (_ann(B['ann_v2'], df) + _gpr(df)) / 2
    elif version == 'v3': p = _ann(B['ann_v3'], df)
    else: raise ValueError(f'unknown version {version}')
    return dict(zip(mats, [float(x) for x in p]))

def validate(conc, time, pH, dose):
    out = {}
    for name, v in zip(['conc', 'time', 'pH', 'dose'], [conc, time, pH, dose]):
        lo, hi = RANGES[name]
        if not (lo <= v <= hi): out[name] = f'{name} must be between {lo} and {hi} (the range the lab data covers)'
    return out
