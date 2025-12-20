"""
QCT Dark Energy from E_pair Saturation

RIGOROUS IMPLEMENTATION of E_pair evolution with:
1. Conformal regime (high z)
2. Saturation cutoff (z_sat)
3. Logarithmic regime (low z)
4. Dark energy density calculation

ASSUMPTIONS EXPLICITLY STATED:
- Conformal scaling: Ω(z) ~ (1+z)^(3/4) in radiation era
- UV cutoff: Λ_QCT ~ 107 TeV
- Triple suppression factors from manuscript
- w = -1 for released energy

Date: 2025-12-20
Status: HYPOTHESIS TESTING - REQUIRES VALIDATION
"""

import numpy as np
import matplotlib.pyplot as plt

# ============================================================================
# PHYSICAL CONSTANTS
# ============================================================================

# Fundamental
c = 2.99792458e8  # m/s
hbar_eV_s = 6.582119569e-16  # eV·s
m_nu_eV = 0.1  # eV (neutrino mass, approximate)
m_p_eV = 938.27e6  # eV (proton mass)
m_e_eV = 0.511e6  # eV (electron mass)

# QCT parameters (calibrated)
E_pair_0_eV = 5.38e18  # eV (today's pairing energy)
E_0_eV = 0.1  # eV (seed energy)
kappa_conf_eV = 0.48e18  # eV (confinement constant)
Lambda_QCT_eV = 107e12  # eV (107 TeV, UV cutoff)

# Cosmological
n_nu_0 = 336.0  # cm^-3 (relic neutrino density today)
n_nu_0_SI = n_nu_0 * 1e6  # m^-3
z_start = 1e8  # Turn-on redshift
k_turnon = 0.5  # Steepness

# Conversion factors
GeV_to_eV = 1e9
eV_per_Joule = 6.242e18
m_to_fm = 1e15

# ============================================================================
# CONFORMAL FACTOR Ω(z)
# ============================================================================

def Omega(z):
    """
    Conformal factor evolution in radiation-dominated era.

    ASSUMPTION: Ω(z) ~ (1+z)^(3/4) for z >> z_eq (matter-radiation equality)

    Source: preprint.tex lines 1800-1832

    CAVEAT: This is an APPROXIMATION valid only for radiation era!
    For z < z_eq ~ 3400, need full ΛCDM calculation.

    Args:
        z: Redshift

    Returns:
        Ω(z) conformal factor (dimensionless)
    """
    z_eq = 3400  # Matter-radiation equality (approximate)

    if z > z_eq:
        # Radiation era: Ω ~ (1+z)^(3/4)
        return (1.0 + z)**(3.0/4.0)
    else:
        # Matter era: different scaling (not implemented rigorously here)
        # Use radiation era formula at z_eq, then scale differently
        Omega_eq = (1.0 + z_eq)**(3.0/4.0)
        # PLACEHOLDER: Need proper ΛCDM calculation here!
        return Omega_eq * ((1.0 + z) / (1.0 + z_eq))**(1.0/2.0)


# ============================================================================
# SATURATION REDSHIFT z_sat
# ============================================================================

def calculate_z_sat():
    """
    Calculate saturation redshift where E_pair reaches UV cutoff.

    ASSUMPTION: E_pair^(conf) ~ Ω²(z) × E_pair(0)

    Saturation: E_pair^(conf)(z_sat) = E_pair^(max)

    where E_pair^(max) ~ Λ_QCT² / m_p (dimensional analysis)

    Returns:
        z_sat: Saturation redshift
        E_max: Maximum E_pair (eV)
    """
    # Maximum E_pair from UV cutoff (dimensional analysis)
    # E_pair ~ Λ² / m → units: (energy)² / energy = energy ✓
    E_max = Lambda_QCT_eV**2 / m_p_eV

    # Solve: Ω²(z_sat) × E_pair(0) = E_max
    # Ω(z_sat) = sqrt(E_max / E_pair(0))
    Omega_sat = np.sqrt(E_max / E_pair_0_eV)

    # Invert Ω(z) ~ (1+z)^(3/4) to get z
    # Ω = (1+z)^(3/4)
    # z = Ω^(4/3) - 1
    z_sat = Omega_sat**(4.0/3.0) - 1.0

    return z_sat, E_max


