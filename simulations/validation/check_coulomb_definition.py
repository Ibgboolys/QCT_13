#!/usr/bin/env python3
"""
check_coulomb_definition.py

OVĚŘENÍ: Co je k_Coulomb a odkud pochází 1.03643?

V appendix_mathematical_constants.tex line 139 tvrdí:
    1 C = 1.03643 × 10^-5 mol × N_A × e

Je tohle správně?
"""

import numpy as np
from scipy.constants import elementary_charge, Avogadro, physical_constants

print("="*80)
print("CHECKING: Origin of k_Coulomb = 1.03643")
print("="*80)
print()

# SI 2019 redefinition
e = elementary_charge  # Coulombs (EXACT since 2019)
N_A = Avogadro  # mol^-1 (EXACT since 2019)

print("[1] SI 2019 exact definitions:")
print(f"  e  = {e:.20e} C  (elementary charge, EXACT)")
print(f"  N_A = {N_A:.20e} mol^-1  (Avogadro constant, EXACT)")
print()

# Co je 1 Coulomb v elementárních náhojech?
one_coulomb_in_e = 1.0 / e  # C / (C/e) = e

print("[2] 1 Coulomb = ? elementary charges:")
print(f"  1 C = {one_coulomb_in_e:.15e} e")
print(f"      = {one_coulomb_in_e:.10g} e")
print()

# Zkontrolujeme tvrzení z appendix_mathematical_constants.tex
# 1 C = 1.03643 × 10^-5 mol × N_A × e

k_claimed = 1.03643
mol_factor = 1.03643e-5  # mol

one_C_claimed = mol_factor * N_A * e  # Coulombs
print("[3] Checking claim from LaTeX (line 139):")
print(f"  1 C =? {k_claimed} × 10^-5 mol × N_A × e")
print(f"       = {mol_factor} mol × {N_A:.4e} mol^-1 × {e:.4e} C")
print(f"       = {one_C_claimed:.15f} C")
print()

if abs(one_C_claimed - 1.0) < 0.001:
    print("  ✓ Claim is approximately correct!")
    print(f"    Error: {abs(one_C_claimed - 1.0)*100:.3f}%")
else:
    print(f"  ✗ Claim is WRONG!")
    print(f"    Expected: 1.0 C")
    print(f"    Got:      {one_C_claimed:.10f} C")
    print(f"    Error:    {abs(one_C_claimed - 1.0)*100:.1f}%")
print()

# Zkusme zpětně vypočítat co by měl být správný faktor
# 1 C = k × 10^-5 mol × N_A × e
# → k = 1 C / (10^-5 mol × N_A × e)

correct_k = 1.0 / (1e-5 * N_A * e)
print("[4] Correct value should be:")
print(f"  k_correct = 1 C / (10^-5 mol × N_A × e)")
print(f"            = {correct_k:.10f}")
print()

print(f"  Claimed in LaTeX:  k = {k_claimed:.10f}")
print(f"  Correct value:     k = {correct_k:.10f}")
print(f"  Difference:        Δk = {abs(k_claimed - correct_k):.10f}")
print(f"  Relative error:    {abs(k_claimed - correct_k)/correct_k*100:.2f}%")
print()

# Je k_claimed = k_QCT?
k_QCT = 58.0 / 56.0
print("[5] Comparison with k_QCT:")
print(f"  k_QCT (58/56):     {k_QCT:.10f}")
print(f"  k_claimed:         {k_claimed:.10f}")
print(f"  k_correct:         {correct_k:.10f}")
print()

if abs(k_claimed - k_QCT) < 0.001:
    print("  🚨 SUSPICION: k_claimed ≈ k_QCT!")
    print("     This suggests k_Coulomb was POST-HOC fitted to match k_QCT!")
else:
    print("  k_claimed ≠ k_QCT (not obviously related)")
print()

# Hledat odkud pochází 1.03643
print("[6] Searching for origin of 1.03643...")
print()

# Test různé CODATA konstanty
print("Testing CODATA ratios:")

try:
    # Faraday constant F = N_A × e
    F = physical_constants['Faraday constant'][0]  # C/mol
    print(f"  • Faraday constant F = {F:.10e} C/mol")
    print(f"    F = N_A × e = {N_A * e:.10e} C/mol")
    print()

    # Zkusme různé kombinace
    ratio1 = F / (1e5 * e)  # F / (10^5 × e) = N_A / 10^5
    print(f"  • F / (10^5 × e) = {ratio1:.10e}")

    # electron volt
    eV_joule = physical_constants['electron volt'][0]  # J
    print(f"  • 1 eV = {eV_joule:.10e} J")

except KeyError as ex:
    print(f"  Cannot find: {ex}")

print()

# ZÁVĚR
print("="*80)
print("CONCLUSION")
print("="*80)
print()

if abs(one_C_claimed - 1.0) > 0.01:
    print("❌ The formula in appendix_mathematical_constants.tex is WRONG!")
    print()
    print("   Line 139 claims:")
    print("       1 C = 1.03643 × 10^-5 mol × N_A × e")
    print()
    print("   But this gives:")
    print(f"       1 C = {one_C_claimed:.6f} C  (not 1.0!)")
    print()
    print("🚨 RED FLAG: k_Coulomb = 1.03643 appears to be INVENTED")
    print("   to match k_QCT = 1.0357!")
    print()
    print("⚠️  NUMEROLOGY ALERT: Post-hoc fitting masquerading as")
    print("   'fundamental electromagnetic constant'")
else:
    print("✓ Formula is approximately correct")
    print()

print()
print("RECOMMENDATION:")
print("  → REMOVE claim about k_Coulomb from manuscript")
print("  → Label k = 58/56 as FITTED parameter, not derived")
print("  → Be honest about post-hoc nature of S_tot = 58")
print()
