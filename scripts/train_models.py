"""Train the prediction models served by the web app, on all 480 measured rows.

The model definitions are copied from results/v3/rsm_ann_v3.ipynb (v1 and v2 definitions
are the ones that notebook re-uses), so the app predicts with the same methods that were
evaluated in the reports. Run:  python scripts/train_models.py
"""
import os, warnings
import numpy as np, pandas as pd
import statsmodels.api as sm
from joblib import dump
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.compose import TransformedTargetRegressor
from sklearn.model_selection import GroupKFold
from sklearn.metrics import mean_squared_error
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, WhiteKernel, ConstantKernel

warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(HERE, '..', 'app')
SEED = 42

d = pd.read_csv(os.path.join(APP, 'data.csv'))
MATS = list(d.mat.unique())
X4 = ['x1', 'x2', 'x3', 'x4']
LEVELS = {'x1': [10, 25, 50, 75, 100], 'x2': [60, 120, 180, 240, 360], 'x3': [4, 6, 8, 10, 12], 'x4': [10, 20, 50, 100, 150]}
d['cond'] = np.where(d.run <= 4, 0, d.run)
d['logR'] = np.log(d.conc / d.dose)
PHYS = X4 + ['logR']

# ---- RSM (v1): quadratic, backward elimination, one model per material
LIN = X4
SQ = [f'{a}^2' for a in X4]
INT = [f'{a}*{b}' for i, a in enumerate(X4) for b in X4[i + 1:]]
ALL = LIN + SQ + INT

def design(df, terms):
    X = pd.DataFrame(index=df.index)
    for t in terms:
        if t.endswith('^2'): X[t] = df[t[:-2]] ** 2
        elif '*' in t: a, b = t.split('*'); X[t] = df[a] * df[b]
        else: X[t] = df[t]
    return sm.add_constant(X, has_constant='add')

def fit_rsm(df, reduce=True):
    terms = ALL.copy()
    while reduce:
        m = sm.OLS(df.y, design(df, terms)).fit()
        needed = {x for t in terms if t not in LIN for x in X4 if x in t}
        p = m.pvalues[[t for t in terms if t not in needed]]
        if p.empty or p.max() <= 0.05: break
        terms.remove(p.idxmax())
    m = sm.OLS(df.y, design(df, terms)).fit()
    return {'terms': terms, 'params': m.params.to_dict()}

# ---- ANN helpers (v1 / v2 / v3)
def ann_X(df, cols):
    onehot = pd.get_dummies(df.mat).reindex(columns=MATS, fill_value=0).astype(float)
    return pd.concat([df[cols].astype(float), onehot], axis=1).values

def wrap(net):
    return TransformedTargetRegressor(make_pipeline(StandardScaler(), net), transformer=StandardScaler())

def make_ann(h, a, seed):
    return wrap(MLPRegressor(hidden_layer_sizes=(h,), activation='tanh', solver='lbfgs', alpha=a, max_iter=5000, random_state=seed))

def make_ann_v3(h, a, seed, layers=1, solver='lbfgs'):
    kw = (dict(early_stopping=True, validation_fraction=0.15, n_iter_no_change=50, max_iter=5000)
          if solver == 'adam' else dict(max_iter=20000))
    return wrap(MLPRegressor(hidden_layer_sizes=(h,) * layers, activation='tanh', solver=solver, alpha=a, random_state=seed, **kw))

GRID = [(h, a) for h in (4, 8, 12) for a in (1e-3, 1e-2, 1e-1)]
GRID2 = [(h, a) for h in (4, 8, 12) for a in (1e-2, 1e-1)]

def fit_ens(df, cols, maker, n_ens, grid, k):
    X, y, g = ann_X(df, cols), df.y.values, df.cond.values
    folds = list(GroupKFold(k).split(X, y, g))
    cv = lambda h, a: np.mean([mean_squared_error(y[v], maker(h, a, SEED).fit(X[t], y[t]).predict(X[v])) for t, v in folds])
    h, a = min(grid, key=lambda p: cv(*p))
    print(f'   chosen: {h} neurons, alpha={a}')
    return {'nets': [maker(h, a, SEED + i).fit(X, y) for i in range(n_ens)], 'cols': cols}

def fit_gpr(a):
    kern = ConstantKernel(1.0) * RBF(np.ones(len(PHYS)), (1e-2, 1e2)) + WhiteKernel(0.1, (1e-5, 10))
    sc = StandardScaler().fit(a[PHYS])
    g = GaussianProcessRegressor(kern, normalize_y=True, n_restarts_optimizer=2, random_state=SEED).fit(sc.transform(a[PHYS]), a.y.values)
    return {'scaler': sc, 'gpr': g}

if __name__ == '__main__':
    print('v1 RSM (reduced)'); rsm = {m: fit_rsm(d[d.mat == m]) for m in MATS}
    print('v1 ANN');            ann_v1 = fit_ens(d, X4, make_ann, 5, GRID, 4)
    print('v2 ANN + conc/dose'); ann_v2 = fit_ens(d, PHYS, make_ann, 10, GRID2, 3)
    print('v2 GPR + conc/dose'); gpr = {m: fit_gpr(d[d.mat == m]) for m in MATS}
    print('v3 ANN Adam early-stop + conc/dose')
    ann_v3 = fit_ens(d, PHYS, lambda h, a, s: make_ann_v3(h, a, s, 1, 'adam'), 10, GRID2, 3)
    bundle = {'mats': MATS, 'levels': LEVELS, 'rsm': rsm, 'ann_v1': ann_v1, 'ann_v2': ann_v2, 'gpr': gpr, 'ann_v3': ann_v3}
    out = os.path.join(APP, 'models', 'bundle.joblib')
    dump(bundle, out, compress=3)
    print('saved', out, os.path.getsize(out) // 1024, 'KB')
