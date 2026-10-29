"""Geometric reference data for approximate Eclipson Model A wing (metres)."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Wing:
    stations_mm: tuple = (0, 47, 233, 418, 500)
    chords_mm: tuple = (170, 170, 170, 155, 60)
    leading_edge_mm: tuple = (0, 0, 0, 33, 114)
    dihedral_deg: float = 3.43

    def __post_init__(self):
        n = len(self.stations_mm)
        if n < 2 or len(self.chords_mm) != n or len(self.leading_edge_mm) != n:
            raise ValueError('Stations, chords, and leading edges must have matching lengths')
        if self.stations_mm[0] != 0 or any(b <= a for a,b in zip(self.stations_mm[:-1],self.stations_mm[1:])):
            raise ValueError('Span stations must start at zero and increase')
        if any(c <= 0 for c in self.chords_mm):
            raise ValueError('Chords must be positive')

    @property
    def span_m(self):
        return 2 * self.stations_mm[-1] / 1000

    @property
    def area_m2(self):
        # Projected planform area; no non-planar dihedral correction.
        return 2 * sum((b-a)*(ca+cb)/2 for a,b,ca,cb in zip(
            self.stations_mm[:-1],self.stations_mm[1:],self.chords_mm[:-1],self.chords_mm[1:])) / 1e6

    @property
    def aspect_ratio(self):
        return self.span_m**2/self.area_m2

    @property
    def mean_aerodynamic_chord_m(self):
        # 2/S times integral over the semispan of c(y)^2 dy.
        integral=sum((b-a)*(ca*ca+ca*cb+cb*cb)/3 for a,b,ca,cb in zip(
            self.stations_mm[:-1],self.stations_mm[1:],self.chords_mm[:-1],self.chords_mm[1:]))
        return 2*integral/(self.area_m2*1e6)*1e-3

    def check(self):
        return {'span_m':self.span_m,'area_m2':self.area_m2,
                'aspect_ratio':self.aspect_ratio,'mac_m':self.mean_aerodynamic_chord_m}