# ============================================================================
# E_PAIR EVOLUTION WITH SATURATION
# ============================================================================

def f_turnon(z, z_start=z_start, k=k_turnon):
    """
    Turn-on function (same as before).

    f(z, z_start) = 1 / [1 + exp(-k × ln((1+z)/(1+z_start)))]
    """
    arg = -k * np.log((1.0 + z) / (1.0 + z_start))
    arg = np.clip(arg, -700, 700)
    return 1.0 / (1.0 + np.exp(arg))


def E_pair_conformal(z):
    """
    E_pair in conformal regime (NO saturation).

    Formula: E_pair^(conf)(z) = Ω²(z) × E_pair(0)

    ASSUMPTION: Valid in radiation era with conformal scaling.

    Args:
        z: Redshift

    Returns:
        E_pair (eV) in conformal regime
    """
    return Omega(z)**2 * E_pair_0_eV


def E_pair_logarithmic(z):
    """
    E_pair in logarithmic regime (NO saturation).

    Formula: E_pair^(log)(z) = E_0 + κ × f_turnon(z) × ln(1+z)

    This is the "standard" QCT formula from manuscript.

    Args:
        z: Redshift

    Returns:
        E_pair (eV) in logarithmic regime
    """
    if z >= z_start:
        return E_0_eV
    else:
        return E_0_eV + kappa_conf_eV * f_turnon(z) * np.log(1.0 + z)


def E_pair_saturated(z, z_sat, E_max):
    """
    E_pair with SATURATION implemented.

    REGIME SELECTION:
    1. z >= z_start: E_pair = E_0 (no condensate)
    2. z_sat <= z < z_start: E_pair = min(E_conf, E_max) (saturation)
    3. z < z_sat: E_pair = E_log (logarithmic, post-saturation)

    ASSUMPTION: Transition from conformal to logarithmic at z_sat.

    CAVEAT: Exact transition mechanism is NOT derived rigorously!

    Args:
        z: Redshift
        z_sat: Saturation redshift
        E_max: Maximum E_pair (UV cutoff)

    Returns:
        E_pair (eV) with saturation
    """
    if z >= z_start:
        # No condensate yet
        return E_0_eV

    elif z >= z_sat:
        # Conformal regime with saturation
        E_conf = E_pair_conformal(z)
        return min(E_conf, E_max)

    else:
        # Logarithmic regime (today's era)
        return E_pair_logarithmic(z)


# ============================================================================
# DARK ENERGY CALCULATION
# ============================================================================

def calculate_excess_energy(z, z_sat, E_max):
    """
    Calculate "saved" energy at redshift z due to saturation.

    ΔE(z) = E_pair^(conf)(z) - E_pair^(saturated)(z)

    This is the energy that "would have gone" into E_pair
    but instead becomes dark energy.

    ASSUMPTION: This excess energy is released with w = -1.

    Args:
        z: Redshift
        z_sat: Saturation redshift
        E_max: Maximum E_pair

    Returns:
        ΔE (eV) excess energy per neutrino pair
    """
    E_conf = E_pair_conformal(z)
    E_sat = E_pair_saturated(z, z_sat, E_max)

    # Excess energy (only positive if E_conf > E_sat)
    Delta_E = max(0.0, E_conf - E_sat)

    return Delta_E


