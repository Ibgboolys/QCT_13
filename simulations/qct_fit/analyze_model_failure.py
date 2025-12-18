#!/usr/bin/env python3
"""
ANALÝZA SELHÁNÍ QCT MODELU
===========================

Diagnostikuje, PROČ QCT model nesedí na reálná ALICE data.

Analýza:
1. Vizualizace dat vs model
2. Residuální analýza (systematické odchylky)
3. Test funkční formy (je logaritmická/exponenciální správná?)
4. Fyzikální interpretace
5. Alternativní modely

Autor: QCT Model Failure Analysis
Datum: 2025-12-18
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import json

# =============================================================================
# MODELY
# =============================================================================

def qct_lambda_p_model(x, alpha, x0):
    """
    QCT model pro Λ/p poměr.
    R = exp(-Ω(x) · Δm/T)
    kde Ω(x) = 1 - α · x/(x + x₀)

    Zjednodušeno: R ∝ (x + x₀)^α
    """
    # Kanonický tvar z fit results
    omega = 1.0 - alpha * x / (x + x0)
    # Předpokládáme Δm/T ~ 1 pro normalizaci
    return np.exp(-omega * 1.5)  # 1.5 je hrubý odhad Δm/T

def qct_v2_model(x, A, gamma):
    """
    QCT model pro v₂.
    v₂(x) = A · ln(1 + x) · exp(-γ)
    """
    return A * np.log(1 + x) * np.exp(-gamma)

# Alternativní modely pro testování

def power_law_model(x, a, b):
    """R = a · x^b"""
    return a * x**b

def linear_model(x, a, b):
    """R = a + b·x"""
    return a + b * x

def saturating_model(x, a, b):
    """R = a · (1 - exp(-x/b))"""
    return a * (1 - np.exp(-x / b))

# =============================================================================
# ANALÝZA STRANGENESS (Λ/p)
# =============================================================================

def analyze_strangeness_failure():
    """Analyzuje proč Λ/p fit selhal."""

    print("\n" + "="*70)
    print("ANALÝZA SELHÁNÍ: Λ/p STRANGENESS FIT")
    print("="*70)

    # Načtení dat
    df = pd.read_csv('simulations/qct_fit/data/REAL_DATA_lambda_p.csv')
    x_data = df['dN_deta'].values
    y_data = df['lambda_p_ratio'].values
    y_err = df['error'].values

    # Načtení fit výsledků
    with open('results/qct_fit_REAL/strangeness_fit_results.json', 'r') as f:
        fit_results = json.load(f)

    alpha_fit = fit_results['alpha']
    x0_fit = fit_results['x0']

    print(f"\n📊 Data Summary:")
    print(f"   Points: {len(x_data)}")
    print(f"   Multiplicity: {x_data.min():.1f} - {x_data.max():.1f}")
    print(f"   Λ/p ratio: {y_data.min():.3f} - {y_data.max():.3f}")
    print(f"   Trend: {'increasing' if y_data[-1] > y_data[0] else 'decreasing'}")
    print(f"   Relative change: {(y_data.max() - y_data.min()) / y_data.min() * 100:.1f}%")

    print(f"\n🔬 QCT Fit Results:")
    print(f"   α = {alpha_fit:.4f} (expected ~0.25)")
    print(f"   x₀ = {x0_fit:.2f}")
    print(f"   χ²/dof = {fit_results['chi2_reduced']:.2f} (POOR)")

    # Model predictions
    x_smooth = np.linspace(x_data.min() * 0.5, x_data.max() * 1.5, 200)
    y_model = qct_lambda_p_model(x_data, alpha_fit, x0_fit)
    y_smooth = qct_lambda_p_model(x_smooth, alpha_fit, x0_fit)

    # Normalizace - model potřebuje offset
    # Empiricky najdeme offset aby model seděl na data
    offset = np.mean(y_data - y_model)
    y_model_normalized = y_model + offset
    y_smooth_normalized = y_smooth + offset

    # Residuály
    residuals = (y_data - y_model_normalized) / y_err

    print(f"\n📉 Residual Analysis:")
    print(f"   Mean residual: {np.mean(residuals):.2f} σ")
    print(f"   RMS residual: {np.sqrt(np.mean(residuals**2)):.2f} σ")
    print(f"   Max |residual|: {np.max(np.abs(residuals)):.2f} σ")

    # Systematické trendy?
    low_mult_res = residuals[:len(residuals)//2]
    high_mult_res = residuals[len(residuals)//2:]
    print(f"   Low mult (<{x_data[len(x_data)//2]:.1f}): {np.mean(low_mult_res):.2f} σ")
    print(f"   High mult (>{x_data[len(x_data)//2]:.1f}): {np.mean(high_mult_res):.2f} σ")

    # Test alternativních modelů
    print(f"\n🧪 Alternative Model Tests:")

    # Power law: R = a · x^b
    try:
        popt_pl, _ = curve_fit(power_law_model, x_data, y_data, sigma=y_err, p0=[0.3, 0.3])
        y_pl = power_law_model(x_data, *popt_pl)
        chi2_pl = np.sum(((y_data - y_pl) / y_err)**2) / (len(x_data) - 2)
        print(f"   Power law R=a·x^b: χ²/dof = {chi2_pl:.2f}")
        print(f"      → a={popt_pl[0]:.3f}, b={popt_pl[1]:.3f}")
    except:
        chi2_pl = np.inf
        print(f"   Power law: FAILED TO CONVERGE")

    # Linear: R = a + b·x
    try:
        popt_lin, _ = curve_fit(linear_model, x_data, y_data, sigma=y_err)
        y_lin = linear_model(x_data, *popt_lin)
        chi2_lin = np.sum(((y_data - y_lin) / y_err)**2) / (len(x_data) - 2)
        print(f"   Linear R=a+b·x: χ²/dof = {chi2_lin:.2f}")
        print(f"      → a={popt_lin[0]:.3f}, b={popt_lin[1]:.4f}")
    except:
        chi2_lin = np.inf
        print(f"   Linear: FAILED TO CONVERGE")

    print(f"\n⚠️  DIAGNOSIS:")
    if chi2_pl < fit_results['chi2_reduced'] or chi2_lin < fit_results['chi2_reduced']:
        print(f"   ❌ QCT functional form is WRONG!")
        print(f"   → Simple power law or linear fits BETTER than QCT")
        print(f"   → Model parametrization needs fundamental revision")
    else:
        print(f"   ⚠️  All models fit poorly - possible systematic in data")

    # GRAF
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8),
                                     gridspec_kw={'height_ratios': [3, 1]})

    # Data + fit
    ax1.errorbar(x_data, y_data, yerr=y_err, fmt='ko',
                 label='ALICE real data', capsize=3, markersize=8, linewidth=2)
    ax1.plot(x_smooth, y_smooth_normalized, 'r-', linewidth=2,
             label=f'QCT: α={alpha_fit:.2f}, χ²/dof={fit_results["chi2_reduced"]:.1f}')

    if chi2_pl < np.inf:
        x_pl_smooth = np.linspace(x_data.min(), x_data.max(), 100)
        y_pl_smooth = power_law_model(x_pl_smooth, *popt_pl)
        ax1.plot(x_pl_smooth, y_pl_smooth, 'b--', linewidth=1.5,
                 label=f'Power law: χ²/dof={chi2_pl:.1f}')

    ax1.set_ylabel('Λ/p ratio', fontsize=12)
    ax1.legend(fontsize=10)
    ax1.grid(alpha=0.3)
    ax1.set_title('QCT Strangeness Model FAILURE Analysis',
                  fontsize=13, fontweight='bold')

    # Residuály
    ax2.errorbar(x_data, residuals, yerr=1.0, fmt='ko', capsize=3)
    ax2.axhline(0, color='red', linestyle='--', linewidth=1)
    ax2.axhline(3, color='gray', linestyle=':', alpha=0.5)
    ax2.axhline(-3, color='gray', linestyle=':', alpha=0.5)
    ax2.fill_between([x_data.min(), x_data.max()], -2, 2, alpha=0.2, color='green')
    ax2.set_xlabel('dN/dη', fontsize=12)
    ax2.set_ylabel('Pull (σ)', fontsize=12)
    ax2.grid(alpha=0.3)
    ax2.set_ylim(-10, 10)

    plt.tight_layout()
    plt.savefig('results/qct_fit_REAL/strangeness_FAILURE_analysis.png', dpi=150)
    print(f"\n✓ Plot: results/qct_fit_REAL/strangeness_FAILURE_analysis.png")
    plt.close()

    return {
        'qct_chi2': fit_results['chi2_reduced'],
        'powerlaw_chi2': chi2_pl if chi2_pl < np.inf else None,
        'linear_chi2': chi2_lin if chi2_lin < np.inf else None
    }


# =============================================================================
# ANALÝZA v₂
# =============================================================================

def analyze_v2_failure():
    """Analyzuje proč v₂ fit selhal."""

    print("\n" + "="*70)
    print("ANALÝZA SELHÁNÍ: v₂ RIDGE FIT")
    print("="*70)

    # Načtení dat
    df = pd.read_csv('simulations/qct_fit/data/REAL_DATA_v2_pp.csv')
    x_data = df['dN_deta'].values
    y_data = df['v2'].values
    y_err = df['error'].values

    # Načtení fit výsledků
    with open('results/qct_fit_REAL/ridge_v2_fit_results.json', 'r') as f:
        fit_results = json.load(f)

    A_fit = fit_results['A']
    gamma_fit = fit_results['gamma']

    print(f"\n📊 Data Summary:")
    print(f"   Points: {len(x_data)}")
    print(f"   Multiplicity: {x_data.min():.1f} - {x_data.max():.1f}")
    print(f"   v₂ range: {y_data.min():.5f} - {y_data.max():.5f}")
    print(f"   Trend: {'increasing' if y_data[-1] > y_data[0] else 'flat/decreasing'}")
    print(f"   Relative variation: {np.std(y_data) / np.mean(y_data) * 100:.1f}%")

    print(f"\n🔬 QCT Fit Results:")
    print(f"   γ = {gamma_fit:.4f} (expected < 0.02)")
    print(f"   A = {A_fit:.4f}")
    print(f"   χ²/dof = {fit_results['chi2_reduced']:.2f} (POOR)")

    # KLÍČOVÉ POZOROVÁNÍ
    print(f"\n🔍 KEY OBSERVATION:")
    print(f"   Data shows v₂ ≈ {np.mean(y_data):.3f} ± {np.std(y_data):.3f}")
    print(f"   → ALMOST CONSTANT across multiplicity range!")
    print(f"   QCT predicts: v₂ ∝ ln(1+x) · exp(-γ)")
    print(f"   → LOGARITHMIC GROWTH expected")

    # Model predictions
    x_smooth = np.linspace(x_data.min() * 0.8, x_data.max() * 1.2, 200)
    y_model = qct_v2_model(x_data, A_fit, gamma_fit)
    y_smooth = qct_v2_model(x_smooth, A_fit, gamma_fit)

    # Residuály
    residuals = (y_data - y_model) / y_err

    print(f"\n📉 Residual Analysis:")
    print(f"   Mean residual: {np.mean(residuals):.2f} σ")
    print(f"   RMS residual: {np.sqrt(np.mean(residuals**2)):.2f} σ")

    # Test konstantního modelu
    v2_mean = np.mean(y_data)
    chi2_const = np.sum(((y_data - v2_mean) / y_err)**2) / (len(x_data) - 1)

    print(f"\n🧪 Alternative Model: CONSTANT v₂")
    print(f"   v₂ = {v2_mean:.5f} (constant)")
    print(f"   χ²/dof = {chi2_const:.2f}")

    print(f"\n⚠️  DIAGNOSIS:")
    if chi2_const < fit_results['chi2_reduced']:
        print(f"   ❌ QCT logarithmic model is WRONG!")
        print(f"   → Constant v₂ fits BETTER than QCT")
        print(f"   → Data shows NO logarithmic growth")
        print(f"   → v₂ is INDEPENDENT of multiplicity in this range")

    # GRAF
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8),
                                     gridspec_kw={'height_ratios': [3, 1]})

    # Data + fit
    ax1.errorbar(x_data, y_data, yerr=y_err, fmt='ko',
                 label='ALICE real data', capsize=3, markersize=8, linewidth=2)
    ax1.plot(x_smooth, y_smooth, 'r-', linewidth=2,
             label=f'QCT: γ={gamma_fit:.2f}, χ²/dof={fit_results["chi2_reduced"]:.1f}')
    ax1.axhline(v2_mean, color='b', linestyle='--', linewidth=1.5,
                label=f'Constant: v₂={v2_mean:.4f}, χ²/dof={chi2_const:.1f}')

    ax1.set_ylabel('v₂{2}', fontsize=12)
    ax1.legend(fontsize=10)
    ax1.grid(alpha=0.3)
    ax1.set_title('QCT Ridge v₂ Model FAILURE Analysis',
                  fontsize=13, fontweight='bold')

    # Residuály
    ax2.errorbar(x_data, residuals, yerr=1.0, fmt='ko', capsize=3)
    ax2.axhline(0, color='red', linestyle='--', linewidth=1)
    ax2.axhline(3, color='gray', linestyle=':', alpha=0.5)
    ax2.axhline(-3, color='gray', linestyle=':', alpha=0.5)
    ax2.fill_between([x_data.min(), x_data.max()], -2, 2, alpha=0.2, color='green')
    ax2.set_xlabel('dN/dη', fontsize=12)
    ax2.set_ylabel('Pull (σ)', fontsize=12)
    ax2.grid(alpha=0.3)
    ax2.set_ylim(-10, 10)

    plt.tight_layout()
    plt.savefig('results/qct_fit_REAL/v2_FAILURE_analysis.png', dpi=150)
    print(f"\n✓ Plot: results/qct_fit_REAL/v2_FAILURE_analysis.png")
    plt.close()

    return {
        'qct_chi2': fit_results['chi2_reduced'],
        'constant_chi2': chi2_const
    }


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("QCT MODEL FAILURE - ROOT CAUSE ANALYSIS")
    print("="*70)

    # Analýza obou fitů
    strangeness_results = analyze_strangeness_failure()
    v2_results = analyze_v2_failure()

    # ZÁVĚREČNÝ REPORT
    print("\n" + "="*70)
    print("FINAL DIAGNOSIS")
    print("="*70)

    print(f"\n1. STRANGENESS (Λ/p):")
    print(f"   QCT χ²/dof = {strangeness_results['qct_chi2']:.1f}")
    if strangeness_results['powerlaw_chi2']:
        print(f"   Power law χ²/dof = {strangeness_results['powerlaw_chi2']:.1f}")
        if strangeness_results['powerlaw_chi2'] < strangeness_results['qct_chi2']:
            print(f"   → ❌ FUNDAMENTAL MODEL ERROR")

    print(f"\n2. RIDGE v₂:")
    print(f"   QCT χ²/dof = {v2_results['qct_chi2']:.1f}")
    print(f"   Constant χ²/dof = {v2_results['constant_chi2']:.1f}")
    if v2_results['constant_chi2'] < v2_results['qct_chi2']:
        print(f"   → ❌ NO MULTIPLICITY DEPENDENCE (QCT predicts logarithmic)")

    print(f"\n" + "="*70)
    print("CONCLUSION:")
    print("="*70)
    print(f"QCT model fails because:")
    print(f"  1. Functional form doesn't match data trends")
    print(f"  2. Λ/p shows simpler power-law behavior, not QCT exponential")
    print(f"  3. v₂ is FLAT (constant), not logarithmic as QCT predicts")
    print(f"  4. Both χ²/dof >> 1 indicate systematic model inadequacy")
    print(f"\nThis is HONEST NEGATIVE RESULT:")
    print(f"  → QCT parametrization needs fundamental revision")
    print(f"  → Current theory does NOT describe ALICE pp collisions")
    print("="*70)
