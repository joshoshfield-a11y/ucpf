"""
UAP Power System Architecture
===============================

Evaluation of all power source options for UAP plasma propulsion.
Includes mass budget analysis, thermal management, and beamed power modeling.
"""

import numpy as np
from . import constants as C

class PowerSource:
    """Base class for power source evaluation."""
    def __init__(self, name, specific_power, specific_energy=None):
        self.name = name
        self.specific_power = specific_power  # W/kg
        self.specific_energy = specific_energy  # J/kg

    def mass_for_power(self, P_target):
        """Calculate mass required for target power [kg]."""
        return P_target / self.specific_power

    def mass_for_energy(self, E_target):
        """Calculate mass required for target energy [kg]."""
        if self.specific_energy is None:
            return float('inf')
        return E_target / self.specific_energy

    def viable_for_craft(self, P_target, craft_mass=1500, budget_fraction=0.4):
        """Check if power source fits within craft mass budget."""
        mass = self.mass_for_power(P_target)
        budget = craft_mass * budget_fraction
        return mass <= budget, mass, budget

# Predefined power sources
SOURCES = {
    "chemical_1hr": PowerSource("Chemical (1 hr endurance)", 
                                13.4e6 * 0.35 / 3600, 13.4e6 * 0.35),
    "fission_conservative": PowerSource("Fission (conservative)", 10),
    "fission_advanced": PowerSource("Fission (advanced)", 50),
    "fusion_realistic": PowerSource("Fusion (realistic)", 100),
    "fusion_target": PowerSource("Fusion (target)", 1000),
    "RTG": PowerSource("RTG", 10),
    "beamed_rectenna": PowerSource("Beamed power (rectenna)", 1000 / 5),  # 5 kg/kW
    "li_ion": PowerSource("Li-ion battery", 500, 900e3),
    "solar": PowerSource("Solar panels", 340 / 10),  # 10 kg/m²
}

def evaluate_all_sources(P_target, craft_mass=1500, budget_fraction=0.4):
    """
    Evaluate all power sources against a target power requirement.

    Parameters
    ----------
    P_target : float
        Target power [W]
    craft_mass : float, optional
        Total craft mass [kg] (default: 1500)
    budget_fraction : float, optional
        Fraction of mass available for power system (default: 0.4)

    Returns
    -------
    results : list
        List of dictionaries with evaluation results
    """
    results = []
    budget = craft_mass * budget_fraction

    for name, source in SOURCES.items():
        viable, mass, _ = source.viable_for_craft(P_target, craft_mass, budget_fraction)
        results.append({
            "name": source.name,
            "mass_kg": mass,
            "budget_kg": budget,
            "viable": viable,
            "specific_power_W_kg": source.specific_power,
        })

    return sorted(results, key=lambda x: x["mass_kg"])

def thermal_radiator_area(P_thermal, T_surface=500, emissivity=0.9):
    """
    Calculate required radiator area for heat rejection.

    Parameters
    ----------
    P_thermal : float
        Thermal power to reject [W]
    T_surface : float, optional
        Radiator temperature [K] (default: 500)
    emissivity : float, optional
        Surface emissivity (default: 0.9)

    Returns
    -------
    area : float
        Required radiator area [m²]
    """
    P_per_m2 = emissivity * C.sigma_sb * T_surface**4
    return P_thermal / P_per_m2

def beamed_power_range(P_tx, G_tx, P_craft, A_craft, eta_rectenna=0.8):
    """
    Calculate maximum operational range for beamed power.

    Parameters
    ----------
    P_tx : float
        Transmitter power [W]
    G_tx : float
        Transmitter gain [dimensionless]
    P_craft : float
        Craft power requirement [W]
    A_craft : float
        Craft receiver area [m²]
    eta_rectenna : float, optional
        Rectenna efficiency (default: 0.8)

    Returns
    -------
    R_max : float
        Maximum range [m]
    S_min : float
        Minimum power flux [W/m²]
    """
    S_min = P_craft / (A_craft * eta_rectenna)
    R_max = np.sqrt(P_tx * G_tx / (4 * np.pi * S_min))
    return R_max, S_min

def transmitter_gain(D, wavelength):
    """
    Calculate phased array transmitter gain.

    Parameters
    ----------
    D : float
        Aperture diameter [m]
    wavelength : float
        Wavelength [m]

    Returns
    -------
    G : float
        Gain [dimensionless]
    """
    return (np.pi * D / wavelength)**2

def beam_footprint_radius(R, D, wavelength):
    """
    Calculate beam footprint radius at range R.

    Parameters
    ----------
    R : float
        Range [m]
    D : float
        Aperture diameter [m]
    wavelength : float
        Wavelength [m]

    Returns
    -------
    radius : float
        Footprint radius [m]
    """
    beamwidth = 1.22 * wavelength / D
    return R * np.tan(beamwidth / 2)
