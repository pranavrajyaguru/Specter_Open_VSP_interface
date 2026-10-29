# Specter : - Eclipson Model A Wing Studies

Reproducible **OpenVSP / VSPAERO studies** of a 1 m wingspan, 3D-printed fixed-wing RC aircraft that I have personally assembled.

This repository focuses on **wing geometry, numerical mesh sensitivity and parametric comparisons**. It does not yet claim full-aircraft aerodynamic validation.

## What the code does

| Study | Question | Method |
|---|---|---|
| Mesh sensitivity | How much do calculated coefficients change with discretization? | Run 3 VSPAERO mesh settings on one baseline wing |
| Geometry comparison | What changes when the wingtip chord is modified? | Compare 50, 60 and 70 mm tip-chord configurations |

For each case the Python workflow builds a fresh OpenVSP wing, runs selected angle-of-attack cases, and exports numerical results and plots.

## Repository map

```text
Specter_Open_VSP_interface/
├── studies.py                 # OpenVSP/VSPAERO runs, comparisons, CSVs, plots
├── wing_geometry.py           # Wing inputs and geometry calculations
├── tests/
│   └── test_studies.py        # Independent unit tests
├── docs/
│   └── reference_aircraft.md  # Physical aircraft, measurements, assumptions
├── requirements.txt
├── CHANGELOG.md
├── .gitignore
└── README.md
```

Generated solver files and figures go into `results/` locally; this directory is excluded from Git.

## Run locally

Requires the **OpenVSP Python bindings** and a compatible **VSPAERO executable**. For the Windows Python 3.13 setup:

```powershell
py -3.13 -m pip install -r requirements.txt
py -3.13 studies.py --study all
```

Individual studies:

```powershell
py -3.13 studies.py --study mesh
py -3.13 studies.py --study geometry
```

Unit tests (do **not** require OpenVSP):

```powershell
py -3.13 -m unittest discover -s tests -v
```

## Baseline wing

| Quantity | Value |
|---|---:|
| Span | 1,000 mm |
| Half-span stations | 0, 47, 233, 418, 500 mm |
| Section chords | 170, 170, 170, 155, 60 mm |
| Approximate planform area | 0.156975 m² |
| Approximate aspect ratio | 6.37 |
| Estimated dihedral | 3.43° |
| Airfoil | Provisional NACA 2412 match |
| Angles of attack | −2°, 0°, 2°, 4°, 6° |

See [physical aircraft reference and limitations](docs/reference_aircraft.md).

## Engineering status and limitations

- The project uses geometry reconstructed approximately from STL parts and physical measurements; it is **not** an exact digital twin.
- The prior Windows implementation completed VSPAERO runs, but this reorganized source release has **not been rerun end-to-end**.
- At 4°, previously reported medium-to-fine differences were roughly 0.073% in CL, 8.24% in induced drag, and 2.33% in pitching moment. **Induced drag is not mesh-converged.**
- Vortex-lattice analysis does not predict viscous profile drag or stall; no wind-tunnel correlation has been established.
- Physical photographs and analysis images will be added once the actual files are in the repository. No missing-image placeholders are embedded here.

## Documentation

- [Physical aircraft and measured inputs](docs/reference_aircraft.md)
- [Release notes](CHANGELOG.md)
- [OpenVSP](https://openvsp.org/) · [OpenVSP Python API](https://openvsp.org/pyapi_docs/latest/)
