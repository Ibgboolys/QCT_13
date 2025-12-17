#!/usr/bin/env python3
"""
Strangeness Enhancement Fit Module (R.1, R.2)

Fits the conformal factor Ω(dN/dη) to ALICE Λ/p ratio data.

Theory:
    Y(m) ∝ exp(-Ω(dN/dη) · m / T_fo)

    R_Λ/p(dN/dη) = exp(-Ω(dN/dη) · (m_Λ - m_p) / T_fo)

Parametrization:
    Ω(x) = 1 - α · x/(x + x₀)

Fitované parametry:
    - α ∈ (0, 1): síla zředění koherence
    - x₀ > 0: charakteristická škála přechodu pp → pA
"""

import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from typing import Tuple, Dict, Optional
import json


# === Physical constants ===
M_PROTON = 0.938      # GeV
M_LAMBDA = 1.115      # GeV
T_FREEZE = 0.160      # GeV

DELTA_M = M_LAMBDA - M_PROTON


class OmegaParametrization:
    """
    Conformal factor parametrization.

    Ω(x) = 1 - α · x/(x + x₀)

    Physical interpretation:
        - α = 0: no coherence dilution (vacuum stays pristine)
        - α → 1: strong dilution at high multiplicity
        - x₀: transition scale from pp to heavy-ion regime
    """

    def __init__(self, alpha: float, x0: float):
        self.alpha = alpha
        self.x0 = x0

    def __call__(self, x: np.ndarray) -> np.ndarray:
        """Evaluate Ω(x)."""
        return 1.0 - self.alpha * x / (x + self.x0)

    def derivative(self, x: np.ndarray) -> np.ndarray:
        """Derivative dΩ/dx."""
        return -self.alpha * self.x0 / (x + self.x0)**2


def omega_model(x: np.ndarray, alpha: float, x0: float) -> np.ndarray:
    """
    Conformal factor model.

    Args:
        x: dN/dη (multiplicity)
        alpha: dilution strength
        x0: transition scale

    Returns:
        Ω(x)
    """
    return 1.0 - alpha * x / (x + x0)


def lambda_p_ratio_model(x: np.ndarray, alpha: float, x0: float) -> np.ndarray:
    """
    Theoretical Λ/p ratio as function of multiplicity.

    R_Λ/p = exp(-Ω(x) · Δm / T_fo)

    where Δm = m_Λ - m_p

    Args:
        x: dN/dη values
        alpha: Ω parametrization parameter
        x0: Ω parametrization scale

    Returns:
        R_Λ/p(x) ratio
    """
    Om = omega_model(x, alpha, x0)
    return np.exp(-(Om * DELTA_M) / T_FREEZE)


def fit_omega_to_lambda_p_ratio(
    data_file: Optional[str] = None,
    x_data: Optional[np.ndarray] = None,
    y_data: Optional[np.ndarray] = None,
    y_err: Optional[np.ndarray] = None,
    plot: bool = True,
    save_results: bool = True,
    output_dir: str = "results/qct_fit/"
) -> Dict:
    """
    Fit conformal factor Ω to ALICE Λ/p ratio data.

    Args:
        data_file: Path to CSV file with columns (dN_deta, ratio, err)
        x_data, y_data, y_err: Alternative direct data input
        plot: Whether to generate diagnostic plot
        save_results: Save fit results to JSON
        output_dir: Output directory

    Returns:
        Dictionary with fit results:
            - alpha: fitted α parameter
            - x0: fitted x₀ parameter
            - alpha_err, x0_err: uncertainties
            - chi2: χ² statistic
            - dof: degrees of freedom
            - p_value: fit p-value
    """

    # Load data
    if data_file is not None:
        try:
            x, y, dy = np.loadtxt(data_file, unpack=True)
        except Exception as e:
            print(f"Warning: Could not load {data_file}: {e}")
            print("Using mock data for demonstration.")
            x, y, dy = _generate_mock_data()
    elif x_data is not None and y_data is not None:
        x, y = x_data, y_data
        dy = y_err if y_err is not None else 0.05 * y  # 5% default error
    else:
        print("No data provided. Using mock data for demonstration.")
        x, y, dy = _generate_mock_data()

    # Perform fit
    print("\n" + "="*60)
    print("QCT-FIT: Strangeness Enhancement Analysis")
    print("="*60)
    print(f"Data points: {len(x)}")
    print(f"Multiplicity range: {x.min():.1f} - {x.max():.1f}")
    print(f"Λ/p ratio range: {y.min():.3f} - {y.max():.3f}")

    # Fit with bounds
    bounds_lower = [0.0, 0.1]
    bounds_upper = [0.9, 100.0]

    try:
        popt, pcov = curve_fit(
            lambda_p_ratio_model, x, y,
            sigma=dy,
            absolute_sigma=True,
            bounds=(bounds_lower, bounds_upper),
            p0=[0.3, 10.0]  # initial guess
        )

        alpha_fit, x0_fit = popt
        alpha_err, x0_err = np.sqrt(np.diag(pcov))

        # Calculate χ²
        y_model = lambda_p_ratio_model(x, alpha_fit, x0_fit)
        chi2 = np.sum(((y - y_model) / dy)**2)
        dof = len(x) - 2
        chi2_reduced = chi2 / dof

        # P-value (approximate)
        from scipy.stats import chi2 as chi2_dist
        p_value = 1.0 - chi2_dist.cdf(chi2, dof)

        print(f"\n✓ Fit converged successfully")
        print(f"  α = {alpha_fit:.4f} ± {alpha_err:.4f}")
        print(f"  x₀ = {x0_fit:.2f} ± {x0_err:.2f}")
        print(f"  χ²/dof = {chi2:.2f}/{dof} = {chi2_reduced:.3f}")
        print(f"  p-value = {p_value:.3f}")

        # Physical interpretation
        print(f"\nPhysical interpretation:")
        print(f"  → Dilution strength α = {alpha_fit:.1%}")
        print(f"  → Transition scale x₀ ≈ {x0_fit:.1f} (pp → pA crossover)")

        if alpha_fit < 0.5:
            print(f"  ✓ Realistic dilution (α < 0.5)")
        if 5 < x0_fit < 50:
            print(f"  ✓ x₀ in expected range for pp → pA transition")

        # Create results dictionary
        results = {
            'alpha': float(alpha_fit),
            'alpha_err': float(alpha_err),
            'x0': float(x0_fit),
            'x0_err': float(x0_err),
            'chi2': float(chi2),
            'dof': int(dof),
            'chi2_reduced': float(chi2_reduced),
            'p_value': float(p_value),
            'n_points': len(x),
            'fit_quality': 'good' if chi2_reduced < 2.0 else 'acceptable' if chi2_reduced < 5.0 else 'poor'
        }

        # Save results
        if save_results:
            import os
            os.makedirs(output_dir, exist_ok=True)
            with open(f"{output_dir}/strangeness_fit_results.json", 'w') as f:
                json.dump(results, f, indent=2)
            print(f"\n✓ Results saved to {output_dir}/strangeness_fit_results.json")

        # Plot
        if plot:
            _plot_fit_results(x, y, dy, alpha_fit, x0_fit, results, output_dir)

        return results

    except Exception as e:
        print(f"✗ Fit failed: {e}")
        return {}


