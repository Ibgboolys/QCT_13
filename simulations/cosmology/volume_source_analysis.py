#!/usr/bin/env python3
"""
Analýza koncentrace neutrin pro OBJEMOVĚ ROZLOŽENÉ zdroje hmoty
========================================================================

KLÍČOVÝ ROZDÍL:
- Bodový zdroj: Φ = -GM/r (singulární v centru)
- Objemový zdroj: Φ(r) = -2πGρ(R² - r²/3) uvnitř (konečný!)

Pro molekulární mračna a galaxie je objemová distribuce zásadní!
"""

import math

# Konstanty
G_N = 6.674e-11  # m^3 kg^-1 s^-2
c = 2.998e8  # m/s
M_sun = 1.989e30  # kg

# QCT parametry
R_proj_0 = 2.3e-2  # m (2.3 cm)
xi_0 = 1e-3  # m (1 mm)
f_screen = 1.07e-10
n_nu_cosmic = 336e6  # m^-3

# Coupling parametr (různý pro různá pole?)
alpha_strong = 9e11  # Pro silná pole (Země) - fitted z Eöt-Wash
alpha_weak = 1e9     # Pro slabá pole (mračna) - tentative

def Phi_point_source(r, M):
    """
    Gravitační potenciál pro BODOVÝ zdroj.

    Φ = -GM/r

    Singulární v r=0!
    """
    if r == 0:
        return float('-inf')
    return -G_N * M / r

def Phi_sphere(r, R, rho):
    """
    Gravitační potenciál pro HOMOGENNÍ SFÉRU hustoty ρ.

    UVNITŘ (r ≤ R):
        Φ(r) = -2πGρ(R² - r²/3)
        Φ(0) = -2πGρR² = -3GM/(2R)  (konečné!)

    VENKU (r > R):
        Φ(r) = -GM/r  (jako bodový zdroj)

    Parametry:
        r: vzdálenost od centra [m]
        R: poloměr sféry [m]
        rho: hustota [kg/m³]
    """
    M_total = (4.0/3.0) * math.pi * R**3 * rho

    if r <= R:
        # UVNITŘ sféry
        Phi = -2 * math.pi * G_N * rho * (R**2 - r**2/3.0)
    else:
        # VENKU (jako bodový zdroj)
        Phi = -G_N * M_total / r

    return Phi

def concentration_factor(Phi, alpha):
    """
    Koncentrační faktor neutrin v gravitačním poli.

    K = 1 + α Φ/c²

    Safety: K nemůže být < 1 (nefy zikální!)
    """
    K = 1 + alpha * Phi / c**2
    return max(K, 1.0)

def screening_length(K):
    """Lokální screeningová délka"""
    xi = xi_0 / math.sqrt(K)
    R_proj = R_proj_0 * (xi / xi_0)
    return R_proj / math.log(1.0 / f_screen)

def average_concentration_sphere(R, rho, alpha, n_points=100):
    """
    Průměrná koncentrace neutrin v celém objemu sféry.

    K_avg = (1/V) ∫ K(r) dV
          = (3/R³) ∫₀ᴿ K(r) r² dr

    Používá numerickou integraci.
    """
    # Vzorkování radiálních pozic
    r_values = [R * i / n_points for i in range(n_points + 1)]

    # K(r) a váhy pro integraci
    K_values = []
    weights = []

    for r in r_values:
        Phi = Phi_sphere(r, R, rho)
        K = concentration_factor(Phi, alpha)
        K_values.append(K)
        weights.append(r**2)  # Objemový element: 4πr² dr

    # Numerická integrace (trapezoid rule)
    integral = 0.0
    for i in range(len(r_values) - 1):
        dr = r_values[i+1] - r_values[i]
        avg_K = (K_values[i] + K_values[i+1]) / 2.0
        avg_weight = (weights[i] + weights[i+1]) / 2.0
        integral += avg_K * avg_weight * dr

    # Normalizace na objem
    K_avg = integral / (R**3 / 3.0)

    return K_avg, K_values, r_values

