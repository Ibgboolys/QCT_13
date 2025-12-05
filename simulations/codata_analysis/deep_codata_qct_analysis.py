#!/usr/bin/env python3
"""
DEEP CODATA-QCT CORRELATION ANALYSIS
====================================

Comprehensive numerical analysis of CODATA 2022 constants vs QCT parameters
with full uncertainty propagation, Monte Carlo validation, and physical
interpretation.

Author: Boleslav Plhák + AI (Claude)
Date: 2025-11-16
Version: 2.0 (corrected)

"""

import csv
import math
import random
from typing import Dict, List, Tuple, Optional

# ==============================================================================
# PHYSICAL CONSTANTS (from scipy.constants and CODATA 2022)
# ==============================================================================

# Natural units conversions
HBAR = 6.582119569e-16  # ℏ in eV·s
C = 2.99792458e8  # Speed of light in m/s
HBAR_C_EV_M = 1.97326980e-7  # ℏc in eV·m
HBAR_C_EV_CM = 1.97326980e-5  # ℏc in eV·cm
HBAR_C_GEV_FM = 0.197326980  # ℏc in GeV·fm

# ==============================================================================
# QCT PARAMETERS WITH FULL UNCERTAINTIES
# ==============================================================================

QCT_PARAMS = {
    # PRIMARY: Microscopic parameters
    'lambda_micro': {'value': 0.06, 'unc': 0.02, 'unit': '', 'type': 'fitted'},
    'sigma_max_sq': {'value': 3.0, 'unc': 1.5, 'unit': '', 'type': 'fitted'},
    'alpha_nuG': {'value': -9e11, 'unc': 3e11, 'unit': '', 'type': 'fitted'},

    # DERIVED: Exact or well-defined
    'S_tot': {'value': 58.0, 'unc': 0.0, 'unit': '', 'type': 'exact'},
    'n_nu': {'value': 336.0, 'unc': 0.0, 'unit': '', 'type': 'exact'},
    'phi': {'value': 1.618033988749895, 'unc': 0.0, 'unit': '', 'type': 'math'},

    # DERIVED: From fits
    'E_pair_eV': {'value': 1.8e19, 'unc': 5.4e18, 'unit': 'eV', 'type': 'semi'},
    'Lambda_QCT_eV': {'value': 1.07e14, 'unc': 3.2e13, 'unit': 'eV', 'type': 'derived'},
    'kappa_conf_eV': {'value': 4.8e17, 'unc': 1.4e17, 'unit': 'eV', 'type': 'calib'},
    'm_nu_eV': {'value': 0.1, 'unc': 0.05, 'unit': 'eV', 'type': 'assumed'},
    'v_Higgs_eV': {'value': 246.22e9, 'unc': 2e8, 'unit': 'eV', 'type': 'measured'},
    'alpha_EM': {'value': 1/137.035999177, 'unc': 1e-10, 'unit': '', 'type': 'measured'},

    # GEOMETRIC: Spatial scales
    'R_proj_m': {'value': 0.0228, 'unc': 0.0068, 'unit': 'm', 'type': 'derived'},
    'R_proj_cm': {'value': 2.28, 'unc': 0.68, 'unit': 'cm', 'type': 'derived'},
    'lambda_screen_m': {'value': 40e-6, 'unc': 12e-6, 'unit': 'm', 'type': 'derived'},

    # PHENOMENOLOGICAL
    'G_eff_ratio': {'value': 0.9, 'unc': 0.03, 'unit': '', 'type': 'prediction'},
    'f_screen': {'value': 1.07e-10, 'unc': 5.4e-11, 'unit': '', 'type': 'derived'},
}

# ==============================================================================
# CODATA CSV PARSER
# ==============================================================================

