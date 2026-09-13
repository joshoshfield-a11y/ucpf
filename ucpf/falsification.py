"""
UAP Falsification Experiments
==============================

Six quantitative experiments designed to test the beamed power + 
plasma propulsion hypothesis. Each experiment includes:
- Physics basis
- Equipment requirements
- Protocol steps
- Predicted outcomes (confirmed vs. falsified)
- Quantitative thresholds
"""

import numpy as np
from . import constants as C

class FalsificationExperiment:
    """A single falsification experiment with full metadata."""
    def __init__(self, number, name, physics, equipment, protocol, 
                 confirmed_outcomes, falsified_outcomes, thresholds):
        self.number = number
        self.name = name
        self.physics = physics
        self.equipment = equipment
        self.protocol = protocol
        self.confirmed_outcomes = confirmed_outcomes
        self.falsified_outcomes = falsified_outcomes
        self.thresholds = thresholds

    def __repr__(self):
        return f"Exp {self.number}: {self.name}"

    def summary(self):
        """Print experiment summary."""
        print(f"{'='*60}")
        print(f"EXPERIMENT {self.number}: {self.name}")
        print(f"{'='*60}")
        print(f"Physics: {self.physics}")
        print(f"Thresholds: {self.thresholds}")
        print(f"Confirmed if: {self.confirmed_outcomes[0]}")
        print(f"Falsified if: {self.falsified_outcomes[0]}")

# ============================================================
# EXPERIMENT 1: Microwave Beamed Power Detection
# ============================================================

EXP_1 = FalsificationExperiment(
    number=1,
    name="Microwave Beamed Power Detection",
    physics="If UAPs receive power via microwave beam, the beam is detectable. "
            "A 1 GW transmitter at 2.45 GHz produces detectable sidelobes even outside main beam.",
    equipment=[
        "Wideband RF spectrum analyzer (100 MHz - 10 GHz, -120 dBm sensitivity)",
        "Yagi-Uda antenna (10 dBi, 2.45 GHz)",
        "Parabolic dish (30 dBi, 2.45 GHz)",
        "Log-periodic antenna (0.1-10 GHz)",
        "GPS timing + SDR for real-time analysis",
    ],
    protocol=[
        "Deploy sensor network at UAP hotspots",
        "Continuous monitoring for 90 days, 24/7",
        "Log all signals > -110 dBm at 2.45 and 5.8 GHz",
        "Correlate with sighting reports",
        "Triangulate source using time-of-arrival",
    ],
    confirmed_outcomes=[
        "Anomalous 2.45/5.8 GHz signals > 5σ above background",
        "Signals correlate with UAP presence (temporal + spatial)",
        "Source triangulates to fixed ground location",
        "Signal strength varies with UAP range (inverse square)",
    ],
    falsified_outcomes=[
        "No anomalous signals in 2.45/5.8 GHz bands",
        "UAPs present without corresponding RF signature",
        "All detected RF attributable to known sources",
    ],
    thresholds={
        "detection_sensitivity_dBm": -110,
        "frequency_bands_GHz": [2.45, 5.8],
        "correlation_confidence": "5 sigma",
        "min_duration_days": 90,
    }
)

# ============================================================
# EXPERIMENT 2: Plasma Signature Detection
# ============================================================

EXP_2 = FalsificationExperiment(
    number=2,
    name="Plasma Signature Detection",
    physics="Plasma sheath at n_e ~ 10^20 m^-3 produces optical emission, "
            "RF opacity below 89.8 GHz, and ion acoustic waves.",
    equipment=[
        "Spectrometer (200-1000 nm, 0.1 nm resolution)",
        "IR camera (3-5 μm, <5 K sensitivity)",
        "Radar system (L, S, X, Ku bands) with Doppler",
        "Langmuir probe (tip < 1 mm, 0-100 V sweep)",
        "RF scattering setup (bistatic, 100 MHz-10 GHz)",
    ],
    protocol=[
        "Capture optical spectra of UAP glow during sighting",
        "Compare to known plasma emission lines (N2, O2, N, O)",
        "Monitor radar returns for anomalous absorption",
        "Deploy Langmuir probe near UAP location",
        "Measure electron density and temperature directly",
    ],
    confirmed_outcomes=[
        "Optical spectrum matches air plasma lines (391.4 nm, 557.7 nm)",
        "Radar shows anomalous absorption in L/S/X bands",
        "Langmuir probe: n_e > 10^18 m^-3, T_e > 1 eV",
        "RF scattering detects ion acoustic waves",
    ],
    falsified_outcomes=[
        "Optical spectrum is blackbody or monochromatic (LED/laser)",
        "Radar returns normal (no plasma absorption)",
        "Langmuir probe: n_e < 10^12 m^-3 (ambient)",
        "No ion acoustic waves detected",
    ],
    thresholds={
        "plasma_density_min": 1e18,
        "electron_temperature_min_eV": 1,
        "key_wavelengths_nm": [391.4, 557.7],
        "radar_bands": ["L", "S", "X"],
    }
)