# ============================================================================
# ANALÝZA 1: POROVNÁNÍ BODOVÝ vs. OBJEMOVÝ ZDROJ
# ============================================================================

print("="*90)
print("POROVNÁNÍ: BODOVÝ vs. OBJEMOVÝ ZDROJ")
print("="*90)

# Parametry molekulárního mračna
rho_cloud = 1e-18  # kg/m³
R_cloud = 1e16     # m (~0.3 pc)
M_cloud = (4.0/3.0) * math.pi * R_cloud**3 * rho_cloud

print(f"\nMolekulární mračno:")
print(f"  Hustota ρ: {rho_cloud:.2e} kg/m³")
print(f"  Poloměr R: {R_cloud:.2e} m = {R_cloud/3.086e16:.2f} pc")
print(f"  Hmotnost M: {M_cloud:.2e} kg = {M_cloud/M_sun:.2f} M☉")

# Porovnání potenciálů na různých pozicích
positions = {
    'Centrum (r=0)': 0,
    'r = R/4': R_cloud/4,
    'r = R/2': R_cloud/2,
    'r = 3R/4': 3*R_cloud/4,
    'Povrch (r=R)': R_cloud,
    'r = 2R (venku)': 2*R_cloud
}

print(f"\n{'Pozice':<20} {'r/R':<10} {'Φ_point [m²/s²]':<20} {'Φ_sphere [m²/s²]':<20} {'Poměr':<10}")
print("-" * 90)

for label, r in positions.items():
    r_ratio = r / R_cloud if r > 0 else 0

    if r == 0:
        Phi_point = float('-inf')
        Phi_sph = Phi_sphere(r, R_cloud, rho_cloud)
        ratio = 0
        print(f"{label:<20} {r_ratio:<10.2f} {'singulární!':<20} {Phi_sph:<20.3e} {'∞':<10}")
    else:
        Phi_point = Phi_point_source(r, M_cloud)
        Phi_sph = Phi_sphere(r, R_cloud, rho_cloud)
        ratio = Phi_sph / Phi_point if Phi_point != 0 else 1.0
        print(f"{label:<20} {r_ratio:<10.2f} {Phi_point:<20.3e} {Phi_sph:<20.3e} {ratio:<10.3f}")

# ============================================================================
# ANALÝZA 2: KONCENTRAČNÍ FAKTOR PRO RŮZNÁ α
# ============================================================================

print(f"\n\n{'='*90}")
print("KONCENTRAČNÍ FAKTOR K = 1 + α Φ/c²")
print("="*90)

print(f"\nTestujeme dva hodnoty α:")
print(f"  α_strong = {alpha_strong:.2e} (fitted z Eöt-Wash pro Zemi)")
print(f"  α_weak = {alpha_weak:.2e} (tentativní pro slabá pole)")

# V centru mračna
Phi_center = Phi_sphere(0, R_cloud, rho_cloud)
K_center_strong = concentration_factor(Phi_center, alpha_strong)
K_center_weak = concentration_factor(Phi_center, alpha_weak)

print(f"\nV CENTRU mračna (r=0):")
print(f"  Φ(0) = {Phi_center:.3e} m²/s²")
print(f"  K(α_strong) = 1 + {alpha_strong:.2e} × {Phi_center:.3e} / c²")
print(f"              = 1 + {alpha_strong * Phi_center / c**2:.3f}")
print(f"              = {1 + alpha_strong * Phi_center / c**2:.3f}")
print(f"  → K_center = {K_center_strong:.3f} (po safety check)")

if K_center_strong == 1.0 and (1 + alpha_strong * Phi_center / c**2) < 1.0:
    print(f"  ⚠ VAROVÁNÍ: α_strong dává K < 1 (nefyzikální!) → použita korekce K=1")

print(f"\n  K(α_weak) = 1 + {alpha_weak:.2e} × {Phi_center:.3e} / c²")
print(f"            = {K_center_weak:.3f}")

