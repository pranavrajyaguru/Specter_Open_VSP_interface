"""Run coarse, medium, and fine meshes and compare their coefficients at 4 deg."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.specter.studies import main


if __name__ == '__main__':
    # Use the shared study runner so the mesh settings and comparisons stay
    # consistent with run_studies.py. Save this tutorial in its own folder.
    main(['--study', 'mesh', '--out',
          str(ROOT / 'results' / 'tutorial_02_mesh')])
