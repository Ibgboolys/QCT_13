#!/usr/bin/env python3
"""
RIGOROUS CALCULATION: Dark Energy from E_pair Saturation
=========================================================

Calculates ρ_Λ (dark energy density) from the difference between:
- Conformal/geometric E_pair evolution (naive, no saturation)
- Logarithmic E_pair evolution (actual, with saturation)

The "missing energy" is hypothesized to become dark energy through
a topological phase transition at z_sat ~ 10^6.

Author: AI Assistant (QCT Project)
Date: 2025-11-15
"""

import numpy as np
from scipy.integrate import quad
from scipy.constants import eV, c, hbar

# ============================================================================
# FUNDAMENTAL CONSTANTS
# ============================================================================

# Physical constants
m_nu = 0.1 * eV  # Neutrino mass [J] (assumed, Σm_ν < 0.12 eV from Planck)
m_p = 938.27e6 * eV  # Proton mass [J]
n_nu_today = 336e6  # Neutrino number density today [m^-3] (CνB)

# Conversion factors
eV_to_GeV = 1e-9
GeV4_to_eVm3 = (1e9)**3 * 1e-45  # Rough conversion (ℏc)^3

# QCT Parameters (from manuscript)
E_pair_today = 1.8e19 * eV  # Today's E_pair value [J]
kappa_conf = 0.48e18 * eV  # Confinement constant κ_conf [J] = 0.48 EeV
Lambda_QCT_today = 107e12 * eV  # QCT cutoff today [J] = 107 TeV

# Redshift ranges
z_today = 0
z_BBN = 1e9  # Big Bang Nucleosynthesis
z_CMB = 1100  # CMB recombination
z_sat = 1e6  # Saturation epoch (hypothesis)
z_EW = 1e15  # Electroweak scale

# Observed dark energy density
rho_Lambda_obs = 1e-47 * (1e9)**4  # GeV^4 → (eV)^4 [very rough!]

print("="*70)
print("DARK ENERGY FROM E_PAIR SATURATION - RIGOROUS CALCULATION")
print("="*70)
print()

# ============================================================================
# STEP 1: DEFINE E_PAIR EVOLUTION FORMS
# ============================================================================

def E_pair_logarithmic(z):
    """
    Logarithmic evolution (phenomenological fit, manuscript Eq. 1499):
    E_pair(z) = E_0 + κ_conf × ln(1+z)

    We calibrate E_0 such that E_pair(z=0) = E_pair_today.
    """
    E_0 = E_pair_today  # Simplified: E_pair(0) = E_0 (κ_conf×ln(1) = 0)
    return E_0 + kappa_conf * np.log(1 + z)

def Omega_conformal(z):
    """
    Conformal factor Ω(z) in radiation era (manuscript lines 1762-1764):
    Ω(z) ~ (1+z)^(3/4)

    This comes from:
    Φ_cosmo(z) ~ -(1+z)^(3/2) (gravitational potential in radiation era)
    K(z) ~ 1 + α × Φ_cosmo ~ 1 + α × (1+z)^(3/2)
    Ω(z) ~ √K ~ (1+z)^(3/4)
    """
    return (1 + z)**(3.0/4.0)

def Lambda_QCT_conformal(z):
    """
    Conformal evolution of Λ_QCT (manuscript line 1732):
    Λ_QCT(z) = Ω(z) × Λ_QCT(0)
    """
    return Omega_conformal(z) * Lambda_QCT_today

def E_pair_conformal(z):
    """
    Conformal/geometric evolution (manuscript Eq. 1522 + 1798):
    Λ_QCT(z) = (3/2) × √[E_pair(z) × m_p]

    Solving for E_pair:
    E_pair(z) = (4/9) × Λ_QCT²(z) / m_p
    """
    Lambda_z = Lambda_QCT_conformal(z)
    return (4.0/9.0) * Lambda_z**2 / m_p

# ============================================================================
# STEP 2: CALCULATE ENERGY DIFFERENCE
# ============================================================================

def Delta_E_pair(z):
    """
    Energy difference (conformal - logarithmic):
    ΔE_pair(z) = E_pair^(conf)(z) - E_pair^(log)(z)

    This is the "missing energy" that doesn't go into E_pair growth
    due to saturation mechanism.
    """
    return E_pair_conformal(z) - E_pair_logarithmic(z)

print("STEP 1: E_pair Evolution Forms")
print("-" * 70)

