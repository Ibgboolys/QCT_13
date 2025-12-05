#!/usr/bin/env python3
"""
CODATA 2022 - QCT Parameter Correlation Analysis
================================================
Author: Boleslav Plhák + AI (Claude)
Date: 2025-11-16

Systematically analyzes correlations between CODATA 2022 fundamental
physical constants and QCT parameters to discover hidden mathematical
relationships.
"""

import csv
import math
from typing import Dict, List, Tuple

# ============================================================================
# QCT PARAMETERS (from CLAUDE.md)
# ============================================================================

QCT_PARAMS = {
    # Fitted parameters
    'lambda_micro_GeV': 0.733,  # GeV
    'sigma2_max': 0.2,  # dimensionless
    'alpha': -9e11,  # dimensionless (huge negative)
    'S_tot': 58,  # exact integer

    # Derived/measured
    'n_nu_cm3': 336,  # cm^-3
    'n_nu_m3': 336e6,  # m^-3
    'v_Higgs_GeV': 246.22,  # GeV
    'Lambda_QCT_TeV': 145,  # TeV
    'm_nu_eV': 0.1,  # eV (typical)

    # Additional derived
    'E_pair_eV': 5.38e18,  # eV
    'lambda_screen_m': 40e-6,  # m (40 μm)
    'R_proj_m': 0.0228,  # m (2.28 cm)

    # Mathematical constants discovered
    'S_tot_over_21': 58/21,  # ≈ e (2.76 vs 2.718)
    'S_tot_over_56': 58/56,  # ≈ k_Coulomb (1.036 vs 1.0364)

    # Golden ratio relations
    'phi': (1 + math.sqrt(5))/2,  # φ ≈ 1.618
    'v_Higgs_over_lambda': 246.22/0.733,  # ≈ φ^12.088
}

# ============================================================================
# PHYSICAL CONSTANTS (for conversion)
# ============================================================================

CONSTANTS = {
    'c': 2.99792458e8,  # m/s
    'hbar': 1.054571817e-34,  # J·s
    'hbar_eV_s': 6.582119569e-16,  # eV·s
    'G_N': 6.67430e-11,  # m³/(kg·s²)
    'eV_to_J': 1.602176634e-19,  # J/eV
    'GeV_to_eV': 1e9,
    'TeV_to_eV': 1e12,
}

# ============================================================================
# LOAD CODATA DATA
# ============================================================================

def parse_codata_csv(filepath: str) -> Dict[str, Dict[str, float]]:
    """
    Parse CODATA text file (not standard CSV) with fixed-width columns.

    Returns:
        Dict mapping quantity name to {'value': float, 'uncertainty': float, 'unit': str}
    """
    data = {}

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

        for line in lines:
            # Skip empty lines
            if not line.strip():
                continue

            # Skip header and separator lines
            if ('Quantity' in line or '---' in line or
                'From:' in line or 'CODATA' in line or
                'Fundamental' in line):
                continue

            # Try to parse the line
            # Format: Quantity (60 chars) Value (24 chars) Uncertainty (24 chars) Unit (rest)
            try:
                # Split by multiple spaces to separate columns
                parts = line.split('  ')
                parts = [p.strip() for p in parts if p.strip()]

                if len(parts) < 3:
                    continue

                quantity = parts[0]
                value_str = parts[1] if len(parts) > 1 else ''
                uncertainty_str = parts[2] if len(parts) > 2 else ''
                unit = parts[3] if len(parts) > 3 else ''

                if not quantity or not value_str:
                    continue

                # Parse value (handle scientific notation with space)
                value_str_clean = value_str.replace(' ', '')

                # Handle exact values
                if '(exact)' in uncertainty_str:
                    if '...' in value_str_clean:
                        value_str_clean = value_str_clean.replace('...', '')

                    # Parse with 'e' notation
                    if 'e' in value_str_clean:
                        # Format: "299792458" or "1.23e-45"
                        value = float(value_str_clean)
                    else:
                        value = float(value_str_clean)
                    uncertainty = 0.0
                else:
                    # Parse value with possible 'e' notation
                    if 'e' in value_str_clean:
                        value = float(value_str_clean)
                    else:
                        value = float(value_str_clean)

                    # Parse uncertainty
                    unc_str_clean = uncertainty_str.replace(' ', '')
                    if 'e' in unc_str_clean:
                        uncertainty = float(unc_str_clean)
                    else:
                        uncertainty = float(unc_str_clean)

                data[quantity] = {
                    'value': value,
                    'uncertainty': uncertainty,
                    'unit': unit,
                    'relative_unc': uncertainty/abs(value) if value != 0 and uncertainty != 0 else 0.0
                }
            except (ValueError, IndexError) as e:
                # Skip unparseable rows
                continue

    return data

