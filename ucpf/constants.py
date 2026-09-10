"""
UCPF Physical Constants
=======================
Standard physical constants used throughout the UCPF framework.
All values in SI units unless otherwise noted.
"""

import numpy as np

# Mathematical
pi = np.pi
euler = np.e

# Physical constants (CODATA 2018)
c = 2.99792458e8          # Speed of light [m/s]
h = 6.62607015e-34        # Planck constant [J·s]
hbar = 1.054571817e-34    # Reduced Planck constant [J·s]
G = 6.67430e-11           # Gravitational constant [m³/(kg·s²)]

# Electromagnetic
mu_0 = 4 * pi * 1e-7      # Vacuum permeability [H/m]
epsilon_0 = 8.854187817e-12  # Vacuum permittivity [F/m]
e = 1.602176634e-19       # Elementary charge [C]
alpha = 7.2973525693e-3   # Fine-structure constant [dimensionless]

# Particle masses
m_e = 9.1093837015e-31    # Electron mass [kg]
m_p = 1.67262192369e-27   # Proton mass [kg]
m_n = 1.67492749804e-27   # Neutron mass [kg]

# Thermodynamic
k_B = 1.380649e-23        # Boltzmann constant [J/K]
N_A = 6.02214076e23       # Avogadro constant [1/mol]
R = 8.314462618           # Gas constant [J/(mol·K)]
sigma_sb = 5.670374419e-8 # Stefan-Boltzmann constant [W/(m²·K⁴)]

# Atomic
a_0 = 5.29177210903e-11   # Bohr radius [m]
R_inf = 10973731.568160   # Rydberg constant [1/m]

# Material properties (reference)
rho_aluminum = 2700       # kg/m³
rho_carbon_fiber = 1600   # kg/m³
E_breakdown_air = 3e6     # V/m (DC)
E_breakdown_RF = 1e7      # V/m (RF)
n_air_STP = 2.5e25        # m^-3 (molecular number density at STP)
ionization_energy_N2 = 15.6  # eV
ionization_energy_O2 = 12.1  # eV

# Casimir
F_casimir_coeff = pi**2 * hbar * c / 240  # N·m² (for F = coeff / d⁴)

# Plasma
# Plasma frequency: omega_p = sqrt(n_e * e² / (epsilon_0 * m_e))
def plasma_frequency(n_e):
    """Calculate plasma angular frequency [rad/s] from electron density [m^-3]."""
    return np.sqrt(n_e * e**2 / (epsilon_0 * m_e))

def plasma_frequency_Hz(n_e):
    """Calculate plasma frequency [Hz] from electron density [m^-3]."""
    return plasma_frequency(n_e) / (2 * pi)

def debye_length(n_e, T_e):
    """Calculate Debye length [m] from electron density [m^-3] and temperature [K]."""
    return np.sqrt(epsilon_0 * k_B * T_e / (n_e * e**2))

def alfven_speed(B, n_i):
    """Calculate Alfven speed [m/s] from B-field [T] and ion density [m^-3]."""
    rho = n_i * m_p
    return B / np.sqrt(mu_0 * rho)
