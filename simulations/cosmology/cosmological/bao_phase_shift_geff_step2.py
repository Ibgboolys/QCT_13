#!/usr/bin/env python3
"""
BAO Phase Shift Calculator - Phase 1.2
Growth Rate Modifications from G_eff = 0.9 G_N

This script calculates how the modified gravity in QCT affects structure growth,
which in turn affects the BAO phase shift measurement.

Author: QCT Project (AI-assisted)
Date: 2025-11-19
"""

import math
import csv

# ==============================================================================
# PHYSICAL CONSTANTS
# ==============================================================================
c_km_s = 299792.458  # Speed of light in km/s
H0_planck = 67.4  # Hubble constant in km/s/Mpc (Planck 2018)
h_planck = H0_planck / 100.0

# Cosmological parameters (Planck 2018)
Omega_m_0 = 0.315  # Matter density today
Omega_b_0 = 0.049  # Baryon density today
Omega_Lambda_0 = 1.0 - Omega_m_0  # Dark energy density
Omega_r_0 = 9.24e-5  # Radiation density (negligible at late times)

# QCT parameter
G_eff_ratio = 0.9  # G_eff / G_N on astrophysical scales

# DESI redshift bins (from Whitford et al. 2024)
DESI_redshifts = {
    'BGS': 0.25,
    'LRG1': 0.51,
    'LRG2': 0.706,
    'LRG3+ELG1': 0.93,
    'ELG2': 1.317,
    'QSO': 1.49
}

# ==============================================================================
# COSMOLOGICAL FUNCTIONS
# ==============================================================================

def E_LCDM(z):
    """
    Dimensionless Hubble parameter E(z) = H(z)/H0 for ΛCDM.

    H(z)² = H0² [Ω_r(1+z)⁴ + Ω_m(1+z)³ + Ω_Λ]
    """
    return math.sqrt(
        Omega_r_0 * (1 + z)**4 +
        Omega_m_0 * (1 + z)**3 +
        Omega_Lambda_0
    )

def E_QCT(z):
    """
    Dimensionless Hubble parameter for QCT with G_eff = 0.9 G_N.

    Modified Friedmann equation:
    H²_QCT = (G_eff/G_N) H²_ΛCDM = 0.9 H²_ΛCDM

    Therefore: E_QCT(z) = √0.9 × E_ΛCDM(z)
    """
    return math.sqrt(G_eff_ratio) * E_LCDM(z)

def Omega_m(z, cosmology='LCDM'):
    """
    Matter density parameter Ω_m(z) = ρ_m(z) / ρ_crit(z).

    For ΛCDM: Ω_m(z) = Ω_m,0 (1+z)³ / E²(z)
    For QCT: Same form but with E_QCT(z)
    """
    E = E_QCT(z) if cosmology == 'QCT' else E_LCDM(z)
    return Omega_m_0 * (1 + z)**3 / E**2

# ==============================================================================
# GROWTH RATE CALCULATIONS
# ==============================================================================

def growth_rate_f(z, cosmology='LCDM'):
    """
    Growth rate f(z) = d(ln δ)/d(ln a) where δ is matter overdensity.

    For ΛCDM: f(z) ≈ Ω_m(z)^γ with γ ≈ 0.55 (Linder 2005)
    For QCT: Same approximation but with modified Ω_m(z)

    More accurate form (Peebles 1980):
    f(z) ≈ Ω_m(z)^(5/9) for flat ΛCDM

    Even more accurate (Linder 2005):
    γ(z) = 0.55 + 0.05[1 + w(z)]  where w is dark energy EOS
    For ΛCDM, w = -1, so γ = 0.55
    """
    gamma = 0.55  # Growth index for ΛCDM
    Om_z = Omega_m(z, cosmology)
    return Om_z**gamma

