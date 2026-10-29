# Reference aircraft — Eclipson Model A

This project uses the [Eclipson Model A](https://www.eclipson-airplanes.com/modela), an existing 3D-printable RC-aircraft design.

I **printed and assembled** my own aircraft. My contribution here is the physical build, geometry investigation, Python/OpenVSP workflow and numerical studies—not the original Eclipson aircraft design.

## Measured and reconstructed inputs

| Parameter | Value | Origin |
|---|---:|---|
| Full wingspan | 1,000 mm | Physical aircraft |
| Root/centre chord | ~170 mm | Physical measurement |
| Wingtip rise | ~30 mm | Physical measurement |
| Dihedral | ~3.43° | Simplified estimate from tip rise and half-span |
| Wing sections | 0 / 47 / 233 / 418 / 500 mm | STL-derived approximation |
| Chords | 170 / 170 / 170 / 155 / 60 mm | Reconstructed approximate planform |
| Section profile | NACA 2412 | Provisional geometric fit, not manufacturer-confirmed |

## What is and isn't validated

The aircraft has been physically assembled, but the OpenVSP geometry is an approximation rather than a full metrology-based reconstruction. Wingtip curvature, local twist, control surfaces and structural shell details may differ from the physical object.

The aerodynamic coefficients are numerical study outputs, **not physical-flight or wind-tunnel validation**. Mass and centre-of-gravity comparisons with measured hardware remain future work.

## Original photographic evidence

Original build photos and engineering plots can be added to an `assets/` directory and embedded in the main README after they are committed. Until then, this document intentionally contains no broken links.
