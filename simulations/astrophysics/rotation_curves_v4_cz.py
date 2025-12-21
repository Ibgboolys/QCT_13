import numpy as np
import matplotlib.pyplot as plt

# Nastavení českého fontu pro matplotlib
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# --- 1. FYZIKÁLNÍ KONSTANTY QCT ---
G_unit = 4.302e-6  # (km/s)^2 * kpc / M_sun
a0_galactic = 3700.0  # (km/s)^2 / kpc  (~1.2e-10 m/s^2)

# --- 2. DEFINICE GALAXIÍ (DATA SPARC) ---
# Data z tabulky: L (10^9 Lsun), M_HI (10^9 Msun), R_disk (kpc), V_flat_obs (km/s)
# M/L poměr nastaven na standardní hodnotu 0.5 pro 3.6um pásmo

galaxies = {
    "NGC 6503 (Standardní)": {
        "L": 12.84, "M_HI": 1.62, "Rd": 1.74, "V_obs": 116.3
    },
    "NGC 1560 (LSB - Kritická)": {
        "L": 0.36, "M_HI": 1.34, "Rd": 1.3, "V_obs": 80.0
        # Pozn: L je velmi malé, M_HI je 4x větší než L -> Dominance plynu/temné hmoty
    },
    "UGC 128 (Obří LSB)": {
        "L": 12.02, "M_HI": 9.63, "Rd": 6.9, "V_obs": 129.3
    },
    "NGC 2903 (Vysoká hmotnost)": {
        "L": 81.86, "M_HI": 4.54, "Rd": 2.5, "V_obs": 184.6
    }
}

# --- 3. SIMULAČNÍ FUNKCE (QCT EQUATIONS) ---
def simulate_galaxy(name, params):
    # Parametry
    L = params["L"] * 1e9
    M_HI = params["M_HI"] * 1e9
    Rd = params["Rd"]
    V_target = params["V_obs"]

    # Hmotnosti
    M_star = L * 0.5 # M/L = 0.5
    M_gas = 1.33 * M_HI # Helium correction

    # Radiální profil (0 až 5 násobek disku nebo 30 kpc)
    r_max = max(5 * Rd, 30)
    r = np.linspace(0.1, r_max, 200)

    # 1. NEWTON (Baryony)
    # Modelujeme profil disku (Freeman) a plynu (Halo)
    # V_disk^2 approx G * M_star / r * (1 - exp(-r/Rd)) - zjednodušený profil pro demonstraci
    v_disk_sq = (G_unit * M_star / r) * (1 - np.exp(-r/Rd))

    # Plyn je typicky rozprostřenější (R_gas approx 3*Rd)
    v_gas_sq = (G_unit * M_gas / r) * (1 - np.exp(-r/(3*Rd)))

    v_newton = np.sqrt(v_disk_sq + v_gas_sq)

    # 2. QCT VACUUM RESPONSE (Eq. 831 equivalent)
    # M_baryon_enclosed(r) = r * v_newton^2 / G
    M_enc = (r * v_newton**2) / G_unit

    v_vac_sq = np.sqrt(G_unit * M_enc * a0_galactic)

    # 3. TOTAL VELOCITY
    v_qct = np.sqrt(v_newton**2 + v_vac_sq)

    return r, v_newton, v_qct, V_target

# --- 4. VYKRESLENÍ ---
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes = axes.flatten()

results_summary = []

for i, (name, params) in enumerate(galaxies.items()):
    r, v_newt, v_qct, v_target = simulate_galaxy(name, params)

    # Plot
    ax = axes[i]
    ax.plot(r, v_newt, 'b--', label='Newton (baryony)')
    ax.plot(r, v_qct, 'r-', linewidth=2, label='QCT predikce')

    # Zobrazení cílové rychlosti (Data)
    ax.axhline(y=v_target, color='k', linestyle=':', alpha=0.6, label=f'Pozorovaná plochá ({v_target:.0f} km/s)')

    ax.set_title(name, fontsize=12, fontweight='bold')
    ax.set_xlabel('Poloměr [kpc]')
    ax.set_ylabel('Rychlost [km/s]')
    ax.grid(True, alpha=0.3)
    if i == 0: ax.legend()

    # Uložení výsledku pro textový výpis
    v_final_qct = v_qct[-1]
    diff = 100 * (v_final_qct - v_target) / v_target
    results_summary.append(f"{name}: Pred={v_final_qct:.1f}, Obs={v_target:.1f}, Chyba={diff:.1f}%")

plt.tight_layout()
plt.savefig('manuscripts/latex_source/QCT_Simulation_Graphs_galaxies_cz.png', dpi=300)
plt.close()

print("\n--- VÝSLEDKY SIMULACE QCT ---")
for res in results_summary:
    print(res)
print("\nGrafy uloženy jako 'QCT_Simulation_Graphs_galaxies_cz.png'")