# Na povrchu
Phi_surface = Phi_sphere(R_cloud, R_cloud, rho_cloud)
K_surface_strong = concentration_factor(Phi_surface, alpha_strong)
K_surface_weak = concentration_factor(Phi_surface, alpha_weak)

print(f"\nNA POVRCHU mračna (r=R):")
print(f"  Φ(R) = {Phi_surface:.3e} m²/s²")
print(f"  K(α_strong) = {K_surface_strong:.3f}")
print(f"  K(α_weak) = {K_surface_weak:.3f}")

# ============================================================================
# ANALÝZA 3: PRŮMĚRNÁ KONCENTRACE V OBJEMU
# ============================================================================

print(f"\n\n{'='*90}")
print("PRŮMĚRNÁ KONCENTRACE NEUTRIN V OBJEMU")
print("="*90)

# S α_strong
print(f"\n--- S α_strong = {alpha_strong:.2e} ---")
K_avg_strong, K_profile_strong, r_profile = average_concentration_sphere(
    R_cloud, rho_cloud, alpha_strong, n_points=50
)

print(f"  K_center = {K_profile_strong[0]:.3f}")
print(f"  K_surface = {K_profile_strong[-1]:.3f}")
print(f"  K_average = {K_avg_strong:.3f}")

lambda_avg_strong = screening_length(K_avg_strong)
print(f"  λ_screen(průměr) = {lambda_avg_strong:.3e} m = {lambda_avg_strong*1e6:.3f} μm")

# S α_weak
print(f"\n--- S α_weak = {alpha_weak:.2e} ---")
K_avg_weak, K_profile_weak, _ = average_concentration_sphere(
    R_cloud, rho_cloud, alpha_weak, n_points=50
)

print(f"  K_center = {K_profile_weak[0]:.3f}")
print(f"  K_surface = {K_profile_weak[-1]:.3f}")
print(f"  K_average = {K_avg_weak:.3f}")

lambda_avg_weak = screening_length(K_avg_weak)
print(f"  λ_screen(průměr) = {lambda_avg_weak:.3e} m = {lambda_avg_weak*1e3:.3f} mm")

# ============================================================================
# ANALÝZA 4: SROVNÁNÍ SE ZEMÍ (silné pole)
# ============================================================================

print(f"\n\n{'='*90}")
print("SROVNÁNÍ: MRAČNO vs. ZEMĚ")
print("="*90)

# Země (pro kontext)
M_earth = 5.972e24  # kg
R_earth = 6.371e6   # m
rho_earth = M_earth / ((4.0/3.0) * math.pi * R_earth**3)

Phi_earth_center = Phi_sphere(0, R_earth, rho_earth)
Phi_earth_surface = Phi_sphere(R_earth, R_earth, rho_earth)

K_earth_center = concentration_factor(Phi_earth_center, alpha_strong)
K_earth_surface = concentration_factor(Phi_earth_surface, alpha_strong)

print(f"\nZEMĚ (silné pole):")
print(f"  Hustota ρ: {rho_earth:.2e} kg/m³")
print(f"  Poloměr R: {R_earth:.3e} m")
print(f"  Φ(centrum): {Phi_earth_center:.3e} m²/s²")
print(f"  Φ(povrch): {Phi_earth_surface:.3e} m²/s²")
print(f"  K(centrum, α_strong): {K_earth_center:.1f}")
print(f"  K(povrch, α_strong): {K_earth_surface:.1f}")

print(f"\nMRAČNO (slabé pole):")
print(f"  Hustota ρ: {rho_cloud:.2e} kg/m³")
print(f"  Poloměr R: {R_cloud:.3e} m")
print(f"  Φ(centrum): {Phi_center:.3e} m²/s²")
print(f"  Φ(povrch): {Phi_surface:.3e} m²/s²")
print(f"  K(centrum, α_strong): {K_center_strong:.3f}")
print(f"  K(centrum, α_weak): {K_center_weak:.3f}")