# ============================================================================
# CORRELATION ANALYSIS
# ============================================================================

def find_ratio_correlations(codata: Dict, qct_params: Dict,
                            max_error: float = 0.05) -> List[Tuple]:
    """
    Find ratios between CODATA constants and QCT parameters.

    Args:
        codata: CODATA constants dictionary
        qct_params: QCT parameters
        max_error: Maximum relative error to consider (default 5%)

    Returns:
        List of tuples: (codata_name, qct_name, ratio, error, description)
    """
    correlations = []

    for codata_name, codata_data in codata.items():
        codata_val = codata_data['value']

        if codata_val == 0:
            continue

        for qct_name, qct_val in qct_params.items():
            if qct_val == 0:
                continue

            # Try direct ratio
            ratio = codata_val / qct_val

            # Check if ratio is "interesting" (close to simple values)
            interesting_values = [
                1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                1/2, 1/3, 1/4, 1/6, 2/3, 3/2, 3/4,
                math.pi, math.e, math.sqrt(2), math.sqrt(3), math.sqrt(5),
                (1+math.sqrt(5))/2,  # golden ratio
                56, 58, 336, 246, 137  # QCT special numbers
            ]

            for target in interesting_values:
                error = abs(ratio - target) / target if target != 0 else float('inf')

                if error < max_error:
                    correlations.append((
                        codata_name,
                        qct_name,
                        ratio,
                        target,
                        error,
                        f"{codata_name} / {qct_name} ≈ {target:.4f}"
                    ))

    return correlations

def find_product_correlations(codata: Dict, qct_params: Dict,
                              max_error: float = 0.05) -> List[Tuple]:
    """
    Find products between CODATA constants and QCT parameters that give
    simple values.
    """
    correlations = []

    for codata_name, codata_data in codata.items():
        codata_val = codata_data['value']

        if codata_val == 0:
            continue

        for qct_name, qct_val in qct_params.items():
            if qct_val == 0:
                continue

            # Try product
            product = codata_val * qct_val

            # Interesting target values
            interesting_values = [
                1, 10, 100, 1000, 1e4, 1e5, 1e6, 1e9, 1e12,
                math.pi, math.e, 137, 246, 336, 58, 56
            ]

            for target in interesting_values:
                error = abs(product - target) / target if target != 0 else float('inf')

                if error < max_error:
                    correlations.append((
                        codata_name,
                        qct_name,
                        product,
                        target,
                        error,
                        f"{codata_name} × {qct_name} ≈ {target:.4f}"
                    ))

    return correlations

