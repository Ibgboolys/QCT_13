#!/usr/bin/env python3
"""
TEST QCT TEORETICKÝCH PREDIKCÍ PROTI REÁLNÝM DATŮM
===================================================

Porovnání:
1. Teoretická predikce: α=0.218, γ=0.0174 (FIXED z first-principles)
2. Best-fit: volné parametry α, γ
3. Experimentální data: ALICE real data

Cíl: Zjistit, jak dobře funguje QCT bez empirické adjustace.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd
import json
from pathlib import Path

# =============================================================================
# TEORETICKÉ PREDIKCE (z derive_from_first_principles_CORRECTED.py)
# =============================================================================

ALPHA_THEORY = 0.218   # z T_freeze/Δ_gap
GAMMA_THEORY = 0.0174  # z (η/s) × (T/Λ)

print("="*70)
print("TEST QCT TEORETICKÝCH PREDIKCÍ")
print("="*70)
print(f"\nTeoretické hodnoty (z first-principles):")
print(f"  α = {ALPHA_THEORY:.3f}  (z T_freeze/Δ_gap)")
print(f"  γ = {GAMMA_THEORY:.4f}  (z η/s hydrodynamiky)")
print()

# =============================================================================
# MODEL DEFINICE
# =============================================================================

def conformal_factor_qct(x, alpha, x0):
    """
    QCT conformal factor: Ω(x) = 1 - α·x/(x+x₀)

    x: multiplicity (dN/dη)
    alpha: dilution parameter
    x0: characteristic scale
    """
    return 1.0 - alpha * x / (x + x0)

def lambda_p_ratio_qct(x, alpha, x0, baseline):
    """
    Λ/p ratio model: R(x) = baseline × Ω(x)
    """
    Omega = conformal_factor_qct(x, alpha, x0)
    return baseline * Omega

def v2_ridge_qct(x, gamma, A):
    """
    Ridge v₂ model: v₂(x) = A × ln(1+x) × exp(-γ)

    Note: This model was FALSIFIED by data (v₂ ~ constant)
    """
    return A * np.log(1 + x) * np.exp(-gamma)

# =============================================================================
# CHI-SQUARED CALCULATION
# =============================================================================

def chi_squared(y_data, y_model, y_err, n_params):
    """Calculate χ² and reduced χ²"""
    chi2 = np.sum(((y_data - y_model) / y_err)**2)
    dof = len(y_data) - n_params
    chi2_reduced = chi2 / dof if dof > 0 else np.inf
    return chi2, chi2_reduced, dof

# =============================================================================
# LOAD REAL ALICE DATA
# =============================================================================

data_dir = Path(__file__).parent / "data"

print("="*70)
print("NAČÍTÁNÍ REÁLNÝCH ALICE DAT")
print("="*70)

# Λ/p data
lambda_p_file = data_dir / "REAL_DATA_lambda_p.csv"
try:
    df_lambda = pd.read_csv(lambda_p_file, comment='#')
    x_lambda = df_lambda.iloc[:, 0].values
    y_lambda = df_lambda.iloc[:, 1].values
    yerr_lambda = df_lambda.iloc[:, 2].values if df_lambda.shape[1] > 2 else 0.05 * y_lambda
    print(f"✓ Λ/p data loaded: {len(x_lambda)} points")
    print(f"  Multiplicity range: {x_lambda.min():.1f} - {x_lambda.max():.1f}")
    print(f"  Λ/p range: {y_lambda.min():.3f} - {y_lambda.max():.3f}")
except Exception as e:
    print(f"❌ ERROR loading Λ/p data: {e}")
    x_lambda, y_lambda, yerr_lambda = None, None, None

# v₂ data
v2_file = data_dir / "REAL_DATA_v2_pp.csv"
try:
    df_v2 = pd.read_csv(v2_file, comment='#')
    x_v2 = df_v2.iloc[:, 0].values
    y_v2 = df_v2.iloc[:, 1].values
    yerr_v2 = df_v2.iloc[:, 2].values if df_v2.shape[1] > 2 else 0.05 * y_v2
    print(f"\n✓ v₂ data loaded: {len(x_v2)} points")
    print(f"  Multiplicity range: {x_v2.min():.1f} - {x_v2.max():.1f}")
    print(f"  v₂ range: {y_v2.min():.4f} - {y_v2.max():.4f}")
except Exception as e:
    print(f"❌ ERROR loading v₂ data: {e}")
    x_v2, y_v2, yerr_v2 = None, None, None

print()

# =============================================================================
# Λ/p RATIO FIT
# =============================================================================

results_lambda = {}

if x_lambda is not None:
    print("="*70)
    print("Λ/p RATIO ANALYSIS")
    print("="*70)

    # -------------------------------------------------------------------------
    # FIT 1: THEORETICAL PREDICTION (fixed α=0.218)
    # -------------------------------------------------------------------------

    print("\n" + "-"*70)
    print("FIT 1: TEORETICKÁ PREDIKCE (α=0.218 FIXED)")
    print("-"*70)

    def lambda_p_theory(x, x0, baseline):
        """Fixed α = 0.218"""
        return lambda_p_ratio_qct(x, ALPHA_THEORY, x0, baseline)

    # Initial guess
    p0_theory = [20.0, 0.6]  # x0, baseline

    try:
        popt_theory, pcov_theory = curve_fit(
            lambda_p_theory, x_lambda, y_lambda,
            sigma=yerr_lambda, p0=p0_theory, maxfev=10000
        )

        x0_theory, baseline_theory = popt_theory
        x0_err, baseline_err = np.sqrt(np.diag(pcov_theory))

        # Calculate model
        y_theory = lambda_p_theory(x_lambda, *popt_theory)

        # Chi-squared
        chi2_theory, chi2red_theory, dof_theory = chi_squared(
            y_lambda, y_theory, yerr_lambda, n_params=2
        )

        print(f"\n✓ FIT ÚSPĚŠNÝ:")
        print(f"  α = {ALPHA_THEORY:.3f} (FIXED)")
        print(f"  x₀ = {x0_theory:.2f} ± {x0_err:.2f}")
        print(f"  baseline = {baseline_theory:.3f} ± {baseline_err:.3f}")
        print(f"\n  χ² = {chi2_theory:.2f}")
        print(f"  χ²/dof = {chi2red_theory:.2f} (dof={dof_theory})")

        results_lambda['theory'] = {
            'alpha': ALPHA_THEORY,
            'x0': float(x0_theory),
            'baseline': float(baseline_theory),
            'chi2': float(chi2_theory),
            'chi2_reduced': float(chi2red_theory),
            'dof': int(dof_theory)
        }

    except Exception as e:
        print(f"❌ FIT SELHAL: {e}")
        y_theory = None
        results_lambda['theory'] = {'error': str(e)}

    # -------------------------------------------------------------------------
    # FIT 2: BEST-FIT (free α)
    # -------------------------------------------------------------------------

    print("\n" + "-"*70)
    print("FIT 2: BEST-FIT (α VOLNÉ)")
    print("-"*70)

    def lambda_p_free(x, alpha, x0, baseline):
        """All parameters free"""
        return lambda_p_ratio_qct(x, alpha, x0, baseline)

    # Initial guess
    p0_free = [0.25, 20.0, 0.6]  # alpha, x0, baseline

    try:
        popt_free, pcov_free = curve_fit(
            lambda_p_free, x_lambda, y_lambda,
            sigma=yerr_lambda, p0=p0_free, maxfev=10000,
            bounds=([0, 1, 0.3], [1, 100, 1.0])  # reasonable bounds
        )

        alpha_free, x0_free, baseline_free = popt_free
        alpha_err, x0_err_free, baseline_err_free = np.sqrt(np.diag(pcov_free))

        # Calculate model
        y_free = lambda_p_free(x_lambda, *popt_free)

        # Chi-squared
        chi2_free, chi2red_free, dof_free = chi_squared(
            y_lambda, y_free, yerr_lambda, n_params=3
        )

        print(f"\n✓ FIT ÚSPĚŠNÝ:")
        print(f"  α = {alpha_free:.3f} ± {alpha_err:.3f}")
        print(f"  x₀ = {x0_free:.2f} ± {x0_err_free:.2f}")
        print(f"  baseline = {baseline_free:.3f} ± {baseline_err_free:.3f}")
        print(f"\n  χ² = {chi2_free:.2f}")
        print(f"  χ²/dof = {chi2red_free:.2f} (dof={dof_free})")

        results_lambda['best_fit'] = {
            'alpha': float(alpha_free),
            'alpha_err': float(alpha_err),
            'x0': float(x0_free),
            'baseline': float(baseline_free),
            'chi2': float(chi2_free),
            'chi2_reduced': float(chi2red_free),
            'dof': int(dof_free)
        }

        # Comparison
        print(f"\n📊 POROVNÁNÍ:")
        print(f"  α (theory) = {ALPHA_THEORY:.3f}")
        print(f"  α (fit)    = {alpha_free:.3f} ± {alpha_err:.3f}")
        print(f"  Rozdíl: {abs(alpha_free - ALPHA_THEORY)/ALPHA_THEORY*100:.1f}%")
        print(f"\n  χ²/dof (theory) = {chi2red_theory:.2f}")
        print(f"  χ²/dof (fit)    = {chi2red_free:.2f}")
        print(f"  Δχ²/dof = {chi2red_theory - chi2red_free:.2f}")

    except Exception as e:
        print(f"❌ FIT SELHAL: {e}")
        y_free = None
        results_lambda['best_fit'] = {'error': str(e)}

# =============================================================================
# v₂ RIDGE FIT
# =============================================================================

results_v2 = {}

if x_v2 is not None:
    print("\n" + "="*70)
    print("v₂ RIDGE ANALYSIS")
    print("="*70)

    # First check: is v₂ constant?
    v2_mean = np.mean(y_v2)
    v2_std = np.std(y_v2)
    v2_variation = v2_std / v2_mean

    print(f"\n📊 DATA CHARAKTERISTIKA:")
    print(f"  Mean v₂ = {v2_mean:.4f}")
    print(f"  Std v₂ = {v2_std:.4f}")
    print(f"  Variation = {v2_variation*100:.1f}%")

    if v2_variation < 0.05:
        print(f"  ⚠️  v₂ je téměř KONSTANTNÍ (variace < 5%)")
        print(f"  ⚠️  Logaritmický model pravděpodobně SELŽE")

    # -------------------------------------------------------------------------
    # FIT 1: THEORETICAL PREDICTION (fixed γ=0.0174)
    # -------------------------------------------------------------------------

    print("\n" + "-"*70)
    print("FIT 1: TEORETICKÁ PREDIKCE (γ=0.0174 FIXED)")
    print("-"*70)

    def v2_theory(x, A):
        """Fixed γ = 0.0174"""
        return v2_ridge_qct(x, GAMMA_THEORY, A)

    # Initial guess
    p0_v2_theory = [0.1]  # A

    try:
        popt_v2_theory, pcov_v2_theory = curve_fit(
            v2_theory, x_v2, y_v2,
            sigma=yerr_v2, p0=p0_v2_theory, maxfev=10000
        )

        A_theory = popt_v2_theory[0]
        A_err_theory = np.sqrt(pcov_v2_theory[0, 0])

        # Calculate model
        y_v2_theory = v2_theory(x_v2, A_theory)

        # Chi-squared
        chi2_v2_theory, chi2red_v2_theory, dof_v2_theory = chi_squared(
            y_v2, y_v2_theory, yerr_v2, n_params=1
        )

        print(f"\n✓ FIT ÚSPĚŠNÝ:")
        print(f"  γ = {GAMMA_THEORY:.4f} (FIXED)")
        print(f"  A = {A_theory:.4f} ± {A_err_theory:.4f}")
        print(f"\n  χ² = {chi2_v2_theory:.2f}")
        print(f"  χ²/dof = {chi2red_v2_theory:.2f} (dof={dof_v2_theory})")

        results_v2['theory'] = {
            'gamma': GAMMA_THEORY,
            'A': float(A_theory),
            'chi2': float(chi2_v2_theory),
            'chi2_reduced': float(chi2red_v2_theory),
            'dof': int(dof_v2_theory)
        }

    except Exception as e:
        print(f"❌ FIT SELHAL: {e}")
        y_v2_theory = None
        results_v2['theory'] = {'error': str(e)}

    # -------------------------------------------------------------------------
    # FIT 2: BEST-FIT (free γ)
    # -------------------------------------------------------------------------

    print("\n" + "-"*70)
    print("FIT 2: BEST-FIT (γ VOLNÉ)")
    print("-"*70)

    def v2_free(x, gamma, A):
        """All parameters free"""
        return v2_ridge_qct(x, gamma, A)

    # Initial guess
    p0_v2_free = [0.01, 0.1]  # gamma, A

    try:
        popt_v2_free, pcov_v2_free = curve_fit(
            v2_free, x_v2, y_v2,
            sigma=yerr_v2, p0=p0_v2_free, maxfev=10000,
            bounds=([0, 0], [2, 1])  # reasonable bounds
        )

        gamma_free, A_free = popt_v2_free
        gamma_err_free, A_err_free = np.sqrt(np.diag(pcov_v2_free))

        # Calculate model
        y_v2_free = v2_free(x_v2, *popt_v2_free)

        # Chi-squared
        chi2_v2_free, chi2red_v2_free, dof_v2_free = chi_squared(
            y_v2, y_v2_free, yerr_v2, n_params=2
        )

        print(f"\n✓ FIT ÚSPĚŠNÝ:")
        print(f"  γ = {gamma_free:.4f} ± {gamma_err_free:.4f}")
        print(f"  A = {A_free:.4f} ± {A_err_free:.4f}")
        print(f"\n  χ² = {chi2_v2_free:.2f}")
        print(f"  χ²/dof = {chi2red_v2_free:.2f} (dof={dof_v2_free})")

        results_v2['best_fit'] = {
            'gamma': float(gamma_free),
            'gamma_err': float(gamma_err_free),
            'A': float(A_free),
            'chi2': float(chi2_v2_free),
            'chi2_reduced': float(chi2red_v2_free),
            'dof': int(dof_v2_free)
        }

        # Comparison
        print(f"\n📊 POROVNÁNÍ:")
        print(f"  γ (theory) = {GAMMA_THEORY:.4f}")
        print(f"  γ (fit)    = {gamma_free:.4f} ± {gamma_err_free:.4f}")
        print(f"  Rozdíl: {abs(gamma_free - GAMMA_THEORY)/GAMMA_THEORY*100:.1f}%")
        print(f"\n  χ²/dof (theory) = {chi2red_v2_theory:.2f}")
        print(f"  χ²/dof (fit)    = {chi2red_v2_free:.2f}")
        print(f"  Δχ²/dof = {chi2red_v2_theory - chi2red_v2_free:.2f}")

    except Exception as e:
        print(f"❌ FIT SELHAL: {e}")
        y_v2_free = None
        results_v2['best_fit'] = {'error': str(e)}

    # -------------------------------------------------------------------------
    # FIT 3: CONSTANT MODEL (for comparison)
    # -------------------------------------------------------------------------

    print("\n" + "-"*70)
    print("FIT 3: KONSTANTNÍ MODEL (null hypothesis)")
    print("-"*70)

    # Simply fit a constant
    v2_const = np.mean(y_v2)
    chi2_const = np.sum(((y_v2 - v2_const) / yerr_v2)**2)
    dof_const = len(y_v2) - 1
    chi2red_const = chi2_const / dof_const

    print(f"\n✓ VÝSLEDEK:")
    print(f"  v₂ = {v2_const:.4f} (constant)")
    print(f"\n  χ² = {chi2_const:.2f}")
    print(f"  χ²/dof = {chi2red_const:.2f} (dof={dof_const})")

    results_v2['constant'] = {
        'v2': float(v2_const),
        'chi2': float(chi2_const),
        'chi2_reduced': float(chi2red_const),
        'dof': int(dof_const)
    }

    print(f"\n⚠️  SROVNÁNÍ S KONSTANTNÍM MODELEM:")
    if 'theory' in results_v2 and 'chi2_reduced' in results_v2['theory']:
        print(f"  χ²/dof (QCT theory) = {results_v2['theory']['chi2_reduced']:.2f}")
    if 'best_fit' in results_v2 and 'chi2_reduced' in results_v2['best_fit']:
        print(f"  χ²/dof (QCT fit)    = {results_v2['best_fit']['chi2_reduced']:.2f}")
    print(f"  χ²/dof (constant)   = {chi2red_const:.2f}")

    if chi2red_const < chi2red_v2_theory if y_v2_theory is not None else np.inf:
        print(f"\n  ❌ KONSTANTNÍ MODEL JE LEPŠÍ → QCT logaritmický model VYVRÁCEN!")

# =============================================================================
# SAVE RESULTS
# =============================================================================

results = {
    'theoretical_values': {
        'alpha': ALPHA_THEORY,
        'gamma': GAMMA_THEORY,
        'source': 'derive_from_first_principles_CORRECTED.py'
    },
    'lambda_p_ratio': results_lambda,
    'v2_ridge': results_v2
}

output_file = Path(__file__).parent.parent.parent / "results" / "qct_fit_REAL" / "theoretical_prediction_test.json"
output_file.parent.mkdir(parents=True, exist_ok=True)

with open(output_file, 'w') as f:
    json.dump(results, f, indent=2)

print(f"\n{'='*70}")
print(f"VÝSLEDKY ULOŽENY")
print(f"{'='*70}")
print(f"✓ {output_file}")

# =============================================================================
# PLOTTING
# =============================================================================

print(f"\n{'='*70}")
print(f"VYTVÁŘENÍ GRAFŮ")
print(f"{'='*70}")

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# -------------------------------------------------------------------------
# Plot 1: Λ/p ratio
# -------------------------------------------------------------------------

if x_lambda is not None:
    ax = axes[0]

    # Data points
    ax.errorbar(x_lambda, y_lambda, yerr=yerr_lambda,
                fmt='o', color='black', label='ALICE data',
                capsize=3, markersize=6, zorder=10)

    # Models
    x_plot = np.linspace(x_lambda.min(), x_lambda.max(), 200)

    if y_theory is not None:
        y_plot_theory = lambda_p_theory(x_plot, *popt_theory)
        ax.plot(x_plot, y_plot_theory, '-', color='red', linewidth=2,
                label=f'QCT theory (α={ALPHA_THEORY:.3f}, χ²/dof={chi2red_theory:.2f})')

    if y_free is not None:
        y_plot_free = lambda_p_free(x_plot, *popt_free)
        ax.plot(x_plot, y_plot_free, '--', color='blue', linewidth=2,
                label=f'Best fit (α={alpha_free:.3f}, χ²/dof={chi2red_free:.2f})')

    ax.set_xlabel('Multiplicity dN/dη', fontsize=12)
    ax.set_ylabel('Λ/p ratio', fontsize=12)
    ax.set_title('Λ/p Ratio: Theory vs Best-fit', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)

# -------------------------------------------------------------------------
# Plot 2: v₂ ridge
# -------------------------------------------------------------------------

if x_v2 is not None:
    ax = axes[1]

    # Data points
    ax.errorbar(x_v2, y_v2, yerr=yerr_v2,
                fmt='o', color='black', label='ALICE data',
                capsize=3, markersize=6, zorder=10)

    # Models
    x_plot_v2 = np.linspace(x_v2.min(), x_v2.max(), 200)

    if y_v2_theory is not None:
        y_plot_v2_theory = v2_theory(x_plot_v2, A_theory)
        ax.plot(x_plot_v2, y_plot_v2_theory, '-', color='red', linewidth=2,
                label=f'QCT theory (γ={GAMMA_THEORY:.4f}, χ²/dof={chi2red_v2_theory:.2f})')

    if y_v2_free is not None:
        y_plot_v2_free = v2_free(x_plot_v2, *popt_v2_free)
        ax.plot(x_plot_v2, y_plot_v2_free, '--', color='blue', linewidth=2,
                label=f'Best fit (γ={gamma_free:.4f}, χ²/dof={chi2red_v2_free:.2f})')

    # Constant model
    ax.axhline(v2_const, color='green', linestyle=':', linewidth=2,
               label=f'Constant (χ²/dof={chi2red_const:.2f})')

    ax.set_xlabel('Multiplicity dN/dη', fontsize=12)
    ax.set_ylabel('v₂', fontsize=12)
    ax.set_title('v₂ Ridge: Theory vs Best-fit vs Constant', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)

plt.tight_layout()

# Save plot
plot_file = Path(__file__).parent.parent.parent / "results" / "qct_fit_REAL" / "theoretical_prediction_comparison.png"
plt.savefig(plot_file, dpi=150, bbox_inches='tight')
print(f"✓ {plot_file}")

plt.close()

# -------------------------------------------------------------------------
# Residuals plot
# -------------------------------------------------------------------------

if x_lambda is not None and y_theory is not None and y_free is not None:
    fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    # Residuals for theory
    ax = axes[0]
    residuals_theory = (y_lambda - y_theory) / yerr_lambda
    ax.errorbar(x_lambda, residuals_theory, yerr=1.0,
                fmt='o', color='red', capsize=3, label='Theory')
    ax.axhline(0, color='black', linestyle='--', linewidth=1)
    ax.fill_between([x_lambda.min(), x_lambda.max()], -2, 2,
                     color='gray', alpha=0.2, label='±2σ')
    ax.set_ylabel('Residuals (σ)', fontsize=12)
    ax.set_title(f'Λ/p Residuals: Theory (α={ALPHA_THEORY:.3f})', fontsize=12)
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Residuals for best-fit
    ax = axes[1]
    residuals_free = (y_lambda - y_free) / yerr_lambda
    ax.errorbar(x_lambda, residuals_free, yerr=1.0,
                fmt='o', color='blue', capsize=3, label='Best-fit')
    ax.axhline(0, color='black', linestyle='--', linewidth=1)
    ax.fill_between([x_lambda.min(), x_lambda.max()], -2, 2,
                     color='gray', alpha=0.2, label='±2σ')
    ax.set_xlabel('Multiplicity dN/dη', fontsize=12)
    ax.set_ylabel('Residuals (σ)', fontsize=12)
    ax.set_title(f'Λ/p Residuals: Best-fit (α={alpha_free:.3f})', fontsize=12)
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    residuals_file = Path(__file__).parent.parent.parent / "results" / "qct_fit_REAL" / "residuals_comparison.png"
    plt.savefig(residuals_file, dpi=150, bbox_inches='tight')
    print(f"✓ {residuals_file}")

    plt.close()

print(f"\n{'='*70}")
print(f"ANALÝZA DOKONČENA")
print(f"{'='*70}")
print("\nSoubory:")
print(f"  • {output_file}")
print(f"  • {plot_file}")
if x_lambda is not None and y_theory is not None:
    print(f"  • {residuals_file}")

print("\nDalší krok: Analyzuj výsledky v JSON a grafech!")
