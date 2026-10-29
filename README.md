# Specter | OpenVSP & VSPAERO Wing Studies

**Engineering automation based on a prototype aircraft I built using 3D printing, assembled, and tested in the field.**

This repository develops a parameterized OpenVSP model of the [Eclipson Model A](https://www.eclipson-airplanes.com/modela) RC aircraft wing and uses VSPAERO to study mesh sensitivity and planform changes.

**GitHub:** [@pranavrajyaguru](https://github.com/pranavrajyaguru)

## Studies

| Experiment | Variable | Output |
|---|---|---|
| Mesh sensitivity | Coarse / medium / fine tessellation | ΔCL, ΔCDi, ΔCM and polar plots |
| Wingtip geometry | 50 / 60 / 70 mm tip chords | Geometry metrics and aerodynamic comparison |

**Physical reference:** [My build, measurements and reconstruction assumptions](docs/reference_aircraft.md)

## Repository

```text
├── assets/
│   └── IMG_0046(1).jpg          # Photograph of the assembled aircraft
├── src/
│   └── specter/
│       ├── wing_geometry.py     # Wing stations, area, aspect ratio, MAC
│       └── studies.py           # OpenVSP builder, VSPAERO runs, plots
├── tests/
│   └── test_studies.py          # Geometry and comparison unit tests
├── tutorials/                  # Three runnable Python examples
│   ├── 01_build_baseline.py
│   ├── 02_mesh_sensitivity.py
│   └── 03_wingtip_geometry.py
├── docs/
│   └── reference_aircraft.md   # Built aircraft, dimensions, limitations
├── run_studies.py               # Command-line entrypoint
├── requirements.txt
├── .gitignore
├── CHANGELOG.md
└── README.md
```

## Run in three steps

Once the virtual environment is set up, follow these steps each time you want to run the project:

1. **Open the project terminal.** Open the `Specter_Open_VSP_interface` folder in VS Code, then choose **Terminal → New Terminal** and use PowerShell.

2. **Activate the virtual environment.** Run:

   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
   .\.venv\Scripts\Activate.ps1
   ```

   Your terminal prompt should now start with `(.venv)`.

3. **Run both studies.** Run:

   ```powershell
   python run_studies.py --study all
   ```

CSV tables, VSP3 models, and plots are saved in `results/`. To run only one experiment, replace `all` with `mesh` or `geometry`.

## Runnable tutorials

With `.venv` activated, run any of these scripts from the project folder:

| Tutorial | Command |
|---|---|
| [1. Build the baseline wing](tutorials/01_build_baseline.py) | `python tutorials/01_build_baseline.py` |
| [2. Run the mesh study](tutorials/02_mesh_sensitivity.py) | `python tutorials/02_mesh_sensitivity.py` |
| [3. Run the wingtip geometry study](tutorials/03_wingtip_geometry.py) | `python tutorials/03_wingtip_geometry.py` |

Each script saves its outputs in a separate `results/tutorial_*` folder. The first exports the baseline VSP3 model and geometry metrics; the other two run VSPAERO and generate CSV tables and comparison plots.

## First-time setup

On Windows, use Python 3.13 (64-bit) with the matching OpenVSP / VSPAERO distribution. Create the project environment and install its Python dependencies:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Install the OpenVSP bindings and their bundled support packages into this same environment. Set `$vspPythonDir` to the `python` directory inside your extracted OpenVSP distribution:

```powershell
$vspPythonDir = 'C:\path\to\OpenVSP-3.49.0-win64\python'
.\.venv\Scripts\python.exe -m pip install "$vspPythonDir\openvsp_config" "$vspPythonDir\utilities" "$vspPythonDir\degen_geom" "$vspPythonDir\openvsp"
Copy-Item "$vspPythonDir\openvsp\openvsp\*.pyd" '.\.venv\Lib\site-packages\openvsp\'
.\.venv\Scripts\python.exe -c "import openvsp as vsp; print(vsp.GetVSPVersion())"
.\.venv\Scripts\python.exe run_studies.py --study all
```

The copy step includes the Windows binary modules omitted by the OpenVSP 3.49.0 package's installation manifest.

In VS Code, select `.venv\Scripts\python.exe` as the Python interpreter. A virtual environment created with Python 3.14 cannot use the OpenVSP bindings compiled for Python 3.13.

Run tests without OpenVSP:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
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

**This is a preliminary study—not validated aircraft-performance data.** The OpenVSP geometry approximates measurements and STL geometry of my assembled aircraft. The NACA 2412 section is a provisional match. The mesh tutorial was run with OpenVSP 3.49.0 and Python 3.13; induced drag was not demonstrated mesh-converged (~8.24% medium-to-fine difference at 4°).

The original Eclipson aircraft design is not my work. My contributions are the build, reconstruction, parametric model and numerical experiments.

## Images and outputs

![My 3D-printed Eclipson Model A prototype viewed from above](assets/IMG_0046%281%29.jpg)

This photo shows the Eclipson Model A prototype that I built using 3D printing, assembled, and tested in the field. It serves as the physical reference for the wing reconstruction and aerodynamic studies in this repository.

[OpenVSP documentation](https://openvsp.org/) · [Python API](https://openvsp.org/pyapi_docs/latest/)