def growth_factor_D(z, cosmology='LCDM'):
    """
    Linear growth factor D(z) normalized to D(0) = 1.

    We use the approximate solution (Carroll et al. 1992):
    D(z) ∝ E(z) ∫_z^∞ (1+z')/(E(z'))³ dz'

    For numerical stability, we integrate from z to z_max = 100.
    """
    E = E_QCT if cosmology == 'QCT' else E_LCDM

    # Integration limits
    z_max = 100.0  # Assume D → 0 at high z
    N = 1000  # Integration steps

    # Logarithmic spacing for better high-z resolution
    z_vals = [z + (z_max - z) * (i / N)**2 for i in range(N + 1)]

    # Trapezoid rule
    integral = 0.0
    for i in range(N):
        z1, z2 = z_vals[i], z_vals[i + 1]
        f1 = (1 + z1) / E(z1)**3
        f2 = (1 + z2) / E(z2)**3
        integral += 0.5 * (f1 + f2) * (z2 - z1)

    D_z = E(z) * integral

    # Normalize to D(0) = 1
    # Compute D(0) with same method
    z_vals_0 = [0.0 + (z_max - 0.0) * (i / N)**2 for i in range(N + 1)]
    integral_0 = 0.0
    for i in range(N):
        z1, z2 = z_vals_0[i], z_vals_0[i + 1]
        f1 = (1 + z1) / E(z1)**3
        f2 = (1 + z2) / E(z2)**3
        integral_0 += 0.5 * (f1 + f2) * (z2 - z1)
    D_0 = E(0.0) * integral_0

    return D_z / D_0

def fsigma8(z, cosmology='LCDM', sigma8_0=0.811):
    """
    Observable quantity f(z)σ₈(z) where σ₈ is RMS matter fluctuation in 8 Mpc/h spheres.

    σ₈(z) = σ₈(0) × D(z) / D(0) = σ₈(0) × D(z)  [since D(0) ≡ 1]

    Therefore: fσ₈(z) = f(z) × σ₈(0) × D(z)

    Planck 2018: σ₈(0) = 0.811 ± 0.006
    """
    f = growth_rate_f(z, cosmology)
    D = growth_factor_D(z, cosmology)
    return f * sigma8_0 * D

# ==============================================================================
# BAO WIGGLE AMPLITUDE MODULATION
# ==============================================================================

def bao_wiggle_amplitude_factor(z, cosmology='LCDM'):
    """
    The amplitude of BAO wiggles in P(k) is modulated by growth effects.

    In linear theory:
    P(k, z) = D²(z) × P(k, z=0)

    The BAO feature appears as oscillations around a smooth component:
    P(k) = P_smooth(k) × [1 + A_BAO(k) × sin(k r_s + φ)]

    The amplitude A_BAO depends on the growth of perturbations.
    A stronger/weaker growth changes the contrast of the wiggles.

    This function returns: D²_QCT(z) / D²_ΛCDM(z)
    """
    D_LCDM = growth_factor_D(z, 'LCDM')
    D_QCT = growth_factor_D(z, 'QCT')
    return (D_QCT / D_LCDM)**2

# ==============================================================================
# PHASE SHIFT ESTIMATION
# ==============================================================================

def estimate_beta_phi_from_growth(z):
    """
    Estimate contribution to β_ϕ from growth rate modifications.

    This is highly approximate! The phase shift β_ϕ depends on:
    1. Sound horizon (already calculated in Phase 1.1)
    2. Growth rate (affects wiggle amplitude and shape)
    3. Non-linear evolution (damping, mode coupling)

    Baumann et al. (2017) show that β_ϕ is sensitive to both
    background evolution (via r_s) and perturbation growth (via f σ₈).

    A rough estimate:
    Δβ_ϕ ~ Δ(fσ₈) / (fσ₈)

    But this is ORDER OF MAGNITUDE only!
    """
    fsig8_LCDM = fsigma8(z, 'LCDM')
    fsig8_QCT = fsigma8(z, 'QCT')

    ratio = fsig8_QCT / fsig8_LCDM
    delta_beta_phi = ratio - 1.0

    return delta_beta_phi

