"""
Example: Spectral Coupling Efficiency
======================================

Demonstrates how drive bandwidth affects thrust in ADCE and plasma systems.
"""

import numpy as np
import ucpf
from ucpf.spectral import (adce_thrust_spectral, plasma_wakefield_thrust_spectral,
                           bandwidth_optimization, mode_density_3d)

print("=" * 60)
print("SPECTRAL COUPLING EFFICIENCY EXAMPLES")
print("=" * 60)

# Example 1: ADCE with spectral correction
omega_0 = 2 * np.pi * 10e9  # 10 GHz
delta_omega = omega_0 / 100  # 1% bandwidth

F, P, eta = adce_thrust_spectral(omega_0, delta_omega, 1e-3, 0.5, 1e-4)
print(f"\n1. ADCE with spectral coupling (10 GHz, 1% bandwidth):")
print(f"   Thrust: {F:.3e} N")
print(f"   Power:  {P:.3e} W")
print(f"   Coupling efficiency: {eta:.4f}")

# Example 2: Optimal bandwidth
delta_opt, eta_max = bandwidth_optimization(omega_0, 1000, 'adce')
print(f"\n2. Optimal bandwidth for ADCE at 10 GHz (Q=1000):")
print(f"   delta_omega = {delta_opt:.3e} rad/s = {delta_opt/(2*np.pi)/1e6:.2f} MHz")
print(f"   Max coupling efficiency: {eta_max:.2f}")

# Example 3: Plasma wakefield with spectral enhancement
F_plasma, P_plasma, v_A, eta_plasma = plasma_wakefield_thrust_spectral(
    n=5e6, B=5e-9, v_flow=400e3, A=1.0, L=10.0, eta=0.1
)
print(f"\n3. Plasma wakefield with spectral coupling:")
print(f"   Thrust: {F_plasma:.3e} N")
print(f"   Alfven speed: {v_A/1e3:.1f} km/s")
print(f"   Coupling efficiency: {eta_plasma:.4f}")

# Example 4: Mode density visualization
omega = np.linspace(1e9, 100e9, 1000) * 2 * np.pi
V = 1e-6  # 1 cm³ cavity
rho = mode_density_3d(omega, V)
print(f"\n4. Mode density in 1 cm³ cavity:")
print(f"   At 10 GHz: {rho[100]:.3e} modes/(rad/s)")
print(f"   At 100 GHz: {rho[-1]:.3e} modes/(rad/s)")
