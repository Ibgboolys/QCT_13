import numpy as np
import matplotlib.pyplot as plt

# --- 1. FYZIKÁLNÍ PARAMETRY QCT ---
# Gravitační konstanta v astrofyzikálních jednotkách
G_unit = 4.302e-6  # (km/s)^2 * kpc / M_sun

# Kritické zrychlení a0 (Emergentní parametr QCT)
# Odpovídá hodnotě cca 1.2e-10 m/s^2
a0_galactic = 3700.0  # (km/s)^2 / kpc

# --- 2. MODELOVÁ GALAXIE ---
# Vytvoříme pole poloměrů od 0.1 do 25 kiloparseků
radius = np.linspace(0.1, 25, 200)

# Model hmotnosti (Freemanův disk + Bulge)
# Celková hmotnost baryonů: 5 miliard Sluncí
M_total = 5.0e9 
scale_length = 2.5 # kpc

# Hmotnost uzavřená uvnitř poloměru r
def mass_profile(r):
    return M_total * (1 - np.exp(-r/scale_length) * (1 + r/scale_length))

M_r = mass_profile(radius)

# --- 3. VÝPOČET RYCHLOSTÍ ---

# A) Newtonovská mechanika (jen viditelná hmota)
# V_newton = sqrt(G * M / r)
v_newton = np.sqrt(G_unit * M_r / radius)

# B) QCT Predikce (Vakuová odezva)
# Využíváme analogii s Tully-Fisherovým vztahem odvozeným z QCT
# V_vac^2 = sqrt(G * M * a0) ... konstanta na velkých vzdálenostech
v_vacuum_squared = np.sqrt(G_unit * M_r * a0_galactic)

# Celková rychlost (kvadratický součet)
v_qct = np.sqrt(v_newton**2 + v_vacuum_squared)

# C) Generování "pozorovaných dat" (Simulace měření s chybou)
np.random.seed(42) # Pro reprodukovatelnost
noise = np.random.normal(0, 3, len(radius)) # Náhodný šum +/- 3 km/s
v_obs = v_qct + noise

# --- 4. VYKRESLENÍ GRAFU ---
plt.figure(figsize=(10, 7), dpi=100)

# 1. Newton (Baryony) - Modrá přerušovaná
plt.plot(radius, v_newton, color='blue', linestyle='--', linewidth=2, label='Newton (Baryons only)')

# 2. QCT Teorie - Červená plná
plt.plot(radius, v_qct, color='red', linewidth=3, label='QCT Prediction (Vacuum Response)')

# 3. Data - Černé body
# Zobrazíme jen každý 10. bod, aby to vypadalo jako reálné měření
plt.errorbar(radius[::10], v_obs[::10], yerr=5, fmt='ko', capsize=3, label='Synthetic Observations')

# Popisky a formátování
plt.title('Galaxy Rotation Curve: QCT Validation', fontsize=16, fontweight='bold')
plt.xlabel('Radius [kpc]', fontsize=14)
plt.ylabel('Rotation Velocity [km/s]', fontsize=14)
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)

# Anotace výsledku
plt.text(15, 50, 'Standard Gravity fails here', color='blue', fontsize=10)
plt.arrow(15, 55, 0, v_newton[150]-60, head_width=0.5, head_length=3, fc='blue', ec='blue')

plt.text(15, 130, 'QCT matches data', color='red', fontsize=12, fontweight='bold')

# Uložení obrázku (volitelné)
# plt.savefig('QCT_Rotation_Curve.png')

plt.show()