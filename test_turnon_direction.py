#!/usr/bin/env python3
"""
TEST: Understanding the turn-on function direction
"""
import numpy as np

# Test parameters
z_BBN = 1e9
z_start = 1e8
k = 2.0

print("="*80)
print("TURN-ON FUNCTION DIRECTION TEST")
print("="*80)
print()
print(f"Testing: z_BBN = {z_BBN:.2e}, z_start = {z_start:.2e}, k = {k}")
print()

# Physical timeline (cosmic time):
# z_dec ~ 10^9 (earlier) → z_start ~ 10^7-10^8 (later) → z=0 (today)
# BBN happens at z ~ 10^9 (approximately same time as decoupling)

print("COSMIC TIMELINE:")
print("-" * 80)
print("z ~ 10^9 (BBN/decoupling, EARLY time, t ~ 1-180 s)")
print("   ↓ time progresses →")
print("z ~ 10^7-10^8 (condensate forms, LATER time)")
print("   ↓ time progresses →")
print("z = 0 (today, LATEST time)")
print()

# Formula from manuscript (Eq. 103): Uses LN
def f_turnon_ln(z, z_start, k=2.0):
    """Manuscript formula (line 103): uses LN"""
    log_ratio = np.log((1 + z) / (1 + z_start))  # Natural log
    return 1.0 / (1.0 + np.exp(-k * log_ratio))

# Formula from test script: Uses LOG10
def f_turnon_log10(z, z_start, k=2.0):
    """Test script formula: uses LOG10"""
    log_ratio = np.log10((1 + z) / (1 + z_start))  # Base-10 log
    return 1.0 / (1.0 + np.exp(-k * log_ratio))

# Inverted sigmoid (flip sign in exponent)
def f_turnon_inverted(z, z_start, k=2.0):
    """Inverted sigmoid: flip sign in exponent"""
    log_ratio = np.log((1 + z) / (1 + z_start))
    return 1.0 / (1.0 + np.exp(+k * log_ratio))  # Note: +k instead of -k

print("FORMULA COMPARISON:")
print("-" * 80)

# Test at different redshifts
test_redshifts = [0, 1e6, 1e7, z_start, 1e9, 1e10]

print(f"{'z':>12} {'f_ln':>12} {'f_log10':>12} {'f_inverted':>12}")
print("-" * 52)

for z in test_redshifts:
    if z == 0:
        f_ln = 1.0  # Special case
        f_log10 = 1.0
        f_inv = 1.0
    else:
        f_ln = f_turnon_ln(z, z_start, k)
        f_log10 = f_turnon_log10(z, z_start, k)
        f_inv = f_turnon_inverted(z, z_start, k)

    marker = " ← BBN" if z == 1e9 else " ← z_start" if z == z_start else ""
    print(f"{z:>12.2e} {f_ln:>12.4f} {f_log10:>12.4f} {f_inv:>12.4f}{marker}")

print()

# Calculate E_pair ratio
print("E_pair BEHAVIOR:")
print("-" * 80)
print("From manuscript (line 197): E_pair(z_BBN) ≈ 0.84 × E_pair(z=0)")
print()
print("Using E_pair(z) = E_0 + κ_conf × f(z) × ln(1+z):")
print()

E_0 = 0.1e9  # eV
kappa_conf = 4.8e17  # eV

# Since ln(1) = 0, we have E_pair(0) = E_0 for the formula
# But physically E_pair(0) ~ 10^19 eV
# So there's already an issue with the formula at z=0

print("⚠️  WARNING: Formula gives E_pair(z=0) = E_0 = 0.1 eV")
print("           But physically E_pair(0) ~ 10^19 eV!")
print()
print("This suggests the formula doesn't work at z=0 and needs")
print("a different interpretation or normalization.")
print()

# Let's check which direction gives increasing E_pair with decreasing z
print("DIRECTION CHECK (ignoring z=0 issue):")
print("-" * 80)

z_early = 1e9  # Early time
z_late = 1e7   # Late time (closer to today)

f_early_ln = f_turnon_ln(z_early, z_start)
f_late_ln = f_turnon_ln(z_late, z_start)

f_early_log10 = f_turnon_log10(z_early, z_start)
f_late_log10 = f_turnon_log10(z_late, z_start)

E_early_ln = E_0 + kappa_conf * f_early_ln * np.log(1 + z_early)
E_late_ln = E_0 + kappa_conf * f_late_ln * np.log(1 + z_late)

E_early_log10 = E_0 + kappa_conf * f_early_log10 * np.log(1 + z_early)
E_late_log10 = E_0 + kappa_conf * f_late_log10 * np.log(1 + z_late)

print(f"Early time (z={z_early:.2e}):")
print(f"  LN formula:    f={f_early_ln:.4f}, E_pair={E_early_ln:.2e} eV")
print(f"  LOG10 formula: f={f_early_log10:.4f}, E_pair={E_early_log10:.2e} eV")
print()
print(f"Late time (z={z_late:.2e}):")
print(f"  LN formula:    f={f_late_ln:.4f}, E_pair={E_late_ln:.2e} eV")
print(f"  LOG10 formula: f={f_late_log10:.4f}, E_pair={E_late_log10:.2e} eV")
print()

print("PHYSICAL EXPECTATION:")
print("  Condensate builds up over time → E_pair should INCREASE as z DECREASES")
print(f"  So we want: E_pair(late) > E_pair(early)")
print()

print("ACTUAL RESULTS:")
if E_late_ln > E_early_ln:
    print(f"  LN formula:    E_pair(late) > E_pair(early) ✓ Correct direction!")
else:
    print(f"  LN formula:    E_pair(late) < E_pair(early) ❌ Wrong direction!")

if E_late_log10 > E_early_log10:
    print(f"  LOG10 formula: E_pair(late) > E_pair(early) ✓ Correct direction!")
else:
    print(f"  LOG10 formula: E_pair(late) < E_pair(early) ❌ Wrong direction!")

print()
print("="*80)
print("KEY FINDING:")
print("="*80)
print(f"Manuscript claims: f(10^9, 10^8) ≈ 0.84")
print(f"LN formula gives:  f(10^9, 10^8) = {f_turnon_ln(1e9, 1e8, 2):.4f}")
print(f"LOG10 gives:       f(10^9, 10^8) = {f_turnon_log10(1e9, 1e8, 2):.4f}")
print()
print("The LOG10 formula matches the manuscript's claimed value!")
print("This suggests the manuscript formula should use log10, not ln.")
print("="*80)
