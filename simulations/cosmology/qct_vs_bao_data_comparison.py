#!/usr/bin/env python3
"""
QCT vs BAO DATA: DESI/SDSS COMPARISON
======================================

Direct comparison of QCT predictions with BAO measurements from:
- SDSS/BOSS DR12 (2016)
- eBOSS DR16 (2020)
- DESI Year 1 (2024)

Data sources:
1. SDSS-III/BOSS: arXiv:1607.03155
2. eBOSS: arXiv:2007.08991
3. DESI Y1: arXiv:2404.03002

Key observables:
- D_M(z) / r_d: Angular diameter distance
- D_H(z) / r_d: Hubble distance
- D_V(z) / r_d: Dilation scale (isotropic)
- f σ₈(z): Growth rate

Author: QCT Research Group
Date: 2025-12-11
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# ==============================================================================
# BAO DATA COMPILATION
# ==============================================================================

# Sound horizon from Planck 2018 (used as standard ruler)
r_d_Planck = 147.09  # Mpc (Planck 2018, TT,TE,EE+lowE+lensing)
r_d_Planck_err = 0.26

# SDSS/BOSS DR12 (arXiv:1607.03155)
BOSS_data = {
    'z': np.array([0.38, 0.51, 0.61]),
    'DM_over_rd': np.array([1512.39, 1975.22, 2306.68]),  # Mpc
    'DM_over_rd_err': np.array([24.99, 30.10, 40.13]),
    'DH_over_rd': np.array([2404.48, 2161.65, 1998.34]),
    'DH_over_rd_err': np.array([104.67, 82.99, 70.09]),
    'source': 'BOSS DR12'
}

# eBOSS DR16 (arXiv:2007.08991)
eBOSS_data = {
    'z': np.array([0.698, 1.48]),
    'DM_over_rd': np.array([2620.0, 3850.0]),
    'DM_over_rd_err': np.array([60.0, 140.0]),
    'DH_over_rd': np.array([1860.0, 1350.0]),
    'DH_over_rd_err': np.array([80.0, 90.0]),
    'source': 'eBOSS DR16'
}

# DESI Year 1 (arXiv:2404.03002) - Selected redshift bins
# These are the most precise BAO measurements to date
DESI_data = {
    'z': np.array([0.295, 0.510, 0.706, 0.930, 1.317, 2.330]),
    'DV_over_rd': np.array([7.93, 13.62, 17.85, 21.71, 27.79, 39.71]),  # Dimensionless
    'DV_over_rd_err': np.array([0.14, 0.17, 0.27, 0.35, 0.45, 0.94]),
    'source': 'DESI Y1'
}

# Combined H(z) measurements (cosmic chronometers + BAO)
H_z_data = {
    'z': np.array([0.070, 0.090, 0.120, 0.170, 0.179, 0.199, 0.270,
                   0.350, 0.400, 0.440, 0.480, 0.570, 0.600, 0.680,
                   0.730, 0.780, 0.880, 0.900, 1.037, 1.300, 1.430,
                   1.530, 1.750, 1.965, 2.300, 2.340]),
    'H': np.array([69.0, 69.0, 68.6, 83.0, 75.0, 75.0, 77.0,
                   76.3, 82.0, 82.6, 97.0, 87.9, 87.9, 92.0,
                   97.3, 105.0, 90.0, 117.0, 154.0, 168.0, 177.0,
                   140.0, 202.0, 186.5, 224.0, 222.0]),
    'H_err': np.array([19.6, 12.0, 26.2, 8.0, 4.0, 5.0, 14.0,
                      2.2, 9.0, 7.8, 62.0, 6.1, 6.1, 8.0,
                      7.0, 12.0, 40.0, 23.0, 20.0, 17.0, 18.0,
                      14.0, 40.0, 50.4, 8.6, 7.0]),
    'source': 'Compilation (cosmic chronometers + BAO)'
}

# ==============================================================================
# COSMOLOGICAL PARAMETERS
# ==============================================================================

H_0 = 67.4  # km/s/Mpc (Planck 2018)
c_km = 299792.458  # km/s

Omega_m_0 = 0.315
Omega_Lambda_0 = 0.685
Omega_r_0 = 9.15e-5

# ==============================================================================
# QCT MODEL
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
    """Dark energy density evolution."""
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

def E_cosmology(z, model='QCT'):
    """Dimensionless Hubble parameter E(z) = H(z)/H_0."""
    if model == 'LCDM':
        E_sq = (Omega_r_0 * (1 + z)**4 +
                Omega_m_0 * (1 + z)**3 +
                Omega_Lambda_0)
    else:  # QCT
        rho_DE = rho_DE_ratio(z)
        E_sq = (Omega_r_0 * (1 + z)**4 +
                Omega_m_0 * (1 + z)**3 +
                Omega_Lambda_0 * rho_DE)
    return np.sqrt(E_sq)

def H_z(z, model='QCT'):
    """Hubble parameter H(z) [km/s/Mpc]."""
    return H_0 * E_cosmology(z, model)

def comoving_distance(z, model='QCT'):
    """Comoving distance D_C(z) [Mpc]."""
    if z < 1e-6:
        return 0.0

    z_int = np.linspace(0, z, 500)
    E_int = E_cosmology(z_int, model)
    integrand = 1.0 / E_int

    D_C = (c_km / H_0) * np.trapezoid(integrand, z_int)
    return D_C

def DM_over_rd(z, r_d, model='QCT'):
    """Angular diameter distance over sound horizon: D_M(z) / r_d."""
    D_C = comoving_distance(z, model)
    D_M = D_C / (1 + z)  # Angular diameter distance
    return D_M / r_d

def DH_over_rd(z, r_d, model='QCT'):
    """Hubble distance over sound horizon: D_H(z) / r_d = c / [H(z) × r_d]."""
    H_val = H_z(z, model)
    D_H = c_km / H_val
    return D_H / r_d

def DV_over_rd(z, r_d, model='QCT'):
    """Isotropic dilation scale over sound horizon: D_V(z) / r_d."""
    D_M = comoving_distance(z, model) / (1 + z)
    D_H = c_km / H_z(z, model)
    D_V = ((1 + z)**2 * D_M**2 * z * c_km / H_z(z, model))**(1.0/3.0)
    return D_V / r_d

# ==============================================================================
# VISUALIZATION
# ==============================================================================

def plot_qct_vs_bao_data():
    """
    Create comprehensive comparison with BAO data.
    """
    z_range = np.linspace(0.01, 3.0, 300)

    # Use Planck r_d as fiducial
    r_d = r_d_Planck

    # Calculate QCT and ΛCDM predictions
    DM_qct = np.array([DM_over_rd(z, r_d, 'QCT') for z in z_range])
    DM_lcdm = np.array([DM_over_rd(z, r_d, 'LCDM') for z in z_range])

    DH_qct = np.array([DH_over_rd(z, r_d, 'QCT') for z in z_range])
    DH_lcdm = np.array([DH_over_rd(z, r_d, 'LCDM') for z in z_range])

    DV_qct = np.array([DV_over_rd(z, r_d, 'QCT') for z in z_range])
    DV_lcdm = np.array([DV_over_rd(z, r_d, 'LCDM') for z in z_range])

    H_qct = H_z(z_range, 'QCT')
    H_lcdm = H_z(z_range, 'LCDM')

    # Create figure
    fig = plt.figure(figsize=(18, 12))
    gs = GridSpec(3, 3, figure=fig, hspace=0.35, wspace=0.35)

    # ============================================
    # Panel 1: D_M / r_d
    # ============================================
    ax1 = fig.add_subplot(gs[0, 0])

    ax1.plot(z_range, DM_qct, 'b-', linewidth=3, label='QCT', zorder=3)
    ax1.plot(z_range, DM_lcdm, 'r--', linewidth=2, label='ΛCDM', zorder=2)

    # Plot BOSS data
    ax1.errorbar(BOSS_data['z'], BOSS_data['DM_over_rd'],
                 yerr=BOSS_data['DM_over_rd_err'],
                 fmt='o', color='green', markersize=8, capsize=5,
                 label='BOSS DR12', zorder=5)

    # Plot eBOSS data
    ax1.errorbar(eBOSS_data['z'], eBOSS_data['DM_over_rd'],
                 yerr=eBOSS_data['DM_over_rd_err'],
                 fmt='s', color='orange', markersize=8, capsize=5,
                 label='eBOSS DR16', zorder=5)

    ax1.set_xlabel('Redshift z', fontsize=11, fontweight='bold')
    ax1.set_ylabel('D_M(z) / r_d', fontsize=11, fontweight='bold')
    ax1.set_title('Angular Diameter Distance', fontsize=12, fontweight='bold')
    ax1.set_xlim(0, 2.0)
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=8, loc='upper left')

    # ============================================
    # Panel 2: D_H / r_d
    # ============================================
    ax2 = fig.add_subplot(gs[0, 1])

    ax2.plot(z_range, DH_qct, 'b-', linewidth=3, label='QCT', zorder=3)
    ax2.plot(z_range, DH_lcdm, 'r--', linewidth=2, label='ΛCDM', zorder=2)

    # Plot BOSS data
    ax2.errorbar(BOSS_data['z'], BOSS_data['DH_over_rd'],
                 yerr=BOSS_data['DH_over_rd_err'],
                 fmt='o', color='green', markersize=8, capsize=5,
                 label='BOSS DR12', zorder=5)

    # Plot eBOSS data
    ax2.errorbar(eBOSS_data['z'], eBOSS_data['DH_over_rd'],
                 yerr=eBOSS_data['DH_over_rd_err'],
                 fmt='s', color='orange', markersize=8, capsize=5,
                 label='eBOSS DR16', zorder=5)

    ax2.set_xlabel('Redshift z', fontsize=11, fontweight='bold')
    ax2.set_ylabel('D_H(z) / r_d = c / [H(z) r_d]', fontsize=11, fontweight='bold')
    ax2.set_title('Hubble Distance', fontsize=12, fontweight='bold')
    ax2.set_xlim(0, 2.0)
    ax2.grid(True, alpha=0.3)
    ax2.legend(fontsize=8, loc='upper right')

    # ============================================
    # Panel 3: D_V / r_d (DESI)
    # ============================================
    ax3 = fig.add_subplot(gs[0, 2])

    ax3.plot(z_range, DV_qct, 'b-', linewidth=3, label='QCT', zorder=3)
    ax3.plot(z_range, DV_lcdm, 'r--', linewidth=2, label='ΛCDM', zorder=2)

    # Plot DESI data (most precise!)
    ax3.errorbar(DESI_data['z'], DESI_data['DV_over_rd'],
                 yerr=DESI_data['DV_over_rd_err'],
                 fmt='D', color='purple', markersize=8, capsize=5,
                 label='DESI Y1', zorder=5, linewidth=2)

    ax3.set_xlabel('Redshift z', fontsize=11, fontweight='bold')
    ax3.set_ylabel('D_V(z) / r_d', fontsize=11, fontweight='bold')
    ax3.set_title('BAO Dilation Scale (Isotropic)', fontsize=12, fontweight='bold')
    ax3.set_xlim(0, 2.5)
    ax3.grid(True, alpha=0.3)
    ax3.legend(fontsize=8, loc='upper left')

    # ============================================
    # Panel 4: Residuals D_M
    # ============================================
    ax4 = fig.add_subplot(gs[1, 0])

    # Calculate residuals for BOSS
    z_boss = BOSS_data['z']
    DM_boss_qct = np.array([DM_over_rd(z, r_d, 'QCT') for z in z_boss])
    DM_boss_lcdm = np.array([DM_over_rd(z, r_d, 'LCDM') for z in z_boss])

    residual_boss_qct = (DM_boss_qct - BOSS_data['DM_over_rd']) / BOSS_data['DM_over_rd_err']
    residual_boss_lcdm = (DM_boss_lcdm - BOSS_data['DM_over_rd']) / BOSS_data['DM_over_rd_err']

    x_pos = np.arange(len(z_boss))
    width = 0.35

    ax4.bar(x_pos - width/2, residual_boss_qct, width, label='QCT', color='blue', alpha=0.7)
    ax4.bar(x_pos + width/2, residual_boss_lcdm, width, label='ΛCDM', color='red', alpha=0.7)

    ax4.axhline(y=0, color='black', linestyle='-', linewidth=1)
    ax4.axhline(y=1, color='gray', linestyle='--', alpha=0.5)
    ax4.axhline(y=-1, color='gray', linestyle='--', alpha=0.5)

    ax4.set_ylabel('Residual [σ]', fontsize=11, fontweight='bold')
    ax4.set_title('D_M Residuals (BOSS)', fontsize=12, fontweight='bold')
    ax4.set_xticks(x_pos)
    ax4.set_xticklabels([f'z={z:.2f}' for z in z_boss])
    ax4.grid(True, alpha=0.3, axis='y')
    ax4.legend(fontsize=8)

    # ============================================
    # Panel 5: Residuals D_V (DESI)
    # ============================================
    ax5 = fig.add_subplot(gs[1, 1])

    z_desi = DESI_data['z']
    DV_desi_qct = np.array([DV_over_rd(z, r_d, 'QCT') for z in z_desi])
    DV_desi_lcdm = np.array([DV_over_rd(z, r_d, 'LCDM') for z in z_desi])

    residual_desi_qct = (DV_desi_qct - DESI_data['DV_over_rd']) / DESI_data['DV_over_rd_err']
    residual_desi_lcdm = (DV_desi_lcdm - DESI_data['DV_over_rd']) / DESI_data['DV_over_rd_err']

    x_pos = np.arange(len(z_desi))
    width = 0.35

    ax5.bar(x_pos - width/2, residual_desi_qct, width, label='QCT', color='blue', alpha=0.7)
    ax5.bar(x_pos + width/2, residual_desi_lcdm, width, label='ΛCDM', color='red', alpha=0.7)

    ax5.axhline(y=0, color='black', linestyle='-', linewidth=1)
    ax5.axhline(y=2, color='gray', linestyle='--', alpha=0.5)
    ax5.axhline(y=-2, color='gray', linestyle='--', alpha=0.5)

    ax5.set_ylabel('Residual [σ]', fontsize=11, fontweight='bold')
    ax5.set_title('D_V Residuals (DESI Y1)', fontsize=12, fontweight='bold')
    ax5.set_xticks(x_pos)
    ax5.set_xticklabels([f'{z:.2f}' for z in z_desi], rotation=45, fontsize=8)
    ax5.grid(True, alpha=0.3, axis='y')
    ax5.legend(fontsize=8)

    # Calculate χ²
    chi2_desi_qct = np.sum(residual_desi_qct**2)
    chi2_desi_lcdm = np.sum(residual_desi_lcdm**2)

    textstr = f'χ²/ndof:\nQCT: {chi2_desi_qct:.1f}/{len(z_desi)}\nΛCDM: {chi2_desi_lcdm:.1f}/{len(z_desi)}'
    ax5.text(0.95, 0.95, textstr, transform=ax5.transAxes, fontsize=9,
             va='top', ha='right', bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    # ============================================
    # Panel 6: H(z) measurements
    # ============================================
    ax6 = fig.add_subplot(gs[1, 2])

    ax6.plot(z_range, H_qct, 'b-', linewidth=3, label='QCT', zorder=3)
    ax6.plot(z_range, H_lcdm, 'r--', linewidth=2, label='ΛCDM', zorder=2)

    # Plot H(z) data (subsample for clarity)
    z_h = H_z_data['z'][::3]  # Every 3rd point
    H_h = H_z_data['H'][::3]
    H_h_err = H_z_data['H_err'][::3]

    ax6.errorbar(z_h, H_h, yerr=H_h_err, fmt='o', color='black',
                 markersize=6, capsize=4, alpha=0.6, label='Data', zorder=4)

    ax6.set_xlabel('Redshift z', fontsize=11, fontweight='bold')
    ax6.set_ylabel('H(z) [km/s/Mpc]', fontsize=11, fontweight='bold')
    ax6.set_title('Hubble Parameter Measurements', fontsize=12, fontweight='bold')
    ax6.set_xlim(0, 2.5)
    ax6.set_ylim(50, 250)
    ax6.grid(True, alpha=0.3)
    ax6.legend(fontsize=8, loc='upper left')

    # ============================================
    # Panel 7: Fractional differences
    # ============================================
    ax7 = fig.add_subplot(gs[2, :])

    frac_DM = (DM_qct - DM_lcdm) / DM_lcdm * 100
    frac_DH = (DH_qct - DH_lcdm) / DH_lcdm * 100
    frac_DV = (DV_qct - DV_lcdm) / DV_lcdm * 100

    ax7.plot(z_range, frac_DM, 'b-', linewidth=2.5, label='ΔD_M/D_M')
    ax7.plot(z_range, frac_DH, 'g-', linewidth=2.5, label='ΔD_H/D_H')
    ax7.plot(z_range, frac_DV, 'purple', linewidth=3, label='ΔD_V/D_V')

    ax7.axhline(y=0, color='gray', linestyle='--', alpha=0.5)

    # Add DESI precision band (±1%)
    ax7.axhspan(-1, 1, alpha=0.1, color='orange', label='DESI precision (~1%)')

    # Mark DESI redshift bins
    for z_d in DESI_data['z']:
        ax7.axvline(x=z_d, color='purple', linestyle=':', alpha=0.2)

    ax7.set_xlabel('Redshift z', fontsize=12, fontweight='bold')
    ax7.set_ylabel('Fractional Difference (QCT - ΛCDM) / ΛCDM [%]',
                   fontsize=12, fontweight='bold')
    ax7.set_title('QCT Deviations from ΛCDM vs DESI Precision',
                  fontsize=13, fontweight='bold')
    ax7.set_xlim(0, 2.5)
    ax7.set_ylim(-30, 10)
    ax7.grid(True, alpha=0.3)
    ax7.legend(fontsize=10, loc='lower left')

    plt.savefig('/home/user/QCT_13/qct_vs_bao_data_comparison.png',
                dpi=300, bbox_inches='tight')
    print("✓ Figure saved: qct_vs_bao_data_comparison.png")

    plt.show()

    return chi2_desi_qct, chi2_desi_lcdm

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

if __name__ == "__main__":
    print("="*80)
    print("QCT vs BAO DATA: DESI/SDSS COMPARISON")
    print("="*80)
    print()

    print("BAO DATA SETS:")
    print("-"*80)
    print(f"BOSS DR12:  {len(BOSS_data['z'])} redshift bins (z ~ 0.4-0.6)")
    print(f"eBOSS DR16: {len(eBOSS_data['z'])} redshift bins (z ~ 0.7-1.5)")
    print(f"DESI Y1:    {len(DESI_data['z'])} redshift bins (z ~ 0.3-2.3)")
    print(f"H(z) data:  {len(H_z_data['z'])} measurements (z ~ 0.1-2.3)")
    print()

    print(f"Sound horizon (Planck 2018): r_d = {r_d_Planck} ± {r_d_Planck_err} Mpc")
    print()

    print("Running comparison...")
    chi2_qct, chi2_lcdm = plot_qct_vs_bao_data()

    print()
    print("="*80)
    print("STATISTICAL SUMMARY")
    print("="*80)
    print(f"χ²(QCT) / DESI  = {chi2_qct:.2f} / {len(DESI_data['z'])}")
    print(f"χ²(ΛCDM) / DESI = {chi2_lcdm:.2f} / {len(DESI_data['z'])}")
    print()

    if chi2_qct < chi2_lcdm:
        print("→ QCT provides BETTER fit to DESI data!")
    else:
        Δχ2 = chi2_qct - chi2_lcdm
        print(f"→ ΛCDM fits better (Δχ² = {Δχ2:.2f})")

        if Δχ2 < 4:
            print("  QCT is still viable (Δχ² < 4)")
        elif Δχ2 < 9:
            print("  QCT shows mild tension (4 < Δχ² < 9)")
        else:
            print("  QCT ruled out at >3σ (Δχ² > 9)")

    print("="*80)
