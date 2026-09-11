"""
Spectral Coupling Efficiency
==============================

Formalizes the "bandwidth" insight: drive systems don't couple to a single
vacuum/plasma mode, but to a spectral window. The coupling efficiency depends
on the overlap between the drive spectrum and the medium's mode density.

This bridges the gap between single-frequency models and real broadband systems.
"""

import numpy as np
from . import constants as C


def mode_density_1d(omega, L):
    """
    1D cavity mode density: number of modes per unit frequency.

    Parameters
    ----------
    omega : float or array
        Angular frequency [rad/s]
    L : float
        Cavity length [m]

    Returns
    -------
    rho : float or array
        Mode density [modes/(rad/s)]
    """
    return L / (np.pi * C.c)


def mode_density_3d(omega, V):
    """
    3D cavity mode density (free space).

    Parameters
    ----------
    omega : float or array
        Angular frequency [rad/s]
    V : float
        Cavity volume [m³]

    Returns
    -------
    rho : float or array
        Mode density [modes/(rad/s)]
    """
    return V * omega**2 / (np.pi**2 * C.c**3)


def drive_spectrum_gaussian(omega, omega_0, delta_omega):
    """
    Gaussian drive spectrum centered at omega_0 with bandwidth delta_omega.

    Parameters
    ----------
    omega : array
        Frequency axis [rad/s]
    omega_0 : float
        Center frequency [rad/s]
    delta_omega : float
        RMS bandwidth [rad/s]

    Returns
    -------
    S : array
        Normalized spectral power density [1/(rad/s)]
    """
    S = np.exp(-0.5 * ((omega - omega_0) / delta_omega)**2)
    return S / (delta_omega * np.sqrt(2 * np.pi))


def drive_spectrum_rectangular(omega, omega_0, delta_omega):
    """
    Rectangular drive spectrum (idealized broadband).

    Parameters
    ----------
    omega : array
        Frequency axis [rad/s]
    omega_0 : float
        Center frequency [rad/s]
    delta_omega : float
        Total bandwidth [rad/s]

    Returns
    -------
    S : array
        Normalized spectral power density [1/(rad/s)]
    """
    S = np.zeros_like(omega)
    mask = np.abs(omega - omega_0) <= delta_omega / 2
    S[mask] = 1.0 / delta_omega
    return S


def spectral_coupling_efficiency(omega_drive, S_drive, omega_medium, 
                                  gamma_medium, mode_density_func):
    """
    Calculate spectral coupling efficiency between drive and medium.

    eta_couple = integral[S_drive(omega) * rho(omega) * Lorentzian(omega)] domega

    Parameters
    ----------
    omega_drive : float
        Drive center frequency [rad/s]
    S_drive : callable
        Drive spectrum function S(omega) -> normalized density
    omega_medium : float
        Medium resonant frequency [rad/s]
    gamma_medium : float
        Medium linewidth [rad/s]
    mode_density_func : callable
        Mode density function rho(omega)

    Returns
    -------
    eta : float
        Dimensionless coupling efficiency [0, 1]
    """
    # Integration window: 10 linewidths around center
    omega_min = min(omega_drive, omega_medium) - 10 * gamma_medium
    omega_max = max(omega_drive, omega_medium) + 10 * gamma_medium
    omega = np.linspace(omega_min, omega_max, 10000)

    # Lorentzian medium response
    lorentzian = (gamma_medium / (2 * np.pi)) /                  ((omega - omega_medium)**2 + (gamma_medium / 2)**2)

    # Mode density
    rho = mode_density_func(omega)

    # Drive spectrum
    S = S_drive(omega)

    # Coupling efficiency
    integrand = S * rho * lorentzian
    eta = np.trapz(integrand, omega)

    return eta


