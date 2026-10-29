# Specter | OpenVSP & VSPAERO Wing Studies

**Engineering automation based on an aircraft I physically printed and assembled.**

This repository develops a parameterized OpenVSP model of the [Eclipson Model A](https://www.eclipson-airplanes.com/modela) RC aircraft wing and uses VSPAERO to study mesh sensitivity and planform changes.

## Studies

| Experiment | Variable | Output |
|---|---|---|
| Mesh sensitivity | Coarse / medium / fine tessellation | ΔCL, ΔCDi, ΔCM and polar plots |
| Wingtip geometry | 50 / 60 / 70 mm tip chords | Geometry metrics and aerodynamic comparison |

**Physical reference:** [My build, measurements and reconstruction assumptions](docs/reference_aircraft.md)

## Repository

```text
├── src/
│   └── specter/
│       ├── wing_geometry.py     # Wing stations, area, aspect ratio, MAC
│       └── studies.py           # OpenVSP builder, VSPAERO runs, plots
├── tests/
│   └── test_studies.py          # Geometry and comparison unit tests
├── docs/
│   └── reference_aircraft.md    # Built aircraft, dimensions, limitations
├── run_studies.py               # Command-line entrypoint
├── requirements.txt
├── .gitignore
├── CHANGELOG.md
└── README.md
```

## Reproduce

On Windows with OpenVSP / VSPAERO installed for Python 3.13:

```powershell
py -3.13 -m pip install -r requirements.txt
py -3.13 run_studies.py --study all
```

Run either experiment with `--study mesh` or `--study geometry`. CSV tables, VSP3 models and plots are produced in the ignored local `results/` directory.

Run tests without OpenVSP:

```powershell
py -3.13 -m unittest discover -s tests -v
```

## Baseline geometry

| Parameter | Value |
|---|---:|
| Wingspan | 1.000 m |
| Spanwise stations (half wing) | 0 / 47 / 233 / 418 / 500 mm |
| Station chords | 170 / 170 / 170 / 155 / 60 mm |
| Projected wing area | 0.156975 m² |
| Aspect ratio | ~6.37 |
| Estimated dihedral | 3.43° |
| Airfoil | Provisional NACA 2412 |
| Angle-of-attack cases | −2° to +6°, step 2° |

## Engineering limitations

**This is a preliminary study—not validated aircraft-performance data.** The OpenVSP geometry approximates measurements and STL geometry of my assembled aircraft. The NACA 2412 section is a provisional match. Existing reported VSPAERO runs have not been rerun on this reorganized release; induced drag was not demonstrated mesh-converged (previously ~8.24% medium-to-fine difference at 4°).

The original Eclipson aircraft design is not my work. My contributions are the build, reconstruction, parametric model and numerical experiments.

## Images and outputs

My original aircraft photographs and reconstruction figures are available separately until their actual binary files are committed to GitHub. This README intentionally avoids broken image placeholders.

[OpenVSP documentation](https://openvsp.org/) · [Python API](https://openvsp.org/pyapi_docs/latest/)