def calculate_dark_energy_density(z_trans, z_sat, E_max):
    """
    Calculate dark energy density from saturation.

    HYPOTHESIS: Energy released at topological transition (z ~ z_trans)
    becomes dark energy with w = -1.

    ρ_DE = n_ν(z_trans) × ΔE(z_trans) × suppression_factors

    SUPPRESSION FACTORS (from manuscript lines 2102-2162):
    1. Coherence: f_c ~ m_ν / m_p ~ 10^-10
    2. Hubble time: f_time ~ (needs careful calculation!)
    3. Other geometric factors

    CAVEAT: Triple suppression mechanism NOT rigorously derived here!
    Using ORDER OF MAGNITUDE estimates only.

    Args:
        z_trans: Transition redshift (where energy is released)
        z_sat: Saturation redshift
        E_max: Maximum E_pair

    Returns:
        rho_DE (eV⁴) dark energy density
        rho_DE_GeV4 (GeV⁴) for comparison with observations
    """
    # Neutrino density at transition
    n_nu_trans = n_nu_0_SI * (1.0 + z_trans)**3  # m^-3

    # Excess energy per pair
    Delta_E = calculate_excess_energy(z_trans, z_sat, E_max)

    # Raw energy density (before suppression)
    # Units: m^-3 × eV = eV/m³
    rho_raw_eV_per_m3 = n_nu_trans * Delta_E

    # Convert to eV⁴ (natural units)
    # 1 eV/m³ = (1 eV) / (ℏc/eV)³ = eV⁴ / (ℏc)³
    hbar_c_eV_m = hbar_eV_s * c  # eV·m
    rho_raw_eV4 = rho_raw_eV_per_m3 / (hbar_c_eV_m)**3

    # SUPPRESSION FACTORS (ORDER OF MAGNITUDE ONLY!)

    # (1) Coherence fraction
    f_coherence = m_nu_eV / m_p_eV  # ~ 10^-10

    # (2) Hubble time factor (PLACEHOLDER - needs proper calculation!)
    # From docs: f_time ~ 2.1×10^33 but that's a HUGE factor
    # This needs rigorous derivation!
    f_time = 1.0  # PLACEHOLDER: Setting to 1 for now, NEEDS REVIEW

    # (3) Other factors (PLACEHOLDER)
    f_other = 1.0  # PLACEHOLDER

    # Total suppression
    suppression = f_coherence * f_time * f_other

    # Final dark energy density
    rho_DE_eV4 = rho_raw_eV4 * suppression
    rho_DE_GeV4 = rho_DE_eV4 / GeV_to_eV**4

    # Store intermediate values for inspection
    results = {
        'z_trans': z_trans,
        'n_nu_trans_per_m3': n_nu_trans,
        'Delta_E_eV': Delta_E,
        'rho_raw_eV4': rho_raw_eV4,
        'rho_raw_GeV4': rho_raw_eV4 / GeV_to_eV**4,
        'f_coherence': f_coherence,
        'f_time': f_time,
        'f_other': f_other,
        'suppression_total': suppression,
        'rho_DE_eV4': rho_DE_eV4,
        'rho_DE_GeV4': rho_DE_GeV4,
        'rho_observed_GeV4': 1e-47,  # Observed value
        'ratio_to_observed': rho_DE_GeV4 / 1e-47
    }

    return rho_DE_eV4, rho_DE_GeV4, results


