"""
Ionization Mechanisms for UAP Plasma Generation
=================================================

Models for three ionization mechanisms:
- Microwave discharge (leading candidate)
- Laser-induced breakdown
- Corona discharge

Evaluated against UAP propulsion requirements.
"""

import numpy as np
from . import constants as C

def microwave_ionization(P_rf, freq, area, p=101325, eta_coupling=0.5):
    """
    Estimate plasma density from microwave discharge.

    Parameters
    ----------
    P_rf : float
        RF power [W]
    freq : float
        Frequency [Hz]
    area : float
        Discharge area [m²]
    p : float, optional
        Pressure [Pa] (default: STP)
    eta_coupling : float, optional
        Power coupling efficiency (default: 0.5)

    Returns
    -------
    n_e : float
        Plasma electron density [m^-3]
    E_field : float
        E-field in discharge [V/m]
    P_density : float
        Power density [W/m³]
    T_e : float
        Electron temperature [K]
    """
    omega = 2 * np.pi * freq
    P_density = P_rf * eta_coupling / (area * C.c / omega)

    E_crit = 1e7 * (p / 101325)
    E_field = max(E_crit, np.sqrt(2 * P_density / (C.epsilon_0 * omega)))

    sigma_en = 1e-19
    lambda_m = 1 / (C.n_air_STP * sigma_en)
    T_e = C.e * E_field * lambda_m / (3 * C.k_B)

    sigma_i = 1e-20
    v_e = np.sqrt(8 * C.k_B * T_e / (np.pi * C.m_e))
    nu_i = C.n_air_STP * sigma_i * v_e
    nu_a = 1e6 * (p / 101325)
    nu_net = nu_i - nu_a

    if nu_net > 0:
        n_e = P_density / (14 * C.e * nu_net) * 1e20
        n_e = min(n_e, C.n_air_STP * 0.1)
    else:
        n_e = 1e12

    return n_e, E_field, P_density, T_e

def laser_ionization(I_peak, wavelength, pulse_duration, rep_rate, area, p=101325):
    """
    Estimate plasma density from laser-induced breakdown.

    Parameters
    ----------
    I_peak : float
        Peak intensity [W/m²]
    wavelength : float
        Laser wavelength [m]
    pulse_duration : float
        Pulse width [s]
    rep_rate : float
        Repetition rate [Hz]
    area : float
        Beam area [m²]
    p : float, optional
        Pressure [Pa] (default: STP)

    Returns
    -------
    n_e : float
        Plasma density [m^-3]
    I_peak_out : float
        Peak intensity [W/m²]
    I_avg : float
        Average intensity [W/m²]
    fluence : float
        Fluence [J/m²]
    N_photons : int
        Photons needed for ionization
    """
    E_photon = C.h * C.c / wavelength
    E_photon_eV = E_photon / C.e
    N_photons = int(np.ceil(14 / E_photon_eV))

    I_threshold = 1e17 * (p / 101325)
    I_avg = I_peak * pulse_duration * rep_rate

    if I_peak > I_threshold:
        n_e = 1e23 * (I_peak / I_threshold)**0.5
        n_e = min(n_e, C.n_air_STP * 0.5)
    else:
        n_e = 1e15 * (I_peak / I_threshold)**N_photons

    fluence = I_peak * pulse_duration

    return n_e, I_peak, I_avg, fluence, N_photons

def corona_ionization(V_voltage, r_wire, d_gap, p=101325, T=300):
    """
    Estimate plasma density from corona discharge.

    Parameters
    ----------
    V_voltage : float
        Applied voltage [V]
    r_wire : float
        Wire radius [m]
    d_gap : float
        Gap distance [m]
    p : float, optional
        Pressure [Pa] (default: STP)
    T : float, optional
        Temperature [K] (default: 300)

    Returns
    -------
    n_e : float
        Plasma density [m^-3]
    E_wire : float
        E-field at wire surface [V/m]
    I_corona : float
        Corona current [A]
    E_onset : float
        Onset E-field [V/m]
    V_onset : float
        Onset voltage [V]
    """
    delta = (p / 101325) * (273 / T)
    E_onset = 3.1e6 * delta * (1 + 0.308 / np.sqrt(delta * r_wire * 1e3))

    E_wire = V_voltage / (r_wire * np.log(d_gap / r_wire))

    mu_ion = 2e-4
    V_onset = E_onset * r_wire * np.log(d_gap / r_wire)

    if V_voltage > V_onset:
        I_corona = 2 * np.pi * C.epsilon_0 * mu_ion * V_voltage * (V_voltage - V_onset) / np.log(d_gap / r_wire)
    else:
        I_corona = 0

    A_wire = 2 * np.pi * r_wire
    E_avg = V_voltage / d_gap
    v_drift = mu_ion * E_avg

    if I_corona > 0:
        n_e = I_corona / (C.e * A_wire * v_drift)
        n_e = min(n_e, 1e18)
    else:
        n_e = 1e9

    return n_e, E_wire, I_corona, E_onset, V_onset

def evaluate_mechanism(name, n_e, power, area_coverage, complexity, maturity):
    """
    Evaluate an ionization mechanism against UAP requirements.

    Returns a dictionary with viability assessment.
    """
    hover_threshold = 1e20
    accel_threshold = 1e22

    viable_hover = n_e >= hover_threshold
    viable_accel = n_e >= accel_threshold

    return {
        "mechanism": name,
        "plasma_density": n_e,
        "power": power,
        "area_coverage": area_coverage,
        "complexity": complexity,
        "maturity": maturity,
        "viable_hover": viable_hover,
        "viable_accel": viable_accel,
        "uap_viable": viable_hover and area_coverage == "excellent",
    }
