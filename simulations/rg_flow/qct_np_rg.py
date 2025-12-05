#!/usr/bin/env python3
import math
import csv
import argparse
from dataclasses import dataclass
from typing import List, Tuple

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
except Exception:
    plt = None

# --- Physical constants / reference scales ---
ALPHA_PHYS_1GEV = 1.0/137.035999084  # PDG-ish
M_PL = 1.2209e19  # GeV
M_EW = 91.1876    # GeV (M_Z as proxy for EW window)

# NOTE: Λ_QCT is treated here as a phenomenological EFT cutoff.
# Do NOT derive Λ_QCT numerically from √(E_pair · m_ν) in this script; that
# relation is not used to avoid unit inconsistencies and conceptual confusion.

# --- NP window shapes ---
def logistic_window(lnmu: float, lnmu0: float, width: float) -> float:
    """Smooth window centered at lnmu0 with total area ~ width.
    We normalize separately to get desired integral S_i.
    """
    # s(x) = 1/(1+exp((x-x0)/a))*(1-1/(1+exp((x-x0)/a)))' derivative-like is messy;
    # instead use a normalized bump: sech^2((x-x0)/a), area = 2a
    a = width/2.0
    z = (lnmu - lnmu0)/a
    sech = 1.0/math.cosh(z)
    return (sech*sech)  # area over x is ~ 2a

@dataclass
class NPBump:
    S: float           # target integral over d ln mu
    mu0: float         # center scale in GeV
    width_ln: float    # width in ln mu

    def value(self, mu: float) -> float:
        lnmu = math.log(mu)
        lnmu0 = math.log(self.mu0)
        # raw bump with area ~ 2a = width_ln
        bump = logistic_window(lnmu, lnmu0, self.width_ln)
        # normalize to integrate to S over d(ln mu)
        # integral of sech^2((x-x0)/a) dx = a * tanh((x-x0)/a) from -inf..inf = 2a
        # here a = width_ln/2, so area = width_ln
        norm = self.S / self.width_ln
        return norm * bump


def alpha_running(mu: float, alpha_pl: float, bumps: List[NPBump], include_pert: bool=True, mu_pl: float=M_PL) -> float:
    """Compute alpha(mu) from alpha_Pl via cumulative exponent of eta_A.
    d ln Z_A / dt = eta_A => ln Z_A = ∫ eta_A dt; alpha = alpha_Pl / Z_A
    We integrate approximately by summing NP contributions at mu (local approx)
    and adding a perturbative 1-loop QED correction from M_Pl to mu.
    """
    # NP cumulative integral approximated by summing S_i up to mu using smooth windows.
    # For a quick tool, we approximate ln alpha(mu)/alpha_Pl ≈ sum_i ∫^ln mu s_i = sum_i S_i * W_i(mu),
    # where W_i(mu) is the cumulative of the normalized bump. Use tanh cumulative.

    lnmu = math.log(mu)
    lnmu_pl = math.log(mu_pl)

    # Cumulative for each bump: integral of norm*sech^2((x-x0)/a) dx = norm * a * [tanh((lnmu-lnmu0)/a)+1]
    # from -inf to lnmu; cumulative from -inf yields norm*a*(tanh((lnmu-lnmu0)/a)+1)
    # Since total area = norm*2a = S, the cumulative up to lnmu is S * (tanh(z)+1)/2

    total_S_up_to_mu = 0.0
    for b in bumps:
        a = b.width_ln/2.0
        z = (lnmu - math.log(b.mu0))/a
        frac = 0.5*(math.tanh(z)+1.0)  # cumulative from -inf up to lnmu
        # running from UV (high mu) down: include (1 - frac)
        total_S_up_to_mu += b.S * (1.0 - frac)

    ln_ratio_np = total_S_up_to_mu  # ≈ ln[alpha(mu)/alpha_Pl] from NP (UV→IR)

    # Perturbative 1-loop QED running (tiny here):
    ln_ratio_pert = 0.0
    if include_pert:
        # alpha(μ) ≈ α_Pl / (1 - (2/3π) N_eff α_Pl ln(μ/ M_Pl))
        # rewrite as ln[α(μ)/α_Pl] ≈ ln[1 + (2/3π) N_eff α_Pl ln(M_Pl/μ) + ...] ≈ small
        # Use N_eff ~ O(10) (leptons+quarks below EW not fully relevant across the huge span). Keep it parametric.
        N_eff = 10.0
        coeff = (2.0/(3.0*math.pi))*N_eff
        x = coeff*alpha_pl*abs(math.log(mu_pl/mu))
        ln_ratio_pert = math.log(1.0 + x)

    ln_ratio_total = ln_ratio_np + ln_ratio_pert
    return alpha_pl * math.exp(ln_ratio_total)


def calibrate_alpha_pl(alpha_target: float, mu_target: float, bumps: List[NPBump], include_pert: bool=True) -> float:
    """Solve for alpha_Pl such that alpha_running(mu_target) = alpha_target.
    Uses a robust bisection in alpha_Pl (monotonic mapping)."""
    def f(alpha_pl: float) -> float:
        return alpha_running(mu_target, alpha_pl, bumps, include_pert=include_pert) - alpha_target

    # Bracket in a wide domain
    lo, hi = 1e-40, 1.0
    flo, fhi = f(lo), f(hi)
    # Ensure opposite signs; expand if needed
    expand = 0
    while flo * fhi > 0 and expand < 20:
        lo *= 1e-2
        hi *= 1e+1
        flo, fhi = f(lo), f(hi)
        expand += 1

    # Bisection
    for _ in range(200):
        mid = math.sqrt(lo*hi)
        fm = f(mid)
        if abs(fm) <= 0.0 + 1e-18:
            return mid
        if flo * fm <= 0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
    return math.sqrt(lo*hi)