def adce_thrust_spectral(omega_0, delta_omega, v_eff_over_c, A_asym, area, 
                         Q=1000, eta_dir=0.5):
    """
    ADCE thrust with spectral coupling efficiency.

    Accounts for finite drive bandwidth coupling to vacuum mode continuum.

    Parameters
    ----------
    omega_0 : float
        Drive center frequency [rad/s]
    delta_omega : float
        Drive bandwidth [rad/s]
    v_eff_over_c : float
        Effective modulation velocity / c
    A_asym : float
        Asymmetry parameter
    area : float
        Active area [m²]
    Q : float
        Quality factor
    eta_dir : float
        Directional efficiency

    Returns
    -------
    F : float
        Thrust [N]
    P : float
        Drive power [W]
    eta_couple : float
        Spectral coupling efficiency
    """
    from .vcp import adce_thrust

    # Single-frequency thrust (narrowband limit)
    F_narrow, P, _ = adce_thrust(omega_0, v_eff_over_c, A_asym, area, Q, eta_dir)

    # Spectral correction
    # Mode density for area-sized cavity
    V_eff = area * (C.c / omega_0)  # effective volume ~ area * wavelength

    def rho(omega):
        return mode_density_3d(omega, V_eff)

    def S_drive(omega):
        return drive_spectrum_gaussian(omega, omega_0, delta_omega)

    # Medium linewidth: cavity linewidth = omega_0 / Q
    gamma_medium = omega_0 / Q

    eta_couple = spectral_coupling_efficiency(
        omega_0, S_drive, omega_0, gamma_medium, rho
    )

    # Broadband thrust: reduced by coupling efficiency but enhanced by mode count
    F = F_narrow * eta_couple * (delta_omega / gamma_medium)

    return F, P, eta_couple


def plasma_wakefield_thrust_spectral(n, B, v_flow, A, L, eta=0.1,
                                     omega_drive=None, delta_omega=None):
    """
    Plasma wakefield thrust with spectral coupling to Alfven wave spectrum.

    The Alfven wave spectrum in a magnetized plasma has a continuous
    mode structure. This function calculates the enhanced coupling when
    the drive spectrum overlaps with the Alfven continuum.

    Parameters
    ----------
    n : float
        Plasma density [m^-3]
    B : float
        Magnetic field [T]
    v_flow : float
        Flow velocity [m/s]
    A : float
        Cross-sectional area [m²]
    L : float
        Interaction length [m]
    eta : float
        Base coupling efficiency
    omega_drive : float, optional
        Drive frequency [rad/s] (default: v_A / L)
    delta_omega : float, optional
        Drive bandwidth [rad/s] (default: omega_drive / 10)

    Returns
    -------
    F : float
        Thrust [N]
    P : float
        Power [W]
    v_A : float
        Alfven speed [m/s]
    eta_couple : float
        Spectral coupling efficiency
    """
    from .plasma import plasma_wakefield_thrust

    F_base, P, v_A = plasma_wakefield_thrust(n, B, v_flow, A, L, eta)

    if omega_drive is None:
        omega_drive = v_A / L
    if delta_omega is None:
        delta_omega = omega_drive / 10

    # Alfven wave mode density in plasma column
    V = A * L

    def rho(omega):
        return mode_density_1d(omega, L)

    def S_drive(omega):
        return drive_spectrum_gaussian(omega, omega_drive, delta_omega)

    # Alfven wave damping linewidth
    gamma_alfven = omega_drive * 0.1  # 10% damping

    eta_couple = spectral_coupling_efficiency(
        omega_drive, S_drive, omega_drive, gamma_alfven, rho
    )

    # Enhanced thrust from resonant coupling
    F = F_base * (1 + eta_couple * (delta_omega / gamma_alfven))

    return F, P, v_A, eta_couple


def bandwidth_optimization(omega_0, Q, mechanism='adce'):
    """
    Calculate optimal drive bandwidth for maximum coupling.

    For a Lorentzian cavity and Gaussian drive, optimal bandwidth
    is approximately the cavity linewidth.

    Parameters
    ----------
    omega_0 : float
        Center frequency [rad/s]
    Q : float
        Quality factor
    mechanism : str
        'adce' or 'plasma'

    Returns
    -------
    delta_omega_opt : float
        Optimal drive bandwidth [rad/s]
    eta_max : float
        Maximum coupling efficiency
    """
    gamma = omega_0 / Q

    if mechanism == 'adce':
        # For Gaussian drive + Lorentzian cavity, optimal delta ≈ gamma
        delta_omega_opt = gamma
        eta_max = 0.5  # theoretical maximum for matched bandwidths
    elif mechanism == 'plasma':
        # Alfven waves: broader is better due to continuum
        delta_omega_opt = 2 * gamma
        eta_max = 0.3
    else:
        delta_omega_opt = gamma
        eta_max = 0.5

    return delta_omega_opt, eta_max
