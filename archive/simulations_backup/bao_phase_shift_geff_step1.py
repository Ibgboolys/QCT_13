#!/usr/bin/env python3
"""
BAO Phase Shift Calculator with Modified Gravity (G_eff = 0.9 G_N)
===================================================================

PHASE 1.1: Sound Horizon and Basic Cosmological Evolution

Vypočítá:
1. Sound horizon r_s v QCT kosmologii (G_eff = 0.9 G_N)
2. Hubble parameter evolution H(z) s modifikovanou gravitací
3. Angular diameter distance D_A(z)
4. Základní BAO parametry pro porovnání s ΛCDM

Autor: AI-assisted QCT analysis
Datum: 2025-11-19
Reference: DESI_BAO_PHASE_SHIFT_FINAL_ANALYSIS.md
"""

import math
import csv

# =============================================================================
# FYZIKÁLNÍ KONSTANTY
# =============================================================================

c = 2.99792458e8  # m/s
hbar = 1.054571817e-34  # J·s
k_B = 1.380649e-23  # J/K
G_N = 6.67430e-11  # m³/(kg·s²)

# Konverze
eV_to_J = 1.602176634e-19
Mpc_to_m = 3.08567758149137e22  # m
year_to_s = 365.25 * 24 * 3600

# =============================================================================
# KOSMOLOGICKÉ PARAMETRY (Planck 2018 - ΛCDM baseline)
# =============================================================================

H_0_kmsMpc = 67.4  # km/s/Mpc
H_0 = H_0_kmsMpc  # Keep in km/s/Mpc for calculations

Omega_m_0 = 0.315  # total matter (CDM + baryons)
Omega_b_0 = 0.0493  # baryons only
Omega_c_0 = Omega_m_0 - Omega_b_0  # CDM
Omega_Lambda_0 = 1.0 - Omega_m_0  # flat universe
Omega_r_0 = 9.15e-5  # radiation (photons + neutrinos)
Omega_gamma_0 = 5.38e-5  # photons only
Omega_nu_0 = Omega_r_0 - Omega_gamma_0  # neutrinos

T_CMB_0 = 2.7255  # K
T_nu_0 = T_CMB_0 * (4/11)**(1/3)  # K (standard neutrino temperature)

# Drag epoch (when baryons decouple from photons)
z_drag = 1059.0  # From Planck 2018 (approximate)

# =============================================================================
# QCT PARAMETERS
# =============================================================================

# Modified gravity parameter
G_eff_ratio = 0.9  # G_eff / G_N = 0.9 (QCT prediction)

# QCT energy scales
E_pair_0 = 5.38e18  # eV (today, from G_eff calibration)
m_nu_eV = 0.1  # eV
m_p_eV = 938.272e6  # eV

# =============================================================================
# FUNCTIONS: ΛCDM (Standard) Cosmology
# =============================================================================

def E_LCDM(z):
    """
    Dimensionless Hubble parameter E(z) = H(z)/H_0 for ΛCDM.
    """
    return math.sqrt(
        Omega_r_0 * (1 + z)**4 +
        Omega_m_0 * (1 + z)**3 +
        Omega_Lambda_0
    )

def H_LCDM(z):
    """
    Hubble parameter H(z) in km/s/Mpc for ΛCDM.
    """
    return H_0 * E_LCDM(z)

def sound_speed_squared(z):
    """
    Sound speed squared in photon-baryon fluid: c_s² = c²/3(1 + R)
    where R = 3ρ_b / 4ρ_γ
    """
    R = (3 * Omega_b_0 * (1 + z)) / (4 * Omega_gamma_0 * (1 + z))
    # Simplified: R ~ constant in radiation era
    c_s_sq = (1.0 / 3.0) / (1.0 + R)
    return c_s_sq

def integrand_r_s_LCDM(z):
    """
    Integrand for sound horizon: c_s(z) / H(z)
    Returns value in Mpc (accounting for c and H units)
    """
    c_s_sq = sound_speed_squared(z)
    c_s = math.sqrt(c_s_sq) * c  # m/s
    H_z = H_LCDM(z)  # km/s/Mpc

    # Convert to Mpc: c_s [m/s] / H [km/s/Mpc] = c_s [km/s] / H [km/s/Mpc]
    c_s_kms = c_s / 1000.0
    return c_s_kms / H_z  # Mpc