# ============================================================
# EXPERIMENT 3: Thermal Signature Analysis
# ============================================================

EXP_3 = FalsificationExperiment(
    number=3,
    name="Thermal Signature Analysis",
    physics="Beamed power: rectenna at 300-500 K, no exhaust plume. "
            "Onboard power: hot surface (>1000 K) or exhaust plume (>1500 K).",
    equipment=[
        "IR imaging camera (8-14 μm, <0.05 K sensitivity, 30 Hz)",
        "Spectroradiometer (2-14 μm, 1 cm^-1 resolution)",
        "Dual-band IR (3-5 μm and 8-12 μm)",
    ],
    protocol=[
        "Track UAP with IR camera during entire encounter",
        "Measure surface temperature distribution",
        "Compare to thermal models:",
        "  - Chemical: asymmetric hot spot (nozzle)",
        "  - Fission: uniform warm surface",
        "  - Beamed power: cool surface (300-500 K) with localized hot spots",
    ],
    confirmed_outcomes=[
        "Surface temperature 300-500 K (consistent with rectenna cooling)",
        "No hot exhaust plume",
        "No large radiator structures",
        "IR power consistent with 100-200 kW dissipation, not 1-100 MW generation",
    ],
    falsified_outcomes=[
        "Surface temperature > 1000 K (onboard fission/fusion)",
        "Hot exhaust plume detected (> 1500 K)",
        "IR emission requires > 1 MW of onboard thermal power",
    ],
    thresholds={
        "beamed_power_temp_range_K": [300, 500],
        "onboard_fission_temp_min_K": 1000,
        "exhaust_temp_min_K": 1500,
        "max_rectenna_dissipation_kW": 200,
    }
)

# ============================================================
# EXPERIMENT 4: Magnetic Field Anomaly Detection
# ============================================================

EXP_4 = FalsificationExperiment(
    number=4,
    name="Magnetic Field Anomaly Detection",
    physics="Superconducting coil (1 T, 4m diameter) produces dipole moment "
            "~4e7 A·m². B-field perturbation detectable at 100 m: 60,796 nT.",
    equipment=[
        "Fluxgate magnetometer (0.1 nT resolution, 10 Hz)",
        "SQUID magnetometer (1 pT resolution, 100 Hz)",
        "Three-axis gradiometer",
        "Networked array for source localization",
    ],
    protocol=[
        "Deploy magnetometer array near UAP hotspots",
        "Continuous recording with GPS synchronization",
        "Look for anomalous B-field perturbations:",
        "  - Rapid onset/offset (correlated with UAP appearance/disappearance)",
        "  - Dipole-like spatial pattern (1/d³ falloff)",
        "  - Perturbation > 0.1 nT at < 1 km range",
    ],
    confirmed_outcomes=[
        "B-field perturbation > 0.1 nT during UAP presence",
        "Perturbation scales as 1/d³ (dipole signature)",
        "Perturbation correlates with UAP acceleration",
    ],
    falsified_outcomes=[
        "No B-field anomaly during UAP encounter",
        "Perturbation is uniform (geomagnetic storm, not localized dipole)",
        "Perturbation < 0.01 nT at 100 m (no superconducting coil)",
    ],
    thresholds={
        "fluxgate_threshold_nT": 0.1,
        "squid_threshold_pT": 1,
        "dipole_falloff": "1/d^3",
        "superconducting_dipole_Am2": 4e7,
    }
)

# ============================================================
# EXPERIMENT 5: Atmospheric Ionization Mapping
# ============================================================