# Test at key redshifts
test_redshifts = [0, z_CMB, z_sat, z_EW]
print(f"{'z':<12} {'E_log [eV]':<15} {'E_conf [eV]':<15} {'ΔE [eV]':<15}")
print("-" * 70)
for z in test_redshifts:
    E_log = E_pair_logarithmic(z) / eV
    E_conf = E_pair_conformal(z) / eV
    Delta_E = Delta_E_pair(z) / eV
    print(f"{z:<12.2e} {E_log:<15.3e} {E_conf:<15.3e} {Delta_E:<15.3e}")

print()
print(f"Discrepancy at z_EW: {E_pair_conformal(z_EW)/E_pair_logarithmic(z_EW):.2e}")
print()

# ============================================================================
# STEP 3: ENERGY DENSITY FROM SATURATION
# ============================================================================

def n_nu(z):
    """
    Neutrino number density scales as (1+z)³ (matter conservation):
    n_ν(z) = n_ν(today) × (1+z)³
    """
    return n_nu_today * (1 + z)**3

def rho_saturation_density(z):
    """
    Energy density from saturation at redshift z:
    ρ_sat(z) = n_ν(z) × ΔE_pair(z)

    Units: [m^-3] × [J] = [J/m³]
    """
    return n_nu(z) * Delta_E_pair(z)

print("STEP 2: Energy Density from Saturation")
print("-" * 70)

rho_sat_z_sat = rho_saturation_density(z_sat)
print(f"At z_sat = {z_sat:.0e}:")
print(f"  n_ν(z_sat) = {n_nu(z_sat):.3e} m^-3")
print(f"  ΔE_pair(z_sat) = {Delta_E_pair(z_sat)/eV:.3e} eV")
print(f"  ρ_sat(z_sat) = {rho_sat_z_sat/(eV*1e45):.3e} × 10^45 eV/m³")
print()

# ============================================================================
# STEP 4: INTEGRATED "SAVED" ENERGY
# ============================================================================

print("STEP 3: Integrated Energy from z_sat to z_EW")
print("-" * 70)

def integrand_energy_density(z):
    """
    Integrand for total saved energy density:

    dρ/dz = n_ν(z) × dΔE_pair/dz

    We integrate this over redshift to get total energy "saved" by saturation.
    """
    # Numerical derivative of ΔE_pair
    dz = z * 1e-6  # Small increment
    if z + dz > z_EW:
        return 0

    dDelta_E_dz = (Delta_E_pair(z + dz) - Delta_E_pair(z)) / dz
    return n_nu(z) * dDelta_E_dz

# Integrate energy density production from z_sat to z_EW
# NOTE: This gives TOTAL energy, not accounting for redshift dilution yet!

# For numerical stability, we'll use a different approach:
# Total energy "created" at each z, weighted by volume element

def integrand_comoving_energy(z):
    """
    Energy per comoving volume element.

    For w=-1 (cosmological constant), energy density is CONSTANT.
    So we need to find at which epoch the energy "freezes".

    Hypothesis: Energy freezes at z_trans, then remains constant to today.
    """
    return rho_saturation_density(z)

# Quick estimate: What is ρ_sat at different epochs?
print("Energy density at different epochs:")
for z in [z_sat, 2*z_sat, 10*z_sat]:
    rho = rho_saturation_density(z) / (eV * 1e45)
    print(f"  z = {z:.2e}: ρ_sat = {rho:.3e} × 10^45 eV/m³")

print()

# ============================================================================
# STEP 5: REDSHIFT DILUTION AND EQUATION OF STATE
# ============================================================================

print("STEP 4: Redshift Dilution")
print("-" * 70)

# KEY QUESTION: How does saturation energy density evolve?

# Option A: Radiation-like (w = 1/3): ρ ~ (1+z)^4
# Option B: Matter-like (w = 0): ρ ~ (1+z)^3
# Option C: Dark energy (w = -1): ρ = constant

# Manuscript claims dark energy has w = -1.
# So IF saturation energy freezes at z_trans with w=-1,
# then ρ_Λ(today) = ρ_sat(z_trans) × (some fraction)

# We need to determine z_trans (transition epoch) and freezing fraction.

# HYPOTHESIS: Saturation transition occurs at z_sat ~ 10^6
# A small fraction f_freeze of this energy becomes dark energy with w=-1

def rho_Lambda_from_saturation(z_trans, f_freeze):
    """
    Dark energy density from saturation at z_trans.

    If energy freezes at z_trans with w=-1:
    ρ_Λ(today) = f_freeze × ρ_sat(z_trans)
    """
    return f_freeze * rho_saturation_density(z_trans)