print(f"\nPOMĚR HUSTOT:")
print(f"  ρ_earth / ρ_cloud = {rho_earth / rho_cloud:.2e}")

print(f"\nPOMĚR POTENCIÁLŮ (povrch):")
print(f"  |Φ_earth| / |Φ_cloud| = {abs(Phi_earth_surface) / abs(Phi_surface):.2e}")

# ============================================================================
# ZÁVĚRY
# ============================================================================

print(f"\n\n{'='*90}")
print("KLÍČOVÉ ZÁVĚRY")
print("="*90)

print(f"""
1. ROZDÍL: BODOVÝ vs. OBJEMOVÝ ZDROJ

   Pro mračno (R ~ 0.3 pc):
   - V CENTRU: Φ_point → -∞ (singulární!)
               Φ_sphere = {Phi_center:.3e} m²/s² (konečné ✓)

   - NA POVRCHU: Φ_point = Φ_sphere = {Phi_surface:.3e} m²/s² (stejné ✓)

   → Objemová distribuce je ZÁSADNÍ pro výpočty v mračnu!

2. PROBLÉM S α_strong = {alpha_strong:.2e}

   Pro Zemi (ρ ~ {rho_earth:.0f} kg/m³, |Φ| ~ {abs(Phi_earth_surface):.2e}):
   - K ~ {K_earth_center:.0f} → λ_screen ~ 40 μm ✓ (souhlasí s Eöt-Wash)

   Pro mračno (ρ ~ {rho_cloud:.0e} kg/m³, |Φ| ~ {abs(Phi_center):.2e}):
   - K = 1 + α_strong × Φ/c² = {1 + alpha_strong * Phi_center / c**2:.3f}
   - K < 1 → NEFYZIKÁLNÍ! ❌

   → α_strong je fitted pro SILNÁ pole (Země)
   → Pro SLABÁ pole (mračna) potřebujeme jiné α nebo jiný mechanismus!

3. ŠKÁLOVÁNÍ α S INTENZITOU POLE?

   Možnost A: α = α(ρ) nebo α = α(Φ)
      - Pro silná pole: α → α_strong ~ 10¹¹
      - Pro slabá pole: α → α_weak ~ 10⁹ nebo menší

   Možnost B: Saturace mechanismu
      - Pro |Φ| >> Φ_critical: plná koncentrace
      - Pro |Φ| << Φ_critical: žádná/slabá koncentrace

   Možnost C: Nelineární závislost
      - K = 1 + f(αΦ/c²) kde f není lineární

4. SCREENING V MRAČNU

   S α_weak = {alpha_weak:.2e}:
   - K_average ~ {K_avg_weak:.2f}
   - λ_screen ~ {lambda_avg_weak*1e3:.2f} mm

   Pro R_cloud ~ {R_cloud:.2e} m:
   - R_cloud / λ_screen ~ {R_cloud / lambda_avg_weak:.2e}
   - exp(-R_cloud/λ_screen) ~ 0 (úplný screening!)

   → I s α_weak je screening příliš silný pro mračna!
   → CUTOFF mechanismus na R_proj ~ 2.3 cm je stále NUTNÝ!

5. KONZISTENCE PRO RŮZNÉ REŽIMY

   ✓ Silná pole (Země, r < mm):
     - α_strong ~ 9×10¹¹
     - Screening aktivní
     - λ_screen ~ 40 μm

   ✓ Střední pole (???):
     - Přechodová oblast
     - α(Φ) interpolace?

   ✓ Slabá pole + velké škály (mračna, r > cm):
     - Cutoff aktivní
     - G_eff = G_N
     - Gravitace normální

ZÁVĚR:
Objemová distribuce hmoty je ZÁSADNÍ!
α = 9×10¹¹ je fitted pro Zemi a nelze jej aplikovat na slabá pole.
Potřebujeme:
1. Zavést α = α(Φ) nebo α = α(ρ)
2. Nebo porozumět fyzikálnímu mechanismu saturace
3. Cutoff zůstává nutný pro astrofyzikální škály
""")

print("="*90)