def parse_codata_csv(filepath: str) -> Dict[str, Dict]:
    """Parse CODATA 2022 CSV with improved robustness."""
    data = {}

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.split()
            if len(parts) < 3:
                continue

            # Extract quantity name, value, uncertainty, unit
            quantity = []
            value_str = None

            for i, part in enumerate(parts):
                if any(c.isdigit() for c in part) or 'e' in part.lower():
                    value_str = part
                    uncertainty_str = parts[i+1] if i+1 < len(parts) else '0'
                    unit = ' '.join(parts[i+2:]) if i+2 < len(parts) else ''
                    break
                quantity.append(part)

            if not value_str:
                continue

            quantity_name = ' '.join(quantity).strip()

            try:
                value = float(value_str.replace(' ', ''))
                uncertainty = float(uncertainty_str.replace(' ', ''))

                data[quantity_name] = {
                    'value': value,
                    'uncertainty': uncertainty,
                    'unit': unit.strip()
                }
            except ValueError:
                continue

    return data

# ==============================================================================
# FERMI CONSTANT DEEP ANALYSIS
# ==============================================================================

def analyze_fermi_constant_detailed():
    """
    Comprehensive analysis of G_F ∝ R_proj³ correlation.

    Corrected version with proper error calculations.
    """
    print("\n" + "="*80)
    print("FERMI CONSTANT G_F ∝ R_proj³: DEEP ANALYSIS")
    print("="*80)

    # CODATA 2022
    G_F = 1.1663787e-5  # GeV^-2
    G_F_unc = 0.0000006e-5  # ±0.05 ppm (ultra-precise!)

    # QCT
    R_proj_m = QCT_PARAMS['R_proj_m']['value']  # m
    R_proj_unc = QCT_PARAMS['R_proj_m']['unc']  # m

    # Calculate R_proj³
    R_proj_cube = R_proj_m**3
    R_proj_cube_unc = 3 * R_proj_m**2 * R_proj_unc  # δ(x³) = 3x²δx

    # NUMERICAL COMPARISON (ignoring dimensional inconsistency for now)
    print(f"\n1. NUMERICAL CORRELATION (ignoring units)")
    print(f"   " + "-"*76)
    print(f"   R_proj = {R_proj_m:.4f} ± {R_proj_unc:.4f} m")
    print(f"   R_proj³ = {R_proj_cube:.8e} ± {R_proj_cube_unc:.8e} m³")
    print(f"   G_F (CODATA) = {G_F:.8e} ± {G_F_unc:.8e} GeV⁻²")
    print(f"\n   Numerically:")
    print(f"     R_proj³ = {R_proj_cube:.8e}")
    print(f"     G_F     = {G_F:.8e}")
    print(f"     Ratio = {R_proj_cube/G_F:.6f}")
    print(f"     **Deviation: {abs(R_proj_cube/G_F - 1.0)*100:.4f}%**")

    relative_error = abs(R_proj_cube - G_F) / G_F
    print(f"\n   Direct numerical agreement: {(1-relative_error)*100:.4f}%")
    print(f"   Numerical error: **{relative_error*100:.4f}%**")

    # POWER LAW ANALYSIS
    print(f"\n2. POWER LAW RELATION")
    print(f"   " + "-"*76)
    log_GF = math.log10(abs(G_F))
    log_Rproj = math.log10(R_proj_m)
    exponent = log_GF / log_Rproj

    print(f"   Testing: G_F ∝ R_proj^n")
    print(f"   Fitted exponent: n = {exponent:.6f}")
    print(f"   Target exponent: n = 3.0 (cube)")
    print(f"   Error in exponent: {abs(exponent - 3.0)/3.0*100:.4f}%")

    # DIMENSIONAL ANALYSIS
    print(f"\n3. DIMENSIONAL ANALYSIS")
    print(f"   " + "-"*76)
    print(f"   [G_F] = [energy]⁻² = GeV⁻²")
    print(f"   [R_proj³] = [length]³ = m³")
    print(f"   ")
    print(f"   In natural units (ℏ=c=1): [length] = [energy]⁻¹")
    print(f"   Therefore: [m³] = [energy]⁻³ = [eV]⁻³")
    print(f"   ")
    print(f"   **DIMENSIONAL MISMATCH**: [GeV⁻²] ≠ [eV⁻³]")
    print(f"   ")
    print(f"   Possible explanations:")
    print(f"     (a) Coincidence: numerology (most likely)")
    print(f"     (b) Missing factor with dimensions [energy]")
    print(f"     (c) Implicit unit conversion creates hidden constant")

    # UNIT CONVERSION EXPLORATION
    print(f"\n4. UNIT CONVERSION ANALYSIS")
    print(f"   " + "-"*76)

    # Convert R_proj³ to GeV^-3 in natural units
    # 1 m = (ℏc)^-1 in energy units
    # ℏc ≈ 1.973e-7 eV·m
    energy_per_meter = 1 / HBAR_C_EV_M  # eV/m
    R_proj_eV_inv = R_proj_m * energy_per_meter  # R_proj in eV^-1
    R_proj_cube_eV3 = R_proj_eV_inv**3  # in eV^-3
    R_proj_cube_GeV3 = R_proj_cube_eV3 / (1e9**3)  # in GeV^-3

    print(f"   Converting R_proj³ to natural units:")
    print(f"     1 m = (ℏc)⁻¹ ≈ {energy_per_meter:.3e} eV")
    print(f"     R_proj = {R_proj_m} m = {R_proj_eV_inv:.3e} eV⁻¹")
    print(f"     R_proj³ = {R_proj_cube_eV3:.3e} eV⁻³")
    print(f"     R_proj³ = {R_proj_cube_GeV3:.3e} GeV⁻³")
    print(f"   ")
    print(f"   Still wrong dimension: need GeV⁻², have GeV⁻³")
    print(f"   Required factor: Λ ~ (R_proj³ / G_F)^(1/3) × (R_proj)^-1")

    Lambda_req = (R_proj_cube / G_F)**(1/3) / R_proj_m
    print(f"     Λ ≈ {Lambda_req:.3e} m⁻¹ = {Lambda_req * HBAR_C_EV_M:.3e} eV")
    print(f"   ")
    print(f"   **This is NOT a QCT parameter!** → likely numerical coincidence")

    # PHYSICAL INTERPRETATION (if real)
    print(f"\n5. HYPOTHETICAL PHYSICAL MECHANISM")
    print(f"   " + "-"*76)
    print(f"   IF the correlation were physical (despite dimensional issues):")
    print(f"   ")
    print(f"   G_F = κ × R_proj³  (where κ has dimensions [energy²·length⁻³])")
    print(f"   ")
    print(f"   Interpretation:")
    print(f"     • Weak interaction strength ∝ neutrino condensate volume")
    print(f"     • V_cond = (4π/3) R_proj³ = {4*math.pi/3 * R_proj_cube:.3e} m³")
    print(f"     • β-decay rate enhanced by collective coherence")
    print(f"   ")
    print(f"   Testable prediction:")
    print(f"     • On ISS: R_proj changes by ~6% (gravity weakening)")
    print(f"     • G_F should change by ~(1.06)³ ≈ 19% (!)")
    print(f"     • Current precision: 0.05 ppm → easily detectable IF true")
    print(f"   ")
    print(f"   **Status: Likely numerical coincidence, not physical**")

    # STATISTICAL SIGNIFICANCE
    print(f"\n6. STATISTICAL ASSESSMENT")
    print(f"   " + "-"*76)
    print(f"   Given:")
    print(f"     • 51 CODATA constants")
    print(f"     • 16 QCT parameters")
    print(f"     • ~10 operations tested (ratios, powers, products)")
    print(f"   ")
    print(f"   Expected false positives at 2% threshold:")
    print(f"     N_false ≈ 51 × 16 × 10 × 0.02 ≈ 163 correlations")
    print(f"   ")
    print(f"   Observed: 1.62% numerical match")
    print(f"   → Well within random expectation!")
    print(f"   ")
    print(f"   **Conclusion: Insufficient evidence for physical connection**")

    # SUMMARY
    print(f"\n" + "="*80)
    print(f"SUMMARY:")
    print(f"  ✓ Numerical match: R_proj³ ≈ G_F with 1.62% error (ignoring units)")
    print(f"  ✓ Power law: G_F ∝ R_proj^3.004 (exponent error 0.14%)")
    print(f"  ✗ Dimensional inconsistency: [m³] ≠ [GeV⁻²]")
    print(f"  ✗ Statistical significance: within random expectation")
    print(f"  ✗ No known physical mechanism")
    print(f"  ")
    print(f"  **VERDICT: Numerical coincidence, not a physical prediction**")
    print(f"="*80)

    return {
        'R_proj_m': R_proj_m,
        'G_F': G_F,
        'numerical_error': relative_error,
        'exponent': exponent,
        'exponent_error': abs(exponent - 3.0) / 3.0,
        'verdict': 'coincidence'
    }

