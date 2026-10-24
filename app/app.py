"""Public dashboard: live qe prediction + browser for every model version's files. No authentication."""
import json, os, re
from html import escape
import markdown, pandas as pd
from flask import Flask, abort, jsonify, render_template, request, send_from_directory, url_for
from markupsafe import Markup

import predictor as P

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
RESULTS = os.path.join(ROOT, 'results')
app = Flask(__name__)

# Accuracy of each version's prediction model, copied from results/v3/RSM_ANN_v3_results.xlsx
# and results/v2/RSM_ANN_results.xlsx ("Model comparison"). R2 = 1.0 is perfect; RMSE in mg/g.
ACCURACY = [
    {'id': 'v3', 'model': 'ANN, Adam + early stopping', 'cv_r2': .903, 'cv_rmse': 6.28, 'ho_r2': .937, 'ho_rmse': 3.81, 'lo_r2': .903, 'lo_rmse': 6.29},
    {'id': 'v2', 'model': 'ANN + Gaussian Process ensemble', 'cv_r2': .874, 'cv_rmse': 7.18, 'ho_r2': .907, 'ho_rmse': 4.62, 'lo_r2': .887, 'lo_rmse': 6.78},
    {'id': 'v1-ann', 'model': 'ANN', 'cv_r2': .859, 'cv_rmse': 7.57, 'ho_r2': .918, 'ho_rmse': 4.34, 'lo_r2': .876, 'lo_rmse': 7.11},
    {'id': 'v1-rsm', 'model': 'RSM (quadratic, reduced)', 'cv_r2': .130, 'cv_rmse': 18.22, 'ho_r2': .727, 'ho_rmse': 7.91, 'lo_r2': .540, 'lo_rmse': 13.71},
]
VERSION_FOLDERS = {
    'v1': ('Version 1', 'RSM + ANN: optimum, best material (ANOVA), actual vs predicted.'),
    'v2': ('Version 2', 'Accuracy-improvement methods (conc/dose input, Gaussian Process, ensembles) on the same data.'),
    'v3': ('Version 3 (final)', 'Fair model selection by repeated stratified 5-fold CV; selected model confirmed on hold-out and leave-one-out.'),
}
KIND = {'.md': 'Report', '.docx': 'Word report', '.xlsx': 'Excel results', '.ipynb': 'Notebook', '.png': 'Plot', '.pdf': 'PDF'}
MAT_LABEL = {'Biochar': 'Biochar (control)', 'BC:MgCO3 1:1': 'BC:MgCO₃ 1:1', 'BC:MgCO3 2:1': 'BC:MgCO₃ 2:1'}

def label(m): return MAT_LABEL.get(m, m)

def safe(rel):
    full = os.path.realpath(os.path.join(RESULTS, rel))
    if not full.startswith(RESULTS + os.sep) or not os.path.isfile(full): abort(404)
    return full

def size(path):
    n = os.path.getsize(path)
    return f'{n / 1e6:.1f} MB' if n >= 1e6 else f'{max(n // 1024, 1)} KB'

def files_in(folder):
    base = os.path.join(RESULTS, folder) if folder else RESULTS
    out = []
    for f in sorted(os.listdir(base)):
        p = os.path.join(base, f)
        ext = os.path.splitext(f)[1].lower()
        if os.path.isfile(p) and ext in KIND:
            rel = f'{folder}/{f}' if folder else f
            out.append({'name': f, 'rel': rel, 'kind': KIND[ext], 'size': size(p), 'viewable': ext in ('.md', '.xlsx', '.ipynb', '.png')})
    order = {'Report': 0, 'Word report': 1, 'Excel results': 2, 'Plot': 3, 'Notebook': 4}
    return sorted(out, key=lambda x: (order.get(x['kind'], 9), x['name']))

@app.context_processor
def inject(): return {'label': label}

# ---------------- predict ----------------
@app.get('/')
def home():
    return render_template('predict.html', versions=P.VERSIONS, mats=P.MATS, ranges=P.RANGES, accuracy={a['id']: a for a in ACCURACY})

