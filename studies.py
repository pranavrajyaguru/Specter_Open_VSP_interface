"""Repeatable wing-only VSPAERO experiments.

Mesh study: one geometry, three discretizations.
Geometry study: one mesh, three tip chords.
Each case starts from a fresh OpenVSP model.
"""
import argparse
import csv
from dataclasses import replace
import json
import math
from pathlib import Path
from wing_geometry import Wing

HERE = Path(__file__).resolve().parent
MESHES = {'coarse': (8, 15), 'medium': (16, 25), 'fine': (28, 41)}
# (spanwise SectTess_U, chordwise Tess_W); these are settings, not panel counts.
TIP_CHORDS_MM = {'baseline': 60, 'tip_50mm': 50, 'tip_70mm': 70}
ALPHAS = (-2, 0, 2, 4, 6)


def build_wing(vsp, wing, mesh):
    vsp.ClearVSPModel()
    gid = vsp.AddGeom('WING')
    vsp.SetGeomName(gid, 'Model_A_Wing')
    for _ in range(len(wing.stations_mm) - 2):
        vsp.InsertXSec(gid, 1, vsp.XS_FOUR_SERIES)
    vsp.Update()
    u, w = mesh
    for i in range(1, len(wing.stations_mm)):
        vsp.SetDriverGroup(gid, i, vsp.SPAN_WSECT_DRIVER,
                           vsp.ROOTC_WSECT_DRIVER, vsp.TIPC_WSECT_DRIVER)
        dy = (wing.stations_mm[i] - wing.stations_mm[i - 1]) / 1000
        dx = (wing.leading_edge_mm[i] - wing.leading_edge_mm[i - 1]) / 1000
        for name, val in (('Span', dy),
                          ('Root_Chord', wing.chords_mm[i-1] / 1000),
                          ('Tip_Chord', wing.chords_mm[i] / 1000),
                          ('Sweep_Location', 0.0),
                          ('Sweep', math.degrees(math.atan2(dx, dy))),
                          ('Dihedral', wing.dihedral_deg),
                          ('SectTess_U', u)):
            vsp.SetParmVal(gid, name, f'XSec_{i}', val)
        vsp.Update()
    vsp.SetParmVal(gid, 'Tess_W', 'Shape', w)
    surf = vsp.GetXSecSurf(gid, 0)
    for j in range(vsp.GetNumXSec(surf)):
        vsp.ChangeXSecShape(surf, j, vsp.XS_FOUR_SERIES)
        xs = vsp.GetXSec(surf, j)
        for name, val in (('Camber', .02), ('CamberLoc', .4), ('ThickChord', .12)):
            vsp.SetParmVal(vsp.GetXSecParm(xs, name), val)
    vsp.Update()
    return gid


def compute_geometry(vsp):
    analysis = 'VSPAEROComputeGeometry'
    vsp.SetAnalysisInputDefaults(analysis)
    vsp.SetIntAnalysisInput(analysis, 'GeomSet', [vsp.SET_NONE], 0)
    vsp.SetIntAnalysisInput(analysis, 'ThinGeomSet', [vsp.SET_ALL], 0)
    rid = vsp.ExecAnalysis(analysis)
    if not rid:
        raise RuntimeError('VSPAEROComputeGeometry did not return a result')


def read_coefficients(vsp, result_id):
    available = set(vsp.GetAllDataNames(result_id))

    def read(name):
        if name not in available:
            raise RuntimeError(f'VSPAERO history missing {name}; available: {sorted(available)}')
        values = list(vsp.GetDoubleResults(result_id, name, 0))
        if not values:
            raise RuntimeError(f'VSPAERO history {name} is empty')
        value = float(values[-1])
        if not math.isfinite(value):
            raise RuntimeError(f'Nonfinite result for {name}: {value}')
        return value

    return {'CL': read('CLtot'), 'CDi': read('CDi'), 'CM': read('CMytot')}


def run_alpha(vsp, gid, wing, alpha):
    analysis = 'VSPAEROSweep'
    vsp.SetAnalysisInputDefaults(analysis)
    vsp.SetIntAnalysisInput(analysis, 'AnalysisMethod', [0], 0)  # VLM
    vsp.SetIntAnalysisInput(analysis, 'RefFlag', [0], 0)
    for key, val in (('Sref', wing.area_m2), ('bref', wing.span_m),
                     ('cref', wing.mean_aerodynamic_chord_m),
                     ('AlphaStart', float(alpha)), ('BetaStart', 0.0),
                     ('MachStart', .02)):
        vsp.SetDoubleAnalysisInput(analysis, key, [val], 0)
    vsp.SetIntAnalysisInput(analysis, 'GeomSet', [vsp.SET_NONE], 0)
    vsp.SetIntAnalysisInput(analysis, 'ThinGeomSet', [vsp.SET_ALL], 0)
    vsp.SetIntAnalysisInput(analysis, 'AlphaNpts', [1], 0)
    vsp.SetStringAnalysisInput(analysis, 'WingID', [gid], 0)
    vsp.Update()
    rid = vsp.ExecAnalysis(analysis)
    if not rid:
        raise RuntimeError(f'No solver result at alpha={alpha}')
    history = vsp.FindLatestResultsID('VSPAERO_History')
    if not history:
        raise RuntimeError(f'Missing VSPAERO_History at alpha={alpha}')
    return {'alpha_deg': alpha, **read_coefficients(vsp, history)}


