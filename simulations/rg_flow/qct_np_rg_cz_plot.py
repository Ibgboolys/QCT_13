#!/usr/bin/env python3
"""
Jednoduchý skript pro vygenerování českého grafu alpha(mu) RG běhu
Zjednodušená verze z qct_np_rg.py zaměřená pouze na vykreslení
"""
import numpy as np
import matplotlib.pyplot as plt

# Nastavení českého fontu pro matplotlib
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# Konstanty
M_Z = 91.1876  # GeV
alpha_target = 1.0/137.035999084  # při 1 GeV

# Simulovaný RG běh (zjednodušený model pro vizualizaci)
mu = np.logspace(-5, 19, 1000)  # od 10^-5 GeV do 10^19 GeV (Planck)

# Aproximace: konstantní alpha pod určitou škálou, pak prudký pokles
# Toto je zjednodušená verze - skutečný QCT model je v qct_np_rg.py
alpha_pl = 8e-3  # Planck scale fine structure constant (zjednodušeno)
Lambda_transition = 1e4  # GeV (přibližná škála NP přechodu)

# Jednoduchá logistická funkce pro přechod
def alpha_simplified(mu_val):
    # Pod 1e4 GeV: konstantní ~ alpha_target
    # Nad 1e4 GeV: exponenciálně klesá k alpha_pl
    if mu_val < Lambda_transition:
        return alpha_target
    else:
        # Logistický pokles
        x = np.log10(mu_val / Lambda_transition)
        return alpha_pl + (alpha_target - alpha_pl) / (1 + np.exp(x * 0.5))

alpha_vals = np.array([alpha_simplified(m) for m in mu])

# Vykreslení
plt.figure(figsize=(7, 4))
plt.loglog(mu, alpha_vals, 'b-', linewidth=2)
plt.axvline(M_Z, color='k', ls='--', lw=1.5, label='M_Z')
plt.axhline(alpha_target, color='r', ls=':', lw=1.5, label='alpha_cíl@1GeV')
plt.xlabel(r"$\mu$ [GeV]", fontsize=12)
plt.ylabel(r"$\alpha(\mu)$", fontsize=12)
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3, which='both')
plt.tight_layout()
plt.savefig('manuscripts/latex_source/qct_np_rg_cz.png', dpi=300)
plt.close()

print("Graf RG běhu uložen jako 'qct_np_rg_cz.png'")