# ==============================================================================
# MAIN CALCULATION
# ==============================================================================

def main():
    print("=" * 80)
    print("BAO PHASE SHIFT CALCULATOR - PHASE 1.2")
    print("Growth Rate Modifications: G_eff = 0.9 G_N")
    print("=" * 80)
    print()

    # -------------------------------------------------------------------------
    # STEP 1: Growth Rate Comparison
    # -------------------------------------------------------------------------
    print("STEP 1: GROWTH RATE f(z) COMPARISON")
    print("-" * 80)

    results = []

    for name, z in DESI_redshifts.items():
        # ΛCDM values
        f_LCDM = growth_rate_f(z, 'LCDM')
        D_LCDM = growth_factor_D(z, 'LCDM')
        fsig8_LCDM = fsigma8(z, 'LCDM')

        # QCT values
        f_QCT = growth_rate_f(z, 'QCT')
        D_QCT = growth_factor_D(z, 'QCT')
        fsig8_QCT = fsigma8(z, 'QCT')

        # Ratios
        f_ratio = f_QCT / f_LCDM
        D_ratio = D_QCT / D_LCDM
        fsig8_ratio = fsig8_QCT / fsig8_LCDM

        results.append({
            'tracer': name,
            'z': z,
            'f_LCDM': f_LCDM,
            'f_QCT': f_QCT,
            'f_ratio': f_ratio,
            'D_LCDM': D_LCDM,
            'D_QCT': D_QCT,
            'D_ratio': D_ratio,
            'fsig8_LCDM': fsig8_LCDM,
            'fsig8_QCT': fsig8_QCT,
            'fsig8_ratio': fsig8_ratio
        })

        print(f"{name:12s} z = {z:.3f}")
        print(f"  f(z):     ΛCDM = {f_LCDM:.4f}, QCT = {f_QCT:.4f}, ratio = {f_ratio:.6f}")
        print(f"  D(z):     ΛCDM = {D_LCDM:.4f}, QCT = {D_QCT:.4f}, ratio = {D_ratio:.6f}")
        print(f"  fσ₈(z):   ΛCDM = {fsig8_LCDM:.4f}, QCT = {fsig8_QCT:.4f}, ratio = {fsig8_ratio:.6f}")
        print()

    # -------------------------------------------------------------------------
    # STEP 2: BAO Wiggle Amplitude Modulation
    # -------------------------------------------------------------------------
    print("=" * 80)
    print("STEP 2: BAO WIGGLE AMPLITUDE MODULATION")
    print("-" * 80)
    print()
    print("The BAO wiggles in P(k) are modulated by growth factor D²(z).")
    print("QCT has weaker gravity → slower growth → reduced wiggle amplitude.")
    print()

    for res in results:
        z = res['z']
        amp_factor = bao_wiggle_amplitude_factor(z)
        print(f"{res['tracer']:12s} z = {z:.3f}:  D²_QCT / D²_ΛCDM = {amp_factor:.6f}  ({(amp_factor - 1) * 100:+.3f}%)")

    # -------------------------------------------------------------------------
    # STEP 3: Phase Shift Estimate from Growth
    # -------------------------------------------------------------------------
    print()
    print("=" * 80)
    print("STEP 3: ESTIMATED β_ϕ CONTRIBUTION FROM GROWTH")
    print("-" * 80)
    print()
    print("⚠️  WARNING: This is a ROUGH estimate!")
    print("The actual β_ϕ requires full P(k) calculation and phase fitting.")
    print()

    beta_phi_estimates = []
    for res in results:
        z = res['z']
        delta_beta = estimate_beta_phi_from_growth(z)
        beta_phi_estimates.append(delta_beta)
        print(f"{res['tracer']:12s} z = {z:.3f}:  Δβ_ϕ ~ {delta_beta:+.4f}  (β_ϕ ~ {1 + delta_beta:.4f})")

    avg_delta_beta = sum(beta_phi_estimates) / len(beta_phi_estimates)
    print()
    print(f"Average Δβ_ϕ from growth: {avg_delta_beta:+.4f}")
    print(f"Average β_ϕ estimate: {1 + avg_delta_beta:.4f}")

    # -------------------------------------------------------------------------
    # STEP 4: Combined Effect (Sound Horizon + Growth)
    # -------------------------------------------------------------------------
    print()
    print("=" * 80)
    print("STEP 4: COMBINED EFFECT (SOUND HORIZON + GROWTH)")
    print("-" * 80)
    print()
    print("From Phase 1.1: Sound horizon contributes β_ϕ ~ 1.01 (Δβ_ϕ ~ +0.01)")
    print(f"From Phase 1.2: Growth rate contributes β_ϕ ~ {1 + avg_delta_beta:.4f} (Δβ_ϕ ~ {avg_delta_beta:+.4f})")
    print()

    # Rough linear combination (THIS IS VERY APPROXIMATE!)
    delta_beta_rs = 0.01  # From Phase 1.1
    delta_beta_growth = avg_delta_beta
    delta_beta_combined = delta_beta_rs + delta_beta_growth
    beta_phi_combined = 1 + delta_beta_combined

    print(f"Combined estimate (linear sum): β_ϕ^QCT ~ {beta_phi_combined:.4f}")
    print()
    print("⚠️  CRITICAL NOTE:")
    print(f"   DESI measures: β_ϕ = 2.7 ± 1.7")
    print(f"   QCT prediction from G_eff alone: β_ϕ ~ {beta_phi_combined:.2f}")
    print()
    if beta_phi_combined < 2.0:
        print("   → G_eff = 0.9 G_N CANNOT explain the DESI anomaly!")
        print("   → Need additional mechanisms:")
        print("      1. Non-adiabatic perturbations from neutrino condensate")
        print("      2. E_pair(z) evolution at late times")
        print("      3. Or DESI measurement is statistical fluctuation")
    else:
        print("   → G_eff modification could potentially explain DESI!")

    # -------------------------------------------------------------------------
    # STEP 5: Save Results
    # -------------------------------------------------------------------------
    print()
    print("=" * 80)
    print("STEP 5: SAVING RESULTS")
    print("-" * 80)

    output_file = 'bao_geff_step2_results.csv'
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print(f"Results saved to: {output_file}")

    # -------------------------------------------------------------------------
    # Summary
    # -------------------------------------------------------------------------
    print()
    print("=" * 80)
    print("SUMMARY - PHASE 1.2 RESULTS")
    print("=" * 80)
    print()
    print(f"1. Growth rate ratio: f_QCT / f_ΛCDM ~ {results[3]['f_ratio']:.6f} (at z ~ 0.93)")
    print(f"2. Growth factor ratio: D_QCT / D_ΛCDM ~ {results[3]['D_ratio']:.6f}")
    print(f"3. Observable ratio: (fσ₈)_QCT / (fσ₈)_ΛCDM ~ {results[3]['fsig8_ratio']:.6f}")
    print(f"4. BAO amplitude suppression: D²_QCT / D²_ΛCDM ~ {bao_wiggle_amplitude_factor(0.93):.6f}")
    print()
    print(f"5. Combined β_ϕ estimate: {beta_phi_combined:.4f}")
    print(f"   DESI measurement: 2.7 ± 1.7")
    print(f"   Tension: {(2.7 - beta_phi_combined) / 1.7:.1f}σ")
    print()
    print("NEXT STEPS:")
    print("→ Phase 1.3: Non-adiabatic perturbations (theoretical)")
    print("→ Phase 1.4: Full P(k) calculation with wiggles")
    print("→ Phase 1.5: Proper β_ϕ extraction from phase fitting")
    print()

if __name__ == '__main__':
    main()
