"""
Plasma Wakefield and MHD Coupling
====================================

Models for propulsion via plasma-Alfven wave coupling in magnetized plasmas.
This is the leading candidate for macroscopic UAP propulsion within known physics.
"""

import numpy as np
from . import constants as C

def plasma_wakefield_thrust(n, B, v_flow, A, L, eta=0.1):
    """
    Calculate thrust from plasma wakefield / Alfven wave coupling.

    A craft in magnetized plasma generates Alfven waves, exchanging
    momentum with the bulk flow. Energy comes from the plasma flow,
    not the vacuum ground state.

    Parameters
    ----------
    n : float
        Plasma number density [m^-3]
    B : float
        Magnetic field strength [T]
    v_flow : float
        Plasma bulk flow velocity [m/s]
    A : float
        Cross-sectional area [m²]
    L : float
        Interaction length [m]
    eta : float, optional
        Coupling efficiency (default: 0.1)

    Returns
    -------
    F : float
        Thrust [N]
    P : float
        Power to maintain coupling [W]
    v_A : float
        Alfven speed [m/s]
    """
    rho = n * C.m_p
    v_A = B / np.sqrt(C.mu_0 * rho)

    # Thrust: momentum flux from Alfven wave generation
    F = eta * (B**2 / C.mu_0) * A * (v_flow / v_A)**2

    # Power: energy to generate Alfven waves
    B_pert = eta * B * (v_flow / v_A)
    P = 0.5 * (B_pert**2 / C.mu_0) * A * v_A

    return F, P, v_A

def solar_wind_thrust(A=1.0, L=10.0, eta=0.1):
    """
    Convenience function: thrust in typical solar wind conditions.

    Parameters
    ----------
    A : float
        Cross-sectional area [m²] (default: 1.0)
    L : float
        Interaction length [m] (default: 10.0)
    eta : float
        Coupling efficiency (default: 0.1)

    Returns
    -------
    F, P, v_A : tuple
        Thrust [N], power [W], Alfven speed [m/s]
    """
    n = 5e6       # m^-3
    B = 5e-9      # T
    v_flow = 400e3  # m/s
    return plasma_wakefield_thrust(n, B, v_flow, A, L, eta)

def ionosphere_thrust(A=1.0, L=10.0, eta=0.1):
    """
    Convenience function: thrust in typical ionospheric conditions.

    Parameters
    ----------
    A : float
        Cross-sectional area [m²] (default: 1.0)
    L : float
        Interaction length [m] (default: 10.0)
    eta : float
        Coupling efficiency (default: 0.1)

    Returns
    -------
    F, P, v_A : tuple
        Thrust [N], power [W], Alfven speed [m/s]
    """
    n = 1e12      # m^-3
    B = 5e-5      # T
    v_flow = 1e3  # m/s
    return plasma_wakefield_thrust(n, B, v_flow, A, L, eta)

def nimitz_marine_thrust(A=16.0, L=12.0, eta=0.1):
    """
    Convenience function: thrust in Nimitz encounter marine conditions.

    Parameters
    ----------
    A : float
        Cross-sectional area [m²] (default: 16.0 for Tic Tac)
    L : float
        Interaction length [m] (default: 12.0)
    eta : float
        Coupling efficiency (default: 0.1)

    Returns
    -------
    F, P, v_A : tuple
        Thrust [N], power [W], Alfven speed [m/s]
    """
    n = 1e11      # m^-3 (enhanced marine plasma)
    B = 40e-6     # T (Earth's field at 31°N)
    v_flow = 10   # m/s (minimal flow, craft stationary)
    return plasma_wakefield_thrust(n, B, v_flow, A, L, eta)

def required_plasma_density(F_target, B, v_flow, A, eta=0.1):
    """
    Calculate required plasma density to achieve target thrust.

    Parameters
    ----------
    F_target : float
        Target thrust [N]
    B : float
        Magnetic field [T]
    v_flow : float
        Flow velocity [m/s]
    A : float
        Cross-sectional area [m²]
    eta : float
        Coupling efficiency

    Returns
    -------
    n : float
        Required plasma density [m^-3]
    """
    # F = eta * (B²/μ₀) * A * (v_flow/v_A)²
    # v_A = B / sqrt(μ₀ * n * m_p)
    # F = eta * (B²/μ₀) * A * v_flow² * (μ₀ * n * m_p) / B²
    # F = eta * A * v_flow² * n * m_p
    # n = F / (eta * A * v_flow² * m_p)
    return F_target / (eta * A * v_flow**2 * C.m_p)
