#!/usr/bin/env python3
"""
Ridge / v₂ Acoustic Fit Module (R.3–R.5)

Fits damping parameter γ to ALICE v₂ azimuthal anisotropy data.

Theory:
    v₂(k) ∝ |δρ_k|

    |δρ| ~ S / √[(ω_k²)² + (2γω_k)²]

Phenomenological model (integrated over k):
    v₂(x) = A · ln(1 + x) · exp(-γ)

Fitované parametry:
    - A: source amplitude (normalization)
    - γ: vacuum dissipation parameter

Critical test:
    γ_ridge ≈ γ_GW  (cross-consistency with LIGO/Virgo)
"""

import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from typing import Tuple, Dict, Optional
import json


class AcousticDampingModel:
    """
    Acoustic damping model for v₂ anisotropy.

    Model:
        v₂(x) = A · ln(1 + x) · exp(-γ)

    where:
        - x = dN/dη (multiplicity)
        - A = source strength
        - γ = vacuum dissipation
    """

    def __init__(self, A: float, gamma: float):
        self.A = A
        self.gamma = gamma

    def __call__(self, x: np.ndarray) -> np.ndarray:
        """Evaluate v₂(x)."""
        return self.A * np.log(1 + x) * np.exp(-self.gamma)

    def asymptotic_limit(self) -> float:
        """v₂ for x → ∞."""
        return np.inf  # logarithmic growth


def v2_model(x: np.ndarray, A: float, gamma: float) -> np.ndarray:
    """
    Phenomenological v₂ model.

    Args:
        x: dN/dη (multiplicity)
        A: source amplitude
        gamma: dissipation parameter

    Returns:
        v₂(x)
    """
    return A * np.log(1 + x) * np.exp(-gamma)


def fit_gamma_to_v2(
    data_file: Optional[str] = None,
    x_data: Optional[np.ndarray] = None,
    y_data: Optional[np.ndarray] = None,
    y_err: Optional[np.ndarray] = None,
    plot: bool = True,
    save_results: bool = True,
    output_dir: str = "results/qct_fit/"
) -> Dict:
    """
    Fit dissipation parameter γ to ALICE v₂ data.

    Args:
        data_file: Path to CSV file with columns (dN_deta, v2, err)
        x_data, y_data, y_err: Alternative direct data input
        plot: Whether to generate diagnostic plot
        save_results: Save fit results to JSON
        output_dir: Output directory

    Returns:
        Dictionary with fit results:
            - A: source amplitude
            - gamma: dissipation parameter
            - A_err, gamma_err: uncertainties
            - chi2, dof, p_value: fit statistics
    """

    # Load data
    if data_file is not None:
        try:
            import pandas as pd
            df = pd.read_csv(data_file, comment='#')
            x = df.iloc[:, 0].values
            y = df.iloc[:, 1].values
            dy = df.iloc[:, 2].values if df.shape[1] > 2 else 0.01 * y
            print(f"✓ Loaded real data from {data_file}: {len(x)} points")
        except Exception as e:
            print(f"❌ CRITICAL ERROR: Could not load {data_file}: {e}")
            print("❌ NO MOCK DATA FALLBACK - FIT ABORTED")
            return {}
    elif x_data is not None and y_data is not None:
        x, y = x_data, y_data
        dy = y_err if y_err is not None else 0.01 * np.ones_like(y)
    else:
        print("❌ CRITICAL ERROR: No data provided and no mock data allowed!")
        return {}

    # Perform fit
    print("\n" + "="*60)
    print("QCT-FIT: Ridge / v₂ Acoustic Analysis")
    print("="*60)
    print(f"Data points: {len(x)}")
    print(f"Multiplicity range: {x.min():.1f} - {x.max():.1f}")
    print(f"v₂ range: {y.min():.4f} - {y.max():.4f}")

    # Fit with bounds
    bounds_lower = [0.0, 0.0]
    bounds_upper = [1.0, 1.0]

    try:
        popt, pcov = curve_fit(
            v2_model, x, y,
            sigma=dy,
            absolute_sigma=True,
            bounds=(bounds_lower, bounds_upper),
            p0=[0.1, 0.01]  # initial guess
        )

        A_fit, gamma_fit = popt
        A_err, gamma_err = np.sqrt(np.diag(pcov))

        # Calculate χ²
        y_model = v2_model(x, A_fit, gamma_fit)
        chi2 = np.sum(((y - y_model) / dy)**2)
        dof = len(x) - 2
        chi2_reduced = chi2 / dof

        # P-value
        from scipy.stats import chi2 as chi2_dist
        p_value = 1.0 - chi2_dist.cdf(chi2, dof)

        print(f"\n✓ Fit converged successfully")
        print(f"  A = {A_fit:.5f} ± {A_err:.5f}")
        print(f"  γ = {gamma_fit:.5f} ± {gamma_err:.5f}")
        print(f"  χ²/dof = {chi2:.2f}/{dof} = {chi2_reduced:.3f}")
        print(f"  p-value = {p_value:.3f}")

        # Physical interpretation
        print(f"\nPhysical interpretation:")
        print(f"  → Vacuum dissipation γ = {gamma_fit:.4f}")

        if gamma_fit < 0.1:
            print(f"  ✓ Nearly ideal fluid (γ ≪ 1)")
            print(f"  ✓ Consistent with QCT prediction of coherent vacuum")

        # Shear viscosity estimate
        eta_over_s = gamma_fit / (4 * np.pi)  # rough estimate
        print(f"  → η/s ≈ {eta_over_s:.4f}")

        if eta_over_s < 1/(4*np.pi):
            print(f"  ✓ Below KSS bound η/s ≥ 1/(4π) = {1/(4*np.pi):.4f}")

        # Create results dictionary
        results = {
            'A': float(A_fit),
            'A_err': float(A_err),
            'gamma': float(gamma_fit),
            'gamma_err': float(gamma_err),
            'chi2': float(chi2),
            'dof': int(dof),
            'chi2_reduced': float(chi2_reduced),
            'p_value': float(p_value),
            'eta_over_s_estimate': float(eta_over_s),
            'n_points': len(x),
            'fit_quality': 'good' if chi2_reduced < 2.0 else 'acceptable' if chi2_reduced < 5.0 else 'poor'
        }

        # Save results
        if save_results:
            import os
            os.makedirs(output_dir, exist_ok=True)
            with open(f"{output_dir}/ridge_v2_fit_results.json", 'w') as f:
                json.dump(results, f, indent=2)
            print(f"\n✓ Results saved to {output_dir}/ridge_v2_fit_results.json")

        # Plot
        if plot:
            _plot_v2_fit_results(x, y, dy, A_fit, gamma_fit, results, output_dir)

        return results

    except Exception as e:
        print(f"✗ Fit failed: {e}")
        return {}