def integrate_sound_horizon_LCDM(z_start=1090.0, z_end=0.0, N=10000):
    """
    Trapezoid integration of sound horizon from z_start to z_end.

    r_s = ∫_{z_end}^{z_start} c_s(z) / H(z) dz

    For BAO, we integrate from recombination (z~1090) to drag epoch (z~1059).
    Actually, proper definition: from z_drag to infinity (or very high z).

    Standard approach: integrate from z_drag to z=∞ (or z>>z_drag).
    """
    # Logarithmic spacing for better resolution at high z
    z_min = z_end if z_end > 0 else 1e-3
    z_max = z_start

    # Linear spacing in log(1+z)
    log_1pz_min = math.log(1 + z_min)
    log_1pz_max = math.log(1 + z_max)

    dlog = (log_1pz_max - log_1pz_min) / N

    integral = 0.0
    for i in range(N):
        log_1pz_a = log_1pz_min + i * dlog
        log_1pz_b = log_1pz_min + (i + 1) * dlog

        z_a = math.exp(log_1pz_a) - 1
        z_b = math.exp(log_1pz_b) - 1

        # Trapezoid rule with dz = d(log(1+z)) * (1+z)
        dz_a = (math.exp(log_1pz_a)) * dlog
        dz_b = (math.exp(log_1pz_b)) * dlog

        f_a = integrand_r_s_LCDM(z_a)
        f_b = integrand_r_s_LCDM(z_b)

        # Average of dz for trapezoid
        dz_avg = (dz_a + dz_b) / 2.0
        integral += 0.5 * (f_a + f_b) * dz_avg

    return integral

# =============================================================================
# FUNCTIONS: QCT Modified Cosmology
# =============================================================================

def E_QCT(z):
    """
    Dimensionless Hubble parameter E(z) for QCT with G_eff = 0.9 G_N.

    H² = (8πG/3) ρ_total

    With G_eff = 0.9 G_N:
    H²_QCT = 0.9 × H²_LCDM
    E_QCT = √0.9 × E_LCDM ≈ 0.9487 × E_LCDM
    """
    return math.sqrt(G_eff_ratio) * E_LCDM(z)

def H_QCT(z):
    """
    Hubble parameter H(z) in km/s/Mpc for QCT.
    """
    return H_0 * E_QCT(z)

def integrand_r_s_QCT(z):
    """
    Integrand for sound horizon in QCT: c_s(z) / H_QCT(z)
    """
    c_s_sq = sound_speed_squared(z)
    c_s = math.sqrt(c_s_sq) * c  # m/s
    H_z = H_QCT(z)  # km/s/Mpc

    c_s_kms = c_s / 1000.0
    return c_s_kms / H_z  # Mpc

def integrate_sound_horizon_QCT(z_start=1090.0, z_end=0.0, N=10000):
    """
    Sound horizon integration for QCT cosmology.
    """
    z_min = z_end if z_end > 0 else 1e-3
    z_max = z_start

    log_1pz_min = math.log(1 + z_min)
    log_1pz_max = math.log(1 + z_max)

    dlog = (log_1pz_max - log_1pz_min) / N

    integral = 0.0
    for i in range(N):
        log_1pz_a = log_1pz_min + i * dlog
        log_1pz_b = log_1pz_min + (i + 1) * dlog

        z_a = math.exp(log_1pz_a) - 1
        z_b = math.exp(log_1pz_b) - 1

        dz_a = (math.exp(log_1pz_a)) * dlog
        dz_b = (math.exp(log_1pz_b)) * dlog

        f_a = integrand_r_s_QCT(z_a)
        f_b = integrand_r_s_QCT(z_b)

        dz_avg = (dz_a + dz_b) / 2.0
        integral += 0.5 * (f_a + f_b) * dz_avg

    return integral

# =============================================================================
# ANGULAR DIAMETER DISTANCE
# =============================================================================

def comoving_distance_integrand_LCDM(z):
    """
    Integrand for comoving distance: c / H(z)
    """
    H_z = H_LCDM(z)  # km/s/Mpc
    c_kms = c / 1000.0  # km/s
    return c_kms / H_z  # Mpc

def comoving_distance_integrand_QCT(z):
    """
    Integrand for comoving distance in QCT.
    """
    H_z = H_QCT(z)  # km/s/Mpc
    c_kms = c / 1000.0  # km/s
    return c_kms / H_z  # Mpc

def integrate_comoving_distance(z, cosmology='LCDM', N=1000):
    """
    Comoving distance d_c(z) = ∫_0^z c/H(z') dz'
    """
    if cosmology == 'LCDM':
        integrand = comoving_distance_integrand_LCDM
    else:
        integrand = comoving_distance_integrand_QCT

    if z <= 0:
        return 0.0

    dz = z / N
    integral = 0.0

    for i in range(N):
        z_a = i * dz
        z_b = (i + 1) * dz

        f_a = integrand(z_a)
        f_b = integrand(z_b)

        integral += 0.5 * (f_a + f_b) * dz

    return integral

