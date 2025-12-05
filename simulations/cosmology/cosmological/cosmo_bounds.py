#!/usr/bin/env python3
"""
Quick cosmology constraint mapper for QCT parameters.
- Maps δρ_ent/ρ_crit and κ_gauge -> Δα/α (Oklo/QSO clocks style)
- Maps extra radiation-like fraction f_rad to ΔN_eff for BBN/CMB

This is an order-of-magnitude tool to help keep parameters consistent with
standard constraints without installing heavy external packages.
"""
import argparse
import math

# Constants
T_CMB_K = 2.7255  # K
rho_gamma_GeV4 = 2.006e-51  # photon energy density at T0 in GeV^4 (approx)
# ρ_rad = ρ_γ [1 + (7/8)(4/11)^(4/3) N_eff]
RAD_FACTOR = (7.0/8.0) * (4.0/11.0)**(4.0/3.0)

# Typical conservative bounds (update in paper as needed)
DELTA_NEFF_MAX_BBN = 0.3
DELTA_NEFF_MAX_CMB = 0.2
DELTA_ALPHA_OKLO_MAX = 1.0e-7
DELTA_ALPHA_QSO_MAX = 1.0e-5
DELTA_ALPHA_CMBREC_MAX = 3.0e-3  # at recombination ~ percent-level


def delta_alpha_from_kappa(delta_rho_over_rho: float, kappa_gauge: float) -> float:
    """Linearized model: Δα/α ≈ κ_gauge · (δρ_ent / ρ_crit)."""
    return kappa_gauge * delta_rho_over_rho


def delta_neff_from_extra_radiation(frac_extra: float) -> float:
    """Map an extra radiation-like fraction of photon energy density today
    to ΔN_eff via ρ_rad' = ρ_γ [1 + RAD_FACTOR (N_eff + ΔN_eff)]
    frac_extra is defined as ρ_extra / ρ_γ (today-equivalent).
    """
    return frac_extra / RAD_FACTOR


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--delta-rho-ratio", type=float, default=1e-7, help="δρ_ent/ρ_crit")
    ap.add_argument("--kappa-gauge", type=float, default=1.0, help="κ_gauge")
    ap.add_argument("--extra-radiation-frac", type=float, default=0.0, help="ρ_extra/ρ_gamma (today-equivalent)")
    args = ap.parse_args()

    d_alpha = delta_alpha_from_kappa(args.delta_rho_ratio, args.kappa_gauge)
    d_neff = delta_neff_from_extra_radiation(args.extra_radiation_frac)

    print("Inputs:")
    print("  δρ_ent/ρ_crit =", args.delta_rho_ratio)
    print("  κ_gauge       =", args.kappa_gauge)
    print("  ρ_extra/ρ_γ   =", args.extra_radiation_frac)
    print()
    print("Derived constraints:")
    print("  Δα/α          =", d_alpha)
    print("    vs Oklo max =", DELTA_ALPHA_OKLO_MAX, " -> OK?", abs(d_alpha) <= DELTA_ALPHA_OKLO_MAX)
    print("    vs QSO  max =", DELTA_ALPHA_QSO_MAX,  " -> OK?", abs(d_alpha) <= DELTA_ALPHA_QSO_MAX)
    print("    vs CMBrec   =", DELTA_ALPHA_CMBREC_MAX, " -> OK?", abs(d_alpha) <= DELTA_ALPHA_CMBREC_MAX)
    print()
    print("  ΔN_eff        =", d_neff)
    print("    vs BBN max  =", DELTA_NEFF_MAX_BBN, " -> OK?", abs(d_neff) <= DELTA_NEFF_MAX_BBN)
    print("    vs CMB max  =", DELTA_NEFF_MAX_CMB, " -> OK?", abs(d_neff) <= DELTA_NEFF_MAX_CMB)

if __name__ == "__main__":
    main()