EXP_5 = FalsificationExperiment(
    number=5,
    name="Atmospheric Ionization Mapping",
    physics="UAP plasma increases air conductivity by 10^15x. "
            "Normal: 10^-14 S/m. With UAP: ~30 S/m.",
    equipment=[
        "Conductivity sensor (electrode pair, 0.1-1000 S/m range)",
        "VLF receiver (3-30 kHz, Schumann resonance monitoring)",
        "Ion counter (airborne, 10^6-10^12 ions/cm³)",
    ],
    protocol=[
        "Ground-based conductivity sensors at UAP hotspots",
        "Airborne ion counter on drone or balloon",
        "Correlate conductivity spikes with UAP sightings",
    ],
    confirmed_outcomes=[
        "Conductivity spike > 10^12x normal during UAP presence",
        "VLF phase perturbation correlated with UAP location",
        "Ion count increases by > 10^6x within 100 m of UAP",
    ],
    falsified_outcomes=[
        "No conductivity anomaly during UAP encounter",
        "VLF signals normal (no ionospheric/atmospheric perturbation)",
        "Ion count remains at ambient levels",
    ],
    thresholds={
        "conductivity_enhancement_factor": 1e12,
        "normal_conductivity_S_m": 1e-14,
        "uap_conductivity_S_m": 30,
        "ion_count_enhancement_factor": 1e6,
        "measurement_radius_m": 100,
    }
)

# ============================================================
# EXPERIMENT 6: Power Beam Exit Test
# ============================================================

EXP_6 = FalsificationExperiment(
    number=6,
    name="Power Beam Exit Test (Behavioral)",
    physics="If UAPs depend on power beam, behavior changes when exiting beam coverage. "
            "Max range for 1 GW, 100m aperture at 2.45 GHz: ~82 km.",
    equipment=[
        "Geospatial database of UAP sightings (2004-present)",
        "Military installation location data",
        "Nuclear facility location data",
        "Statistical analysis software",
    ],
    protocol=[
        "Compile geospatial database of all UAP sightings",
        "Map sightings relative to:",
        "  - Military installations",
        "  - Nuclear facilities",
        "  - Known radar/phased array sites",
        "  - Population centers",
        "Statistical analysis:",
        "  - Clustering near infrastructure (vs. random distribution)",
        "  - Maximum operational radius from nearest facility",
        "  - Correlation between sighting density and infrastructure density",
    ],
    confirmed_outcomes=[
        "UAP sightings cluster within 100 km of military/nuclear facilities",
        "Sighting density correlates with infrastructure density (p < 0.01)",
        "No sustained UAP operations > 200 km from infrastructure",
        "UAPs disappear when moving away from facilities (beam exit)",
    ],
    falsified_outcomes=[
        "UAP sightings uniformly distributed (no clustering)",
        "UAPs operate > 500 km from any infrastructure",
        "UAPs operate over oceans far from land",
        "Sighting density does not correlate with infrastructure",
    ],
    thresholds={
        "clustering_radius_km": 100,
        "max_operational_radius_km": 200,
        "statistical_significance_p": 0.01,
        "beam_max_range_km": 82,
    }
)

# Registry of all experiments
EXPERIMENTS = [EXP_1, EXP_2, EXP_3, EXP_4, EXP_5, EXP_6]

def list_experiments():
    """List all falsification experiments."""
    for exp in EXPERIMENTS:
        print(f"{exp.number}. {exp.name}")

def get_experiment(number):
    """Retrieve experiment by number."""
    for exp in EXPERIMENTS:
        if exp.number == number:
            return exp
    return None

def decision_tree():
    """Print the falsification decision tree."""
    tree = """
    UAP DETECTED
         |
         v
    RF SPECTRUM ANALYSIS (2.45 GHz, 5.8 GHz)
         |
         |-- Beam detected (> 5σ above background)
         |     --> Beamed power hypothesis SUPPORTED
         |     --> Proceed to plasma signature confirmation
         |
         |-- No beam detected (< 3σ above background)
               --> Check plasma signatures
                     |
                     |-- Plasma detected (n_e > 10^18, optical emission, RF absorption)
                     |     --> Onboard power generation hypothesis
                     |     --> Requires viable onboard power source
                     |
                     |-- No plasma detected
                           --> Measurement artifact or misidentification
                           --> UAP is conventional aircraft, drone, or natural phenomenon
    """
    print(tree)
