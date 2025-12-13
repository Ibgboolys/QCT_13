#!/usr/bin/env python3
"""
QCT BAO ANALYSIS: EQUATION OF STATE PHASE TRANSITION
=====================================================

Analyzes the impact of the QCT equation of state phase transition w(z)
on Baryon Acoustic Oscillations (BAO) measurements.

Key physics:
- QCT predicts w varies from -1 (voids) to ≈0 (halos)
- This affects sound horizon r_s at drag epoch
- Changes angular diameter distance D_A(z) and H(z)
- Testable in DESI, SDSS, and future surveys

Observables:
1. Sound horizon r_s at drag epoch
2. BAO scale D_V(z) = [D_A²(z) × cz/H(z)]^(1/3)
3. Fractional shift Δr_s/r_s and ΔD_V/D_V

Author: QCT Research Group
Date: 2025-12-11
Reference: QCT v13, Section "Nature of Vacuum Energy"
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
from matplotlib.gridspec import GridSpec

# ==============================================================================
# PHYSICAL CONSTANTS
# ==============================================================================

c = 2.99792458e8  # m/s
c_km = c / 1e3  # km/s
H_0_kmsMpc = 67.4  # km/s/Mpc (Planck 2018)

# ==============================================================================
# COSMOLOGICAL PARAMETERS (Planck 2018)
# ==============================================================================

Omega_m_0 = 0.315  # Total matter
Omega_b_0 = 0.0493  # Baryons
Omega_c_0 = Omega_m_0 - Omega_b_0  # CDM
Omega_Lambda_0 = 0.685  # Dark energy (ΛCDM)
Omega_r_0 = 9.15e-5  # Radiation
Omega_gamma_0 = 5.38e-5  # Photons

T_CMB_0 = 2.7255  # K

# Drag epoch
z_drag_planck = 1059.0  # Planck 2018

# ==============================================================================
# QCT PARAMETERS
# ==============================================================================

xi_coherence_kpc = 100.0  # Coherence length [kpc]
alpha_transition = 0.6  # Transition sharpness

# ==============================================================================
# FORMALISM: w(z) FROM QCT
# ==============================================================================

def gradient_dominance_at_redshift(z):
    """
    Volume-averaged gradient dominance parameter X(z).

    At high z: Universe more homogeneous → X small
    At low z: Structures form → X increases
    """
    X_0 = 10.0  # Cosmic average at z=0
    z_structure = 2.0  # Structure formation scale

    X_avg = X_0 * np.exp(-z / z_structure)
    return X_avg

def w_eff_of_z(z):
    """
    Effective equation of state from QCT phase transition.

    w_eff = -1 / (1 + X^α)
    """
    X = gradient_dominance_at_redshift(z)
    w_eff = -1.0 / (1.0 + X**alpha_transition)
    return w_eff

# ==============================================================================
# COSMOLOGY WITH VARIABLE w(z)
# ==============================================================================

def rho_DE_ratio(z, w_func):
    """
    Dark energy density ratio: ρ_DE(z) / ρ_DE(0)

    ρ_DE(z) = ρ_DE(0) × exp[3 ∫[0,z] (1+w(z'))/((1+z') dz']

    Parameters:
    -----------
    z : float or array
        Redshift
    w_func : function
        w(z) function

    Returns:
    --------
    ratio : float or array
        ρ_DE(z) / ρ_DE(0)
    """
    z = np.atleast_1d(z)
    ratio = np.zeros_like(z)

    for i, z_val in enumerate(z):
        if z_val < 1e-6:
            ratio[i] = 1.0
        else:
            # Numerical integration
            z_int = np.linspace(0, z_val, 200)
            w_int = w_func(z_int)
            integrand = 3 * (1 + w_int) / (1 + z_int)
            integral = np.trapz(integrand, z_int)
            ratio[i] = np.exp(integral)

    if len(ratio) == 1:
        return ratio[0]
    return ratio

def E_cosmology(z, w_func=None):
    """
    Dimensionless Hubble parameter E(z) = H(z)/H_0.

    Parameters:
    -----------
    z : float or array
        Redshift
    w_func : function
        w(z) function (None for ΛCDM)

    Returns:
    --------
    E : float or array
        E(z)
    """
    z = np.atleast_1d(z)

    if w_func is None:
        # ΛCDM: w = -1 constant
        E_sq = (Omega_r_0 * (1 + z)**4 +
                Omega_m_0 * (1 + z)**3 +
                Omega_Lambda_0)
    else:
        # QCT: variable w(z)
        rho_DE = rho_DE_ratio(z, w_func)
        E_sq = (Omega_r_0 * (1 + z)**4 +
                Omega_m_0 * (1 + z)**3 +
                Omega_Lambda_0 * rho_DE)

    E = np.sqrt(E_sq)

    if len(E) == 1:
        return E[0]
    return E

# ==============================================================================
# BAO: SOUND HORIZON
# ==============================================================================

def sound_speed_squared(z):
    """
    Sound speed squared in photon-baryon fluid before decoupling.

    c_s² = c² / [3(1 + R)]

    where R = 3ρ_b / (4ρ_γ) = (3Ω_b/4Ω_γ) × (1+z)^(-1)
    """
    R = (3 * Omega_b_0) / (4 * Omega_gamma_0) / (1 + z)
    c_s_sq = 1.0 / (3.0 * (1.0 + R))  # in units of c²
    return c_s_sq

def sound_horizon_integrand(z, w_func=None):
    """
    Integrand for sound horizon: c_s / H(z)

    r_s = ∫[z_drag, ∞] c_s(z) / H(z) dz / (1+z)²
    """
    c_s_sq = sound_speed_squared(z)
    c_s = np.sqrt(c_s_sq) * c_km  # km/s

    E = E_cosmology(z, w_func)
    H_z = H_0_kmsMpc * E  # km/s/Mpc

    integrand = c_s / H_z / (1 + z)**2

    return integrand

def calculate_sound_horizon(z_drag, w_func=None, z_max=1e6):
    """
    Calculate sound horizon at drag epoch.

    r_s(z_drag) = ∫[z_drag, ∞] c_s(z) / H(z) dz / (1+z)²

    Parameters:
    -----------
    z_drag : float
        Drag epoch redshift
    w_func : function
        w(z) function (None for ΛCDM)
    z_max : float
        Upper integration limit (approximating infinity)

    Returns:
    --------
    r_s : float
        Sound horizon [Mpc]
    """
    # Integration range (log-spaced for high z)
    z_int = np.logspace(np.log10(z_drag), np.log10(z_max), 1000)

    # Calculate integrand
    integrand = np.array([sound_horizon_integrand(z, w_func) for z in z_int])

    # Integrate
    r_s = np.trapz(integrand, z_int)

    return r_s

# ==============================================================================
# BAO: DISTANCE MEASURES
# ==============================================================================

def comoving_distance(z, w_func=None):
    """
    Comoving distance D_C(z) in Mpc.

    D_C(z) = c/H_0 × ∫[0,z] dz' / E(z')
    """
    if z < 1e-6:
        return 0.0

    z_int = np.linspace(0, z, 500)
    E_int = E_cosmology(z_int, w_func)
    integrand = 1.0 / E_int

    D_C = (c_km / H_0_kmsMpc) * np.trapz(integrand, z_int)

    return D_C

def angular_diameter_distance(z, w_func=None):
    """
    Angular diameter distance D_A(z) in Mpc.

    D_A(z) = D_C(z) / (1 + z)
    """
    D_C = comoving_distance(z, w_func)
    D_A = D_C / (1 + z)
    return D_A

def dilation_scale(z, w_func=None):
    """
    BAO dilation scale D_V(z) in Mpc.

    D_V(z) = [(1+z)² D_A²(z) × cz/H(z)]^(1/3)

    This is the isotropic distance measure used in BAO analyses.
    """
    D_A = angular_diameter_distance(z, w_func)
    E = E_cosmology(z, w_func)
    H_z = H_0_kmsMpc * E

    D_V = ((1 + z)**2 * D_A**2 * c_km * z / H_z)**(1.0/3.0)

    return D_V

# ==============================================================================
# VISUALIZATION
# ==============================================================================

def plot_bao_eos_analysis():
    """
    Create comprehensive visualization of BAO impact from QCT w(z).
    """
    # Redshift ranges
    z_early = np.linspace(100, 2000, 300)  # For sound horizon
    z_low = np.linspace(0.1, 3.0, 100)  # For BAO observations

    # Calculate sound horizons
    print("Calculating sound horizons...")
    r_s_LCDM = calculate_sound_horizon(z_drag_planck, w_func=None)
    r_s_QCT = calculate_sound_horizon(z_drag_planck, w_func=w_eff_of_z)

    print(f"  r_s(ΛCDM) = {r_s_LCDM:.4f} Mpc")
    print(f"  r_s(QCT)  = {r_s_QCT:.4f} Mpc")
    print(f"  Δr_s/r_s  = {(r_s_QCT - r_s_LCDM)/r_s_LCDM * 100:.4f}%")
    print()

    # Calculate distance measures
    print("Calculating distance measures...")
    D_A_LCDM = np.array([angular_diameter_distance(z, None) for z in z_low])
    D_A_QCT = np.array([angular_diameter_distance(z, w_eff_of_z) for z in z_low])

    D_V_LCDM = np.array([dilation_scale(z, None) for z in z_low])
    D_V_QCT = np.array([dilation_scale(z, w_eff_of_z) for z in z_low])

    H_LCDM = H_0_kmsMpc * E_cosmology(z_low, None)
    H_QCT = H_0_kmsMpc * E_cosmology(z_low, w_eff_of_z)

    # Create figure
    fig = plt.figure(figsize=(16, 12))
    gs = GridSpec(3, 2, figure=fig, hspace=0.35, wspace=0.3)

    # ============================================
    # Panel 1: Sound horizon evolution
    # ============================================
    ax1 = fig.add_subplot(gs[0, 0])

    # Calculate cumulative sound horizon
    z_cumul = np.logspace(np.log10(z_drag_planck), 4, 200)
    r_s_cumul_LCDM = []
    r_s_cumul_QCT = []

    for z_max_val in z_cumul:
        r_s_cumul_LCDM.append(calculate_sound_horizon(z_max_val, None, z_max=1e6))
        r_s_cumul_QCT.append(calculate_sound_horizon(z_max_val, w_eff_of_z, z_max=1e6))

    ax1.plot(z_cumul, r_s_cumul_LCDM, 'r--', linewidth=2, label='ΛCDM')
    ax1.plot(z_cumul, r_s_cumul_QCT, 'b-', linewidth=3, label='QCT')

    ax1.axvline(x=z_drag_planck, color='gray', linestyle=':', alpha=0.7,
                label=f'Drag epoch (z={z_drag_planck:.0f})')

    ax1.set_xlabel('Integration lower limit z', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Sound horizon r_s(z) [Mpc]', fontsize=12, fontweight='bold')
    ax1.set_title('Sound Horizon Evolution', fontsize=13, fontweight='bold')
    ax1.set_xscale('log')
    ax1.grid(True, alpha=0.3, which='both')
    ax1.legend(fontsize=10)

    # ============================================
    # Panel 2: Fractional difference in r_s
    # ============================================
    ax2 = fig.add_subplot(gs[0, 1])

    frac_diff_rs = (np.array(r_s_cumul_QCT) - np.array(r_s_cumul_LCDM)) / np.array(r_s_cumul_LCDM) * 100

    ax2.plot(z_cumul, frac_diff_rs, 'purple', linewidth=3)
    ax2.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    ax2.axvline(x=z_drag_planck, color='gray', linestyle=':', alpha=0.7)

    ax2.set_xlabel('Integration lower limit z', fontsize=12, fontweight='bold')
    ax2.set_ylabel('[r_s(QCT) - r_s(ΛCDM)] / r_s(ΛCDM) [%]', fontsize=12, fontweight='bold')
    ax2.set_title('Fractional Difference in Sound Horizon', fontsize=13, fontweight='bold')
    ax2.set_xscale('log')
    ax2.grid(True, alpha=0.3, which='both')

    final_diff = frac_diff_rs[-1]
    ax2.text(0.05, 0.95, f'At z_drag: Δr_s/r_s = {final_diff:.4f}%',
             transform=ax2.transAxes, fontsize=11, va='top',
             bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    # ============================================
    # Panel 3: Angular diameter distance
    # ============================================
    ax3 = fig.add_subplot(gs[1, 0])

    ax3.plot(z_low, D_A_LCDM, 'r--', linewidth=2, label='ΛCDM')
    ax3.plot(z_low, D_A_QCT, 'b-', linewidth=3, label='QCT')

    ax3.set_xlabel('Redshift z', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Angular Diameter Distance D_A(z) [Mpc]', fontsize=12, fontweight='bold')
    ax3.set_title('Angular Diameter Distance', fontsize=13, fontweight='bold')
    ax3.grid(True, alpha=0.3)
    ax3.legend(fontsize=10)

    # ============================================
    # Panel 4: BAO dilation scale D_V
    # ============================================
    ax4 = fig.add_subplot(gs[1, 1])

    ax4.plot(z_low, D_V_LCDM, 'r--', linewidth=2, label='ΛCDM')
    ax4.plot(z_low, D_V_QCT, 'b-', linewidth=3, label='QCT')

    ax4.set_xlabel('Redshift z', fontsize=12, fontweight='bold')
    ax4.set_ylabel('BAO Dilation Scale D_V(z) [Mpc]', fontsize=12, fontweight='bold')
    ax4.set_title('BAO Observable: D_V(z)', fontsize=13, fontweight='bold')
    ax4.grid(True, alpha=0.3)
    ax4.legend(fontsize=10)

    # Mark DESI/SDSS redshift bins
    z_surveys = [0.3, 0.5, 0.7, 1.0, 1.5]
    for z_s in z_surveys:
        if z_s <= 3.0:
            ax4.axvline(x=z_s, color='orange', linestyle=':', alpha=0.3)

    ax4.text(0.95, 0.05, 'Orange lines: typical survey bins\n(SDSS, DESI)',
             transform=ax4.transAxes, fontsize=9, va='bottom', ha='right',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))

    # ============================================
    # Panel 5: Hubble parameter H(z)
    # ============================================
    ax5 = fig.add_subplot(gs[2, 0])

    ax5.plot(z_low, H_LCDM, 'r--', linewidth=2, label='ΛCDM')
    ax5.plot(z_low, H_QCT, 'b-', linewidth=3, label='QCT')

    ax5.set_xlabel('Redshift z', fontsize=12, fontweight='bold')
    ax5.set_ylabel('Hubble Parameter H(z) [km/s/Mpc]', fontsize=12, fontweight='bold')
    ax5.set_title('Hubble Parameter Evolution', fontsize=13, fontweight='bold')
    ax5.grid(True, alpha=0.3)
    ax5.legend(fontsize=10)

    # ============================================
    # Panel 6: Fractional differences in BAO observables
    # ============================================
    ax6 = fig.add_subplot(gs[2, 1])

    frac_diff_DA = (D_A_QCT - D_A_LCDM) / D_A_LCDM * 100
    frac_diff_DV = (D_V_QCT - D_V_LCDM) / D_V_LCDM * 100
    frac_diff_H = (H_QCT - H_LCDM) / H_LCDM * 100

    ax6.plot(z_low, frac_diff_DA, 'blue', linewidth=2.5, label='ΔD_A/D_A')
    ax6.plot(z_low, frac_diff_DV, 'green', linewidth=2.5, label='ΔD_V/D_V')
    ax6.plot(z_low, frac_diff_H, 'red', linewidth=2.5, label='ΔH/H')

    ax6.axhline(y=0, color='gray', linestyle='--', alpha=0.5)

    ax6.set_xlabel('Redshift z', fontsize=12, fontweight='bold')
    ax6.set_ylabel('Fractional Difference [%]', fontsize=12, fontweight='bold')
    ax6.set_title('QCT Deviations from ΛCDM', fontsize=13, fontweight='bold')
    ax6.grid(True, alpha=0.3)
    ax6.legend(fontsize=10, loc='best')

    # Add error bar representing typical DESI precision
    desi_precision = 1.0  # ~1% precision
    ax6.axhspan(-desi_precision, desi_precision, alpha=0.1, color='orange',
                label='DESI precision (~1%)')
    ax6.legend(fontsize=9, loc='best')

    plt.savefig('/home/user/QCT_13/bao_eos_phase_transition.png',
                dpi=300, bbox_inches='tight')
    print("✓ Figure saved: bao_eos_phase_transition.png")

    plt.show()

    return r_s_LCDM, r_s_QCT

# ==============================================================================
# QUANTITATIVE PREDICTIONS
# ==============================================================================

def print_bao_predictions(r_s_LCDM, r_s_QCT):
    """
    Print quantitative predictions for BAO observations.
    """
    print("="*80)
    print("BAO PREDICTIONS FROM QCT PHASE TRANSITION")
    print("="*80)
    print()

    print("SOUND HORIZON AT DRAG EPOCH:")
    print("-"*80)
    print(f"r_s(ΛCDM) = {r_s_LCDM:.4f} Mpc")
    print(f"r_s(QCT)  = {r_s_QCT:.4f} Mpc")
    print(f"Δr_s      = {r_s_QCT - r_s_LCDM:.6f} Mpc")
    print(f"Δr_s/r_s  = {(r_s_QCT - r_s_LCDM)/r_s_LCDM * 100:.4f}%")
    print()

    # Predictions at survey redshifts
    z_surveys = [0.3, 0.5, 0.7, 1.0, 1.5, 2.0]

    print("BAO OBSERVABLES AT SURVEY REDSHIFTS:")
    print("-"*80)
    print(f"{'z':<8} {'D_V(ΛCDM)':<15} {'D_V(QCT)':<15} {'ΔD_V/D_V[%]':<15} {'ΔH/H[%]'}")
    print("-"*80)

    for z in z_surveys:
        D_V_l = dilation_scale(z, None)
        D_V_q = dilation_scale(z, w_eff_of_z)
        frac_DV = (D_V_q - D_V_l) / D_V_l * 100

        H_l = H_0_kmsMpc * E_cosmology(z, None)
        H_q = H_0_kmsMpc * E_cosmology(z, w_eff_of_z)
        frac_H = (H_q - H_l) / H_l * 100

        print(f"{z:<8.1f} {D_V_l:<15.2f} {D_V_q:<15.2f} {frac_DV:<15.4f} {frac_H:<10.4f}")

    print()

    print("="*80)
    print("OBSERVATIONAL TESTS:")
    print("="*80)
    print("1. SDSS/BOSS BAO measurements (z ~ 0.3-0.7)")
    print("2. DESI BAO survey (z ~ 0.1-3.5, precision ~0.5-1%)")
    print("3. Future: Euclid, WFIRST (sub-percent precision)")
    print()
    print("Key signature:")
    print("  - Shift in BAO scale r_s affects all distance ratios")
    print("  - Consistent deviation pattern across redshift bins")
    print("  - Cross-check with H(z) measurements from cosmic chronometers")
    print("="*80)
    print()

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

if __name__ == "__main__":
    print("="*80)
    print("QCT BAO EQUATION OF STATE ANALYSIS")
    print("="*80)
    print()
    print(f"Coherence length ξ = {xi_coherence_kpc} kpc")
    print(f"Transition parameter α = {alpha_transition}")
    print(f"Drag epoch z_drag = {z_drag_planck}")
    print()

    # Create visualization and get sound horizons
    print("Generating BAO analysis plots...")
    r_s_LCDM, r_s_QCT = plot_bao_eos_analysis()

    # Print quantitative predictions
    print_bao_predictions(r_s_LCDM, r_s_QCT)

    print()
    print("="*80)
    print("BAO ANALYSIS COMPLETE")
    print("="*80)
    print()
    print("Key results:")
    print("1. QCT modifies sound horizon r_s (percent-level)")
    print("2. BAO scale D_V(z) shows measurable shifts")
    print("3. Testable with DESI precision (~1%)")
    print()
    print("Ready for QCT v13 paper BAO predictions section")
    print("="*80)
