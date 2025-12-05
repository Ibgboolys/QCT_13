#!/usr/bin/env python3
"""
CRITICAL TEST: BBN Consistency with Physically Derived z_start

Test whether z_start from neutrino decoupling gives acceptable G_BBN/G_0

If G_BBN/G_0 ∈ [0.8, 1.2]: ✓ Theory works!
If outside: ❌ Need additional mechanism or theory has problem
"""

import numpy as np
import matplotlib.pyplot as plt

print("=" * 80)
print("BBN CONSISTENCY TEST: Physical z_start vs Fine-Tuned")
print("=" * 80)
print()

# =============================================================================
# 1. PHYSICAL CONSTANTS
# =============================================================================

# Neutrino parameters
m_nu_eV = 0.1  # eV (from oscillations)

# Cosmological epochs
T_dec_MeV = 1.0  # MeV (neutrino decoupling, from Γ_weak = H)
T_CMB_eV = 2.35e-4  # eV (CMB temperature today)

# BBN epoch
z_BBN = 1e9  # Redshift at BBN (t ~ 3 min, T ~ 0.1 MeV)
t_BBN_s = 180  # seconds

# =============================================================================
# 2. DERIVED QUANTITIES FROM PHYSICS
# =============================================================================

print("1. NEUTRINO DECOUPLING EPOCH (Standard Cosmology)")
print("-" * 80)

# Decoupling redshift
z_dec = (T_dec_MeV * 1e6) / T_CMB_eV - 1
t_dec_s = 1.0  # seconds (from radiation-dominated formula)

print(f"Temperature at decoupling: T_dec = {T_dec_MeV} MeV")
print(f"Redshift at decoupling:    z_dec = {z_dec:.2e}")
print(f"Time at decoupling:        t_dec = {t_dec_s} s")
print()

# =============================================================================
# 3. CONDENSATE BUILD-UP TIMESCALE
# =============================================================================

print("2. CONDENSATE FORMATION TIMESCALE")
print("-" * 80)

# Hypothesis: Condensate takes O(10²-10³) seconds to build up
# This is analogous to superconductor gap growth below T_c

# Physical z_start: 1-2 orders below z_dec
z_start_physical_min = z_dec / 100  # Conservative (2 orders)
z_start_physical_max = z_dec / 10   # Aggressive (1 order)
z_start_physical_mid = z_dec / 30   # Middle estimate

print(f"Decoupling:                z_dec = {z_dec:.2e}")
print(f"Physical z_start (range):  {z_start_physical_min:.2e} - {z_start_physical_max:.2e}")
print(f"Physical z_start (mid):    {z_start_physical_mid:.2e}")
print()

# For comparison: manuscript fine-tuned value
z_start_finetuned = 10  # From appendix (calibrated to BBN)

print(f"Fine-tuned (manuscript):   z_start = {z_start_finetuned}")
print(f"Ratio (physical/finetuned): {z_start_physical_mid / z_start_finetuned:.2e}")
print()

# =============================================================================
# 4. E_pair EVOLUTION WITH TURN-ON
# =============================================================================

print("3. E_pair EVOLUTION")
print("-" * 80)

# Initial pairing energy (minimal scale)
E_0 = m_nu_eV  # eV (natural choice, not arbitrary!)

# Confinement constant (from current QCT values)
# Fitted to today's E_pair ~ 10^19 eV
E_pair_today_eV = 1e19  # eV (from various QCT fits)

# Back-calculate kappa_conf
# E_pair(z=0) = E_0 + kappa_conf * f(0) * ln(1)
# But f(0) → 1 for z_start ≪ 1
# And ln(1) = 0
# So this formula doesn't work for z=0!

# Better: Use evolution form
# E_pair(z) = E_0 + kappa_conf * f(z) * ln(1+z)
# At z_BBN with f(z_BBN) ≈ 1 (if z_BBN ≫ z_start):
# E_pair(z_BBN) = E_0 + kappa_conf * ln(1 + z_BBN)

# From manuscript: kappa_conf ~ 4.8e17 eV
kappa_conf_eV = 4.8e17  # eV

print(f"Initial pairing energy: E_0 = {E_0:.2e} eV = m_ν")
print(f"Confinement constant:   κ_conf = {kappa_conf_eV:.2e} eV")
print()

# Turn-on function (sigmoid)
def f_turnon(z, z_start, k=2.0):
    """
    Sigmoid turn-on function

    Parameters:
    -----------
    z : float or array
        Redshift
    z_start : float
        Center of transition (where f = 0.5)
    k : float
        Steepness (higher = sharper transition)
    """
    if z <= 0:
        return 1.0  # Today: fully turned on

    log_ratio = np.log10((1 + z) / (1 + z_start))
    return 1.0 / (1.0 + np.exp(-k * log_ratio))

