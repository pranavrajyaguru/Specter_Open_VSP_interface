# Windows setup and troubleshooting

Use **Python 3.13, 64-bit**, with the matching OpenVSP / VSPAERO distribution. The project has been run with OpenVSP 3.49.0.

## Create the environment

Open PowerShell in the project folder:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Install OpenVSP into the same environment

Set `$vspPythonDir` to the `python` directory inside your extracted OpenVSP distribution. Replace the example path below with your actual path:

```powershell
$vspPythonDir = 'C:\path\to\OpenVSP-3.49.0-win64\python'
.\.venv\Scripts\python.exe -m pip install "$vspPythonDir\openvsp_config" "$vspPythonDir\utilities" "$vspPythonDir\degen_geom" "$vspPythonDir\openvsp"
Copy-Item "$vspPythonDir\openvsp\openvsp\*.pyd" '.\.venv\Lib\site-packages\openvsp\'
```

The copy step includes the Windows binary modules omitted by the OpenVSP 3.49.0 package's installation manifest. `requirements.txt` installs the numerical and plotting libraries; install the native OpenVSP bindings from the matching distribution as shown above.

Verify the installation:

```powershell
.\.venv\Scripts\python.exe -c "import openvsp as vsp; print(vsp.GetVSPVersion()); print('VSPAERO available:', vsp.CheckForVSPAERO(vsp.GetVSPAEROPath()))"
.\.venv\Scripts\python.exe -m pip check
```

You should see an OpenVSP version, `VSPAERO available: True`, and no broken requirements.

## Activate and run

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
python run_studies.py --study all
```

Select `.venv\Scripts\python.exe` as the Python interpreter in VS Code. A Python 3.14 environment cannot use the native OpenVSP bindings compiled for Python 3.13.

Use `--study mesh` or `--study geometry` to run one experiment. Use a different output folder to preserve an earlier run:

```powershell
python run_studies.py --study mesh --out results/my_mesh_run
```

The [three tutorial scripts](../README.md#three-runnable-tutorials) save their outputs in separate `results/tutorial_*` folders. The baseline tutorial exports geometry without running VSPAERO; the other two run five angles of attack for three cases each.

## Run the tests

The geometry and comparison tests do not require OpenVSP:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## If OpenVSP cannot be imported

Check the interpreter first:

```powershell
.\.venv\Scripts\python.exe -c "import sys; print(sys.executable); print(sys.version)"
```

It should report this project's `.venv` and Python 3.13. If importing `_vsp` fails, check that the matching `_vsp.pyd` and `_vsp_g.pyd` files were copied into `.venv\Lib\site-packages\openvsp`.

[OpenVSP Python API documentation](https://openvsp.org/pyapi_docs/latest/) · [Back to README](../README.md)
