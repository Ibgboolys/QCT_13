# QCT_Simulation.py - Complete simulation code for f(m_q) interpolation in lattice QCD style
# Run on PC: python QCT_Simulation.py
# Requires: numpy, scipy, matplotlib (install: pip install numpy scipy matplotlib)
# Output: Graphs (m_N vs m_q, f(x) vs x) with comparison of limits 5/6 and (3+sqrt(3))/6
# Data: Proxy from typical lattice QCD values (FLAG/PDG-inspired; m_pi proxy for m_q)

import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# === CONSTANTS FROM QCT ===
Lambda_micro = 0.733  # GeV (microscopic scale)
Lambda_QCD = 0.332    # GeV (standard QCD scale, PDG/FLAG)
m_q_phys = 0.009      # GeV (approximately 2m_u + m_d ~9 MeV)

# === ALGEBRAIC LIMITS ===
limit_chiral = 5 / 6  # 0.8333
limit_physical = (3 + np.sqrt(3)) / 6  # ~0.7887

# === SIMULATED/PROXY DATA FROM LATTICE QCD ===
# (m_pi [MeV] as proxy for m_q; m_N [GeV]; from typical FLAG/CLS values)
# Source: Inspired by FLAG 2021-2024, CLS/ETMC ensembles; m_pi^2 ∝ m_q
data_points = [
    # Chiral limit (m_pi ~0, m_N ~0.88 GeV)
    {'m_pi': 0,   'm_N': 0.88,  'error_m_N': 0.015},
    # Higher m_pi (lattice simulations)
    {'m_pi': 135, 'm_N': 0.938, 'error_m_N': 0.002},  # Physical
    {'m_pi': 200, 'm_N': 0.95,  'error_m_N': 0.005},
    {'m_pi': 300, 'm_N': 1.00,  'error_m_N': 0.01},
    {'m_pi': 400, 'm_N': 1.05,  'error_m_N': 0.015},
    {'m_pi': 500, 'm_N': 1.10,  'error_m_N': 0.02},
]

# Convert m_pi to m_q (proxy: m_q ∝ m_pi^2; normalized to physical m_pi=135 MeV)
m_pi_phys = 135  # MeV
m_q_data = np.array([(p['m_pi'] / m_pi_phys)**2 * m_q_phys for p in data_points])  # GeV
m_N_data = np.array([p['m_N'] for p in data_points])
errors_m_N = np.array([p['error_m_N'] for p in data_points])

# Normalize x = m_q / Lambda_QCD
x_data = m_q_data / Lambda_QCD

# === ChPT MODEL FOR m_N(x) - NLO approx ===
# m_N = m0 + c * m_pi^2 + d * m_pi^3 (non-analytic)
def m_N_model(x, m0, c, d):
    m_pi_sq = x * Lambda_QCD  # Proxy m_pi^2 ∝ m_q
    return m0 + c * m_pi_sq + d * m_pi_sq ** 1.5

# Fit data
popt, pcov = curve_fit(m_N_model, x_data, m_N_data, sigma=errors_m_N, p0=[0.88, 0.5, -0.1])
m0_fit, c_fit, d_fit = popt
print(f"Fitted parameters: m0 = {m0_fit:.3f} GeV, c = {c_fit:.3f}, d = {d_fit:.3f}")

# Interpolated function f(x) = Lambda_micro / m_N(x)
def f_interp(x):
    return Lambda_micro / m_N_model(x, *popt)

# Calculate f for data
f_data = Lambda_micro / m_N_data

# Verify limits
f_chiral_calc = f_interp(0)
f_phys_calc = f_interp(m_q_phys / Lambda_QCD)
print(f"Calculated f(0) = {f_chiral_calc:.4f} (vs. target 5/6 = {limit_chiral:.4f})")
print(f"Calculated f(phys) = {f_phys_calc:.4f} (vs. target (3+sqrt(3))/6 = {limit_physical:.4f})")

# === GRAPHS WITH COMPARISON ===
# Graph 1: m_N vs m_q
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.errorbar(m_q_data * 1000, m_N_data, yerr=errors_m_N, fmt='o', label='Lattice-style data', color='blue')
x_fit = np.linspace(0, max(m_q_data) * 1.2, 100)
plt.plot(x_fit * 1000, m_N_model(x_fit / Lambda_QCD, *popt), 'r-', label='ChPT fit')
plt.axhline(0.88, color='green', ls='--', label='Chiral limit M_0 ≈ 0.88 GeV')
plt.axhline(0.9293, color='purple', ls='--', label='Physical m_p^QCD ≈ 0.929 GeV')
plt.xlabel('m_q [MeV]')
plt.ylabel('m_N [GeV]')
plt.title('m_N vs m_q (with ChPT fit)')
plt.legend()
plt.grid(True)

# Graph 2: f(x) vs x with limit comparison
plt.subplot(1, 2, 2)
plt.scatter(x_data, f_data, label='Data', color='blue')
plt.plot(x_fit / Lambda_QCD, Lambda_micro / m_N_model(x_fit / Lambda_QCD, *popt), 'r-', label='Interpolation f(x)')
plt.axhline(limit_chiral, color='green', ls='--', label='Target chiral: 5/6 ≈ 0.833')
plt.axhline(limit_physical, color='purple', ls='--', label='Target physical: (3+√3)/6 ≈ 0.789')
plt.xlabel('x = m_q / Λ_QCD')
plt.ylabel('f(x) = Λ_micro / m_N')
plt.title('Interpolation f(m_q) with limit comparison')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig('QCT_Simulation_Graphs.png')  # Saves graphs as PNG
plt.show()

print("Simulation completed! Graphs saved as 'QCT_Simulation_Graphs.png'")