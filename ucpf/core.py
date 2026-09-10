"""
UCPF Core Framework
===================
Fundamental formulas, axioms, categories, and epistemic calibration.

This module provides the ontological and mathematical foundation
for all UCPF analyses. Every claim is tagged with an epistemic status.
"""

import numpy as np
from . import constants as C

# ============================================================
# EPISTEMIC CALIBRATION ENUM
# ============================================================

class EpistemicStatus:
    """Calibration levels for scientific claims."""
    PROVEN = "PROVEN"                    # Peer-reviewed, replicated
    CONSISTENT = "THEORETICALLY_CONSISTENT"  # Math sound, limited experimental test
    SPECULATIVE = "SPECULATIVE"          # Requires new physics or unconfirmed assumptions
    RULED_OUT = "RULED_OUT"              # Falsified by experiment or thermodynamics
    UNKNOWN = "UNKNOWN"                  # Insufficient data to classify

# ============================================================
# CATEGORY REGISTRY
# ============================================================

CATEGORIES = {
    "07": "Quantum Field Dynamics",
    "14": "Non-Equilibrium Thermodynamics",
    "22": "Propulsion & Field Coupling",
    "31": "Axiomatic Foundations",
    "VCP": "Vacuum-Coupled Propulsion",
}

# ============================================================
# AXIOMS (load-bearing assumptions)
# ============================================================

AXIOMS = {
    "31.07": {
        "statement": "Vacuum is structured, not empty",
        "description": "The quantum vacuum possesses measurable properties: permittivity, permeability, Casimir forces, and zero-point energy.",
        "status": EpistemicStatus.PROVEN,
    },
    "31.12": {
        "statement": "Consciousness may be understood as field resonance",
        "description": "Consciousness is hypothesized to emerge from resonant coupling between information-processing systems and structured fields.",
        "status": EpistemicStatus.SPECULATIVE,
    },
    "VCP.01": {
        "statement": "Vacuum can act as a directional reaction medium",
        "description": "Under non-equilibrium, asymmetric boundary conditions, the vacuum can mediate momentum transfer without providing net energy.",
        "status": EpistemicStatus.CONSISTENT,
    },
}

# ============================================================
# FORMULA REGISTRY
# ============================================================

class Formula:
    """A registered UCPF formula with metadata."""
    def __init__(self, fid, name, expression, category, status, references=None):
        self.fid = fid
        self.name = name
        self.expression = expression
        self.category = category
        self.status = status
        self.references = references or []

    def __repr__(self):
        return f"Formula({self.fid}: {self.name} [{self.status}])"

FORMULAS = {
    "07.03": Formula(
        "07.03", "Vacuum Polarization",
        "P_vac = epsilon_0 * chi * E",
        "07", EpistemicStatus.PROVEN,
        ["Schwinger 1951", "QED textbooks"]
    ),
    "07.12": Formula(
        "07.12", "Casimir Energy Density",
        "E_cas = -pi**2 * hbar * c / (240 * d**4)",
        "07", EpistemicStatus.PROVEN,
        ["Casimir 1948", "Lamoreaux 1997"]
    ),
    "14.07": Formula(
        "14.07", "Detailed Balance Violation",
        "dS/dt > 0 for non-equilibrium systems",
        "14", EpistemicStatus.PROVEN,
        ["Prigogine 1967"]
    ),
    "22.04": Formula(
        "22.04", "EM Momentum Transfer",
        "F = (1/c) * dE/dt for photon rocket",
        "22", EpistemicStatus.PROVEN,
        ["Maxwell 1865"]
    ),
    "22.11": Formula(
        "22.11", "Plasma Wakefield Coupling",
        "F = eta * (B**2/mu_0) * A * (v_flow/v_A)**2",
        "22", EpistemicStatus.CONSISTENT,
        ["Alfven 1942", "Tajima & Dawson 1979"]
    ),
    "VCP.01": Formula(
        "VCP.01", "Asymmetric DCE Thrust",
        "F = (hbar * A * A_asym * eta * v_eff**2 * omega**4) / (8*pi**3 * c**5)",
        "VCP", EpistemicStatus.CONSISTENT,
        ["Wilson et al. 2011", "Maclay & Fearn 2002"]
    ),
    "VCP.02": Formula(
        "VCP.02", "Zip-Line Efficiency Bound",
        "eta <= eta_max (fluctuation-dissipation)",
        "VCP", EpistemicStatus.PROVEN,
        ["Callen & Welton 1951"]
    ),
}

def get_formula(fid):
    """Retrieve a formula by its UCPF ID."""
    return FORMULAS.get(fid)

def list_formulas(category=None, status=None):
    """List formulas filtered by category and/or status."""
    results = []
    for f in FORMULAS.values():
        if category and f.category != category:
            continue
        if status and f.status != status:
            continue
        results.append(f)
    return results

def epistemic_summary():
    """Print summary of epistemic calibration across all formulas."""
    counts = {s: 0 for s in [EpistemicStatus.PROVEN, EpistemicStatus.CONSISTENT,
                               EpistemicStatus.SPECULATIVE, EpistemicStatus.RULED_OUT]}
    for f in FORMULAS.values():
        counts[f.status] = counts.get(f.status, 0) + 1

    print("UCPF Epistemic Calibration Summary")
    print("=" * 40)
    for status, count in counts.items():
        print(f"  {status:<25}: {count}")
    print(f"  {'TOTAL':<25}: {len(FORMULAS)}")
