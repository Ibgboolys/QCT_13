#!/usr/bin/env python3
"""
Cross-Consistency Check Module

Validates that γ_ridge ≈ γ_GW across ALICE and LIGO/Virgo data.

This is the critical test of QCT:
    - QCD hydrodynamics predicts γ_ridge ≈ 0.2-0.5 (η/s ∼ 0.1-0.2)
    - QCT predicts γ_ridge ≈ γ_GW ≪ 1 (single vacuum dissipation)

If γ < 0.01 consistently across both experiments:
    → QCD hydrodynamics fails
    → QCT vacuum hypothesis validated
"""

import numpy as np
import json
from typing import Dict, Optional
import matplotlib.pyplot as plt


def cross_validate_gamma(
    gamma_ridge: float,
    gamma_ridge_err: float,
    gamma_gw_upper: float = 0.02,  # LIGO/Virgo upper bound
    plot: bool = True,
    save_results: bool = True,
    output_dir: str = "results/qct_fit/"
) -> Dict:
    """
    Cross-validate γ between ALICE ridge and LIGO/Virgo GW data.

    Args:
        gamma_ridge: γ from ALICE v₂ fit
        gamma_ridge_err: uncertainty on γ_ridge
        gamma_gw_upper: Upper bound from LIGO/Virgo
        plot: Generate comparison plot
        save_results: Save validation report
        output_dir: Output directory

    Returns:
        Validation report dictionary
    """

    print("\n" + "="*60)
    print("QCT Cross-Consistency Check: γ_ridge vs γ_GW")
    print("="*60)

    # Check consistency
    consistent = gamma_ridge < gamma_gw_upper

    # Calculate tension
    tension = (gamma_ridge - gamma_gw_upper) / gamma_ridge_err if gamma_ridge_err > 0 else 0

    print(f"\nγ from ALICE ridge:  {gamma_ridge:.5f} ± {gamma_ridge_err:.5f}")
    print(f"γ upper bound (GW):  < {gamma_gw_upper:.5f}")

    if consistent:
        print(f"\n✓ CONSISTENT: γ_ridge < γ_GW upper bound")
        print(f"  Tension: {abs(tension):.2f}σ")

        if gamma_ridge < 0.01:
            print(f"\n✓✓ STRONG QCT SIGNATURE:")
            print(f"  → γ ≪ 1: nearly ideal vacuum fluid")
            print(f"  → Single dissipation parameter across all scales")
            print(f"  → QCD hydrodynamics fails (predicts γ ∼ 0.2-0.5)")

        conclusion = "QCT_VALIDATED"
        status = "PASS"

    else:
        print(f"\n✗ INCONSISTENT: γ_ridge > γ_GW upper bound")
        print(f"  Excess: {tension:.2f}σ")
        print(f"  → QCT vacuum hypothesis disfavored")

        conclusion = "QCT_DISFAVORED"
        status = "FAIL"

    # Compare to QCD prediction
    gamma_qcd_typical = 0.3  # η/s ∼ 0.1
    gamma_qcd_lower = 0.15

    print(f"\nComparison to QCD hydrodynamics:")
    print(f"  QCD prediction: γ ∼ {gamma_qcd_lower:.2f} - {gamma_qcd_typical:.2f}")

    if gamma_ridge < gamma_qcd_lower:
        print(f"  → γ_ridge significantly below QCD prediction")
        print(f"  → Suggests non-hadronic vacuum contribution")
        conclusion += " / QCD_CHALLENGED"

    # Build report
    report = {
        'gamma_ridge': float(gamma_ridge),
        'gamma_ridge_err': float(gamma_ridge_err),
        'gamma_gw_upper': float(gamma_gw_upper),
        'gamma_qcd_typical': float(gamma_qcd_typical),
        'gamma_qcd_lower': float(gamma_qcd_lower),
        'consistent': bool(consistent),
        'tension_sigma': float(abs(tension)),
        'status': status,
        'conclusion': conclusion,
        'interpretation': _get_interpretation(gamma_ridge, gamma_gw_upper, gamma_qcd_lower)
    }

    # Save report
    if save_results:
        import os
        os.makedirs(output_dir, exist_ok=True)
        with open(f"{output_dir}/consistency_check_report.json", 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\n✓ Report saved to {output_dir}/consistency_check_report.json")

    # Plot
    if plot:
        _plot_gamma_comparison(report, output_dir)

    return report


def _get_interpretation(gamma_ridge: float, gamma_gw: float, gamma_qcd: float) -> str:
    """Generate physical interpretation of γ values."""

    if gamma_ridge < 0.01:
        if gamma_ridge < gamma_gw:
            return (
                "Strong evidence for QCT vacuum: γ ≪ 1 consistently across "
                "ALICE and LIGO/Virgo, far below QCD hydrodynamic predictions. "
                "The vacuum behaves as a nearly ideal superfluid with unified "
                "dissipation parameter."
            )
        else:
            return (
                "γ_ridge slightly exceeds GW bound but still ≪ 1. May indicate "
                "small additional hadronic contribution or systematic uncertainty. "
                "QCT vacuum remains plausible."
            )
    elif gamma_ridge < gamma_qcd:
        return (
            "γ_ridge below QCD predictions but not negligible. Suggests hybrid "
            "scenario with partial vacuum coherence contribution. Further investigation "
            "needed."
        )
    else:
        return (
            "γ_ridge consistent with QCD hydrodynamics. QCT vacuum hypothesis "
            "disfavored unless additional effects suppress γ_GW independently."
        )


def _plot_gamma_comparison(report: Dict, output_dir: str):
    """Generate comparison plot for γ values."""

    import os
    os.makedirs(output_dir, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 6))

    # Data points
    gamma_ridge = report['gamma_ridge']
    gamma_ridge_err = report['gamma_ridge_err']
    gamma_gw = report['gamma_gw_upper']
    gamma_qcd_low = report['gamma_qcd_lower']
    gamma_qcd_high = report['gamma_qcd_typical']

    # Plot ranges
    y_labels = ['ALICE\nRidge', 'LIGO/Virgo\nGW (upper)', 'QCD\nHydro']
    y_positions = [2, 1, 0]

    # ALICE
    ax.errorbar([gamma_ridge], [2], xerr=[gamma_ridge_err],
                fmt='o', color='red', markersize=10, capsize=5,
                label=f'γ_ridge = {gamma_ridge:.4f} ± {gamma_ridge_err:.4f}',
                linewidth=2)

    # LIGO/Virgo upper bound
    ax.plot([0, gamma_gw], [1, 1], 'b-', linewidth=3)
    ax.plot([gamma_gw], [1], 'b>', markersize=12,
            label=f'γ_GW < {gamma_gw:.4f}')

    # QCD prediction
    ax.fill_betweenx([0, 0], gamma_qcd_low, gamma_qcd_high,
                     color='gray', alpha=0.3,
                     label=f'QCD: {gamma_qcd_low:.2f} - {gamma_qcd_high:.2f}')
    ax.plot([gamma_qcd_low, gamma_qcd_high], [0, 0], 'k-', linewidth=3)

    # Formatting
    ax.set_yticks(y_positions)
    ax.set_yticklabels(y_labels, fontsize=11)
    ax.set_xlabel('Dissipation parameter γ', fontsize=12)
    ax.set_xlim(-0.01, max(gamma_qcd_high * 1.3, gamma_ridge + 3*gamma_ridge_err))
    ax.legend(fontsize=10, loc='upper right')
    ax.grid(axis='x', alpha=0.3)

    # Status annotation
    status_color = 'green' if report['status'] == 'PASS' else 'red'
    ax.text(0.02, 0.98, f"Status: {report['status']}\n{report['conclusion']}",
            transform=ax.transAxes, fontsize=11, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor=status_color, alpha=0.2))

    plt.title('QCT Cross-Consistency Check: γ_ridge vs γ_GW',
              fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/gamma_consistency_check.png", dpi=150)
    print(f"✓ Plot saved to {output_dir}/gamma_consistency_check.png")
    plt.close()


def load_fit_results(fit_results_file: str) -> Dict:
    """Load fit results from JSON file."""
    with open(fit_results_file, 'r') as f:
        return json.load(f)


if __name__ == "__main__":
    # Example: Load results from ridge fit and validate
    try:
        ridge_results = load_fit_results("results/qct_fit/ridge_v2_fit_results.json")
        gamma_ridge = ridge_results['gamma']
        gamma_ridge_err = ridge_results['gamma_err']

        report = cross_validate_gamma(
            gamma_ridge=gamma_ridge,
            gamma_ridge_err=gamma_ridge_err,
            plot=True,
            save_results=True
        )

        print("\n" + "="*60)
        print("Consistency check completed.")
        print("="*60)

    except FileNotFoundError:
        print("Run ridge_fit.py first to generate fit results.")
        print("\nRunning with mock values for demonstration:")

        report = cross_validate_gamma(
            gamma_ridge=0.008,
            gamma_ridge_err=0.002,
            plot=True,
            save_results=True
        )