def D_A(z, cosmology='LCDM'):
    """
    Angular diameter distance D_A(z) = d_c(z) / (1+z)
    """
    d_c = integrate_comoving_distance(z, cosmology)
    return d_c / (1 + z)

# =============================================================================
# BAO PARAMETERS
# =============================================================================

def compute_alpha_parameters(z, r_s_template, cosmology='LCDM'):
    """
    Compute BAO distortion parameters α and α_AP.

    α = [D_V(z) / D_V^f(z)] × [r_s^template / r_s^true]
    α_AP = α_∥ / α_⊥

    where:
    α_∥ = [H^f(z) × r_s^template] / [H(z) × r_s^true]
    α_⊥ = [D_A(z) × r_s^template] / [D_A^f(z) × r_s^true]

    For simplicity, assume fiducial = LCDM template.
    """
    # True values (data cosmology)
    if cosmology == 'LCDM':
        H_true = H_LCDM(z)
        D_A_true = D_A(z, 'LCDM')
    else:
        H_true = H_QCT(z)
        D_A_true = D_A(z, 'QCT')

    # Fiducial values (template = LCDM)
    H_fid = H_LCDM(z)
    D_A_fid = D_A(z, 'LCDM')

    # r_s values
    # r_s_template is input (LCDM value)
    # r_s_true depends on cosmology

    if cosmology == 'LCDM':
        r_s_true = r_s_template  # Same cosmology
    else:
        # Need to compute r_s for QCT
        r_s_true = integrate_sound_horizon_QCT(z_start=1090.0, z_end=0.0)

    # Distortion parameters
    alpha_parallel = (H_fid * r_s_template) / (H_true * r_s_true)
    alpha_perp = (D_A_true * r_s_template) / (D_A_fid * r_s_true)

    # Isotropic and AP
    alpha_iso = alpha_parallel**(1/3) * alpha_perp**(2/3)
    alpha_AP = alpha_parallel / alpha_perp

    # Volume-averaged distance
    D_V_true = ((1 + z)**2 * D_A_true**2 * c / (1000 * H_true))**(1/3)
    D_V_fid = ((1 + z)**2 * D_A_fid**2 * c / (1000 * H_fid))**(1/3)

    return {
        'alpha_iso': alpha_iso,
        'alpha_parallel': alpha_parallel,
        'alpha_perp': alpha_perp,
        'alpha_AP': alpha_AP,
        'D_V_ratio': D_V_true / D_V_fid,
        'r_s_ratio': r_s_true / r_s_template,
        'H_ratio': H_true / H_fid,
        'D_A_ratio': D_A_true / D_A_fid
    }

# =============================================================================
# MAIN CALCULATION
# =============================================================================

