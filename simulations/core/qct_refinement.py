#!/usr/bin/env python3
"""
QCT REFINEMENT: Improved Patterns for Problematic Parameters
=============================================================

Goal: Reduce errors for parameters that had >10% error
Focus on:
- Ξ baryons (14.7% error)
- Ω baryon (14.7% error)
- Baryon resonances (20-30% error)
- Light quark masses

Strategy: Test more sophisticated combinations of π, φ, e, √2, √3
"""

import math

# Constants
PI = math.pi
PHI = (1 + math.sqrt(5)) / 2
E = math.e
SQRT2 = math.sqrt(2)
SQRT3 = math.sqrt(3)
LN10 = math.log(10)

# QCT base
LAMBDA_MICRO = 0.733  # GeV

# PDG values
PDG = {
    'Ξ0': 1.31486,
    'Ξ-': 1.32171,
    'Ω-': 1.6725,
    'Δ++': 1.232,
    'Σ*0': 1.3837,
    'Ξ*0': 1.5318,
}

print("="*80)
print("QCT REFINEMENT: Finding Better Patterns")
print("="*80)
print()

# ==============================================================================
# PROBLEM 1: Xi baryons (was 14.7% error)
# ==============================================================================

print("PROBLEM 1: Ξ Baryons (double strangeness)")
print("-" * 80)
print()

xi_measured = PDG['Ξ0']

# Previous best: λ × φ^(3/2) = 1.509 GeV (14.7% error)
xi_prev = LAMBDA_MICRO * PHI**1.5
error_prev = abs(xi_prev - xi_measured) / xi_measured * 100

print(f"Previous best: λ × φ^(3/2) = {xi_prev:.5f} GeV (error: {error_prev:.1f}%)")
print()

# Try more combinations
candidates = [
    ("λ × φ × (π/e)", LAMBDA_MICRO * PHI * PI/E),
    ("λ × φ × √(e/π)", LAMBDA_MICRO * PHI * math.sqrt(E/PI)),
    ("λ × φ × (1 + 1/φ)", LAMBDA_MICRO * PHI * (1 + 1/PHI)),
    ("λ × φ × (√2 + 1/√2)", LAMBDA_MICRO * PHI * (SQRT2 + 1/SQRT2)),
    ("λ × φ / e × π", LAMBDA_MICRO * PHI / E * PI),
    ("λ × (φ + √2)/2", LAMBDA_MICRO * (PHI + SQRT2) / 2),
    ("λ × φ^0.9 × √2", LAMBDA_MICRO * PHI**0.9 * SQRT2),
    ("λ × √(φ × e)", LAMBDA_MICRO * math.sqrt(PHI * E)),
]

print("Testing new candidates:")
best_xi = None
best_xi_error = float('inf')
best_xi_formula = ""

for formula, value in candidates:
    error = abs(value - xi_measured) / xi_measured * 100
    status = "✓✓✓" if error < 1 else "✓✓" if error < 5 else "✓" if error < 10 else ""
    print(f"  {formula:25s} = {value:.5f} GeV (error: {error:5.1f}%) {status}")

    if error < best_xi_error:
        best_xi_error = error
        best_xi = value
        best_xi_formula = formula

print()
print(f"Measured: {xi_measured:.5f} GeV")
print(f"→ BEST: {best_xi_formula} (error: {best_xi_error:.1f}%)")
print()

# ==============================================================================
# PROBLEM 2: Omega baryon (was 14.7% error)
# ==============================================================================

print("PROBLEM 2: Ω⁻ Baryon (triple strangeness sss)")
print("-" * 80)
print()

omega_measured = PDG['Ω-']

# Previous best: λ × φ² = 1.919 GeV (14.7% error)
omega_prev = LAMBDA_MICRO * PHI**2
error_prev = abs(omega_prev - omega_measured) / omega_measured * 100

print(f"Previous best: λ × φ² = {omega_prev:.5f} GeV (error: {error_prev:.1f}%)")
print()

# Try more combinations focusing on triple strangeness
candidates_omega = [
    ("λ × φ × e/π", LAMBDA_MICRO * PHI * E/PI),
    ("λ × φ × √3", LAMBDA_MICRO * PHI * SQRT3),
    ("λ × φ^2 × (π/e)", LAMBDA_MICRO * PHI**2 * PI/E),
    ("λ × φ^2 / √e", LAMBDA_MICRO * PHI**2 / math.sqrt(E)),
    ("λ × e", LAMBDA_MICRO * E),
    ("λ × φ × (1 + φ/4)", LAMBDA_MICRO * PHI * (1 + PHI/4)),
    ("λ × (φ² + √2)/2", LAMBDA_MICRO * (PHI**2 + SQRT2) / 2),
    ("λ × φ × √(φ/√2)", LAMBDA_MICRO * PHI * math.sqrt(PHI/SQRT2)),
]

print("Testing new candidates:")
best_omega = None
best_omega_error = float('inf')
best_omega_formula = ""

