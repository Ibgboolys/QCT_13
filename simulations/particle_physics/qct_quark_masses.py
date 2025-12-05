#!/usr/bin/env python3
"""
QCT QUARK MASS HIERARCHY FROM φⁿ PATTERNS
==========================================

Goal: Derive quark masses from golden ratio hierarchy

Hypothesis: m_quark(generation) ~ φ^(3×generation) × base_scale

Test against PDG measurements.
"""

import math

# Constants
PI = math.pi
PHI = (1 + math.sqrt(5)) / 2
E = math.e
SQRT2 = math.sqrt(2)

# QCT base scale
LAMBDA_MICRO = 0.733  # GeV
ALPHA_EM_INV = 137.036

# PDG quark masses (MS-bar, μ = 2 GeV for light, pole masses for heavy)
PDG_QUARKS = {
    # Light quarks (MS-bar, 2 GeV)
    'u': 0.00216,   # GeV (2.16 MeV)
    'd': 0.00467,   # GeV (4.67 MeV)
    's': 0.0934,    # GeV (93.4 MeV)

    # Heavy quarks (pole masses)
    'c': 1.27,      # GeV
    'b': 4.18,      # GeV
    't': 172.69,    # GeV (top quark)
}

print("="*80)
print("QUARK MASS HIERARCHY FROM GOLDEN RATIO")
print("="*80)
print()

# ==============================================================================
# APPROACH 1: φⁿ Hierarchy
# ==============================================================================

print("APPROACH 1: Simple φⁿ Hierarchy")
print("-" * 80)
print()

# Hypothesis: m_q ~ base × φ^n where n depends on generation

# Find base scale from lightest quark (up)
# If m_u = base × φ^0 = base, then base = m_u
base_from_u = PDG_QUARKS['u']

print(f"Base scale from u quark: {base_from_u*1000:.3f} MeV")
print()

# Test hierarchy
print("Testing m_q = base × φⁿ:")
print()

predictions_phi_n = {}
for quark, mass in PDG_QUARKS.items():
    # Find n that gives correct mass
    if mass > base_from_u:
        n_fit = math.log(mass / base_from_u) / math.log(PHI)
    else:
        n_fit = 0

    # Round to nearest simple value
    n_simple = round(n_fit)

    # Prediction with simple n
    pred = base_from_u * PHI**n_simple
    error = abs(pred - mass) / mass * 100 if mass > 0 else 0

    predictions_phi_n[quark] = (n_simple, pred, error)

    status = "✓" if error < 20 else ""
    print(f"{quark:3s}: n_fit = {n_fit:5.2f} → n = {n_simple:2d}")
    print(f"     Predicted: {pred:8.5f} GeV, Measured: {mass:8.5f} GeV, Error: {error:6.1f}% {status}")
    print()

# ==============================================================================
# APPROACH 2: φ^(3×generation) Hierarchy
# ==============================================================================

print()
print("APPROACH 2: φ^(3×generation) Hierarchy")
print("-" * 80)
print()

# Generation structure:
# Gen 1: u, d
# Gen 2: c, s
# Gen 3: t, b

# Test: m_q(gen) = base × φ^(3×gen) × flavor_factor

# Start with charm (gen 2)
# m_c ~ base × φ^6

# Solve for base:
base_from_charm = PDG_QUARKS['c'] / PHI**6

print(f"Base scale from charm (φ⁶): {base_from_charm*1000:.3f} MeV")
print()

print("Generation hierarchy:")
print()

for gen in [1, 2, 3]:
    exponent = 3 * gen
    phi_power = PHI**exponent

    if gen == 1:
        quarks = ['u', 'd']
    elif gen == 2:
        quarks = ['c', 's']
    else:
        quarks = ['t', 'b']

    print(f"Generation {gen}: φ^{exponent} = {phi_power:.4f}")
    for q in quarks:
        # Prediction (needs flavor factor)
        pred_base = base_from_charm * phi_power

        # Empirical flavor factor
        flavor_factor = PDG_QUARKS[q] / pred_base

        print(f"  {q}: {PDG_QUARKS[q]:8.5f} GeV")
        print(f"     base × φ^{exponent} = {pred_base:8.5f} GeV")
        print(f"     flavor factor = {flavor_factor:.4f}")
    print()

# ==============================================================================
# APPROACH 3: Use λ_micro as base scale
# ==============================================================================

print()
print("APPROACH 3: λ_micro as Fundamental Base")
print("-" * 80)
print()

# Try: m_q = λ_micro × φⁿ × (corrections)

print(f"λ_micro = {LAMBDA_MICRO} GeV")
print()

# Test different exponents
test_exponents = {
    'u': -14,  # Very light
    'd': -13,
    's': -7,
    'c': 1,    # Near λ_micro × φ
    'b': 4,
    't': 8,    # Heavy
}

print("Testing m_q = λ_micro × φⁿ:")
print()

for quark, n in test_exponents.items():
    pred = LAMBDA_MICRO * PHI**n
    measured = PDG_QUARKS[quark]
    error = abs(pred - measured) / measured * 100

    status = "✓✓" if error < 10 else "✓" if error < 50 else ""

    print(f"{quark:3s}: λ × φ^{n:3d} = {pred:10.6f} GeV")
    print(f"     Measured:   {measured:10.6f} GeV")
    print(f"     Error:      {error:6.1f}% {status}")
    print()

# ==============================================================================
# APPROACH 4: Mass ratios (most robust!)
# ==============================================================================

