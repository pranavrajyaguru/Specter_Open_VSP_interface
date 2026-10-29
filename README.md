# Specter — Wing Aerodynamic Studies

Python automation of a parametric, wing-only aerodynamic study of the Eclipson Model A RC aircraft using OpenVSP and VSPAERO.

The repository contains two repeatable experiments: a **mesh-resolution sensitivity study** and a **wingtip-chord geometry sweep**. Each run generates its own OpenVSP model, VSPAERO results, numerical tables, and comparison plots.

## Run

On Windows, use the Python 3.13 interpreter where the OpenVSP bindings and VSPAERO executable are installed:

```powershell
py -3.13 studies.py --study all
```

Run a single study:

```powershell
py -3.13 studies.py --study mesh
py -3.13 studies.py --study geometry
```

Python unit tests do not require OpenVSP:

```powershell
py -3.13 -m unittest discover -s tests -v
```

Install matplotlib for plots, if needed: `py -3.13 -m pip install -r requirements.txt`. The OpenVSP Python bindings must come from a compatible OpenVSP installation.

## Engineering inputs

| Parameter | Baseline |
| --- | --- |
| Full wingspan | 1.000 m |
| Spanwise stations, half wing | 0, 47, 233, 418, 500 mm |
| Section chords | 170, 170, 170, 155, 60 mm |
| Baseline planform area | 0.156975 m² |
| Baseline aspect ratio | approximately 6.37 |
| Section shape | provisional NACA 2412 |
| Dihedral | 3.43° |
| Angle-of-attack cases | −2°, 0°, 2°, 4°, 6° |

The section profile and much of the geometry are approximate reconstructions, not manufacturer-confirmed measurements.

## Experiments

**Mesh sensitivity.** The baseline wing runs with three spanwise/chordwise tessellation settings: 8/15, 16/25, and 28/41. At 4° angle of attack, the code compares signed, absolute, and percentage changes in `CL`, `CDi`, and `CM`.

**Geometry sweep.** The wingtip chord changes to 50, 60, and 70 mm, with span and other station coordinates fixed. All variants use the medium mesh and the same angle-of-attack cases. Wing area and aspect ratio are recalculated for every variant.

VSPAERO result keys are mapped as `CLtot → CL`, `CDi → CDi`, and `CMytot → CM` for the installed API. The moment reference must be checked before physical interpretation.

## Files

- `studies.py`: VSPAERO orchestration, numerical comparison, CSV writing, plotting
- `wing_geometry.py`: geometric parameters and reference calculations
- `tests/test_studies.py`: independent computational tests
- `CHANGELOG.md`: release notes
- `results/`: generated locally; intentionally excluded from version control

## Validation and limitations

The previous working implementation completed OpenVSP/VSPAERO analysis on Windows using Python 3.13. This frozen source release **has not yet been rerun end-to-end** on that installation.

In the earlier mesh study at 4°, medium-to-fine differences were approximately **0.073% in CL**, **8.24% in induced drag**, and **2.33% in pitching moment**. The induced drag is therefore **not demonstrated to be mesh-converged**. These are numerical sensitivity checks, not experimental validation.

Vortex-lattice analysis does not resolve viscous profile drag or stall. Neither the geometry nor its coefficients have been validated against model-specific wind-tunnel measurements. Results are suitable for preliminary method demonstration only.

## External documentation

- [OpenVSP](https://openvsp.org/)
- [OpenVSP Python API](https://openvsp.org/pyapi_docs/latest/)
