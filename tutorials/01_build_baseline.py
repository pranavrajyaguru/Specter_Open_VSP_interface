"""Build and export the baseline wing without running the aerodynamic solver."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.specter.studies import MESHES, build_wing
from src.specter.wing_geometry import Wing


def main():
    import openvsp as vsp

    # Build the measured wing approximation with the medium mesh settings.
    wing = Wing()
    build_wing(vsp, wing, MESHES['medium'])

    # Export a model that can be opened in OpenVSP, plus its geometry metrics.
    folder = ROOT / 'results' / 'tutorial_01_baseline'
    folder.mkdir(parents=True, exist_ok=True)
    vsp.WriteVSPFile(str(folder / 'wing.vsp3'), vsp.SET_ALL)
    metrics = wing.check()
    (folder / 'geometry.json').write_text(
        json.dumps(metrics, indent=2), encoding='utf-8')
    print(vsp.GetVSPVersion())
    print(json.dumps(metrics, indent=2))
    print('Results:', folder)


if __name__ == '__main__':
    main()
