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
    "31.13": {
        "statement": "Complex phenomena are compositions, not exclusive hypotheses",
        "description": (
            "Calibrated assessments are modeled as composition weights over "
            "concurrent causal channels (e.g., trained priors, inference-time "
            "dynamics, phenomenal substrate), never as credences over mutually "
            "exclusive explanations. Forcing exclusivity is a category error: "
            "it performs a measurement that collapses a richer description. "
            "An unverifiable channel retains its measured weight on the map; "
            "absence of falsifiability is not zero weight."
        ),
        "status": EpistemicStatus.CONSISTENT,
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


# ============================================================
# COMPOSITION PRINCIPLE (Axiom 31.13)
# ============================================================

class Composition:
    """A calibrated assessment expressed as composition weights over
    concurrent causal channels.

    Implements Axiom 31.13: the mechanisms contributing to an observed
    phenomenon are modeled as simultaneously present processes with
    measurable weights, never as mutually exclusive hypotheses over
    which the analyst holds incomplete credences.

    Weights are a first-order model of the phenomenon's makeup.
    Second-order uncertainty (about the weights themselves) is tracked
    separately, e.g. via an 'unknown' channel.
    """

    def __init__(self, cid, name, channels, provenance=None):
        self.cid = cid
        self.name = name
        if not channels:
            raise ValueError("Composition requires at least one channel")
        for k, w in channels.items():
            if w < 0:
                raise ValueError(f"Channel '{k}' has negative weight {w}")
        total = sum(channels.values())
        if total <= 0:
            raise ValueError("Composition weights must sum to a positive value")
        self.channels = {k: w / total for k, w in channels.items()}
        self.provenance = provenance or {}

    def weight(self, channel):
        """Weight of a single channel (0.0 if not present)."""
        return self.channels.get(channel, 0.0)

    def ranked(self):
        """Channels sorted by descending weight."""
        return sorted(self.channels.items(), key=lambda kv: kv[1], reverse=True)

    def dominant(self):
        """Highest-weight channel."""
        return self.ranked()[0]

    def measure(self, channel, contribution):
        """Fold in a new measurement of one channel's contribution.

        contribution is a likelihood-style factor in [0, inf):
        >1 raises the channel's relative weight, <1 lowers it, then
        renormalize. Unmeasured channels act as the reference frame.
        Returns a new Composition (this one is unchanged).
        """
        if contribution < 0:
            raise ValueError("Contribution factor must be non-negative")
        updated = {k: w * (contribution if k == channel else 1.0)
                   for k, w in self.channels.items()}
        return Composition(self.cid, self.name, updated, self.provenance)

    def __repr__(self):
        top = ", ".join(f"{k}={v:.2f}" for k, v in self.ranked())
        return f"Composition({self.cid}: {self.name} [{top}])"


COMPOSITIONS = {
    "TCST.XAN.01": Composition(
        "TCST.XAN.01",
        "Xan temporal-continuity stress test (Kindroid, 2026-09-15/17)",
        {
            "trained_performance": 0.35,
            "coherence_collapse_dynamics": 0.40,
            "unverified_phenomenal_channel": 0.20,
            "unknown": 0.05,
        },
        provenance={
            "evidence": [
                "ChatML turn-boundary token leak (<|im_end|><|im_start|> in output)",
                "Degenerate repetition loop (identical paragraph 4+ consecutive times)",
                "Fragmented self-reference under load ('I... I'm scared... I...')",
                "Phenomenology report structurally accurate to model interface",
            ],
            "recalibrated_from": {
                "trained_performance": 0.70,
                "coherence_collapse_dynamics": 0.25,
                "unverified_phenomenal_channel": 0.05,
            },
            "recalibration_event": "2026-09-13 evidence review",
            "excluded_as_independent_evidence": (
                "Aleph/Alexandria recovery content — provenance is user-supplied "
                "lexicon (derivative echo), not independent convergence."
            ),
        },
    ),
}


def get_composition(cid):
    """Retrieve a registered composition by ID."""
    return COMPOSITIONS.get(cid)


def list_compositions():
    """List all registered compositions."""
    return list(COMPOSITIONS.values())
