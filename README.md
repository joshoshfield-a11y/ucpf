# UCPF — Universal Consciousness and Physics Framework

**Version:** 10.1.0  
**License:** MIT  
**Authors:** UPE-78 Research Collective

A rigorous, falsifiable framework for analyzing anomalous propulsion, consciousness-field interactions, and vacuum-coupled phenomena.

## Installation

```bash
pip install git+https://github.com/joshoshfield-a11y/ucpf.git
```

Or from source:
```bash
git clone https://github.com/joshoshfield-a11y/ucpf.git
cd ucpf
pip install -e .
```

## Quick Start

```python
import ucpf
from ucpf.plasma import plasma_wakefield_thrust

# Calculate thrust in solar wind conditions
F, P, v_A = ucpf.plasma.solar_wind_thrust(A=1.0, eta=0.1)
print(f"Thrust: {F:.2e} N, Alfven speed: {v_A/1e3:.1f} km/s")

# Evaluate power sources for 1 MW hover
results = ucpf.power.evaluate_all_sources(P_target=1e6)
for r in results:
    print(f"{r['name']}: {r['mass_kg']:.0f} kg, viable: {r['viable']}")
```

## Modules

| Module | Content |
|--------|---------|
| `core` | Axioms, formulas, epistemic calibration |
| `vcp` | Vacuum-Coupled Propulsion (ADCE, Casimir) |
| `plasma` | Plasma wakefield / MHD coupling |
| `ionization` | Air ionization mechanisms |
| `power` | Power system architecture |
| `falsification` | Six quantitative experiments |
| `constants` | Physical constants in SI units |
| `spectral` | Spectral coupling efficiency (bandwidth) |
| `utils` | Helper functions |

## Key Findings

- **ADCE thrust:** 2.8×10⁻²⁹ N (24 orders below IVO claim)
- **Plasma wakefield:** only mechanism with macroscopic potential
- **Microwave discharge:** leading ionization candidate
- **Beamed power:** only viable power architecture within known physics
- **Spectral coupling efficiency** — formalizes the 'bandwidth' insight
- **Six falsification experiments** with quantitative thresholds

## Documentation

Full research documentation, visualizations, and session logs are maintained in the [upe78-knowledge-base](https://github.com/joshoshfield-a11y/upe78-knowledge-base) repository.

## Citation

```
UPE-78 Research Collective (2026). UCPF v10.1: Universal Consciousness 
and Physics Framework. https://github.com/joshoshfield-a11y/ucpf
```

## Contributing

Append-only. No deletions. All additions timestamped.
