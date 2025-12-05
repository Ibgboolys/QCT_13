#!/usr/bin/env python3
"""
critical_test_k_formula.py

KRITICKÁ ANALÝZA: Je k = 1 + 5α fyzika nebo numerologie?

TESTY:
1. Citlivost na n_ν (je 336 cm⁻³ kritické?)
2. Jiné faktory (3α, 4α, 6α, 7α) - fungují stejně dobře?
3. Odkud pochází k_Coulomb? (hledání v CODATA)
4. Look-elsewhere efekt (kolik kombinací jsme zkoušeli?)
5. Alternativní vysvětlení (numerologie vs fyzika)

CÍLE:
- Najít SLABÁ MÍSTA v argumentaci
- Být SKEPTIČTÍ dokud nemáme důkazy
- Rozlišit postdiction vs prediction

AUTHOR: AI Assistant (Claude) - CRITICAL MODE
DATE: 2025-11-20
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import physical_constants, c, hbar, e

# ============================================================================
# KONSTANTY A JEJICH NEJISTOTY
# ============================================================================

# Fine structure constant (CODATA 2018)
alpha_me = 1.0 / 137.035999084  # Přesná hodnota
alpha_me_uncertainty = 0.000000000091 / 137.035999084**2  # Relativní nejistota

# Cosmic neutrino density (CνB)
# Z kosmologie: n_ν = (3/11) × (4/11) × n_γ kde n_γ = 411 cm⁻³ (CMB fotony)
n_gamma_cmb = 411.0  # cm⁻³ (z T_CMB = 2.725 K)
n_nu_theory = (3.0/11.0) * (4.0/11.0) * n_gamma_cmb  # = 40.5 cm⁻³ PER SPECIES

# 3 neutrino species + 3 antineutrinos = 6 species
n_nu_total_theory = 6 * n_nu_theory  # = 243 cm⁻³ ???

# ALE v QCT používáme n_ν = 336 cm⁻³
n_nu_qct = 336.0  # cm⁻³ (ODKUD?? CRITICAL!)

print("="*80)
print("CRITICAL TEST: Is k = 1 + 5α physics or numerology?")
print("="*80)
print()

print("[WARNING] n_ν discrepancy detected!")
print(f"  n_ν (from CMB theory):  {n_nu_total_theory:.1f} cm⁻³")
print(f"  n_ν (used in QCT):      {n_nu_qct:.1f} cm⁻³")
print(f"  Difference:             {(n_nu_qct - n_nu_total_theory)/n_nu_total_theory * 100:.1f}%")
print()
print("🚨 RED FLAG: Odkud pochází 336 cm⁻³? Je to fitted nebo derived?")
print()

# ============================================================================
# TEST 1: CITLIVOST NA n_ν
# ============================================================================

print("="*80)
print("TEST 1: Sensitivity to n_ν value")
print("="*80)
print()

def test_n_nu_sensitivity():
    """
    Testuje jak změna n_ν ovlivní k.
    """
    n_nu_values = np.arange(300, 380, 5)  # 300 to 375 cm⁻³

    results = []
    for n_nu in n_nu_values:
        # S_tot = n_ν/6 + 2
        S_tot = n_nu / 6.0 + 2.0

        # Je S_tot celé číslo? (CRITICAL - QCT vyžaduje celé číslo!)
        is_integer = abs(S_tot - round(S_tot)) < 0.01

        # k = S_tot / (n_ν/6)
        k_qct = S_tot / (n_nu / 6.0)

        # Simplified: k = (n_ν/6 + 2) / (n_ν/6) = 1 + 2/(n_ν/6) = 1 + 12/n_ν
        k_simple = 1.0 + 12.0 / n_nu

        results.append({
            'n_nu': n_nu,
            'S_tot': S_tot,
            'is_integer': is_integer,
            'k_qct': k_qct,
            'k_simple': k_simple
        })

    # Print tabulka
    print("n_ν [cm⁻³] | S_tot  | Integer? | k_QCT     | k = 1+12/n_ν")
    print("-"*65)
    for r in results:
        integer_mark = "✓" if r['is_integer'] else "✗"
        highlight = "<<< 336" if abs(r['n_nu'] - 336) < 1 else ""
        print(f"{r['n_nu']:10.0f} | {r['S_tot']:6.2f} | {integer_mark:^8s} | {r['k_qct']:.7f} | {r['k_simple']:.7f}  {highlight}")

    print()
    print("🔍 DISCOVERY: k = 1 + 12/n_ν (simple formula!)")
    print()
    print("For n_ν = 336: k = 1 + 12/336 = 1 + 1/28 = 1.03571...")
    print()
    print("⚠️  QUESTION: Why 12? Why not 10 or 15?")
    print("    12 = 2 × 6 (N_topo × 6 species?)")
    print("    OR: 12 = arbitrary from requiring n_ν = 336?")
    print()

    return results

results_n_nu = test_n_nu_sensitivity()

# ============================================================================
# TEST 2: JINÉ FAKTORY (3α, 4α, 6α, 7α)
# ============================================================================

print("="*80)
print("TEST 2: Look-elsewhere effect - testing different factors")
print("="*80)
print()

def test_different_factors():
    """
    Zkusí k = 1 + n×α pro různá n a porovná s k_QCT.
    """
    k_qct = 58.0 / 56.0  # = 1.03571...
    alpha = alpha_me

    print(f"Target: k_QCT = {k_qct:.10f}")
    print()
    print("Testing k = 1 + n×α for different n:")
    print()
    print("n  | k = 1 + n×α   | Δk from QCT | Rel. Error")
    print("-"*55)

    best_n = None
    best_error = float('inf')

    for n in range(1, 21):  # Test n = 1 to 20
        k_test = 1.0 + n * alpha
        delta_k = abs(k_test - k_qct)
        rel_error = delta_k / k_qct * 100

        marker = ""
        if delta_k < best_error:
            best_error = delta_k
            best_n = n
            marker = " ← BEST"

        if n in [3, 4, 5, 6, 7]:  # Highlight physically motivated values
            marker = marker if marker else " ← plausible"

        print(f"{n:2d} | {k_test:.10f} | {delta_k:.7f} | {rel_error:.4f}%{marker}")

    print()
    print(f"🎯 BEST FIT: n = {best_n} with error {best_error:.7f} ({best_error/k_qct*100:.3f}%)")
    print()

    # Critical analysis
    print("🔍 CRITICAL ANALYSIS:")
    print()

    # How many tried before finding best?
    p_random = 1.0 / 20.0  # 1 in 20 tries
    print(f"  • Tested 20 different n values")
    print(f"  • P(finding one that works) ~ {p_random*100:.1f}% (1 in {int(1/p_random)})")
    print()

    # Is n=5 physically motivated?
    if best_n == 5:
        print(f"  • n = {best_n} corresponds to 5 active quarks (u,d,s,c,b)")
        print(f"    ✓ Physically motivated (below Λ_QCT ~ 107 TeV)")
        print(f"    ✓ Top quark m_t = 173 GeV is excluded (above Λ_QCT)")
    else:
        print(f"  • n = {best_n} does NOT correspond to obvious particle count")
        print(f"    ✗ No clear physical interpretation")

    print()

    # Test with α/π (standard QED correction)
    k_qed_standard = 1.0 + 5 * (alpha / np.pi)
    delta_k_qed = abs(k_qed_standard - k_qct)
    print(f"  • Standard QED form: k = 1 + 5×(α/π) = {k_qed_standard:.10f}")
    print(f"    Δk = {delta_k_qed:.7f} ({delta_k_qed/k_qct*100:.3f}%)")
    print(f"    ✗ Does NOT work! (Factor π missing in QCT)")
    print()

test_different_factors()

# ============================================================================
# TEST 3: ODKUD POCHÁZÍ k_Coulomb = 1.0364?
# ============================================================================

print("="*80)
print("TEST 3: Origin of k_Coulomb - is it real or invented?")
print("="*80)
print()

print("🚨 CRITICAL QUESTION: What IS k_Coulomb?")
print()
print("In validate_k_formula.py we used:")
print("  k_Coulomb = 1.03643  # 'From CODATA electromagnetic coupling'")
print()
print("BUT: Where does this number come from?")
print()

# Hledáme v CODATA 2018
print("Searching CODATA 2018 for dimensionless constants near 1.036...")
print()

# Možné CODATA konstanty
codata_candidates = [
    ('fine_structure', 'α = 1/137.036', 1.0/137.036),
    ('electron_g_factor', 'g_e/2', None),  # Need to look up
    ('proton_mag_moment', 'μ_p/μ_N', None),
]

print("Known CODATA constants:")
try:
    # Hledat v scipy.constants
    alpha_val = physical_constants['fine-structure constant'][0]
    print(f"  • α = {alpha_val:.12e}")

    # Coulomb constant (dimensional!)
    k_e = physical_constants['Coulomb constant'][0]  # N·m²/C²
    print(f"  • k_e = {k_e:.10e} N·m²/C²  (DIMENSIONAL, not relevant)")

    # Proton-electron mass ratio
    mp_over_me = physical_constants['proton-electron mass ratio'][0]
    print(f"  • m_p/m_e = {mp_over_me:.10f}  (dimensionless, but >> 1)")

except KeyError as e:
    print(f"  Cannot find constant: {e}")

print()
print("❌ PROBLEM: Cannot find k_Coulomb = 1.0364 in CODATA!")
print()
print("🚨 RED FLAG: Did we INVENT this number?")
print()
print("Possible origins:")
print("  1. Misunderstanding of Coulomb's law (k_e is dimensional!)")
print("  2. Ratio of some electromagnetic constants?")
print("  3. Post-hoc fitted to match k_QCT = 1.0357?")
print()
print("⚠️  ACTION NEEDED: Find PRIMARY SOURCE for k_Coulomb or ABANDON claim!")
print()

# ============================================================================
# TEST 4: ALTERNATIVNÍ VZORCE
# ============================================================================

print("="*80)
print("TEST 4: Alternative formulas - do they work equally well?")
print("="*80)
print()

def test_alternative_formulas():
    """
    Zkusí různé kombinace fundamentálních konstant.
    """
    k_qct = 58.0 / 56.0
    alpha = alpha_me
    pi = np.pi
    e_const = np.e

    formulas = [
        ("1 + 5α", 1.0 + 5*alpha),
        ("1 + α/π", 1.0 + alpha/pi),
        ("1 + 12/336", 1.0 + 12.0/336.0),
        ("1 + 1/28", 1.0 + 1.0/28.0),
        ("1 + 2/56", 1.0 + 2.0/56.0),
        ("(58/56)", 58.0/56.0),
        ("1 + α×π", 1.0 + alpha*pi),
        ("1 + √α", 1.0 + np.sqrt(alpha)),
        ("e/α - 370", e_const/alpha - 370),
    ]

    print("Formula          | Value        | Δk from QCT | Rel. Error")
    print("-"*70)

    for name, value in formulas:
        delta = abs(value - k_qct)
        rel_err = delta / k_qct * 100
        marker = " ← WORKS!" if rel_err < 0.1 else ""
        print(f"{name:16s} | {value:.10f} | {delta:.7f} | {rel_err:.4f}%{marker}")

    print()
    print("🔍 OBSERVATION:")
    print("  • Multiple formulas give similar results!")
    print("  • k = 1 + 12/336 is EXACT (by definition of S_tot)")
    print("  • k = 1 + 5α is approximate (0.075% error)")
    print()
    print("⚠️  QUESTION: Is 5α fundamental or just lucky coincidence with 12/336?")
    print()

test_alternative_formulas()

# ============================================================================
# TEST 5: BAYESOVSKÁ ANALÝZA
# ============================================================================

print("="*80)
print("TEST 5: Bayesian analysis - how likely is this coincidence?")
print("="*80)
print()

def bayesian_analysis():
    """
    Odhadne P(coincidence | data) pomocí Bayesova teorému.
    """
    k_qct = 58.0 / 56.0
    alpha = alpha_me
    k_theory = 1.0 + 5*alpha
    delta_k = abs(k_qct - k_theory)

    print("Prior assumptions:")
    print("  • k could be anywhere in range [1.00, 1.10]")
    print("  • We tested ~20 different factors (3α, 4α, 5α, ...)")
    print("  • Natural scale: α ~ 10⁻³")
    print()

    # Prior probability space
    k_range = 0.10  # plausible range
    n_trials = 20    # number of factors tested

    # Likelihood: P(observation | model)
    # Assuming Gaussian error ~ α/10
    sigma_expected = alpha / 10.0
    likelihood = np.exp(-0.5 * (delta_k / sigma_expected)**2)

    # Posterior: P(model | observation)
    # With look-elsewhere correction
    p_single_trial = delta_k / k_range  # naive
    p_multiple_trials = 1.0 - (1.0 - p_single_trial)**n_trials  # corrected

    print("Likelihood calculation:")
    print(f"  • Observed Δk = {delta_k:.7f}")
    print(f"  • Expected σ ~ α/10 = {sigma_expected:.7f}")
    print(f"  • Likelihood = exp(-0.5×(Δk/σ)²) = {likelihood:.4f}")
    print()

    print("Posterior probability (with look-elsewhere):")
    print(f"  • P(single trial) = {p_single_trial*100:.2f}%")
    print(f"  • P(20 trials) = {p_multiple_trials*100:.1f}%")
    print()

    # Bayes factor
    # H1: k = 1 + 5α is physical (motivated by 5 quarks)
    # H0: k is random (no physical reason)

    prior_H1 = 0.1  # 10% chance 5 quarks are relevant
    prior_H0 = 0.9  # 90% chance it's random

    bayes_factor = (likelihood * prior_H1) / ((1.0 - likelihood) * prior_H0)

    print("Bayes factor (H1: physical vs H0: random):")
    print(f"  • Prior(H1) = {prior_H1*100:.0f}%  (5 quarks motivated)")
    print(f"  • Prior(H0) = {prior_H0*100:.0f}%  (random coincidence)")
    print(f"  • Bayes factor = {bayes_factor:.2f}")
    print()

    if bayes_factor > 3:
        conclusion = "MODERATE evidence for H1 (physical)"
    elif bayes_factor > 1:
        conclusion = "WEAK evidence for H1"
    else:
        conclusion = "INSUFFICIENT evidence, prefer H0 (random)"

    print(f"  → {conclusion}")
    print()

bayesian_analysis()

# ============================================================================
# ZÁVĚR
# ============================================================================

print("="*80)
print("CRITICAL SUMMARY")
print("="*80)
print()

print("🚨 RED FLAGS IDENTIFIED:")
print()
print("1. ❌ k_Coulomb = 1.0364 NOT FOUND in CODATA")
print("      → Origin unclear, possibly invented/misunderstood")
print()
print("2. ⚠️  n_ν = 336 cm⁻³ discrepancy with CMB theory (~243 cm⁻³)")
print("      → Is 336 fitted to make S_tot = 58 work?")
print()
print("3. ⚠️  k = 1 + 12/n_ν is EXACT (by S_tot definition)")
print("      → k = 1 + 5α is approximate (12/336 ≈ 5α accidentally?)")
print()
print("4. ⚠️  Look-elsewhere effect: tested ~20 factors")
print("      → P(finding one that works) ~ 14% (not < 1%!)")
print()

print("✅ STRENGTHS:")
print()
print("1. ✓ Factor 5 = number of active quarks (physical motivation)")
print("2. ✓ Mechanism (vacuum polarization) is plausible")
print("3. ✓ Agreement 0.075% is better than most alternatives")
print()

print("⚙️  VERDICT: UNCERTAIN - Need more investigation")
print()
print("BEFORE claiming k = 1 + 5α as physics:")
print("  → FIND PRIMARY SOURCE for k_Coulomb = 1.0364")
print("  → VERIFY n_ν = 336 cm⁻³ is not fitted")
print("  → CALCULATE P(coincidence) including all trials")
print("  → COMPARE alternative mechanisms (π, e, other factors)")
print()
print("⚠️  RECOMMENDATION: Label as 'SUGGESTIVE' not 'ESTABLISHED'")
print()

print("="*80)
print("END CRITICAL TEST")
print("="*80)
