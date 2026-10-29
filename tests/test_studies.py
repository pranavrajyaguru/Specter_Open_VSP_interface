import sys
import unittest
from pathlib import Path
from dataclasses import replace
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from wing_geometry import Wing
from studies import relative_change, converge

class StudyTests(unittest.TestCase):
    def test_reference_area(self):
        self.assertAlmostEqual(Wing().area_m2, 0.156975)

    def test_tip_chord_changes_area(self):
        wing = Wing()
        smaller = replace(wing, chords_mm=(*wing.chords_mm[:-1], 50))
        self.assertLess(smaller.area_m2, wing.area_m2)

    def test_relative_change(self):
        self.assertAlmostEqual(relative_change(1, 1.02), 2)

    def test_zero_reference_is_not_percent(self):
        self.assertIsNone(relative_change(0, 0.01))

    def test_abs_delta_not_signed(self):
        rows = [{'case': name, 'alpha_deg': 4, 'CL': v, 'CDi': v/10, 'CM': -v/4}
                for name, v in [('coarse', .4), ('medium', .5), ('fine', .49)]]
        checks = converge(rows)
        self.assertAlmostEqual(checks[-1]['CL_signed_delta'], -.01)
        self.assertAlmostEqual(checks[-1]['CL_abs_delta'], .01)

    def test_wing_mac_is_physical(self):
        wing = Wing()
        self.assertGreater(wing.mean_aerodynamic_chord_m, .1)
        self.assertLess(wing.mean_aerodynamic_chord_m, .2)

    def test_convergence(self):
        rows = [{'case': name, 'alpha_deg': 4, 'CL': v, 'CDi': v/10, 'CM': -v/4}
                for name, v in [('coarse', .4), ('medium', .5), ('fine', .51)]]
        checks = converge(rows)
        self.assertEqual(len(checks), 2)
        self.assertAlmostEqual(checks[-1]['CL_pct_delta'], 2)

if __name__ == '__main__':
    unittest.main()