@app.post('/api/predict')
def api_predict():
    j = request.get_json(silent=True) or {}
    try:
        vals = {k: float(j[k]) for k in ('conc', 'time', 'pH', 'dose')}
    except (KeyError, TypeError, ValueError):
        return jsonify(error='Enter a number for every field.'), 400
    errs = P.validate(**vals)
    if errs: return jsonify(error='; '.join(errs.values()), fields=list(errs)), 400
    version = j.get('version', 'v3')
    if version not in P.VERSIONS: return jsonify(error='Unknown model version.'), 400
    pred = P.predict(version, P.MATS, **vals)
    compare = {v: P.predict(v, P.MATS, **vals) for v in P.VERSIONS}
    best = max(pred, key=pred.get)
    return jsonify(version=version, label=P.VERSIONS[version][0], inputs=vals, best=best,
                   predictions=[{'mat': m, 'name': label(m), 'qe': round(q, 2)} for m, q in pred.items()],
                   compare=[{'id': v, 'label': P.VERSIONS[v][0], 'values': {m: round(q, 2) for m, q in c.items()}} for v, c in compare.items()])

# ---------------- results ----------------
@app.get('/results')
def results():
    versions = [{'id': k, 'title': t, 'blurb': b, 'files': files_in(k)} for k, (t, b) in VERSION_FOLDERS.items()]
    return render_template('results.html', versions=versions, accuracy=ACCURACY, labels={k: v[0] for k, v in P.VERSIONS.items()},
                           overview=files_in(''))

@app.get('/results/<v>')
def version_page(v):
    if v not in VERSION_FOLDERS: abort(404)
    title, blurb = VERSION_FOLDERS[v]
    files = files_in(v)
    plots = [f for f in files if f['kind'] == 'Plot']
    return render_template('version.html', v=v, title=title, blurb=blurb, files=files, plots=plots,
                           accuracy=[a for a in ACCURACY if a['id'].startswith(v)], labels={k: x[0] for k, x in P.VERSIONS.items()},
                           nav=list(VERSION_FOLDERS.items()))

@app.get('/files/<path:rel>')
def raw(rel):
    safe(rel)
    return send_from_directory(RESULTS, rel, as_attachment=request.args.get('download') is not None)

def render_md(rel, text):
    html = markdown.markdown(text, extensions=['tables', 'fenced_code', 'sane_lists', 'toc'])
    folder = os.path.dirname(rel)
    def fix(m):
        src = m.group(1)
        if re.match(r'^(https?:|/|data:)', src): return m.group(0)
        return f'src="{url_for("raw", rel=(folder + "/" if folder else "") + src)}"'
    html = re.sub(r'src="([^"]+)"', fix, html)
    return Markup(html.replace('<table>', '<div class="tablewrap"><table>').replace('</table>', '</table></div>'))

def render_xlsx(path):
    sheets = []
    for name, df in pd.read_excel(path, sheet_name=None).items():
        df = df.copy()
        for c in df.select_dtypes('float').columns: df[c] = df[c].round(3)
        sheets.append({'name': name, 'rows': len(df), 'html': Markup(df.fillna('').to_html(index=False, border=0, classes='data', max_rows=400))})
    return sheets

def render_ipynb(path):
    cells = []
    for c in json.load(open(path, encoding='utf-8'))['cells']:
        src = ''.join(c['source'])
        if c['cell_type'] == 'markdown': cells.append({'type': 'md', 'html': Markup(markdown.markdown(src, extensions=['tables', 'fenced_code']))})
        else:
            if len(src) > 6000: src = src[:600] + '\n\n# ... (embedded lab-data table hidden; see data.csv) ...\n'
            cells.append({'type': 'code', 'html': Markup(escape(src))})
    return cells

@app.get('/view/<path:rel>')
def view(rel):
    full = safe(rel)
    ext = os.path.splitext(rel)[1].lower()
    ctx = dict(rel=rel, name=os.path.basename(rel), folder=os.path.dirname(rel), size=size(full))
    if ext == '.md': return render_template('view.html', kind='md', body=render_md(rel, open(full, encoding='utf-8').read()), **ctx)
    if ext == '.xlsx': return render_template('view.html', kind='xlsx', sheets=render_xlsx(full), **ctx)
    if ext == '.ipynb': return render_template('view.html', kind='ipynb', cells=render_ipynb(full), **ctx)
    if ext == '.png': return render_template('view.html', kind='img', **ctx)
    return render_template('view.html', kind='download', **ctx)

@app.get('/healthz')
def healthz(): return 'ok'

if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))