def run_case(vsp, label, wing, mesh, root, alphas):
    folder = root / label
    folder.mkdir(parents=True, exist_ok=True)
    gid = build_wing(vsp, wing, mesh)
    project = folder / 'wing.vsp3'
    vsp.WriteVSPFile(str(project), vsp.SET_ALL)
    compute_geometry(vsp)
    results = []
    for alpha in alphas:
        coeffs = run_alpha(vsp, gid, wing, alpha)
        results.append({'case': label, 'u': mesh[0], 'w': mesh[1],
                        'tip_chord_mm': wing.chords_mm[-1],
                        'span_m': wing.span_m, 'area_m2': wing.area_m2,
                        'aspect_ratio': wing.aspect_ratio, **coeffs})
        print(f'{label:18s} alpha={alpha:+3g}: CL={coeffs["CL"]:.5f}, CDi={coeffs["CDi"]:.5f}')
    write_csv(folder / 'polar.csv', results)
    return results


def write_csv(path, rows):
    if not rows:
        raise ValueError('Empty results')
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def relative_change(reference, new, *, atol=1e-8):
    if abs(reference) <= atol:
        return None
    return 100.0 * (new - reference) / abs(reference)


def converge(rows, at_alpha=4):
    """Compare adjacent mesh levels with signed and absolute differences."""
    lookup = {(row['case'], row['alpha_deg']): row for row in rows}
    comparisons = []
    for low, high in (('coarse', 'medium'), ('medium', 'fine')):
        left, right = lookup[(low, at_alpha)], lookup[(high, at_alpha)]
        item = {'pair': f'{low}_to_{high}', 'alpha_deg': at_alpha}
        for coef in ('CL', 'CDi', 'CM'):
            item[f'{coef}_signed_delta'] = right[coef] - left[coef]
            item[f'{coef}_abs_delta'] = abs(right[coef] - left[coef])
            item[f'{coef}_pct_delta'] = relative_change(left[coef], right[coef])
        comparisons.append(item)
    return comparisons


def plots(mesh_rows, shape_rows, folder):
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print('matplotlib not installed; CSV files are available (pip install matplotlib).')
        return
    for name, rows in (('mesh', mesh_rows), ('tip_chord', shape_rows)):
        if not rows:
            continue
        fig, axes = plt.subplots(1, 3, figsize=(13, 4))
        cases = list(dict.fromkeys(r['case'] for r in rows))
        for case in cases:
            data = sorted((r for r in rows if r['case'] == case), key=lambda r: r['alpha_deg'])
            for ax, coef in zip(axes, ('CL', 'CDi', 'CM')):
                ax.plot([r['alpha_deg'] for r in data], [r[coef] for r in data], 'o-', label=case)
        for ax, coef in zip(axes, ('CL', 'CDi', 'CM')):
            ax.set_xlabel('Angle of attack (deg)')
            ax.set_ylabel(coef)
            ax.grid(alpha=.3)
        axes[0].legend()
        fig.suptitle(f'Model A wing — {name} study (VLM)')
        fig.tight_layout()
        fig.savefig(folder / f'{name}_comparison.png', dpi=160)
        plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--study', choices=('all', 'mesh', 'geometry'), default='all')
    parser.add_argument('--out', type=Path, default=HERE / 'results')
    args = parser.parse_args()
    try:
        import openvsp as vsp
    except ImportError as exc:
        raise SystemExit('The selected Python interpreter cannot import openvsp. Select the working OpenVSP interpreter.') from exc
    args.out.mkdir(parents=True, exist_ok=True)
    base = Wing()
    mesh_rows, shape_rows = [], []
    if args.study in ('all', 'mesh'):
        for name, mesh in MESHES.items():
            mesh_rows += run_case(vsp, name, base, mesh, args.out / 'mesh', ALPHAS)
        write_csv(args.out / 'mesh_summary.csv', mesh_rows)
        checks = converge(mesh_rows)
        write_csv(args.out / 'mesh_convergence_at_4deg.csv', checks)
        print('Convergence (medium -> fine, alpha=4 deg):', json.dumps(checks[-1], indent=2))
    if args.study in ('all', 'geometry'):
        for name, tip in TIP_CHORDS_MM.items():
            chords = (*base.chords_mm[:-1], tip)
            wing = replace(base, chords_mm=chords)
            shape_rows += run_case(vsp, name, wing, MESHES['medium'], args.out / 'geometry', ALPHAS)
        write_csv(args.out / 'geometry_summary.csv', shape_rows)
    (args.out / 'study_settings.json').write_text(json.dumps({
        'mesh_settings': MESHES, 'tip_chords_mm': TIP_CHORDS_MM,
        'alpha_deg': ALPHAS, 'method': 'VSPAERO VLM',
        'coefficient_names': {'CL': 'CLtot', 'CDi': 'CDi', 'CM': 'CMytot'},
        'wing': base.check()}, indent=2), encoding='utf-8')
    plots(mesh_rows, shape_rows, args.out)
    print('Results:', args.out)


if __name__ == '__main__':
    main()
