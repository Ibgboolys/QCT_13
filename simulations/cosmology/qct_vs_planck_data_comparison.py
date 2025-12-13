#!/usr/bin/env python3
"""
QCT vs PLANCK 2018: CMB DATA COMPARISON
========================================

Direct comparison of QCT predictions with Planck 2018 CMB measurements.

Data sources:
1. Planck 2018 cosmological parameters (Table 1, arXiv:1807.06209)
2. Planck 2018 low-ℓ TT power spectrum (ISW regime)
3. H(z) constraints from CMB + BAO

Key tests:
- Does QCT w(z) satisfy Planck constraints on w_0, w_a?
- Is ISW modification within error bars?
- Are H(z) predictions consistent?

Author: QCT Research Group
Date: 2025-12-11
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# ==============================================================================
# PLANCK 2018 DATA (arXiv:1807.06209, Table 1)
# ==============================================================================

# Cosmological parameters (TT,TE,EE+lowE+lensing)
PLANCK_H0 = 67.36  # km/s/Mpc
PLANCK_H0_err = 0.54

PLANCK_Omega_m = 0.3153
PLANCK_Omega_m_err = 0.0073

PLANCK_Omega_Lambda = 0.6847
PLANCK_Omega_Lambda_err = 0.0073

# Dark energy equation of state constraints
# Planck 2018 + BAO (assuming CPL parameterization: w(a) = w_0 + w_a(1-a))
PLANCK_w0 = -1.03  # Central value
PLANCK_w0_err = 0.03  # 68% CL

PLANCK_wa = -0.05  # Central value (consistent with Λ)
PLANCK_wa_err = 0.3  # 68% CL (weakly constrained)

# H(z) measurements from CMB acoustic scale
# These are indirect constraints combining CMB + BAO
H_z_data = {
    'z': np.array([0.38, 0.51, 0.61, 2.34]),
    'H': np.array([83.0, 90.4, 97.3, 222.0]),  # km/s/Mpc
    'H_err': np.array([2.5, 2.0, 2.1, 7.0]),
    'source': ['BOSS', 'BOSS', 'BOSS', 'Planck+BAO']
}

# ISW-LSS cross-correlation amplitude (relative to ΛCDM)
# From Planck 2018 IX: Constraints on primordial non-Gaussianity
ISW_amplitude_ratio = 1.00  # Consistent with ΛCDM
ISW_amplitude_err = 0.15  # ~15% uncertainty

# ==============================================================================
# QCT MODEL (from our previous analysis)
# ==============================================================================

def gradient_dominance_at_redshift(z):
    """Volume-averaged gradient dominance X(z)."""
    X_0 = 10.0
    z_structure = 2.0
    X_avg = X_0 * np.exp(-z / z_structure)
    return X_avg

def w_QCT(z):
    """QCT equation of state."""
    alpha = 0.6
    X = gradient_dominance_at_redshift(z)
    w_eff = -1.0 / (1.0 + X**alpha)
    return w_eff

def rho_DE_ratio(z):
    """Dark energy density evolution in QCT."""
    z_arr = np.atleast_1d(z)
    ratio = np.zeros_like(z_arr)

    for i, z_val in enumerate(z_arr):
        if z_val < 1e-6:
            ratio[i] = 1.0
        else:
            z_int = np.linspace(0, z_val, 200)
            w_int = w_QCT(z_int)
            integrand = 3 * (1 + w_int) / (1 + z_int)
            integral = np.trapezoid(integrand, z_int)
            ratio[i] = np.exp(integral)

    return ratio[0] if len(ratio) == 1 else ratio

def E_QCT(z):
    """Dimensionless Hubble parameter E(z) = H(z)/H_0 for QCT."""
    Omega_r_0 = 9.15e-5
    Omega_m_0 = PLANCK_Omega_m
    Omega_Lambda_0 = PLANCK_Omega_Lambda

    rho_DE = rho_DE_ratio(z)
    E_sq = (Omega_r_0 * (1 + z)**4 +
            Omega_m_0 * (1 + z)**3 +
            Omega_Lambda_0 * rho_DE)
    return np.sqrt(E_sq)

def H_QCT(z):
    """Hubble parameter H(z) for QCT [km/s/Mpc]."""
    return PLANCK_H0 * E_QCT(z)

def E_LCDM(z):
    """ΛCDM for comparison."""
    Omega_r_0 = 9.15e-5
    E_sq = (Omega_r_0 * (1 + z)**4 +
            PLANCK_Omega_m * (1 + z)**3 +
            PLANCK_Omega_Lambda)
    return np.sqrt(E_sq)

def H_LCDM(z):
    """ΛCDM Hubble parameter [km/s/Mpc]."""
    return PLANCK_H0 * E_LCDM(z)

# ==============================================================================
# CPL PARAMETERIZATION FOR COMPARISON
# ==============================================================================

def w_CPL(z, w0=-1.0, wa=0.0):
    """
    Chevallier-Polarski-Linder parameterization.
    w(a) = w_0 + w_a × (1 - a) = w_0 + w_a × z/(1+z)
    """
    return w0 + wa * z / (1 + z)

def extract_w0_wa_from_QCT():
    """
    Extract effective w_0 and w_a from QCT w(z) using Taylor expansion.

    w_QCT(z) ≈ w_0 + w_a × z/(1+z) for small z
    """
    z_sample = np.array([0.0, 0.5, 1.0])
    w_sample = w_QCT(z_sample)

    # Fit to CPL form (simple least squares)
    # w(0) = w_0
    w0_eff = w_sample[0]

    # w(z) ≈ w_0 + w_a × z/(1+z)
    # w_a ≈ [w(z) - w_0] × (1+z)/z for z=1
    wa_eff = (w_sample[2] - w0_eff) * (1 + z_sample[2]) / z_sample[2]

    return w0_eff, wa_eff

# ==============================================================================
# VISUALIZATION
# ==============================================================================

def plot_qct_vs_planck():
    """
    Create comprehensive comparison plot.
    """
    z_range = np.linspace(0, 3.0, 300)

    # QCT predictions
    w_qct_vals = w_QCT(z_range)
    H_qct_vals = H_QCT(z_range)

    # ΛCDM
    H_lcdm_vals = H_LCDM(z_range)

    # CPL with Planck best-fit
    w_cpl_planck = w_CPL(z_range, PLANCK_w0, PLANCK_wa)

    # Extract effective w0, wa from QCT
    w0_qct, wa_qct = extract_w0_wa_from_QCT()

    # Create figure
    fig = plt.figure(figsize=(16, 12))
    gs = GridSpec(3, 2, figure=fig, hspace=0.35, wspace=0.3)

    # ============================================
    # Panel 1: w(z) comparison
    # ============================================
    ax1 = fig.add_subplot(gs[0, :])

    # Plot QCT
    ax1.plot(z_range, w_qct_vals, 'b-', linewidth=3, label='QCT Prediction')

    # Plot Planck CPL constraint
    ax1.plot(z_range, w_cpl_planck, 'r--', linewidth=2,
             label=f'Planck 2018: w₀={PLANCK_w0:.2f}±{PLANCK_w0_err:.2f}')

    # Planck error band (1σ)
    w_cpl_upper = w_CPL(z_range, PLANCK_w0 + PLANCK_w0_err, PLANCK_wa + PLANCK_wa_err)
    w_cpl_lower = w_CPL(z_range, PLANCK_w0 - PLANCK_w0_err, PLANCK_wa - PLANCK_wa_err)
    ax1.fill_between(z_range, w_cpl_lower, w_cpl_upper, alpha=0.2, color='red',
                     label='Planck 1σ band')

    # ΛCDM reference
    ax1.axhline(y=-1, color='gray', linestyle=':', linewidth=2, alpha=0.5,
                label='ΛCDM (w = -1)')

    ax1.set_xlabel('Redshift z', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Equation of State w(z)', fontsize=12, fontweight='bold')
    ax1.set_title('QCT vs Planck 2018: Dark Energy Equation of State',
                  fontsize=14, fontweight='bold')
    ax1.set_xlim(0, 3)
    ax1.set_ylim(-1.3, 0.0)
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=10, loc='lower right')

    # Add text box with QCT effective parameters
    textstr = f'QCT effective parameters:\n'
    textstr += f'w₀ = {w0_qct:.3f}\n'
    textstr += f'wₐ = {wa_qct:.3f}\n\n'
    textstr += f'Planck constraint:\n'
    textstr += f'w₀ = {PLANCK_w0:.2f} ± {PLANCK_w0_err:.2f}\n'
    textstr += f'wₐ = {PLANCK_wa:.2f} ± {PLANCK_wa_err:.2f}'

    # Check if QCT is within Planck bounds
    w0_sigma = abs(w0_qct - PLANCK_w0) / PLANCK_w0_err
    wa_sigma = abs(wa_qct - PLANCK_wa) / PLANCK_wa_err

    textstr += f'\n\nTension:\n'
    textstr += f'w₀: {w0_sigma:.1f}σ\n'
    textstr += f'wₐ: {wa_sigma:.1f}σ'

    ax1.text(0.02, 0.05, textstr, transform=ax1.transAxes,
             fontsize=9, verticalalignment='bottom',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    # ============================================
    # Panel 2: H(z) comparison with data
    # ============================================
    ax2 = fig.add_subplot(gs[1, 0])

    # Plot predictions
    ax2.plot(z_range, H_qct_vals, 'b-', linewidth=3, label='QCT')
    ax2.plot(z_range, H_lcdm_vals, 'r--', linewidth=2, label='ΛCDM (Planck)')

    # Plot observational data
    z_obs = H_z_data['z']
    H_obs = H_z_data['H']
    H_obs_err = H_z_data['H_err']

    ax2.errorbar(z_obs, H_obs, yerr=H_obs_err, fmt='o', color='black',
                 markersize=8, capsize=5, capthick=2, label='Data (BOSS, Planck+BAO)')

    # H0 measurement
    ax2.errorbar([0], [PLANCK_H0], yerr=[PLANCK_H0_err], fmt='s', color='red',
                 markersize=8, capsize=5, capthick=2, label='Planck H₀')

    ax2.set_xlabel('Redshift z', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Hubble Parameter H(z) [km/s/Mpc]', fontsize=12, fontweight='bold')
    ax2.set_title('H(z) Measurements vs QCT', fontsize=13, fontweight='bold')
    ax2.set_xlim(-0.1, 2.5)
    ax2.grid(True, alpha=0.3)
    ax2.legend(fontsize=9, loc='upper left')

    # ============================================
    # Panel 3: χ² residuals for H(z)
    # ============================================
    ax3 = fig.add_subplot(gs[1, 1])

    # Calculate residuals
    H_qct_obs = H_QCT(z_obs)
    H_lcdm_obs = H_LCDM(z_obs)

    residual_qct = (H_qct_obs - H_obs) / H_obs_err
    residual_lcdm = (H_lcdm_obs - H_obs) / H_obs_err

    x_pos = np.arange(len(z_obs))
    width = 0.35

    ax3.bar(x_pos - width/2, residual_qct, width, label='QCT', color='blue', alpha=0.7)
    ax3.bar(x_pos + width/2, residual_lcdm, width, label='ΛCDM', color='red', alpha=0.7)

    # Reference lines
    ax3.axhline(y=0, color='black', linestyle='-', linewidth=1)
    ax3.axhline(y=1, color='gray', linestyle='--', alpha=0.5, label='±1σ')
    ax3.axhline(y=-1, color='gray', linestyle='--', alpha=0.5)
    ax3.axhline(y=2, color='gray', linestyle=':', alpha=0.3, label='±2σ')
    ax3.axhline(y=-2, color='gray', linestyle=':', alpha=0.3)

    ax3.set_xlabel('Measurement', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Residual [σ]', fontsize=12, fontweight='bold')
    ax3.set_title('H(z) Residuals', fontsize=13, fontweight='bold')
    ax3.set_xticks(x_pos)
    ax3.set_xticklabels([f'z={z:.2f}' for z in z_obs], rotation=45)
    ax3.grid(True, alpha=0.3, axis='y')
    ax3.legend(fontsize=9)

    # Calculate χ²
    chi2_qct = np.sum(residual_qct**2)
    chi2_lcdm = np.sum(residual_lcdm**2)
    ndof = len(z_obs)

    textstr = f'χ² / ndof:\n'
    textstr += f'QCT:  {chi2_qct:.1f} / {ndof}\n'
    textstr += f'ΛCDM: {chi2_lcdm:.1f} / {ndof}'

    ax3.text(0.95, 0.95, textstr, transform=ax3.transAxes,
             fontsize=10, verticalalignment='top', horizontalalignment='right',
             bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    # ============================================
    # Panel 4: ISW comparison
    # ============================================
    ax4 = fig.add_subplot(gs[2, 0])

    # Qualitative ISW amplitude (from our previous calculation)
    # Real ISW calculation would require full Boltzmann code
    ISW_qct_ratio = 0.23  # From our previous analysis
    ISW_qct_ratio_err = 0.05  # Estimated uncertainty

    models = ['ΛCDM\n(reference)', 'QCT\n(prediction)', 'Planck 2018\n(measurement)']
    ratios = [1.0, ISW_qct_ratio, ISW_amplitude_ratio]
    errors = [0.0, ISW_qct_ratio_err, ISW_amplitude_err]
    colors = ['red', 'blue', 'green']

    x_pos = np.arange(len(models))
    bars = ax4.bar(x_pos, ratios, yerr=errors, color=colors, alpha=0.6,
                   capsize=10, error_kw={'linewidth': 2})

    ax4.axhline(y=1.0, color='gray', linestyle='--', linewidth=2, alpha=0.5)
    ax4.set_ylabel('ISW Amplitude Ratio (relative to ΛCDM)', fontsize=11, fontweight='bold')
    ax4.set_title('Integrated Sachs-Wolfe Effect', fontsize=13, fontweight='bold')
    ax4.set_xticks(x_pos)
    ax4.set_xticklabels(models, fontsize=10)
    ax4.set_ylim(0, 1.5)
    ax4.grid(True, alpha=0.3, axis='y')

    # Add tension assessment
    isw_tension = abs(ISW_qct_ratio - ISW_amplitude_ratio) / np.sqrt(ISW_qct_ratio_err**2 + ISW_amplitude_err**2)

    textstr = f'Tension: {isw_tension:.1f}σ'
    if isw_tension < 1:
        status = 'CONSISTENT'
        color_box = 'lightgreen'
    elif isw_tension < 2:
        status = 'MILD TENSION'
        color_box = 'yellow'
    else:
        status = 'TENSION'
        color_box = 'lightcoral'

    textstr += f'\n{status}'

    ax4.text(0.5, 0.95, textstr, transform=ax4.transAxes,
             fontsize=11, ha='center', va='top',
             bbox=dict(boxstyle='round', facecolor=color_box, alpha=0.8))

    # ============================================
    # Panel 5: Summary statistics
    # ============================================
    ax5 = fig.add_subplot(gs[2, 1])
    ax5.axis('off')

    summary = "QCT vs PLANCK 2018: STATISTICAL SUMMARY\n"
    summary += "="*50 + "\n\n"

    summary += "DARK ENERGY EQUATION OF STATE:\n"
    summary += f"  QCT w₀ = {w0_qct:.3f}  (Planck: {PLANCK_w0:.2f}±{PLANCK_w0_err:.2f})\n"
    summary += f"  Tension: {w0_sigma:.1f}σ\n\n"

    summary += "HUBBLE PARAMETER:\n"
    summary += f"  χ²(QCT) = {chi2_qct:.1f} / {ndof} dof\n"
    summary += f"  χ²(ΛCDM) = {chi2_lcdm:.1f} / {ndof} dof\n"

    if chi2_qct < chi2_lcdm:
        summary += f"  → QCT fits better!\n\n"
    else:
        summary += f"  → ΛCDM fits better\n\n"

    summary += "ISW EFFECT:\n"
    summary += f"  QCT/ΛCDM = {ISW_qct_ratio:.2f}±{ISW_qct_ratio_err:.2f}\n"
    summary += f"  Observed = {ISW_amplitude_ratio:.2f}±{ISW_amplitude_err:.2f}\n"
    summary += f"  Tension: {isw_tension:.1f}σ\n\n"

    summary += "OVERALL ASSESSMENT:\n"
    if w0_sigma < 2 and chi2_qct < 2*ndof and isw_tension < 2:
        summary += "  ✓ QCT is CONSISTENT with Planck 2018\n"
        summary += "    within 2σ confidence level"
    elif w0_sigma < 3 and chi2_qct < 3*ndof and isw_tension < 3:
        summary += "  ~ QCT shows MILD TENSION\n"
        summary += "    but not ruled out (< 3σ)"
    else:
        summary += "  ✗ QCT shows SIGNIFICANT TENSION\n"
        summary += "    with Planck measurements (> 3σ)\n"
        summary += "    → Model parameters need adjustment"

    ax5.text(0.1, 0.9, summary, transform=ax5.transAxes,
             fontsize=9, verticalalignment='top', family='monospace',
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3))

    plt.savefig('/home/user/QCT_13/qct_vs_planck2018_comparison.png',
                dpi=300, bbox_inches='tight')
    print("✓ Figure saved: qct_vs_planck2018_comparison.png")

    plt.show()

    return w0_qct, wa_qct, chi2_qct, chi2_lcdm, isw_tension

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

if __name__ == "__main__":
    print("="*80)
    print("QCT vs PLANCK 2018: CMB DATA COMPARISON")
    print("="*80)
    print()

    print("PLANCK 2018 CONSTRAINTS:")
    print("-"*80)
    print(f"H₀ = {PLANCK_H0} ± {PLANCK_H0_err} km/s/Mpc")
    print(f"Ω_m = {PLANCK_Omega_m} ± {PLANCK_Omega_m_err}")
    print(f"Ω_Λ = {PLANCK_Omega_Lambda} ± {PLANCK_Omega_Lambda_err}")
    print(f"w₀ = {PLANCK_w0} ± {PLANCK_w0_err}")
    print(f"wₐ = {PLANCK_wa} ± {PLANCK_wa_err}")
    print()

    print("H(z) DATA POINTS:")
    print("-"*80)
    for z, H, err, src in zip(H_z_data['z'], H_z_data['H'],
                               H_z_data['H_err'], H_z_data['source']):
        print(f"z={z:.2f}: H={H:.1f}±{err:.1f} km/s/Mpc ({src})")
    print()

    print("Running QCT model and comparison...")
    print()

    w0, wa, chi2_qct, chi2_lcdm, isw_tension = plot_qct_vs_planck()

    print()
    print("="*80)
    print("RESULTS")
    print("="*80)
    print(f"QCT effective w₀ = {w0:.4f}")
    print(f"QCT effective wₐ = {w0:.4f}")
    print(f"χ²(QCT) = {chi2_qct:.2f}")
    print(f"χ²(ΛCDM) = {chi2_lcdm:.2f}")
    print(f"ISW tension = {isw_tension:.2f}σ")
    print("="*80)
