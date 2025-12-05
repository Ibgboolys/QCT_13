#!/usr/bin/env python3
"""
QCT Renormalization Group Flow Solver

Řeší spřažené RG rovnice pro QCT parametry od Planckovy škály k IR.
Zahrnuje perturbativní i non-perturbativní efekty.

Author: QCT Research Team
Date: 2025-10-10
Version: 1.0
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from typing import Dict, Callable
import json

# =============================================================================
# FYZIKÁLNÍ KONSTANTY
# =============================================================================

M_PL = 1.22e19  # GeV (Planck mass)
M_EW = 91.2     # GeV (Electroweak scale)
M_Z = 91.2      # GeV (Z boson mass)
m_e = 0.000511  # GeV (electron mass)

# =============================================================================
# BETA FUNCTIONS
# =============================================================================

def beta_lambda_perturbative(lam: float, alpha_eff: float) -> float:
    """
    1-loop beta function pro λ (quartic coupling).
    
    β_λ = (3λ²)/(16π²) - (α_eff·λ)/(8π²)
    """
    term1 = (3 * lam**2) / (16 * np.pi**2)
    term2 = (alpha_eff * lam) / (8 * np.pi**2)
    return term1 - term2

def beta_alpha_eff_perturbative(alpha_eff: float) -> float:
    """
    1-loop beta function pro α_eff.
    
    β_α = α²/(4π²)
    """
    return alpha_eff**2 / (4 * np.pi**2)

def beta_kappa_grav(kappa: float, alpha_eff: float, mu: float) -> float:
    """
    Beta function pro κ_grav (gravitační coupling).
    Gravitační tok je kvadraticky potlačen.
    
    β_κ ≈ c_g (κ²/M_Pl²) μ²
    """
    c_g = 1.0  # Numerical coefficient
    return c_g * (kappa**2 / M_PL**2) * mu**2

def S_instanton(alpha_EM: float, mu: float) -> float:
    """
    Instantonová akce jako funkce energie.
    
    S_inst(μ) = 2π/α_EM(μ)
    """
    return 2 * np.pi / alpha_EM

def S_effective_total(mu: float, M_EW: float, M_PL: float,
                     S1: float, S2: float, S3: float, S4: float) -> float:
    """
    Celková non-perturbativní efektivní akce.
    
    S_eff = S_inst + S_Berry + S_Higgs + S_holo
    
    Každý term má energy dependence.
    """
    # Normalized parameter: t = (ln μ - ln M_EW) / (ln M_PL - ln M_EW)
    # t=1 at Planck, t=0 at EW
    t = (np.log(mu) - np.log(M_EW)) / (np.log(M_PL) - np.log(M_EW))
    t = np.clip(t, 0, 1)  # Keep in [0,1]
    
    # Each mechanism has different energy profile
    S_inst_mu = S1 * (1 - np.exp(-5*(1-t)))  # Rapid at low energies
    S_Berry_mu = S2 * (1 - t)                # Linear
    S_Higgs_mu = S3 * (1 if mu < 1000 else 0)  # Step at EW
    S_holo_mu = S4 * (1 - t)**1.5            # Slower falloff
    
    return S_inst_mu + S_Berry_mu + S_Higgs_mu + S_holo_mu

# =============================================================================
# RG EQUATIONS
# =============================================================================

def rg_equations(y: np.ndarray, t: float, S_params: Dict) -> np.ndarray:
    """
    Spřažené RG rovnice.
    
    Parameters:
    -----------
    y : array
        [lambda, alpha_eff, kappa_grav, alpha_EM]
    t : float
        RG "time" = ln(μ/M_PL)
    S_params : dict
        Non-perturbative action parameters
        
    Returns:
    --------
    dydt : array
        Derivatives [dlambda/dt, dalpha_eff/dt, ...]
    """
    lam, alpha_eff, kappa, alpha_EM = y
    
    # Current energy scale
    mu = M_PL * np.exp(t)
    
    # Perturbative beta functions
    beta_lam_pert = beta_lambda_perturbative(lam, alpha_eff)
    beta_alpha_pert = beta_alpha_eff_perturbative(alpha_eff)
    beta_kappa = beta_kappa_grav(kappa, alpha_eff, mu)
    
    # Standard QED running for α_EM (1-loop)
    beta_0_QED = 4/3  # 3 generations of leptons
    beta_alpha_EM_pert = (alpha_EM**2) / (2*np.pi) * beta_0_QED
    
    # Non-perturbative corrections
    S_eff = S_effective_total(mu, M_EW, M_PL, **S_params)
    
    # dS_eff/d(ln μ) using a stable central difference in t = ln μ
    eps_t = float(S_params.get('eps_t', 1e-3))  # small step in log-scale
    mu_plus = mu * np.exp(eps_t)
    mu_minus = mu * np.exp(-eps_t)
    S_eff_plus = S_effective_total(mu_plus, M_EW, M_PL, **S_params)
    S_eff_minus = S_effective_total(mu_minus, M_EW, M_PL, **S_params)
    dS_dt = (S_eff_plus - S_eff_minus) / (2.0 * eps_t)
    
    # Non-perturbative contribution to alpha_EM
    # β_α^{non-pert} = α · dS_eff/dt
    beta_alpha_EM_nonpert = alpha_EM * dS_dt
    
    # Total betas
    beta_lam = beta_lam_pert
    beta_alpha = beta_alpha_pert
    beta_kappa = beta_kappa
    beta_alpha_EM = beta_alpha_EM_pert + beta_alpha_EM_nonpert
    
    return np.array([beta_lam, beta_alpha, beta_kappa, beta_alpha_EM])

# =============================================================================
# SOLVER
# =============================================================================

def solve_rg_flow(initial_conditions: Dict,
                 S_params: Dict,
                 N_steps: int = 1000) -> Dict:
    """
    Solve RG flow equations.
    
    Parameters:
    -----------
    initial_conditions : dict
        Values at M_PL: lambda_qct, alpha_eff, kappa_grav, alpha_EM
    S_params : dict
        Non-perturbative action parameters: S1, S2, S3, S4
    N_steps : int
        Number of integration steps
        
    Returns:
    --------
    solution : dict
        mu : array of energy scales
        lambda : array
        alpha_eff : array
        kappa_grav : array
        alpha_EM : array
    """
    # Initial conditions
    y0 = np.array([
        initial_conditions['lambda_qct'],
        initial_conditions['alpha_eff'],
        initial_conditions['kappa_grav'],
        initial_conditions['alpha_EM']
    ])
    
    # RG "time" from M_PL to m_e
    t_start = 0  # ln(M_PL/M_PL) = 0
    t_end = np.log(m_e / M_PL)  # ~-40
    t_array = np.linspace(t_start, t_end, N_steps)
    
    # Solve ODE
    print("Solving RG equations...")
    solution = odeint(rg_equations, y0, t_array, args=(S_params,))
    
    # Extract solutions
    mu_array = M_PL * np.exp(t_array)
    
    result = {
        'mu': mu_array,
        'lambda_qct': solution[:, 0],
        'alpha_eff': solution[:, 1],
        'kappa_grav': solution[:, 2],
        'alpha_EM': solution[:, 3],
        'alpha_EM_inverse': 1 / solution[:, 3],
        't': t_array
    }
    
    return result

# =============================================================================
# VISUALIZATION
# =============================================================================

def plot_rg_flow(solution: Dict):
    """Plot RG flow of all couplings."""
    
    mu = solution['mu']
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. Lambda
    ax = axes[0, 0]
    ax.loglog(mu, solution['lambda_qct'], 'b-', linewidth=2)
    ax.axvline(M_EW, color='r', linestyle='--', alpha=0.5, label='M_EW')
    ax.axvline(M_Z, color='g', linestyle='--', alpha=0.5, label='M_Z')
    ax.set_xlabel('μ [GeV]')
    ax.set_ylabel('λ')
    ax.set_title('Quartic Coupling λ(μ)')
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    # 2. Alpha_eff
    ax = axes[0, 1]
    ax.loglog(mu, solution['alpha_eff'], 'b-', linewidth=2)
    ax.axvline(M_EW, color='r', linestyle='--', alpha=0.5, label='M_EW')
    ax.set_xlabel('μ [GeV]')
    ax.set_ylabel('α_eff [GeV⁻²]')
    ax.set_title('Effective Coupling α_eff(μ)')
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    # 3. Kappa_grav
    ax = axes[1, 0]
    ax.loglog(mu, solution['kappa_grav'], 'b-', linewidth=2)
    ax.axvline(M_EW, color='r', linestyle='--', alpha=0.5, label='M_EW')
    ax.set_xlabel('μ [GeV]')
    ax.set_ylabel('κ_grav [m³/kg]')
    ax.set_title('Gravitational Coupling κ_grav(μ)')
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    # 4. Alpha_EM inverse
    ax = axes[1, 1]
    ax.semilogx(mu, solution['alpha_EM_inverse'], 'b-', linewidth=2, label='QCT')
    
    # Add experimental points
    alpha_inv_low = 137.036
    alpha_inv_MZ = 127.944
    ax.plot(m_e, alpha_inv_low, 'ro', markersize=10, label='Thomson limit')
    ax.plot(M_Z, alpha_inv_MZ, 'go', markersize=10, label='M_Z measurement')
    
    ax.axvline(M_EW, color='r', linestyle='--', alpha=0.5)
    ax.axvline(145e3, color='m', linestyle='--', alpha=0.5, label='Λ_QCT = 145 TeV')
    ax.set_xlabel('μ [GeV]')
    ax.set_ylabel('α⁻¹')
    ax.set_title('Fine Structure α⁻¹(μ)')
    ax.grid(True, alpha=0.3)
    ax.legend()
    ax.set_ylim([100, 150])
    
    plt.tight_layout()
    plt.savefig('QCT_Theory/06_analysis_tools/rg_flow.png', dpi=300)
    print("Plot saved to: QCT_Theory/06_analysis_tools/rg_flow.png")
    plt.show()

def plot_hierarchy_evolution(solution: Dict):
    """Plot evolution of force hierarchy."""
    
    mu = solution['mu']
    alpha_EM = solution['alpha_EM']
    
    # Gravitační coupling (prakticky konstantní)
    alpha_g = 5.9e-39 * np.ones_like(mu)
    
    # Ratio
    ratio = alpha_EM / alpha_g
    
    plt.figure(figsize=(12, 6))
    plt.loglog(mu, ratio, 'b-', linewidth=2)
    
    # Reference lines
    plt.axhline(1e10, color='g', linestyle='--', alpha=0.5, 
                label='Planck unification: 10¹⁰')
    plt.axhline(1e36, color='r', linestyle='--', alpha=0.5,
                label='Observed hierarchy: 10³⁶')
    
    plt.axvline(M_PL, color='k', linestyle='--', alpha=0.3, label='M_Pl')
    plt.axvline(M_EW, color='r', linestyle='--', alpha=0.3, label='M_EW')
    
    plt.xlabel('Energy Scale μ [GeV]', fontsize=12)
    plt.ylabel('α_EM / α_gravity', fontsize=12)
    plt.title('Evolution of Force Hierarchy', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=10)
    
    plt.tight_layout()
    plt.savefig('QCT_Theory/06_analysis_tools/hierarchy_evolution.png', dpi=300)
    print("Plot saved to: QCT_Theory/06_analysis_tools/hierarchy_evolution.png")
    plt.show()

# =============================================================================
# MAIN
# =============================================================================

def main():
    """Main RG flow computation."""
    
    print("="*60)
    print("QCT RENORMALIZATION GROUP FLOW")
    print("="*60)
    
    # Initial conditions at Planck scale
    initial_conditions = {
        'lambda_qct': 4.0e-31,
        'alpha_eff': 1.0e-25,    # GeV^-2
        'kappa_grav': 1.0e-37,   # m^3/kg
        'alpha_EM': 2.65e-28,    # QCT bare value
    }
    
    # Non-perturbative action parameters (from Fg_EM.tex)
    S_params = {
        'S1': 15,  # Instantons
        'S2': 15,  # Berry phase
        'S3': 5,   # Higgs coupling
        'S4': 23,  # Holography
        'eps_t': 1e-3,  # central-diff step in t=ln mu
    }
    
    print("\nInitial conditions (at M_Pl):")
    for key, val in initial_conditions.items():
        print(f"  {key:15s} = {val:.2e}")
    
    print("\nNon-perturbative parameters:")
    for key, val in S_params.items():
        print(f"  {key:5s} = {val}")
    
    print(f"\nTotal S_eff = {sum(S_params.values())}")
    
    # Solve
    solution = solve_rg_flow(initial_conditions, S_params, N_steps=2000)

    # Convergence check: halve eps_t and compare alpha^{-1}(M_Z)
    S_params_ref = dict(S_params)
    S_params_ref['eps_t'] = S_params.get('eps_t', 1e-3) / 2.0
    solution_ref = solve_rg_flow(initial_conditions, S_params_ref, N_steps=2000)
    
    # Extract key values
    print("\n" + "="*60)
    print("RESULTS")
    print("="*60)
    
    # At M_Z
    idx_MZ = np.argmin(np.abs(solution['mu'] - M_Z))
    print(f"\nAt M_Z = {M_Z} GeV:")
    print(f"  α⁻¹(M_Z) = {solution['alpha_EM_inverse'][idx_MZ]:.3f}")
    print(f"  (Experimental: 127.944 ± 0.014)")

    # Convergence diagnostic
    idx_MZ_ref = np.argmin(np.abs(solution_ref['mu'] - M_Z))
    alpha_inv_MZ = solution['alpha_EM_inverse'][idx_MZ]
    alpha_inv_MZ_ref = solution_ref['alpha_EM_inverse'][idx_MZ_ref]
    rel_diff = abs(alpha_inv_MZ - alpha_inv_MZ_ref) / max(alpha_inv_MZ_ref, 1e-12)
    print(f"  Convergence check (eps_t vs eps_t/2): rel. diff = {rel_diff:.3e}")
    
    # At low energy
    idx_low = -1
    print(f"\nAt low energy ({solution['mu'][idx_low]:.2e} GeV):")
    print(f"  α⁻¹ = {solution['alpha_EM_inverse'][idx_low]:.3f}")
    print(f"  (Experimental Thomson: 137.036)")
    
    # Hierarchy
    alpha_EM_MZ = solution['alpha_EM'][idx_MZ]
    alpha_g = 5.9e-39
    print(f"\nForce hierarchy at M_Z:")
    print(f"  α_EM/α_g = {alpha_EM_MZ/alpha_g:.2e}")
    print(f"  (Should be ~ 10³⁶)")
    
    # Save results
    save_dict = {
        'mu': solution['mu'].tolist(),
        'lambda_qct': solution['lambda_qct'].tolist(),
        'alpha_eff': solution['alpha_eff'].tolist(),
        'kappa_grav': solution['kappa_grav'].tolist(),
        'alpha_EM_inverse': solution['alpha_EM_inverse'].tolist(),
    }
    
    with open('QCT_Theory/06_analysis_tools/rg_flow_solution.json', 'w') as f:
        json.dump(save_dict, f, indent=2)
    
    print("\nResults saved to: QCT_Theory/06_analysis_tools/rg_flow_solution.json")
    
    # Plots
    plot_rg_flow(solution)
    plot_hierarchy_evolution(solution)

if __name__ == '__main__':
    main()