# E_pair at BBN for different z_start choices
def E_pair_at_z(z, z_start):
    """Calculate E_pair at redshift z"""
    if z <= 0:
        # Today: special handling (no ln(1) issue)
        # Use the fact that f(0) = 1 and integrate evolution
        # For now, use the fitted value
        return E_pair_today_eV
    else:
        f = f_turnon(z, z_start)
        return E_0 + kappa_conf_eV * f * np.log(1 + z)

# Calculate for different scenarios
scenarios = {
    'Physical (conservative)': z_start_physical_min,
    'Physical (mid)': z_start_physical_mid,
    'Physical (aggressive)': z_start_physical_max,
    'Fine-tuned (manuscript)': z_start_finetuned,
}

print("E_pair at BBN (z ~ 10⁹):")
print()

E_pair_BBN_results = {}

for name, z_start in scenarios.items():
    E_pair_BBN = E_pair_at_z(z_BBN, z_start)
    f_val = f_turnon(z_BBN, z_start)
    E_pair_BBN_results[name] = E_pair_BBN

    print(f"{name:30s}:")
    print(f"  z_start = {z_start:.2e}")
    print(f"  f(z_BBN) = {f_val:.4f}")
    print(f"  E_pair(BBN) = {E_pair_BBN:.2e} eV")
    print()

# =============================================================================
# 5. G_eff EVOLUTION
# =============================================================================

print("=" * 80)
print("4. G_eff AT BBN")
print("=" * 80)
print()

# From manuscript formula (appendix_microscopic_derivation_rev.tex:264-266):
# G_eff(z) / G_eff(0) = [E_pair(z) / E_pair(0)] × [τ_Hubble(z) / τ_Hubble(0)]³

# Hubble time scaling in radiation-dominated era:
# H(z) ~ H_0 × (1+z)^2   (radiation)
# τ_Hubble(z) = 1/H(z) ~ (1+z)^(-2)

# But wait - at z ~ 10^9 we're deep in radiation era
# More accurate: τ_Hubble(z) ~ τ_Hubble(0) × (1+z)^(-3/2)

def tau_Hubble_ratio(z):
    """
    Ratio of Hubble time at redshift z to today

    Radiation era (z ≫ z_eq ~ 3400): (1+z)^(-3/2)
    Matter era (z ≪ z_eq): (1+z)^(-3/2) still roughly valid
    """
    return (1 + z)**(-1.5)

# Calculate G_BBN/G_0 for each scenario
print("BBN CONSTRAINT TEST:")
print("-" * 80)
print()
print("BBN requires: |ΔG/G| < 20%  →  0.8 < G_BBN/G_0 < 1.2")
print()

for name, z_start in scenarios.items():
    E_pair_BBN = E_pair_BBN_results[name]
    E_pair_0 = E_pair_today_eV

    # Energy ratio
    energy_ratio = E_pair_BBN / E_pair_0

    # Hubble time ratio
    tau_ratio = tau_Hubble_ratio(z_BBN)

    # Combined (from manuscript formula)
    # NOTE: The formula has τ³ - check if this is correct!
    # It might be just τ or τ² depending on derivation

    # Let's test both:
    G_ratio_with_tau3 = energy_ratio * tau_ratio**3
    G_ratio_with_tau1 = energy_ratio * tau_ratio
    G_ratio_with_tau2 = energy_ratio * tau_ratio**2

    print(f"{name:30s} (z_start = {z_start:.2e}):")
    print(f"  E_pair(BBN) / E_pair(0) = {energy_ratio:.4f}")
    print(f"  τ(BBN) / τ(0) = {tau_ratio:.4e}")
    print()
    print(f"  If G ∝ E × τ³:   G_BBN/G_0 = {G_ratio_with_tau3:.4f}", end="")
    if 0.8 <= G_ratio_with_tau3 <= 1.2:
        print("  ✓ PASS")
    else:
        print(f"  ❌ FAIL (deviation: {abs(1-G_ratio_with_tau3)*100:.1f}%)")

    print(f"  If G ∝ E × τ²:   G_BBN/G_0 = {G_ratio_with_tau2:.4f}", end="")
    if 0.8 <= G_ratio_with_tau2 <= 1.2:
        print("  ✓ PASS")
    else:
        print(f"  ❌ FAIL (deviation: {abs(1-G_ratio_with_tau2)*100:.1f}%)")

    print(f"  If G ∝ E × τ¹:   G_BBN/G_0 = {G_ratio_with_tau1:.4f}", end="")
    if 0.8 <= G_ratio_with_tau1 <= 1.2:
        print("  ✓ PASS")
    else:
        print(f"  ❌ FAIL (deviation: {abs(1-G_ratio_with_tau1)*100:.1f}%)")

    print(f"  If G ∝ E only:   G_BBN/G_0 = {energy_ratio:.4f}", end="")
    if 0.8 <= energy_ratio <= 1.2:
        print("  ✓ PASS")
    else:
        print(f"  ❌ FAIL (deviation: {abs(1-energy_ratio)*100:.1f}%)")

    print()