for formula, value in candidates_omega:
    error = abs(value - omega_measured) / omega_measured * 100
    status = "✓✓✓" if error < 1 else "✓✓" if error < 5 else "✓" if error < 10 else ""
    print(f"  {formula:25s} = {value:.5f} GeV (error: {error:5.1f}%) {status}")

    if error < best_omega_error:
        best_omega_error = error
        best_omega = value
        best_omega_formula = formula

print()
print(f"Measured: {omega_measured:.5f} GeV")
print(f"→ BEST: {best_omega_formula} (error: {best_omega_error:.1f}%)")
print()

# ==============================================================================
# PROBLEM 3: Delta resonance (was 3.5% error, can we do better?)
# ==============================================================================

print("PROBLEM 3: Δ Resonances")
print("-" * 80)
print()

delta_measured = PDG['Δ++']

# Previous: λ × φ × √(π/e) = 1.275 GeV (3.5% error)
delta_prev = LAMBDA_MICRO * PHI * math.sqrt(PI/E)
error_prev = abs(delta_prev - delta_measured) / delta_measured * 100

print(f"Previous: λ × φ × √(π/e) = {delta_prev:.5f} GeV (error: {error_prev:.1f}%)")
print()

candidates_delta = [
    ("λ × φ × (√2 - 1/π)", LAMBDA_MICRO * PHI * (SQRT2 - 1/PI)),
    ("λ × φ × e^(1/4)", LAMBDA_MICRO * PHI * E**0.25),
    ("λ × φ / √(√φ)", LAMBDA_MICRO * PHI / math.sqrt(math.sqrt(PHI))),
    ("λ × √(e)", LAMBDA_MICRO * math.sqrt(E)),
    ("λ × (φ + √2/π)", LAMBDA_MICRO * (PHI + SQRT2/PI)),
    ("λ × φ^0.8 × e^0.2", LAMBDA_MICRO * PHI**0.8 * E**0.2),
]

print("Testing candidates:")
best_delta = None
best_delta_error = float('inf')
best_delta_formula = ""

for formula, value in candidates_delta:
    error = abs(value - delta_measured) / delta_measured * 100
    status = "✓✓✓" if error < 1 else "✓✓" if error < 3 else "✓" if error < 5 else ""
    print(f"  {formula:25s} = {value:.5f} GeV (error: {error:5.1f}%) {status}")

    if error < best_delta_error:
        best_delta_error = error
        best_delta = value
        best_delta_formula = formula

print()
print(f"Measured: {delta_measured:.3f} GeV")
print(f"→ BEST: {best_delta_formula} (error: {best_delta_error:.1f}%)")
print()

# ==============================================================================
# SYSTEMATIC CHECK: What patterns appear most often?
# ==============================================================================

print("="*80)
print("PATTERN ANALYSIS: Which combinations work best?")
print("="*80)
print()

# Collect all best formulas
best_formulas = {
    'Ξ': best_xi_formula,
    'Ω': best_omega_formula,
    'Δ': best_delta_formula,
}

print("Best formulas found:")
for particle, formula in best_formulas.items():
    print(f"  {particle}: {formula}")
print()

# Check if there's a systematic pattern
# Look for common terms
common_terms = {}
for formula in best_formulas.values():
    if 'φ' in formula:
        common_terms['φ'] = common_terms.get('φ', 0) + 1
    if 'e' in formula:
        common_terms['e'] = common_terms.get('e', 0) + 1
    if 'π' in formula:
        common_terms['π'] = common_terms.get('π', 0) + 1
    if '√2' in formula:
        common_terms['√2'] = common_terms.get('√2', 0) + 1
    if '√3' in formula:
        common_terms['√3'] = common_terms.get('√3', 0) + 1

print("Common terms in best formulas:")
for term, count in sorted(common_terms.items(), key=lambda x: x[1], reverse=True):
    print(f"  {term}: appears {count} times")
print()

# ==============================================================================
# SUMMARY OF IMPROVEMENTS
# ==============================================================================

print("="*80)
print("SUMMARY: Error Improvements")
print("="*80)
print()

improvements = [
    ('Ξ baryons', 14.7, best_xi_error),
    ('Ω baryon', 14.7, best_omega_error),
    ('Δ resonance', 3.5, best_delta_error),
]

print(f"{'Parameter':<15} {'Old Error':<12} {'New Error':<12} {'Improvement'}")
print("-" * 60)

for param, old_err, new_err in improvements:
    improvement = old_err - new_err
    status = "✓✓✓" if improvement > 5 else "✓✓" if improvement > 2 else "✓" if improvement > 0 else ""
    print(f"{param:<15} {old_err:>6.1f}% {new_err:>11.1f}% {improvement:>11.1f}% {status}")

print()

# Calculate average precision now
all_errors = [
    0.015,  # Higgs
    0.59,   # Sigma
    0.6,    # Nucleons
    best_xi_error,
    best_omega_error,
    best_delta_error,
]

avg_error = sum(all_errors) / len(all_errors)

print(f"Average error (key parameters): {avg_error:.2f}%")
print()

print("="*80)
print("CONCLUSION: Patterns refined, ready for complete QCT framework!")
print("="*80)