def main():
    print("=" * 80)
    print("BAO PHASE SHIFT CALCULATOR - PHASE 1.1")
    print("Modified Gravity: G_eff = 0.9 G_N")
    print("=" * 80)
    print()

    # Step 1: Calculate sound horizon
    print("STEP 1: SOUND HORIZON CALCULATION")
    print("-" * 80)

    # ΛCDM
    print("Computing r_s for ΛCDM...")
    r_s_LCDM = integrate_sound_horizon_LCDM(z_start=3000.0, z_end=0.0, N=10000)
    print(f"  r_s^ΛCDM = {r_s_LCDM:.4f} Mpc")
    print(f"  r_s^ΛCDM × h = {r_s_LCDM * H_0/100:.4f} Mpc/h")

    # Expected from Planck: r_s ≈ 147.09 Mpc (Planck 2018, Table 2)
    r_s_Planck = 147.09  # Mpc
    print(f"  Planck 2018: r_s = {r_s_Planck:.2f} Mpc")
    print(f"  Difference: {abs(r_s_LCDM - r_s_Planck)/r_s_Planck * 100:.2f}%")
    print()

    # QCT
    print("Computing r_s for QCT (G_eff = 0.9 G_N)...")
    r_s_QCT = integrate_sound_horizon_QCT(z_start=3000.0, z_end=0.0, N=10000)
    print(f"  r_s^QCT = {r_s_QCT:.4f} Mpc")
    print(f"  r_s^QCT × h = {r_s_QCT * H_0/100:.4f} Mpc/h")
    print()

    # Comparison
    r_s_ratio = r_s_QCT / r_s_LCDM
    print("COMPARISON:")
    print(f"  r_s^QCT / r_s^ΛCDM = {r_s_ratio:.6f}")
    print(f"  Change: {(r_s_ratio - 1.0) * 100:.3f}%")
    print()

    # Expected: H_QCT ~ √0.9 × H_LCDM → r_s_QCT ~ r_s_LCDM / √0.9 ≈ 1.054 × r_s_LCDM
    expected_ratio = 1.0 / math.sqrt(G_eff_ratio)
    print(f"  Expected ratio (1/√0.9) = {expected_ratio:.6f}")
    print(f"  Expected change: {(expected_ratio - 1.0) * 100:.3f}%")
    print()

    # Step 2: Calculate BAO parameters at DESI redshifts
    print("=" * 80)
    print("STEP 2: BAO PARAMETERS AT DESI REDSHIFTS")
    print("-" * 80)
    print()

    # DESI redshift bins (from Table 1 in Whitford et al.)
    desi_tracers = [
        ("BGS", 0.25),      # z = 0.1-0.4, effective z ~ 0.25
        ("LRG1", 0.51),     # z = 0.4-0.6
        ("LRG2", 0.706),    # z = 0.6-0.8
        ("LRG3+ELG1", 0.93), # z = 0.8-1.1
        ("ELG2", 1.317),    # z = 1.1-1.6
        ("QSO", 1.49),      # z = 0.8-2.1, effective z ~ 1.49
    ]

    # Use LCDM r_s as template
    r_s_template = r_s_LCDM

    results = []

    print(f"{'Tracer':<15} {'z':>6} {'α_iso':>10} {'α_∥':>10} {'α_⊥':>10} {'α_AP':>10}")
    print("-" * 80)

    for tracer, z in desi_tracers:
        params_QCT = compute_alpha_parameters(z, r_s_template, 'QCT')

        print(f"{tracer:<15} {z:>6.3f} "
              f"{params_QCT['alpha_iso']:>10.6f} "
              f"{params_QCT['alpha_parallel']:>10.6f} "
              f"{params_QCT['alpha_perp']:>10.6f} "
              f"{params_QCT['alpha_AP']:>10.6f}")

        results.append({
            'tracer': tracer,
            'z': z,
            **params_QCT
        })

    print()

    # Step 3: Estimate β_ϕ contribution
    print("=" * 80)
    print("STEP 3: ESTIMATING β_ϕ FROM α SHIFTS")
    print("-" * 80)
    print()

    print("The measured α parameters differ from unity when fitting QCT data")
    print("with ΛCDM template. This creates an apparent 'shift' in BAO position.")
    print()
    print("Phase shift β_ϕ is related but not identical to α shifts.")
    print("Detailed calculation requires fitting actual P(k) - see next phase.")
    print()

    # Rough estimate: β_ϕ - 1 ~ (α - 1)
    # But this is oversimplified!

    avg_alpha = sum(r['alpha_iso'] for r in results) / len(results)
    print(f"Average α_iso across DESI redshifts: {avg_alpha:.6f}")
    print(f"Deviation from unity: {(avg_alpha - 1.0) * 100:.3f}%")
    print()

    print("ROUGH ESTIMATE (very approximate!):")
    print(f"If β_ϕ - 1 ~ α - 1: β_ϕ ≈ {avg_alpha:.3f}")
    print()
    print("⚠️  WARNING: This is a rough order-of-magnitude estimate!")
    print("   Actual β_ϕ calculation requires:")
    print("   1. Full P(k) with wiggles")
    print("   2. Proper phase shift extraction")
    print("   3. Fitting to Baumann et al. parametrization")
    print()

    # Step 4: Save results
    print("=" * 80)
    print("STEP 4: SAVING RESULTS")
    print("-" * 80)

    output_file = "bao_geff_step1_results.csv"
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'tracer', 'z', 'alpha_iso', 'alpha_parallel', 'alpha_perp',
            'alpha_AP', 'D_V_ratio', 'r_s_ratio', 'H_ratio', 'D_A_ratio'
        ])
        writer.writeheader()
        writer.writerows(results)

    print(f"Results saved to: {output_file}")
    print()

    # Summary
    print("=" * 80)
    print("SUMMARY - PHASE 1.1 RESULTS")
    print("=" * 80)
    print()
    print(f"1. Sound horizon change: r_s^QCT / r_s^ΛCDM = {r_s_ratio:.6f} (+{(r_s_ratio-1)*100:.2f}%)")
    print(f"2. This creates α ≠ 1 when fitting with ΛCDM template")
    print(f"3. Average α_iso ≈ {avg_alpha:.4f} across DESI redshifts")
    print(f"4. Rough estimate: β_ϕ ~ {avg_alpha:.2f}")
    print()
    print("NEXT STEPS:")
    print("→ Phase 1.2: Calculate growth rate f(z) modifications")
    print("→ Phase 1.3: Compute full P(k) with BAO wiggles")
    print("→ Phase 1.4: Extract actual β_ϕ from P(k) phase")
    print()

if __name__ == "__main__":
    main()
