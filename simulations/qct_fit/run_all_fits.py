#!/usr/bin/env python3
"""
QCT-FIT: Master Execution Script

Runs complete QCT fitting workflow:
    1. Fit Ω to ALICE Λ/p strangeness enhancement
    2. Fit γ to ALICE v₂ ridge data
    3. Cross-validate γ_ridge vs γ_GW

Usage:
    python run_all_fits.py [--data-dir PATH] [--output-dir PATH]
"""

import argparse
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from qct_fit.strangeness_fit import fit_omega_to_lambda_p_ratio
from qct_fit.ridge_fit import fit_gamma_to_v2
from qct_fit.consistency_check import cross_validate_gamma


def run_qct_fit_workflow(
    data_dir: str = "simulations/qct_fit/data",
    output_dir: str = "results/qct_fit",
    use_real_data: bool = False
):
    """
    Execute complete QCT-FIT workflow.

    Args:
        data_dir: Directory containing ALICE data files
        output_dir: Output directory for results
        use_real_data: If True, load real ALICE data; otherwise use mock data
    """

    print("\n" + "="*70)
    print(" "*15 + "QCT-FIT NUMERICAL PROTOCOL")
    print(" "*10 + "Vacuum Parameter Extraction from ALICE Data")
    print("="*70)

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # ========================================================================
    # STEP 1: Strangeness Enhancement (Ω fit)
    # ========================================================================
    print("\n" + "-"*70)
    print("STEP 1: Strangeness Enhancement — Conformal Factor Ω")
    print("-"*70)

    lambda_p_file = None
    if use_real_data:
        lambda_p_file = f"{data_dir}/alice_lambda_p.csv"
        if not os.path.exists(lambda_p_file):
            print(f"Warning: {lambda_p_file} not found. Using mock data.")
            lambda_p_file = None

    omega_results = fit_omega_to_lambda_p_ratio(
        data_file=lambda_p_file,
        plot=True,
        save_results=True,
        output_dir=output_dir
    )

    if not omega_results:
        print("✗ Ω fit failed. Aborting workflow.")
        return

    print(f"\n✓ Ω fit completed:")
    print(f"  α = {omega_results['alpha']:.4f} ± {omega_results['alpha_err']:.4f}")
    print(f"  x₀ = {omega_results['x0']:.2f} ± {omega_results['x0_err']:.2f}")

    # ========================================================================
    # STEP 2: Ridge / v₂ (γ fit)
    # ========================================================================
    print("\n" + "-"*70)
    print("STEP 2: Ridge / v₂ Anisotropy — Dissipation Parameter γ")
    print("-"*70)

    v2_file = None
    if use_real_data:
        v2_file = f"{data_dir}/alice_v2_pp.csv"
        if not os.path.exists(v2_file):
            print(f"Warning: {v2_file} not found. Using mock data.")
            v2_file = None

    ridge_results = fit_gamma_to_v2(
        data_file=v2_file,
        plot=True,
        save_results=True,
        output_dir=output_dir
    )

    if not ridge_results:
        print("✗ γ fit failed. Aborting workflow.")
        return

    print(f"\n✓ γ fit completed:")
    print(f"  γ = {ridge_results['gamma']:.5f} ± {ridge_results['gamma_err']:.5f}")
    print(f"  A = {ridge_results['A']:.5f} ± {ridge_results['A_err']:.5f}")

    # ========================================================================
    # STEP 3: Cross-Consistency Check
    # ========================================================================
    print("\n" + "-"*70)
    print("STEP 3: Cross-Consistency — γ_ridge vs γ_GW")
    print("-"*70)

    consistency_report = cross_validate_gamma(
        gamma_ridge=ridge_results['gamma'],
        gamma_ridge_err=ridge_results['gamma_err'],
        gamma_gw_upper=0.02,  # LIGO/Virgo upper bound
        plot=True,
        save_results=True,
        output_dir=output_dir
    )

    # ========================================================================
    # FINAL SUMMARY
    # ========================================================================
    print("\n" + "="*70)
    print(" "*20 + "QCT-FIT WORKFLOW COMPLETED")
    print("="*70)

    print("\nFitted Parameters:")
    print(f"  1. Conformal factor:    α = {omega_results['alpha']:.4f} ± {omega_results['alpha_err']:.4f}")
    print(f"                          x₀ = {omega_results['x0']:.2f} ± {omega_results['x0_err']:.2f}")
    print(f"  2. Vacuum dissipation:  γ = {ridge_results['gamma']:.5f} ± {ridge_results['gamma_err']:.5f}")
    print(f"  3. Source amplitude:    A = {ridge_results['A']:.5f} ± {ridge_results['A_err']:.5f}")

    print(f"\nFit Quality:")
    print(f"  Ω fit:  χ²/dof = {omega_results['chi2_reduced']:.2f} ({omega_results['fit_quality']})")
    print(f"  γ fit:  χ²/dof = {ridge_results['chi2_reduced']:.2f} ({ridge_results['fit_quality']})")

    print(f"\nConsistency Check:")
    print(f"  Status: {consistency_report['status']}")
    print(f"  Conclusion: {consistency_report['conclusion']}")
    print(f"  Tension: {consistency_report['tension_sigma']:.2f}σ")

    print(f"\nPhysical Interpretation:")
    print(f"  {consistency_report['interpretation']}")

    print(f"\nResults saved to: {output_dir}/")
    print(f"  - strangeness_fit_results.json")
    print(f"  - ridge_v2_fit_results.json")
    print(f"  - consistency_check_report.json")
    print(f"  - *.png (diagnostic plots)")

    print("\n" + "="*70)

    # Final verdict
    if consistency_report['status'] == 'PASS' and ridge_results['gamma'] < 0.01:
        print("\n✓✓ QCT VACUUM HYPOTHESIS VALIDATED ✓✓")
        print("   → Single dissipation parameter γ ≪ 1 across all scales")
        print("   → Vacuum behaves as nearly ideal superfluid")
        print("   → QCD hydrodynamics fails to explain γ < 0.01")
    elif consistency_report['status'] == 'PASS':
        print("\n✓ QCT VACUUM HYPOTHESIS PLAUSIBLE")
        print("   → γ_ridge consistent with γ_GW")
        print("   → Further investigation recommended")
    else:
        print("\n✗ QCT VACUUM HYPOTHESIS CHALLENGED")
        print("   → γ_ridge > γ_GW upper bound")
        print("   → May indicate systematic effects or QCT modification needed")

    print("="*70 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description='QCT-FIT: Extract vacuum parameters from ALICE data',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with mock data (for testing)
  python run_all_fits.py

  # Run with real ALICE data
  python run_all_fits.py --use-real-data --data-dir data/alice

  # Specify custom output directory
  python run_all_fits.py --output-dir my_results/
        """
    )

    parser.add_argument(
        '--data-dir',
        type=str,
        default='simulations/qct_fit/data',
        help='Directory containing ALICE data files (default: simulations/qct_fit/data)'
    )

    parser.add_argument(
        '--output-dir',
        type=str,
        default='results/qct_fit',
        help='Output directory for results (default: results/qct_fit)'
    )

    parser.add_argument(
        '--use-real-data',
        action='store_true',
        help='Use real ALICE data instead of mock data'
    )

    args = parser.parse_args()

    run_qct_fit_workflow(
        data_dir=args.data_dir,
        output_dir=args.output_dir,
        use_real_data=args.use_real_data
    )


if __name__ == "__main__":
    main()