def find_power_relations(codata: Dict, qct_params: Dict,
                         max_error: float = 0.05) -> List[Tuple]:
    """
    Find power relations: codata_val ≈ qct_val^n for simple n.
    """
    correlations = []

    for codata_name, codata_data in codata.items():
        codata_val = abs(codata_data['value'])

        if codata_val == 0 or codata_val < 1e-100:
            continue

        for qct_name, qct_val in qct_params.items():
            if abs(qct_val) <= 1e-100:
                continue

            # Try to find exponent
            try:
                exponent = math.log(codata_val) / math.log(abs(qct_val))
            except (ValueError, ZeroDivisionError):
                continue

            # Check if exponent is close to simple values
            simple_exponents = [
                0.5, 1, 1.5, 2, 2.5, 3, 4, 5, 6, 10, 12,
                -0.5, -1, -1.5, -2, -3, -4
            ]

            for target_exp in simple_exponents:
                error = abs(exponent - target_exp) / abs(target_exp) if target_exp != 0 else float('inf')

                if error < max_error:
                    predicted = abs(qct_val) ** target_exp
                    correlations.append((
                        codata_name,
                        qct_name,
                        exponent,
                        target_exp,
                        error,
                        f"{codata_name} ≈ {qct_name}^{target_exp:.1f}"
                    ))

    return correlations

def analyze_specific_qct_relations(codata: Dict) -> List[str]:
    """
    Analyze specific QCT-relevant relations in CODATA data.
    """
    results = []

    # Extract key CODATA values
    alpha_em = codata.get('fine-structure constant', {}).get('value', 7.297352564e-3)
    m_e = codata.get('electron mass energy equivalent in MeV', {}).get('value', 0.51099895)  # MeV
    m_p = codata.get('proton mass energy equivalent in MeV', {}).get('value', 938.272089)  # MeV
    m_n = codata.get('neutron mass energy equivalent in MeV', {}).get('value', 939.565421)  # MeV
    G = codata.get('Newtonian constant of gravitation', {}).get('value', 6.67430e-11)

    # 1. Check S_tot = n_ν/6 + 2
    n_nu = 336
    S_tot_predicted = n_nu/6 + 2
    results.append(f"\n=== QCT Core Relations ===")
    results.append(f"S_tot = n_ν/6 + 2 = {n_nu}/6 + 2 = {S_tot_predicted:.1f} (exact: 58)")
    results.append(f"Error: {abs(S_tot_predicted - 58):.6f} (should be 0)")

    # 2. Coulomb constant relation
    k_coulomb_qct = 58/56
    results.append(f"\nk_Coulomb (QCT) = S_tot/56 = {k_coulomb_qct:.6f}")
    results.append(f"k_Coulomb (expected) ≈ 1.0364")
    results.append(f"Error: {abs(k_coulomb_qct - 1.0364)/1.0364 * 100:.3f}%")

    # 3. Golden ratio in Higgs/lambda
    v_higgs = 246.22  # GeV
    lambda_micro = 0.733  # GeV
    ratio = v_higgs / lambda_micro
    phi = (1 + math.sqrt(5))/2
    expected_power = math.log(ratio) / math.log(phi)
    results.append(f"\nv_Higgs/λ_micro = {ratio:.4f}")
    results.append(f"φ^{expected_power:.4f} = {phi**expected_power:.4f}")
    results.append(f"Expected: φ^12.088 (from baryon analysis)")

    # 4. Check proton/neutrino mass ratio
    m_nu_eV = 0.1  # eV
    m_p_eV = m_p * 1e6  # Convert MeV to eV
    ratio_mp_mnu = m_p_eV / m_nu_eV
    results.append(f"\nm_p/m_ν = {ratio_mp_mnu:.4e}")
    results.append(f"f_screen = m_ν/m_p = {1/ratio_mp_mnu:.4e}")
    results.append(f"Expected f_screen ≈ 1.07×10^-10")

    # 5. Check fine structure constant relations
    alpha_inv = 1/alpha_em
    results.append(f"\nα^-1 (CODATA) = {alpha_inv:.6f}")
    results.append(f"Compare with QCT numbers: 137 (expected)")
    results.append(f"Error: {abs(alpha_inv - 137)/137 * 100:.4f}%")

    # 6. Check G relation to QCT parameters
    results.append(f"\nG_N (CODATA) = {G:.6e} m³/(kg·s²)")
    results.append(f"α (QCT coupling) = -9×10^11")
    results.append(f"Ratio |α|/G ~ {abs(-9e11/G):.4e}")

    return results