# Solve for required f_freeze to match observations
# ρ_Λ(obs) ~ 10^-47 GeV^4 ~ X eV/m³

# Convert observed ρ_Λ to eV/m³ (approximately)
# 1 GeV^4 = (10^9 eV)^4 / (ℏc)^3 in eV/m³
# Very rough: 1 GeV^4 ~ 10^45 eV/m³ (order of magnitude)

rho_Lambda_obs_eVm3 = 1e-47 * 1e45  # Very rough conversion!
print(f"Observed ρ_Λ ~ 10^-47 GeV^4 ~ {rho_Lambda_obs_eVm3:.3e} eV/m³ (rough)")
print()

# Required freezing fraction
rho_sat_at_z_sat = rho_saturation_density(z_sat)
f_freeze_required = rho_Lambda_obs_eVm3 / (rho_sat_at_z_sat / eV)

print(f"At z_trans = z_sat = {z_sat:.0e}:")
print(f"  ρ_sat(z_sat) = {rho_sat_at_z_sat/eV:.3e} eV/m³")
print(f"  Required f_freeze = {f_freeze_required:.3e}")
print()

# ============================================================================
# STEP 6: TRIPLE SUPPRESSION MECHANISM
# ============================================================================

print("STEP 5: Triple Suppression Mechanism")
print("-" * 70)

# Manuscript claims (lines 2105-2151) three suppression factors:

# (A) Equation of state w = -1
#     This doesn't suppress density, but changes evolution
#     Factor: ~1 (not a suppression, just dynamics change)

# (B) Coherence fraction f_c ~ f_screen = m_ν / m_p ~ 10^-10
#     Only coherent fraction contributes
f_c = m_nu / m_p
print(f"(B) Coherence fraction f_c = m_ν/m_p = {f_c:.3e}")

# (C) Non-local averaging factor
#     Manuscript claims ~ (ξ / R_Hubble)^3 ~ 10^-39
#     Where ξ is correlation length
#
#     This is VERY uncertain and model-dependent!
#     For now, treat as free parameter.
f_avg = 1e-39  # Manuscript's claim (very uncertain!)
print(f"(C) Non-local averaging f_avg ~ {f_avg:.3e} (manuscript claim)")

# Combined suppression
f_total_suppression = f_c * f_avg
print(f"Total suppression (B×C) = {f_total_suppression:.3e}")
print()

# ============================================================================
# STEP 7: FINAL RESULT
# ============================================================================

print("="*70)
print("FINAL RESULT: Dark Energy Density")
print("="*70)

# Apply triple suppression to saturation density
rho_Lambda_predicted = f_total_suppression * rho_sat_at_z_sat

# Convert to GeV^4 (roughly)
rho_Lambda_predicted_GeV4 = rho_Lambda_predicted / eV / 1e45

print(f"Saturation density at z_sat = {z_sat:.0e}:")
print(f"  ρ_sat(z_sat) = {rho_sat_at_z_sat/eV:.3e} eV/m³")
print()
print(f"After triple suppression (f_c × f_avg):")
print(f"  f_c = {f_c:.3e}")
print(f"  f_avg = {f_avg:.3e} (manuscript, uncertain!)")
print(f"  Combined = {f_total_suppression:.3e}")
print()
print(f"PREDICTED ρ_Λ:")
print(f"  {rho_Lambda_predicted/eV:.3e} eV/m³")
print(f"  ~ {rho_Lambda_predicted_GeV4:.1e} GeV^4 (rough conversion)")
print()
print(f"OBSERVED ρ_Λ (Planck 2018):")
print(f"  ~ 1.0 × 10^-47 GeV^4")
print()

# Comparison
ratio = rho_Lambda_predicted_GeV4 / 1e-47
print(f"RATIO (predicted / observed) = {ratio:.2e}")
print()

# ============================================================================
# STEP 8: PARAMETER SPACE EXPLORATION
# ============================================================================

print("="*70)
print("PARAMETER SPACE: What f_freeze is needed?")
print("="*70)

# We have:
# ρ_Λ = f_freeze × f_c × f_avg × ρ_sat(z_trans)
#
# Observed ρ_Λ ~ 10^-47 GeV^4 ~ 10^-2 eV/m³ (rough)
# ρ_sat(z_sat) ~ 10^54 eV/m³
# f_c ~ 10^-10
# f_avg ~ 10^-39 (claimed, uncertain)
#
# Solving for f_freeze:

