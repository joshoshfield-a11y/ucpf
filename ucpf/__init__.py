"""
UCPF — Universal Consciousness and Physics Framework
====================================================

A rigorous, falsifiable framework for analyzing anomalous propulsion,
consciousness-field interactions, and vacuum-coupled phenomena.

Version: 10.1
License: MIT
Authors: UPE-78 Research Collective

Modules
-------
core : Fundamental formulas, axioms, and epistemic calibration
vcp : Vacuum-Coupled Propulsion (ADCE, zip-line hypothesis)
plasma : Plasma wakefield and MHD coupling
ionization : Air ionization mechanisms for plasma generation
power : Power system architecture and source evaluation
falsification : Experimental protocols with quantitative thresholds
constants : Physical constants in SI units
utils : Helper functions and validation

Examples
--------
>>> import ucpf
>>> from ucpf.plasma import plasma_wakefield_thrust
>>> F, P, v_A = plasma_wakefield_thrust(n=5e6, B=5e-9, v_flow=400e3, A=1.0, L=10.0)
>>> print(f"Thrust: {F:.2e} N")

>>> from ucpf.vcp import adce_thrust
>>> F, P, N = adce_thrust(omega=2*pi*10e9, v_eff_over_c=1e-3, A_asym=0.5, area=1e-4)
>>> print(f"ADCE thrust: {F:.2e} N")
"""

__version__ = "10.1.0"
__author__ = "UPE-78 Research Collective"
__license__ = "MIT"

from . import constants
from . import core
from . import vcp
from . import plasma
from . import ionization
from . import power
from . import falsification
from . import utils

__all__ = [
    "constants",
    "core",
    "vcp",
    "plasma",
    "ionization",
    "power",
    "falsification",
    "utils",
]
