#!/usr/bin/env python3
"""
Search for hidden mathematical constants in QCT parameters
Check if any ratios/combinations give e, π, √2, √3, φ, etc.
"""

import numpy as np
from itertools import combinations

# Mathematical constants
E = np.e  # 2.718281828...
PI = np.pi  # 3.141592654...
PHI = (1 + np.sqrt(5)) / 2  # 1.618033989... (golden ratio)
SQRT2 = np.sqrt(2)  # 1.414213562...
SQRT3 = np.sqrt(3)  # 1.732050808...
SQRT5 = np.sqrt(5)  # 2.236067977...
LN2 = np.log(2)  # 0.693147181...
LN10 = np.log(10)  # 2.302585093...

# QCT Parameters (from repository)
params = {
    'lambda_micro': 0.733,  # GeV
    'lambda_micro/m_p': 0.789,  # = (3+√3)/6
    'm_p_QCD': 0.9293,  # GeV
    'alpha_mag': 9.2e11,  # |α| = 9.2×10^11
    'f_screen': 1e-10,  # m_ν/m_p
    'sigma_max_sq': 0.2,  # phase variance
    'lambda_coupling': 0.06,  # 6×10^-2
    'S_tot': 58,  # NP-RG entropy
    'kappa_conf_EeV': 0.48,  # EeV
    'E_pair_EeV': 5.38,  # ×10^18 eV = 5.38 EeV
    'V_proj': 72.3,  # cm³
    'R_proj': 2.3,  # cm
    'n_nu': 336,  # cm^-3
    'm_nu': 0.1,  # eV
    'Lambda_QCT': 107,  # TeV
    'v_Higgs': 246.22,  # GeV
    'phi_exponent': 12.088,  # v/lambda_micro = φ^12.088
}

# Derived quantities
params['ln_f_screen_inv'] = np.log(1/params['f_screen'])  # ln(10^10)
params['lambda_screen_mm'] = params['R_proj'] / params['ln_f_screen_inv'] * 10  # mm
params['E_pair/m_nu'] = params['E_pair_EeV'] * 1e18 / params['m_nu']  # ratio

print("=" * 80)
print("QCT HIDDEN CONSTANTS SEARCH")
print("=" * 80)
print()

# Target constants to search for
targets = {
    'e (Euler)': E,
    'π': PI,
    'φ (golden ratio)': PHI,
    '√2': SQRT2,
    '√3': SQRT3,
    '√5': SQRT5,
    'ln(2)': LN2,
    'ln(10)': LN10,
    'e^π': np.exp(PI),
    'π^e': PI**E,
    'e/π': E/PI,
    'π/e': PI/E,
    'e×π': E*PI,
}

def check_match(value, target, name, tolerance=0.05):
    """Check if value matches target within tolerance"""
    if abs(value) < 1e-20:  # Skip zero values
        return False

    relative_error = abs(value - target) / abs(target)
    if relative_error < tolerance:
        print(f"  ✓ {name:40s} = {value:12.6f}  ≈ {target:12.6f}  (error: {relative_error*100:5.2f}%)")
        return True
    return False

print("DIRECT PARAMETER CHECKS:")
print("-" * 80)
for param_name, param_value in params.items():
    print(f"\n{param_name} = {param_value}")
    for target_name, target_value in targets.items():
        check_match(param_value, target_value, f"  vs {target_name}")

print("\n" + "=" * 80)
print("RATIOS OF PARAMETERS:")
print("-" * 80)

param_list = list(params.items())
matches = []

for i, (name1, val1) in enumerate(param_list):
    for name2, val2 in param_list[i+1:]:
        if abs(val2) < 1e-20:
            continue

        ratio = val1 / val2

        # Check if ratio matches any target
        for target_name, target_value in targets.items():
            if check_match(ratio, target_value, f"{name1} / {name2}", tolerance=0.03):
                matches.append({
                    'expression': f"{name1} / {name2}",
                    'value': ratio,
                    'target': target_name,
                    'target_value': target_value,
                    'error': abs(ratio - target_value) / abs(target_value)
                })

print("\n" + "=" * 80)
print("PRODUCTS OF PARAMETERS:")
print("-" * 80)

for i, (name1, val1) in enumerate(param_list[:10]):  # Limit to avoid explosion
    for name2, val2 in param_list[i+1:10]:
        product = val1 * val2

        for target_name, target_value in targets.items():
            if check_match(product, target_value, f"{name1} × {name2}", tolerance=0.03):
                matches.append({
                    'expression': f"{name1} × {name2}",
                    'value': product,
                    'target': target_name,
                    'target_value': target_value,
                    'error': abs(product - target_value) / abs(target_value)
                })

print("\n" + "=" * 80)
print("SPECIAL COMBINATIONS:")
print("-" * 80)

# Check specific meaningful combinations
special_combos = {
    'ln(1/f_screen)': params['ln_f_screen_inv'],
    'sqrt(lambda_micro)': np.sqrt(params['lambda_micro']),
    'sqrt(lambda_micro/m_p)': np.sqrt(params['lambda_micro/m_p']),
    'lambda_micro^2': params['lambda_micro']**2,
    '(3+√3)/6': (3 + np.sqrt(3)) / 6,
    'sigma_max_sq × 10': params['sigma_max_sq'] * 10,
    'S_tot / 20': params['S_tot'] / 20,
    'ln(Lambda_QCT)': np.log(params['Lambda_QCT']),
    'ln(v_Higgs)': np.log(params['v_Higgs']),
    'phi_exponent / 12': params['phi_exponent'] / 12,
    '1 / alpha_EM': 137.036,  # fine structure
}

print("\nSpecial QCT combinations:")
for expr, value in special_combos.items():
    print(f"\n{expr} = {value:.10f}")
    for target_name, target_value in targets.items():
        check_match(value, target_value, f"  vs {target_name}", tolerance=0.02)

print("\n" + "=" * 80)
print("SUMMARY OF BEST MATCHES:")
print("-" * 80)

if matches:
    # Sort by error
    matches.sort(key=lambda x: x['error'])
    print(f"\nFound {len(matches)} potential matches:\n")
    for match in matches[:20]:  # Top 20
        print(f"  {match['expression']:50s} = {match['value']:12.6f}  ≈ {match['target']} = {match['target_value']:12.6f}  (error: {match['error']*100:5.2f}%)")
else:
    print("\nNo strong matches found with current tolerance.")

# CRITICAL CHECK: Baryon error = 2.71% vs e = 2.718?
print("\n" + "=" * 80)
print("CRITICAL CHECK: Ω⁻ BARYON ERROR vs EULER'S NUMBER:")
print("-" * 80)
omega_error_percent = 2.71
e_truncated = 2.71828

print(f"Ω⁻ error: {omega_error_percent}%")
print(f"e (Euler): {e_truncated}")
print(f"Match: {omega_error_percent:.2f} ≈ {e_truncated:.2f}? ")

if abs(omega_error_percent - E) / E < 0.01:
    print("  ✓ POSSIBLE MATCH! Error might be related to e!")
else:
    print("  ✗ Likely coincidence (error: {:.1f}%)".format(abs(omega_error_percent - E) / E * 100))

# Check if ln(something) = 1
print("\n" + "=" * 80)
print("SEARCH FOR ln(X) = 1 (implies X = e):")
print("-" * 80)
for name, value in params.items():
    if value > 0:
        ln_val = np.log(value)
        if abs(ln_val - 1.0) < 0.1:
            print(f"  ln({name}) = {ln_val:.6f}  (target: 1.000)")

print("\n" + "=" * 80)
print("DONE")
print("=" * 80)