# ==============================================================================
# MULTI-PARAMETER CORRELATION SEARCH
# ==============================================================================

def search_complex_correlations(codata: Dict, threshold=0.01):
    """
    Search for correlations involving combinations of QCT parameters.

    Examples:
        - CODATA ∝ (QCT1 × QCT2)
        - CODATA ∝ QCT1 / QCT2
        - CODATA ∝ √(QCT1 × QCT2)
        - etc.
    """
    print("\n" + "="*80)
    print("MULTI-PARAMETER CORRELATION SEARCH")
    print("="*80)
    print(f"Threshold: {threshold*100}% error")

    correlations = []

    # Extract QCT numerical values
    qct_names = list(QCT_PARAMS.keys())

    # 2-parameter combinations
    print("\nSearching 2-parameter combinations...")
    count = 0

    for i, name1 in enumerate(qct_names):
        val1 = QCT_PARAMS[name1]['value']

        for j, name2 in enumerate(qct_names):
            if i >= j:
                continue

            val2 = QCT_PARAMS[name2]['value']

            if val1 == 0 or val2 == 0:
                continue

            # Operations
            operations = [
                (f"{name1} × {name2}", val1 * val2),
                (f"{name1} / {name2}", val1 / val2 if val2 != 0 else 0),
                (f"√({name1} × {name2})", math.sqrt(abs(val1 * val2))),
                (f"{name1}² / {name2}", val1**2 / val2 if val2 != 0 else 0),
                (f"{name1} / {name2}²", val1 / val2**2 if val2 != 0 else 0),
            ]

            for op_name, op_val in operations:
                if op_val == 0 or abs(op_val) > 1e50:
                    continue

                # Compare to CODATA
                for codata_name, codata_info in codata.items():
                    codata_val = abs(codata_info['value'])

                    if codata_val == 0 or codata_val > 1e50:
                        continue

                    # Check ratio (with various scalings)
                    for scale in [1, 1e-3, 1e3, 1e-6, 1e6, 1e-9, 1e9, 1e-12, 1e12]:
                        scaled_op = op_val * scale

                        error = abs(scaled_op - codata_val) / codata_val

                        if error < threshold:
                            scale_str = f"×10^{int(math.log10(scale))}" if scale != 1 else ""
                            correlations.append({
                                'qct_formula': op_name + scale_str,
                                'qct_value': scaled_op,
                                'codata_name': codata_name,
                                'codata_value': codata_val,
                                'error': error,
                                'scale': scale
                            })
                            count += 1

    print(f"Found {len(correlations)} correlations at <{threshold*100}% threshold")

    # Sort by error
    correlations.sort(key=lambda x: x['error'])

    # Display top 30
    print(f"\nTop 30 multi-parameter correlations:")
    print("-" * 120)

    for i, corr in enumerate(correlations[:30], 1):
        print(f"\n{i}. {corr['codata_name']} ≈ {corr['qct_formula']}")
        print(f"    QCT: {corr['qct_value']:.6e}")
        print(f"    CODATA: {corr['codata_value']:.6e}")
        print(f"    Error: {corr['error']*100:.6f}%")

    return correlations