def _generate_mock_data() -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Generate mock ALICE-like Λ/p ratio data for testing.

    Returns:
        (dN/dη, Λ/p ratio, error)
    """
    # Mock multiplicity range
    x = np.array([2, 5, 10, 15, 20, 30, 40, 50])

    # Generate data with true parameters
    alpha_true = 0.25
    x0_true = 12.0

    y_true = lambda_p_ratio_model(x, alpha_true, x0_true)

    # Add realistic noise
    np.random.seed(42)
    dy = 0.03 * y_true  # 3% error
    y = y_true + np.random.normal(0, dy)

    return x, y, dy


def _plot_fit_results(
    x: np.ndarray,
    y: np.ndarray,
    dy: np.ndarray,
    alpha: float,
    x0: float,
    results: Dict,
    output_dir: str
):
    """Generate diagnostic plot for Ω fit."""

    import os
    os.makedirs(output_dir, exist_ok=True)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8),
                                     gridspec_kw={'height_ratios': [3, 1]})

    # Smooth curve for model
    x_smooth = np.linspace(x.min() * 0.8, x.max() * 1.2, 200)
    y_smooth = lambda_p_ratio_model(x_smooth, alpha, x0)

    # Top panel: data vs model
    ax1.errorbar(x, y, yerr=dy, fmt='o', color='black',
                 label='ALICE data', capsize=3, markersize=6)
    ax1.plot(x_smooth, y_smooth, 'r-', linewidth=2,
             label=f'QCT fit: α={alpha:.3f}, x₀={x0:.1f}')
    ax1.set_ylabel('Λ/p ratio', fontsize=12)
    ax1.legend(fontsize=11)
    ax1.grid(alpha=0.3)
    ax1.set_title(f'QCT Strangeness Enhancement Fit  (χ²/dof = {results["chi2_reduced"]:.2f})',
                  fontsize=13, fontweight='bold')

    # Bottom panel: residuals
    y_model = lambda_p_ratio_model(x, alpha, x0)
    residuals = (y - y_model) / dy

    ax2.errorbar(x, residuals, yerr=1.0, fmt='o', color='black', capsize=3)
    ax2.axhline(0, color='red', linestyle='--', linewidth=1)
    ax2.axhline(2, color='gray', linestyle=':', alpha=0.5)
    ax2.axhline(-2, color='gray', linestyle=':', alpha=0.5)
    ax2.set_xlabel('dN/dη', fontsize=12)
    ax2.set_ylabel('Pull (σ)', fontsize=12)
    ax2.grid(alpha=0.3)
    ax2.set_ylim(-3.5, 3.5)

    plt.tight_layout()
    plt.savefig(f"{output_dir}/strangeness_fit.png", dpi=150)
    print(f"✓ Plot saved to {output_dir}/strangeness_fit.png")
    plt.close()


if __name__ == "__main__":
    # Run standalone fit with mock data
    results = fit_omega_to_lambda_p_ratio(
        plot=True,
        save_results=True
    )

    print("\n" + "="*60)
    print("Strangeness enhancement fit completed.")
    print("="*60)