# ============================================================================
# MAIN CALCULATION
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("QCT DARK ENERGY FROM E_PAIR SATURATION")
    print("="*70 + "\n")

    print("WARNING: This is a HYPOTHESIS TEST, not a rigorous derivation!")
    print("Several suppression factors use PLACEHOLDER values.\n")

    # Step 1: Calculate saturation redshift
    print("STEP 1: Calculate Saturation Redshift")
    print("-" * 70)
    z_sat, E_max = calculate_z_sat()
    print(f"UV cutoff: Λ_QCT = {Lambda_QCT_eV/1e12:.0f} TeV")
    print(f"Maximum E_pair: E_max = {E_max:.3e} eV")
    print(f"Saturation redshift: z_sat = {z_sat:.3e}")
    print(f"Conformal factor at saturation: Ω(z_sat) = {Omega(z_sat):.3e}\n")

    # Step 2: Calculate E_pair at key redshifts
    print("STEP 2: E_pair at Key Redshifts")
    print("-" * 70)

    z_values = [0, 1000, 1e6, 1e8, 1e9]
    print(f"{'z':<12} {'E_conf (eV)':<15} {'E_log (eV)':<15} {'E_sat (eV)':<15} {'ΔE (eV)':<15}")
    print("-" * 70)

    for z in z_values:
        E_conf = E_pair_conformal(z)
        E_log = E_pair_logarithmic(z)
        E_sat_val = E_pair_saturated(z, z_sat, E_max)
        Delta_E = calculate_excess_energy(z, z_sat, E_max)
        print(f"{z:<12.0e} {E_conf:<15.3e} {E_log:<15.3e} {E_sat_val:<15.3e} {Delta_E:<15.3e}")

    print()

    # Step 3: Calculate dark energy density
    print("STEP 3: Dark Energy Density Calculation")
    print("-" * 70)

    # Assume transition happens at saturation
    z_trans = z_sat

    rho_DE_eV4, rho_DE_GeV4, results = calculate_dark_energy_density(
        z_trans, z_sat, E_max
    )

    print(f"Transition redshift: z_trans = {results['z_trans']:.3e}")
    print(f"Neutrino density at transition: n_ν = {results['n_nu_trans_per_m3']:.3e} m^-3")
    print(f"Excess energy per pair: ΔE = {results['Delta_E_eV']:.3e} eV")
    print()
    print(f"Raw energy density: ρ_raw = {results['rho_raw_GeV4']:.3e} GeV⁴")
    print()
    print("Suppression factors:")
    print(f"  f_coherence (m_ν/m_p) = {results['f_coherence']:.3e}")
    print(f"  f_time (PLACEHOLDER!) = {results['f_time']:.3e}")
    print(f"  f_other (PLACEHOLDER!) = {results['f_other']:.3e}")
    print(f"  Total suppression = {results['suppression_total']:.3e}")
    print()
    print(f"RESULT: ρ_DE = {results['rho_DE_GeV4']:.3e} GeV⁴")
    print(f"OBSERVED: ρ_Λ = {results['rho_observed_GeV4']:.3e} GeV⁴")
    print(f"RATIO: ρ_DE / ρ_Λ = {results['ratio_to_observed']:.3e}")
    print()

    # Interpretation
    print("="*70)
    print("INTERPRETATION")
    print("="*70)

    if results['ratio_to_observed'] > 1e10:
        print(f"⚠️  RESULT TOO LARGE by factor {results['ratio_to_observed']:.1e}")
        print("    → Need MUCH stronger suppression factors!")
        print("    → f_time and/or f_other must provide ~10^{:.0f} suppression".format(
            np.log10(results['ratio_to_observed'])))
    elif results['ratio_to_observed'] > 10:
        print(f"⚠️  RESULT TOO LARGE by factor {results['ratio_to_observed']:.1e}")
        print("    → Need additional suppression")
    elif results['ratio_to_observed'] > 0.1:
        print(f"✓  RESULT WITHIN ORDER OF MAGNITUDE!")
        print(f"    Ratio: {results['ratio_to_observed']:.2f}")
        print("    → Promising! Fine-tuning suppression factors could work")
    else:
        print(f"⚠️  RESULT TOO SMALL by factor {1/results['ratio_to_observed']:.1e}")
        print("    → Suppression too strong, or z_trans wrong?")

    print()
    print("="*70)
    print("CAVEATS & NEXT STEPS")
    print("="*70)
    print("1. f_time factor is PLACEHOLDER (needs rigorous calculation)")
    print("2. Transition redshift z_trans = z_sat is ASSUMED (not derived)")
    print("3. w = -1 for released energy is ASSUMED (needs justification)")
    print("4. Conformal scaling Ω(z) uses approximate form")
    print("5. Triple suppression mechanism needs microscopic derivation")
    print()
    print("RECOMMENDATION: Treat this as ORDER OF MAGNITUDE estimate only!")
    print("="*70 + "\n")