# ==============================================================================
# MONTE CARLO FALSE-POSITIVE TEST
# ==============================================================================

def monte_carlo_false_positives(n_trials=1000, threshold=0.05):
    """
    Estimate expected number of false correlations via random sampling.
    """
    print("\n" + "="*80)
    print("MONTE CARLO FALSE-POSITIVE ANALYSIS")
    print("="*80)

    n_codata = 51
    n_qct = 16
    n_ops = 10

    false_pos_counts = []

    for trial in range(n_trials):
        # Generate random values (log-uniform distribution)
        codata_random = [10**random.uniform(-50, 50) for _ in range(n_codata)]
        qct_random = [10**random.uniform(-20, 20) for _ in range(n_qct)]

        # Count matches
        matches = 0
        for c_val in codata_random:
            for q_val in qct_random:
                # Test operations
                tests = [c_val/q_val, q_val/c_val, c_val*q_val, c_val**2/q_val]

                for result in tests:
                    if abs(result - 1.0) < threshold:
                        matches += 1

        false_pos_counts.append(matches)

    mean_false = sum(false_pos_counts) / len(false_pos_counts)
    std_false = (sum((x - mean_false)**2 for x in false_pos_counts) / len(false_pos_counts))**0.5

    print(f"\nTrials: {n_trials}")
    print(f"Expected false positives (mean ± std): {mean_false:.1f} ± {std_false:.1f}")
    print(f"95% CI: [{mean_false - 2*std_false:.1f}, {mean_false + 2*std_false:.1f}]")
    print(f"\nConclusion: Most correlations at {threshold*100}% threshold are noise.")

    return {'mean': mean_false, 'std': std_false}

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

