"""
Vacuum-Coupled Propulsion (VCP)
=================================

Models for propulsion via quantum vacuum coupling, including:
- Asymmetric Dynamical Casimir Effect (ADCE)
- Standard Casimir forces
- Thrust-to-power scaling laws

All models calibrated to Wilson et al. (2011) SQUID DCE experiment.
"""

import numpy as np
from . import constants as C

def adce_thrust(omega, v_eff_over_c, A_asym, area, Q=1000, eta_dir=0.5):
    """
    Calculate ADCE thrust from time-modulated boundaries.

    Calibrated to Wilson et al. (2011) SQUID experiment.

    Parameters
    ----------
    omega : float
        Modulation angular frequency [rad/s]
    v_eff_over_c : float
        Effective modulation velocity as fraction of c (e.g., 1e-3 = 0.1% c)
    A_asym : float
        Asymmetry parameter [0, 1]
    area : float
        Active surface area [m²]
    Q : float, optional
        Quality factor (default: 1000)
    eta_dir : float, optional
        Directional efficiency (default: 0.5)

    Returns
    -------
    F : float
        Thrust [N]
    P : float
        Drive power [W]
    N_dot : float
        Photon production rate [photons/s]
    """
    v_eff = v_eff_over_c * C.c

    # Number of modes
    lam = 2 * np.pi * C.c / omega
    N_modes = max(1, area / lam**2)

    # Photon production rate (Wilson 2011 scaling)
    gamma_0 = (1 / (4 * np.pi)) * v_eff_over_c**2 * omega
    N_dot = gamma_0 * N_modes

    # Thrust
    p_photon = C.hbar * omega / C.c
    F = N_dot * p_photon * A_asym * eta_dir

    # Power (dielectric modulation model)
    P_0 = 1e6  # W·s/m² (phenomenological for SQUID arrays)
    P = P_0 * area * v_eff_over_c**2 * omega / Q

    return F, P, N_dot

def casimir_force(d, area=1.0):
    """
    Calculate static Casimir force between parallel plates.

    Parameters
    ----------
    d : float
        Gap distance [m]
    area : float, optional
        Plate area [m²] (default: 1.0)

    Returns
    -------
    F : float
        Casimir force [N] (attractive, negative sign)
    """
    F_per_area = (np.pi**2 * C.hbar * C.c) / (240 * d**4)
    return -F_per_area * area

def casimir_pressure(d):
    """
    Calculate Casimir pressure between parallel plates.

    Parameters
    ----------
    d : float
        Gap distance [m]

    Returns
    -------
    P : float
        Casimir pressure [N/m²] (attractive, negative)
    """
    return (np.pi**2 * C.hbar * C.c) / (240 * d**4)

def adce_thrust_to_power(omega, Q=1000, A_asym=0.5, eta_dir=0.5):
    """
    Theoretical maximum thrust-to-power ratio for ADCE.

    T2P = F/P = [ℏ * A_asym * η * ω³ * Q] / [32 π³ c³ * P_0]

    Note: This is independent of v_eff and area.

    Parameters
    ----------
    omega : float
        Modulation angular frequency [rad/s]
    Q : float
        Quality factor
    A_asym : float
        Asymmetry parameter
    eta_dir : float
        Directional efficiency

    Returns
    -------
    t2p : float
        Thrust-to-power ratio [N/W]
    """
    P_0 = 1e6  # W·s/m²
    return (C.hbar * A_asym * eta_dir * omega**3 * Q) / (32 * np.pi**3 * C.c**3 * P_0)

def area_needed_for_thrust(F_target, omega, v_eff_over_c, A_asym=0.5, eta_dir=0.5):
    """
    Calculate required area to achieve target thrust via ADCE.

    Parameters
    ----------
    F_target : float
        Target thrust [N]
    omega : float
        Modulation angular frequency [rad/s]
    v_eff_over_c : float
        Effective modulation velocity / c

    Returns
    -------
    area : float
        Required area [m²]
    """
    lam = 2 * np.pi * C.c / omega
    N_modes_per_area = 1 / lam**2
    K = (1 / (4 * np.pi)) * omega * N_modes_per_area * (C.hbar * omega / C.c) * A_asym * eta_dir
    return F_target / K