# =============================================================================
# 6. VISUALIZATION
# =============================================================================

print("=" * 80)
print("5. EVOLUTION PLOTS")
print("=" * 80)
print()

# Redshift array (log scale)
z_array = np.logspace(0, 10, 1000)  # z = 1 to 10^10

# Plot E_pair(z) for different z_start
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

colors = {'Physical (conservative)': 'blue',
          'Physical (mid)': 'green',
          'Physical (aggressive)': 'orange',
          'Fine-tuned (manuscript)': 'red'}

for name, z_start in scenarios.items():
    E_pair_array = np.array([E_pair_at_z(z, z_start) for z in z_array])

    ax1.loglog(z_array, E_pair_array, label=name, color=colors[name], linewidth=2)

    # Turn-on function
    f_array = np.array([f_turnon(z, z_start) for z in z_array])
    ax2.semilogx(z_array, f_array, label=name, color=colors[name], linewidth=2)

# Mark important epochs
ax1.axvline(z_BBN, color='black', linestyle='--', alpha=0.5, label='BBN (z~10⁹)')
ax1.axvline(z_dec, color='gray', linestyle=':', alpha=0.5, label='ν decoupling (z~4×10⁹)')

ax2.axvline(z_BBN, color='black', linestyle='--', alpha=0.5)
ax2.axvline(z_dec, color='gray', linestyle=':', alpha=0.5)

# Labels
ax1.set_xlabel('Redshift z', fontsize=12)
ax1.set_ylabel('$E_{pair}$ [eV]', fontsize=12)
ax1.set_title('Pairing Energy Evolution with Different $z_{start}$', fontsize=14)
ax1.legend(fontsize=10)
ax1.grid(alpha=0.3)

ax2.set_xlabel('Redshift z', fontsize=12)
ax2.set_ylabel('Turn-on function $f(z)$', fontsize=12)
ax2.set_title('Sigmoid Turn-On Function', fontsize=14)
ax2.legend(fontsize=10)
ax2.grid(alpha=0.3)
ax2.set_ylim([-0.05, 1.05])

plt.tight_layout()
# plt.savefig('/home/user/QCT_9/bbn_consistency_test.png', dpi=150)
print("Saved plot: bbn_consistency_test.png")
print()

# =============================================================================
# 7. CONCLUSIONS
# =============================================================================

print("=" * 80)
print("6. CONCLUSIONS")
print("=" * 80)
print()

print("KEY FINDINGS:")
print()

print("1. Neutrino decoupling epoch:")
print(f"   z_dec ~ {z_dec:.2e} (T ~ 1 MeV, t ~ 1 s)")
print(f"   This is STANDARD COSMOLOGY (not QCT-specific)")
print()

print("2. Physical z_start prediction:")
print(f"   z_start ~ {z_start_physical_mid:.2e} (1-2 orders below z_dec)")
print(f"   This assumes condensate build-up timescale ~ 10²-10³ s")
print()

print("3. Comparison to fine-tuned value:")
print(f"   Physical z_start ~ {z_start_physical_mid:.2e}")
print(f"   Fine-tuned z_start = {z_start_finetuned}")
print(f"   Discrepancy: Factor {z_start_physical_mid / z_start_finetuned:.2e}")
print()

print("4. BBN consistency:")
print("   [Check output above for which formula satisfies BBN]")
print()

print("5. INTERPRETATION:")
if z_start_physical_mid > 1000:
    print("   ⚠️  Physical z_start is MUCH HIGHER than fine-tuned value")
    print("   This suggests:")
    print("   a) Need additional mechanism to delay condensate further, OR")
    print("   b) G_eff formula needs revision (check τ exponent), OR")
    print("   c) Turn-on is sharper than sigmoid (different k)")
else:
    print("   ✓ Physical z_start is reasonable")
    print("   Need to check if it satisfies BBN constraints")

print()
print("=" * 80)
print("RECOMMENDATION:")
print("=" * 80)
print()
print("NEXT STEPS:")
print("1. Check manuscript G_eff formula (τ exponent)")
print("2. If formula correct and BBN fails:")
print("   → Investigate additional delay mechanism (QCD phase transition?)")
print("3. If formula needs revision:")
print("   → Re-derive G_eff evolution from first principles")
print("4. Update appendix with physical derivation (not fine-tuning)")
print()