# ============================================================================
# MAIN ANALYSIS
# ============================================================================

def main():
    print("=" * 80)
    print("CODATA 2022 - QCT CORRELATION ANALYSIS")
    print("=" * 80)

    # Load CODATA data
    csv_path = '/home/user/QCT_9/QCT_7-QCT/literature/Fundamental Physical Constants Complete Listing 2022 CODATA adjustment.csv'
    print(f"\nLoading CODATA data from: {csv_path}")
    codata = parse_codata_csv(csv_path)
    print(f"Loaded {len(codata)} physical constants")

    # Display some key constants
    print("\n" + "=" * 80)
    print("KEY CODATA CONSTANTS")
    print("=" * 80)

    key_constants = [
        'fine-structure constant',
        'Newtonian constant of gravitation',
        'electron mass energy equivalent in MeV',
        'proton mass energy equivalent in MeV',
        'neutron mass energy equivalent in MeV',
        'Planck constant',
        'Planck length',
        'Planck mass',
        'speed of light in vacuum',
        'Boltzmann constant',
    ]

    for const_name in key_constants:
        if const_name in codata:
            data = codata[const_name]
            print(f"{const_name:50s}: {data['value']:.6e} {data['unit']}")

    # Analyze specific QCT relations
    print("\n" + "=" * 80)
    print("QCT-SPECIFIC RELATIONS")
    print("=" * 80)
    qct_results = analyze_specific_qct_relations(codata)
    for result in qct_results:
        print(result)

    # Find ratio correlations
    print("\n" + "=" * 80)
    print("RATIO CORRELATIONS (error < 5%)")
    print("=" * 80)
    ratio_corr = find_ratio_correlations(codata, QCT_PARAMS, max_error=0.05)
    ratio_corr.sort(key=lambda x: x[4])  # Sort by error

    for i, (codata_name, qct_name, ratio, target, error, desc) in enumerate(ratio_corr[:20]):
        print(f"{i+1:2d}. {desc}")
        print(f"    Error: {error*100:.3f}%")

    if len(ratio_corr) == 0:
        print("No significant ratio correlations found at 5% threshold.")

    # Find product correlations
    print("\n" + "=" * 80)
    print("PRODUCT CORRELATIONS (error < 5%)")
    print("=" * 80)
    product_corr = find_product_correlations(codata, QCT_PARAMS, max_error=0.05)
    product_corr.sort(key=lambda x: x[4])

    for i, (codata_name, qct_name, product, target, error, desc) in enumerate(product_corr[:20]):
        print(f"{i+1:2d}. {desc}")
        print(f"    Error: {error*100:.3f}%")

    if len(product_corr) == 0:
        print("No significant product correlations found at 5% threshold.")

    # Find power relations
    print("\n" + "=" * 80)
    print("POWER RELATIONS (error < 5%)")
    print("=" * 80)
    power_corr = find_power_relations(codata, QCT_PARAMS, max_error=0.05)
    power_corr.sort(key=lambda x: x[4])

    for i, (codata_name, qct_name, exp, target_exp, error, desc) in enumerate(power_corr[:20]):
        print(f"{i+1:2d}. {desc}")
        print(f"    Actual exponent: {exp:.4f}, Target: {target_exp:.1f}")
        print(f"    Error: {error*100:.3f}%")

    if len(power_corr) == 0:
        print("No significant power relations found at 5% threshold.")

    # Summary statistics
    print("\n" + "=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)
    print(f"Total CODATA constants analyzed: {len(codata)}")
    print(f"QCT parameters checked: {len(QCT_PARAMS)}")
    print(f"Ratio correlations found: {len(ratio_corr)}")
    print(f"Product correlations found: {len(product_corr)}")
    print(f"Power correlations found: {len(power_corr)}")
    print(f"\nTotal correlations: {len(ratio_corr) + len(product_corr) + len(power_corr)}")

    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)

if __name__ == '__main__':
    main()
