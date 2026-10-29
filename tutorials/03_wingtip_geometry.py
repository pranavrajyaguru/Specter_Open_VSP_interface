"""Run the 50, 60, and 70 mm wingtip chords with the same medium mesh settings."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.specter.studies import main


if __name__ == '__main__':
    # The shared runner changes the tip chord, recalculates reference geometry,
    # and writes the coefficient tables and comparison plot for all three cases.
    main(['--study', 'geometry', '--out',
          str(ROOT / 'results' / 'tutorial_03_geometry')])