def required_N_eff_perturbative_only(alpha_pl: float, alpha_target: float, mu_target: float, mu_pl: float=M_PL) -> float:
    # From 1-loop QED: 1/alpha(μ) = 1/alpha_Pl - (2/3π) N_eff ln(μ/M_Pl)
    # ⇒ N_eff = [1/α_Pl - 1/α(μ)] / [(2/3π) ln(M_Pl/μ)]
    num = (1.0/alpha_pl) - (1.0/alpha_target)
    den = (2.0/(3.0*math.pi))*math.log(mu_pl/mu_target)
    return num/den


def g_minus_2_scale(delta_a_mu: float=2.5e-9, C_mu: float=1.0) -> float:
    # Rough estimate: Δa_μ ~ (m_μ^2)/(Λ^2) * C_μ / (8π^2)  ⇒ Λ ~ m_μ / sqrt(8π^2 Δa_μ / C_μ)
    m_mu = 0.1056583745  # GeV
    return m_mu / math.sqrt(8.0*math.pi**2 * delta_a_mu / C_mu)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out-prefix", default="/workspace/outputs/qct_np_rg")
    p.add_argument("--alpha-target", type=float, default=ALPHA_PHYS_1GEV)
    p.add_argument("--mu-target", type=float, default=1.0)  # GeV
    p.add_argument("--include-pert", action="store_true")
    p.add_argument("--no-plot", action="store_true")
    args = p.parse_args()

    # Define bumps near EW window
    bumps = [
        # Place NP transition above the direct precision window (≫ M_Z),
        # so that both 1 GeV and M_Z lie effectively below the step.
        NPBump(S=15.0, mu0=1.0e3, width_ln=0.7),   # instanton/DAR (around ~1 TeV)
        NPBump(S=15.0, mu0=1.0e3, width_ln=0.7),   # Berry
        NPBump(S=15.0, mu0=1.0e3, width_ln=0.7),   # Higgs coupling
        NPBump(S=13.0, mu0=1.0e3, width_ln=0.7),   # holographic
    ]

    alpha_pl = calibrate_alpha_pl(args.alpha_target, args.mu_target, bumps, include_pert=args.include_pert)

    # Sweep mu
    mus = []
    alphas = []
    for exp in [x/20.0 for x in range(-40*20, 41*20)]:  # ln mu from ~ -40..40
        lnmu = exp
        mu = math.exp(lnmu)
        if mu < 1e-6:
            continue
        a = alpha_running(mu, alpha_pl, bumps, include_pert=args.include_pert)
        mus.append(mu)
        alphas.append(a)

    # Key points
    alpha_MZ = alpha_running(M_EW, alpha_pl, bumps, include_pert=args.include_pert)
    delta_alpha_rel = (alpha_MZ - args.alpha_target)/args.alpha_target

    # Required N_eff if only perturbative from alpha_Pl to alpha_target at mu_target
    Neff_req = required_N_eff_perturbative_only(alpha_pl, args.alpha_target, args.mu_target)

    # g-2 scale
    Lambda_eff = g_minus_2_scale()

    # Save CSV
    csv_path = f"{args.out_prefix}.csv"
    with open(csv_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["mu_GeV","alpha"])
        for mu, a in zip(mus, alphas):
            w.writerow([mu, a])

    # Plot
    if (plt is not None) and (not args.no_plot):
        plt.figure(figsize=(7,4))
        plt.loglog(mus, alphas)
        plt.axvline(M_EW, color='k', ls='--', lw=0.8, label='M_Z')
        plt.axhline(args.alpha_target, color='r', ls=':', lw=0.8, label='alpha_target@1GeV')
        plt.xlabel(r"$\mu$ [GeV]")
        plt.ylabel(r"$\alpha(\mu)$")
        plt.legend()
        plt.tight_layout()
        png_path = f"{args.out_prefix}.png"
        plt.savefig(png_path, dpi=160)
    else:
        png_path = None

    # Report
    txt_path = f"{args.out_prefix}_report.txt"
    with open(txt_path, "w") as f:
        f.write("QCT NP-RG quick report\n")
        f.write(f"alpha_target(mu={args.mu_target} GeV) = {args.alpha_target:.12e}\n")
        f.write(f"alpha_Pl (calibrated) = {alpha_pl:.12e}\n")
        f.write(f"alpha(M_Z) = {alpha_MZ:.12e}\n")
        f.write(f"delta_alpha_rel@M_Z = {delta_alpha_rel:.6e}\n")
        f.write(f"N_eff_required (pert-only) = {Neff_req:.6e}\n")
        f.write(f"Lambda_eff for g-2 (C_mu=1) [GeV] = {Lambda_eff:.3f}\n")
        f.write(f"CSV: {csv_path}\n")
        f.write(f"PNG: {png_path}\n")

    print("alpha_Pl(calibrated)=", alpha_pl)
    print("alpha(M_Z)=", alpha_MZ, " delta_alpha_rel=", delta_alpha_rel)
    print("N_eff_required(pert-only)=", Neff_req)
    print("Lambda_eff[g-2,C_mu=1]=", Lambda_eff, "GeV")
    print("CSV:", csv_path)
    print("PNG:", png_path)
    print("Report:", txt_path)

if __name__ == "__main__":
    main()