def main():
    print("="*80)
    print("DEEP CODATA-QCT CORRELATION ANALYSIS (v2.0 CORRECTED)")
    print("="*80)

    # Load CODATA
    csv_path = "/home/user/QCT_9/QCT_7-QCT/literature/Fundamental Physical Constants Complete Listing 2022 CODATA adjustment.csv"
    codata = parse_codata_csv(csv_path)
    print(f"\nLoaded {len(codata)} CODATA 2022 constants")
    print(f"Loaded {len(QCT_PARAMS)} QCT parameters")

    # Run analyses
    print("\n" + "="*80)
    print("ANALYSIS 1: Fermi Constant G_F ∝ R_proj³")
    print("="*80)
    gf_result = analyze_fermi_constant_detailed()

    print("\n" + "="*80)
    print("ANALYSIS 2: Monte Carlo False-Positive Test")
    print("="*80)
    mc_result = monte_carlo_false_positives(n_trials=500, threshold=0.02)

    print("\n" + "="*80)
    print("ANALYSIS 3: Multi-Parameter Correlations")
    print("="*80)
    multi_corr = search_complex_correlations(codata, threshold=0.005)

    # Final summary
    print("\n" + "="*80)
    print("FINAL SUMMARY")
    print("="*80)
    print(f"\n1. G_F correlation:")
    print(f"   Numerical match: {(1-gf_result['numerical_error'])*100:.2f}%")
    print(f"   Exponent error: {gf_result['exponent_error']*100:.3f}%")
    print(f"   Verdict: {gf_result['verdict'].upper()}")
    print(f"\n2. False-positive expectation:")
    print(f"   Random correlations: {mc_result['mean']:.0f} ± {mc_result['std']:.0f}")
    print(f"\n3. Multi-parameter search:")
    print(f"   Found {len(multi_corr)} correlations at <0.5% threshold")
    print(f"   Most likely: numerical artifacts + look-elsewhere effect")
    print(f"\n{'='*80}")
    print("RECOMMENDATION: Focus on QCT's established predictions")
    print("(baryon masses, Higgs VEV relations, cosmological evolution)")
    print("rather than searching for new numerical coincidences.")
    print("="*80)

if __name__ == "__main__":
    main()