rho_Lambda_target = 1e-47 * 1e45  # GeV^4 to eV/m³ (rough)
f_freeze_needed = rho_Lambda_target / (f_c * f_avg * (rho_sat_at_z_sat / eV))

print(f"To match ρ_Λ ~ 10^-47 GeV^4:")
print(f"  With f_c = {f_c:.2e}, f_avg = {f_avg:.2e}")
print(f"  Required f_freeze = {f_freeze_needed:.3e}")
print()

# Alternative: What if f_avg is different?
print("Sensitivity to f_avg:")
for f_avg_test in [1e-35, 1e-37, 1e-39, 1e-41]:
    f_freeze_alt = rho_Lambda_target / (f_c * f_avg_test * (rho_sat_at_z_sat / eV))
    rho_pred_alt = f_freeze_alt * f_c * f_avg_test * (rho_sat_at_z_sat / eV)
    print(f"  f_avg = {f_avg_test:.0e} → f_freeze = {f_freeze_alt:.2e}, " +
          f"ρ_Λ = {rho_pred_alt/1e45:.1e}×10^45 eV/m³")

print()

# ============================================================================
# STEP 9: ALTERNATIVE CALCULATION - INTEGRATED ENERGY
# ============================================================================

print("="*70)
print("ALTERNATIVE: Total Integrated Saturation Energy")
print("="*70)

# Instead of density at one epoch, integrate total energy "saved"

# Energy saved per neutrino across cosmic history:
def energy_saved_per_neutrino():
    """
    Integrate ΔE_pair from z_sat to z_EW.

    E_saved = ∫[z_sat to z_EW] dΔE/dz dz
              = ΔE_pair(z_EW) - ΔE_pair(z_sat)
    """
    return Delta_E_pair(z_EW) - Delta_E_pair(z_sat)

E_saved = energy_saved_per_neutrino()
print(f"Energy saved per neutrino (z_sat → z_EW):")
print(f"  E_saved = {E_saved/eV:.3e} eV")
print()

# If this energy is released at z_sat and frozen with w=-1:
rho_from_integrated = n_nu(z_sat) * E_saved
rho_from_integrated_suppressed = f_c * f_avg * rho_from_integrated

print(f"If released at z_sat with n_ν(z_sat) = {n_nu(z_sat):.2e}:")
print(f"  ρ_release = {rho_from_integrated/eV:.3e} eV/m³")
print(f"  After suppression: {rho_from_integrated_suppressed/eV:.3e} eV/m³")
print(f"  ~ {(rho_from_integrated_suppressed/eV/1e45):.1e} GeV^4 (rough)")
print()

# ============================================================================
# SUMMARY
# ============================================================================

print("="*70)
print("SUMMARY")
print("="*70)
print()
print("E_pair saturation mechanism:")
print(f"  Conformal E_pair(z_EW) = {E_pair_conformal(z_EW)/eV:.2e} eV")
print(f"  Logarithmic E_pair(z_EW) = {E_pair_logarithmic(z_EW)/eV:.2e} eV")
print(f"  Discrepancy: factor {E_pair_conformal(z_EW)/E_pair_logarithmic(z_EW):.2e}")
print()
print("Saturation energy density at z_sat:")
print(f"  ρ_sat(z_sat={z_sat:.0e}) = {rho_sat_at_z_sat/eV:.3e} eV/m³")
print()
print("Triple suppression mechanism:")
print(f"  f_c (coherence) = {f_c:.3e}")
print(f"  f_avg (non-local) = {f_avg:.3e} [UNCERTAIN!]")
print(f"  f_freeze (topology) = {f_freeze_needed:.3e} [REQUIRED]")
print(f"  Total = {f_c * f_avg * f_freeze_needed:.3e}")
print()
print("Dark energy prediction:")
print(f"  ρ_Λ(predicted) ~ {rho_Lambda_predicted_GeV4:.1e} GeV^4")
print(f"  ρ_Λ(observed) ~ 1.0 × 10^-47 GeV^4")
print(f"  Ratio = {ratio:.2e}")
print()
print("CONCLUSION:")
if 0.1 < ratio < 10:
    print("  ✓ ORDER OF MAGNITUDE AGREEMENT!")
    print("  Mechanism is VIABLE with appropriate f_avg and f_freeze.")
elif 0.01 < ratio < 100:
    print("  ~ Within factor ~10-100")
    print("  Mechanism is PROMISING but needs refinement.")
else:
    print("  ✗ Off by more than 2 orders of magnitude")
    print("  Mechanism needs significant revision or f_avg/f_freeze tuning.")
print()
print("="*70)