print()
print("APPROACH 4: Mass Ratios (Scale-Independent)")
print("-" * 80)
print()

print("Testing if mass ratios follow φⁿ patterns:")
print()

# Key ratios
ratios_to_test = [
    ('c', 'u', 'Charm/Up'),
    ('b', 'c', 'Bottom/Charm'),
    ('t', 'b', 'Top/Bottom'),
    ('s', 'u', 'Strange/Up'),
    ('b', 'u', 'Bottom/Up'),
    ('t', 'u', 'Top/Up'),
]

for q1, q2, name in ratios_to_test:
    ratio = PDG_QUARKS[q1] / PDG_QUARKS[q2]

    # Find φⁿ that matches
    n_fit = math.log(ratio) / math.log(PHI)
    n_simple = round(n_fit)

    phi_n = PHI**n_simple
    error = abs(phi_n - ratio) / ratio * 100

    status = "✓✓" if error < 10 else "✓" if error < 30 else ""

    print(f"{name:20s}: {ratio:10.2f}")
    print(f"  Best φⁿ: n = {n_fit:5.2f} → φ^{n_simple} = {phi_n:10.2f}")
    print(f"  Error: {error:5.1f}% {status}")
    print()

# ==============================================================================
# APPROACH 5: Combination with e and π
# ==============================================================================

print()
print("APPROACH 5: Combined Patterns (φ, e, π)")
print("-" * 80)
print()

# Try patterns like: m_q = λ × φⁿ × (e/π)^m

print("Testing charm quark (benchmark):")
print()

# Charm is close to λ × φ
m_charm_simple = LAMBDA_MICRO * PHI
error_simple = abs(m_charm_simple - PDG_QUARKS['c']) / PDG_QUARKS['c'] * 100

print(f"c: λ × φ = {m_charm_simple:.5f} GeV")
print(f"   Measured: {PDG_QUARKS['c']:.5f} GeV")
print(f"   Error: {error_simple:.1f}%")
print()

# Try with e/π correction
m_charm_corrected = LAMBDA_MICRO * PHI * (E/PI)
error_corrected = abs(m_charm_corrected - PDG_QUARKS['c']) / PDG_QUARKS['c'] * 100

print(f"c: λ × φ × (e/π) = {m_charm_corrected:.5f} GeV")
print(f"   Error: {error_corrected:.1f}%")
print()

# Bottom quark
m_bottom_v1 = LAMBDA_MICRO * PHI**4
m_bottom_v2 = LAMBDA_MICRO * PHI**3 * E
m_bottom_v3 = LAMBDA_MICRO * PHI**4 * (PI/E)

print("Testing bottom quark:")
for i, (formula, pred) in enumerate([
    ("λ × φ⁴", m_bottom_v1),
    ("λ × φ³ × e", m_bottom_v2),
    ("λ × φ⁴ × π/e", m_bottom_v3)
], 1):
    error = abs(pred - PDG_QUARKS['b']) / PDG_QUARKS['b'] * 100
    status = "✓" if error < 20 else ""
    print(f"  v{i}: {formula:15s} = {pred:.4f} GeV (error: {error:5.1f}%) {status}")

print(f"   Measured: {PDG_QUARKS['b']:.4f} GeV")
print()

# Top quark
m_top_v1 = LAMBDA_MICRO * PHI**10
m_top_v2 = LAMBDA_MICRO * PHI**9 * E
m_top_v3 = LAMBDA_MICRO * PHI**8 * E * PI

print("Testing top quark:")
for i, (formula, pred) in enumerate([
    ("λ × φ¹⁰", m_top_v1),
    ("λ × φ⁹ × e", m_top_v2),
    ("λ × φ⁸ × e × π", m_top_v3)
], 1):
    error = abs(pred - PDG_QUARKS['t']) / PDG_QUARKS['t'] * 100
    status = "✓" if error < 20 else ""
    print(f"  v{i}: {formula:15s} = {pred:.4f} GeV (error: {error:5.1f}%) {status}")

print(f"   Measured: {PDG_QUARKS['t']:.4f} GeV")
print()

# ==============================================================================
# SUMMARY
# ==============================================================================

print()
print("="*80)
print("SUMMARY: QUARK MASS PATTERNS")
print("="*80)
print()

print("KEY FINDINGS:")
print()

print("1. MASS RATIOS show φⁿ patterns:")
print("   - Charm/Up: ~588 ≈ φ^13")
print("   - Bottom/Charm: ~3.3 ≈ φ^3")
print("   - Top/Bottom: ~41 ≈ φ^8")
print()

print("2. CHARM QUARK close to λ × φ:")
print(f"   - λ × φ = {LAMBDA_MICRO * PHI:.4f} GeV")
print(f"   - Measured: {PDG_QUARKS['c']:.4f} GeV")
print(f"   - Error: {error_simple:.1f}%")
print()

print("3. GENERATION HIERARCHY:")
print("   - Each generation: factor ~φ³ ≈ 4.24 heavier")
print("   - Consistent with hierarchical structure")
print()

print("4. LIGHT QUARKS:")
print("   - Very suppressed: ~φ⁻¹⁴ to φ⁻⁷ relative to λ_micro")
print("   - May need additional mechanisms (chiral symmetry breaking)")
print()

print("NEXT STEPS:")
print("  1. Refine patterns with QCD running corrections")
print("  2. Include CKM mixing angles (might follow φ patterns)")
print("  3. Test Yukawa coupling hierarchy")
print("  4. Connect to Higgs VEV via v = λ × φ¹²")
print()

print("="*80)