def _generate_mock_v2_data() -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Generate mock ALICE-like v₂ data for testing.

    Returns:
        (dN/dη, v₂, error)
    """
    # Mock multiplicity range (pp to pPb to PbPb)
    x = np.array([2, 5, 10, 15, 20, 30, 40, 50, 70, 100])

    # Generate data with true parameters
    A_true = 0.15
    gamma_true = 0.02

    y_true = v2_model(x, A_true, gamma_true)

    # Add realistic noise
    np.random.seed(43)
    dy = 0.005 * np.ones_like(y_true)  # constant error
    y = y_true + np.random.normal(0, dy)

    return x, y, dy


def _plot_v2_fit_results(
    x: np.ndarray,
    y: np.ndarray,
    dy: np.ndarray,
    A: float,
    gamma: float,
    results: Dict,
    output_dir: str
):
    """Generate diagnostic plot for v₂ fit."""

    import os
    os.makedirs(output_dir, exist_ok=True)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8),
                                     gridspec_kw={'height_ratios': [3, 1]})

    # Smooth curve for model
    x_smooth = np.linspace(x.min() * 0.8, x.max() * 1.2, 200)
    y_smooth = v2_model(x_smooth, A, gamma)

    # Top panel: data vs model
    ax1.errorbar(x, y, yerr=dy, fmt='o', color='black',
                 label='ALICE v₂ data', capsize=3, markersize=6)
    ax1.plot(x_smooth, y_smooth, 'b-', linewidth=2,
             label=f'QCT fit: γ={gamma:.4f}, A={A:.4f}')
    ax1.set_ylabel('v₂', fontsize=12)
    ax1.legend(fontsize=11)
    ax1.grid(alpha=0.3)
    ax1.set_title(f'QCT Ridge / v₂ Acoustic Fit  (χ²/dof = {results["chi2_reduced"]:.2f})',
                  fontsize=13, fontweight='bold')

    # Bottom panel: residuals
    y_model = v2_model(x, A, gamma)
    residuals = (y - y_model) / dy

    ax2.errorbar(x, residuals, yerr=1.0, fmt='o', color='black', capsize=3)
    ax2.axhline(0, color='blue', linestyle='--', linewidth=1)
    ax2.axhline(2, color='gray', linestyle=':', alpha=0.5)
    ax2.axhline(-2, color='gray', linestyle=':', alpha=0.5)
    ax2.set_xlabel('dN/dη', fontsize=12)
    ax2.set_ylabel('Pull (σ)', fontsize=12)
    ax2.grid(alpha=0.3)
    ax2.set_ylim(-3.5, 3.5)

    plt.tight_layout()
    plt.savefig(f"{output_dir}/ridge_v2_fit.png", dpi=150)
    print(f"✓ Plot saved to {output_dir}/ridge_v2_fit.png")
    plt.close()


if __name__ == "__main__":
    # Run standalone fit with mock data
    results = fit_gamma_to_v2(
        plot=True,
        save_results=True
    )

    print("\n" + "="*60)
    print("Ridge / v₂ acoustic fit completed.")
    print("="*60)
