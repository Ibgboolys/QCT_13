#!/usr/bin/env python3
"""
TESTOVÁNÍ HYPOTÉZY: α ZÁVISÍ NA BARIONICKÉ HUSTOTĚ
========================================================================

FYZIKÁLNÍ MOTIVACE:
α popisuje coupling mezi neutriny a gravitačním polem.
Tento coupling by mohl záviset na LOKÁLNÍ KONCENTRACI barionů!

MODELY:
1. α(ρ) = α_0 × (ρ / ρ_0)^β   (power-law škálování)
2. Testujeme různé exponenty β: 0.5, 1.0, 1.5, 2.0

CÍLE:
- Vyřešit problém K < 1 pro slabá pole
- Zachovat Eöt-Wash constraint (λ ~ 40 μm na Zemi)
- Zjistit, zda cutoff je stále nutný
"""

import math

# Konstanty
G_N = 6.674e-11  # m^3 kg^-1 s^-2
c = 2.998e8  # m/s
M_sun = 1.989e30  # kg

# QCT parametry (baseline)
R_proj_0 = 2.3e-2  # m
xi_0 = 1e-3  # m
f_screen = 1.07e-10

# Reference hodnoty (Z Eöt-Wash experimentu)
rho_earth_ref = 5515  # kg/m³ (průměrná hustota Země)
lambda_earth_target = 40e-6  # m (40 μm, Eöt-Wash limit)
K_earth_target = 625  # Cílový K faktor pro Zemi (z Eöt-Wash)

# alpha_earth_ref bude kalibrován později (po definici Phi_sphere)
alpha_earth_ref = None  # Placeholder

def Phi_sphere(r, R, rho):
    """Gravitační potenciál homogenní sféry"""
    M_total = (4.0/3.0) * math.pi * R**3 * rho

    if r <= R:
        # Uvnitř
        Phi = -2 * math.pi * G_N * rho * (R**2 - r**2/3.0)
    else:
        # Venku
        Phi = -G_N * M_total / r

    return Phi

def alpha_scaling(rho, beta, alpha_0, rho_0=rho_earth_ref):
    """
    α(ρ) = α_0 × (ρ / ρ_0)^β

    Parametry:
        rho: lokální barionická hustota [kg/m³]
        beta: exponent škálování
        alpha_0: referenční α při ρ = ρ_0
        rho_0: referenční hustota (Země)
    """
    if rho <= 0:
        return 0.0

    scaling_factor = (rho / rho_0) ** beta
    return alpha_0 * scaling_factor

def concentration_factor(Phi, alpha):
    """K = 1 + α Φ/c²"""
    K = 1 + alpha * Phi / c**2
    return max(K, 1.0)  # Safety

def screening_length(K):
    """λ_screen(K)"""
    xi = xi_0 / math.sqrt(K)
    R_proj = R_proj_0 * (xi / xi_0)
    return R_proj / math.log(1.0 / f_screen)

def G_eff_ratio(r, lambda_scr):
    """G_eff / G_N = exp(-r/λ)"""
    return math.exp(-r / lambda_scr)

# ============================================================================
# KALIBRACE α_0 Z EÖT-WASH
# ============================================================================

print("="*100)
print("KALIBRACE α_0 Z EÖT-WASH EXPERIMENTU")
print("="*100)

# Víme, že pro Zemi: λ_screen ~ 40 μm → K ~ 625
# K = 1 + α Φ / c²
# → α = (K - 1) × c² / Φ

M_earth_calib = 5.972e24
R_earth_calib = 6.371e6
rho_earth_calib = M_earth_calib / ((4.0/3.0) * math.pi * R_earth_calib**3)
Phi_earth_surface_calib = Phi_sphere(R_earth_calib, R_earth_calib, rho_earth_calib)

# Kalibrujeme α_0 tak, aby K(Země) = K_earth_target
alpha_earth_ref = (K_earth_target - 1) * c**2 / Phi_earth_surface_calib

print(f"\nParametry Země:")
print(f"  ρ_earth = {rho_earth_calib:.0f} kg/m³")
print(f"  Φ(povrch) = {Phi_earth_surface_calib:.3e} m²/s²")
print(f"  Cílové K = {K_earth_target}")
print(f"  Cílové λ = {lambda_earth_target*1e6:.0f} μm")

print(f"\nKalibrovaný α_0:")
print(f"  α_0 = (K - 1) × c² / Φ")
print(f"      = ({K_earth_target} - 1) × ({c:.2e})² / ({Phi_earth_surface_calib:.3e})")
print(f"      = {alpha_earth_ref:.3e}")

# Ověření
K_check = 1 + alpha_earth_ref * Phi_earth_surface_calib / c**2
lambda_check = screening_length(K_check)

print(f"\nOvěření:")
print(f"  K(Země) = {K_check:.1f} (target: {K_earth_target})")
print(f"  λ(Země) = {lambda_check*1e6:.1f} μm (target: {lambda_earth_target*1e6:.0f} μm)")

if abs(lambda_check - lambda_earth_target) / lambda_earth_target < 0.1:
    print(f"  ✓ KALIBRACE OK!")
else:
    print(f"  ✗ KALIBRACE SELHALA!")

print()

# ============================================================================
# DEFINICE OBJEKTŮ
# ============================================================================

objects = {
    'Země': {
        'R': 6.371e6,  # m
        'M': 5.972e24,  # kg
        'rho': None,  # vypočte se
        'test_distances': {
            'Povrch': 6.371e6,
            'Eöt-Wash (100 μm)': 100e-6,
            'Eöt-Wash (1 mm)': 1e-3,
        }
    },
    'Slunce': {
        'R': 6.96e8,  # m
        'M': 1.989e30,  # kg
        'rho': None,
        'test_distances': {
            'Povrch': 6.96e8,
            'Centrum': 0,
            'r = R/2': 6.96e8 / 2,
        }
    },
    'Bílý trpaslík': {
        'R': 5e6,  # m (typický poloměr)
        'M': 1.989e30,  # kg (1 M☉)
        'rho': None,
        'test_distances': {
            'Povrch': 5e6,
            'Centrum': 0,
        }
    },
    'Molekulární mračno': {
        'R': 1e16,  # m (~0.3 pc)
        'M': 4.19e30,  # kg (~2.1 M☉)
        'rho': 1e-18,  # kg/m³
        'test_distances': {
            'Centrum': 0,
            'r = R/2': 1e16 / 2,
            'Povrch': 1e16,
        }
    },
    'Mezihvězdné medium (ISM)': {
        'R': 3e18,  # m (~10 pc, typická škála)
        'M': 1e32,  # kg
        'rho': 1e-21,  # kg/m³ (velmi řídké)
        'test_distances': {
            'Centrum': 0,
            'Povrch': 3e18,
        }
    }
}

# Vypočítat hustoty pro objekty bez zadané ρ
for name, obj in objects.items():
    if obj['rho'] is None:
        obj['rho'] = obj['M'] / ((4.0/3.0) * math.pi * obj['R']**3)

# ============================================================================
# ANALÝZA: TESTOVÁNÍ RŮZNÝCH β
# ============================================================================

betas = [0.5, 1.0, 1.5, 2.0]

print("="*100)
print("TESTOVÁNÍ HYPOTÉZY: α(ρ) = α_0 × (ρ / ρ_0)^β")
print("="*100)

print(f"\nREFERENCE (Eöt-Wash experiment):")
print(f"  ρ_0 (Země): {rho_earth_ref:.0f} kg/m³")
print(f"  α_0: {alpha_earth_ref:.2e}")
print(f"  Cílová λ_screen na Zemi: ~{lambda_earth_target*1e6:.0f} μm")

print(f"\n{'OBJEKT':<25} {'ρ [kg/m³]':<15} {'ρ/ρ_earth':<15}")
print("-" * 100)
for name, obj in objects.items():
    rho_ratio = obj['rho'] / rho_earth_ref
    print(f"{name:<25} {obj['rho']:<15.2e} {rho_ratio:<15.2e}")

# ============================================================================
# PRO KAŽDÉ β TESTUJ VŠECHNY OBJEKTY
# ============================================================================

for beta in betas:
    print(f"\n\n{'='*100}")
    print(f"EXPONENT β = {beta}")
    print(f"α(ρ) = {alpha_earth_ref:.2e} × (ρ / {rho_earth_ref:.0f})^{beta}")
    print("="*100)

    # Ověření na Zemi (musí vyhovovat Eöt-Wash!)
    print(f"\n{'='*100}")
    print("OVĚŘENÍ: ZEMĚ (Eöt-Wash constraint)")
    print("="*100)

    obj = objects['Země']
    rho = obj['rho']
    R = obj['R']

    # Potenciál na povrchu
    Phi_surface = Phi_sphere(R, R, rho)

    # α pro Zemi s tímto β
    alpha_earth = alpha_scaling(rho, beta, alpha_earth_ref)

    # K faktor
    K_earth = concentration_factor(Phi_surface, alpha_earth)

    # Screening délka
    lambda_earth = screening_length(K_earth)

    print(f"\nZeměkoule:")
    print(f"  ρ = {rho:.0f} kg/m³")
    print(f"  Φ(povrch) = {Phi_surface:.3e} m²/s²")
    print(f"  α(ρ_earth) = {alpha_earth:.3e}")
    print(f"  K = {K_earth:.1f}")
    print(f"  λ_screen = {lambda_earth*1e6:.1f} μm")

    # Check constraint
    if abs(lambda_earth - lambda_earth_target) / lambda_earth_target < 0.1:
        print(f"  ✓ VYHOVUJE Eöt-Wash (~{lambda_earth_target*1e6:.0f} μm)")
    else:
        print(f"  ✗ NEVYHOVUJE Eöt-Wash (target: ~{lambda_earth_target*1e6:.0f} μm)")
        print(f"  → Tento β není správný!")
        continue  # Skip další analýzu pro toto β

    # Test na různých vzdálenostech
    print(f"\n{'Vzdálenost':<25} {'r [m]':<15} {'G_eff/G_N':<15}")
    print("-" * 100)

    for label, r in obj['test_distances'].items():
        if r == 0:
            continue  # Skip centrum pro Zemi
        lambda_scr = screening_length(K_earth)
        g_ratio = G_eff_ratio(r, lambda_scr)
        print(f"{label:<25} {r:<15.3e} {g_ratio:<15.3e}")

    # ============================================================================
    # OSTATNÍ OBJEKTY
    # ============================================================================

    for obj_name in ['Slunce', 'Bílý trpaslík', 'Molekulární mračno', 'Mezihvězdné medium (ISM)']:
        print(f"\n{'='*100}")
        print(f"{obj_name.upper()}")
        print("="*100)

        obj = objects[obj_name]
        rho = obj['rho']
        R = obj['R']
        M = obj['M']

        # α pro tento objekt
        alpha_obj = alpha_scaling(rho, beta, alpha_earth_ref)

        print(f"\nParametry:")
        print(f"  ρ = {rho:.2e} kg/m³")
        print(f"  R = {R:.2e} m")
        print(f"  M = {M:.2e} kg = {M/M_sun:.2f} M☉")
        print(f"  α(ρ) = {alpha_obj:.2e}")
        print(f"  α(ρ) / α_earth = {alpha_obj / alpha_earth_ref:.2e}")

        # Analýza na různých pozicích
        print(f"\n{'Pozice':<25} {'r [m]':<15} {'Φ [m²/s²]':<15} {'K':<12} {'λ [m]':<15} {'G_eff/G_N':<15}")
        print("-" * 100)

        for label, r in obj['test_distances'].items():
            # Potenciál
            Phi = Phi_sphere(r, R, rho)

            # K faktor
            K = concentration_factor(Phi, alpha_obj)

            # Screening délka
            lambda_scr = screening_length(K)

            # G_eff
            g_ratio = G_eff_ratio(r, lambda_scr) if r > 0 else 1.0

            # Kontrola, zda K < 1 bez safety
            K_raw = 1 + alpha_obj * Phi / c**2
            warning = " ⚠ (K_raw < 1)" if K_raw < 1 else ""

            if r == 0:
                print(f"{label:<25} {r:<15.3e} {Phi:<15.3e} {K:<12.3f} {lambda_scr:<15.3e} {'N/A':<15}{warning}")
            else:
                print(f"{label:<25} {r:<15.3e} {Phi:<15.3e} {K:<12.3f} {lambda_scr:<15.3e} {g_ratio:<15.3e}{warning}")

        # Závěr pro tento objekt
        print(f"\nZÁVĚR pro {obj_name}:")

        # Test v centru (pokud existuje)
        if 'Centrum' in obj['test_distances'] or 0 in obj['test_distances'].values():
            Phi_center = Phi_sphere(0, R, rho)
            K_center = concentration_factor(Phi_center, alpha_obj)
            K_center_raw = 1 + alpha_obj * Phi_center / c**2

            if K_center_raw < 1:
                print(f"  ⚠ V centru: K_raw = {K_center_raw:.3f} < 1 (nefyzikální!)")
                print(f"  → α je příliš velké pro tuto hustotu!")
            else:
                print(f"  ✓ V centru: K = {K_center:.3f} ≥ 1 (fyzikální)")

        # Test screeningu
        Phi_surface = Phi_sphere(R, R, rho)
        K_surface = concentration_factor(Phi_surface, alpha_obj)
        lambda_surface = screening_length(K_surface)

        if R > lambda_surface:
            ratio = R / lambda_surface
            g_eff_surface = G_eff_ratio(R, lambda_surface)

            if g_eff_surface < 1e-10:
                print(f"  ⚠ Na povrchu: R/λ = {ratio:.2e} → G_eff ≈ 0")
                print(f"  → Screening příliš silný! Potřeba cutoff.")
            elif g_eff_surface < 0.1:
                print(f"  ⚠ Na povrchu: G_eff/G_N = {g_eff_surface:.3e}")
                print(f"  → Mírný screening, může ovlivnit dynamiku")
            else:
                print(f"  ✓ Na povrchu: G_eff/G_N = {g_eff_surface:.3e}")
                print(f"  → Screening zanedbatelný")
        else:
            print(f"  ✓ R < λ → screening neaktivní")

# ============================================================================
# CELKOVÉ ZÁVĚRY
# ============================================================================

print(f"\n\n{'='*100}")
print("CELKOVÉ ZÁVĚRY")
print("="*100)

print(f"""
TESTOVALI JSME HYPOTÉZU: α(ρ) = α_0 × (ρ / ρ_0)^β

Pro různé exponenty β = {betas}

KLÍČOVÉ OTÁZKY:

1. VYHOVUJE Eöt-Wash constraint (λ ~ 40 μm na Zemi)?
   → Pouze β, která dávají správnou λ_screen na Zemi, jsou platná

2. ŘEŠÍ PROBLÉM K < 1 pro slabá pole?
   → Pokud α(ρ_cloud) << α(ρ_earth), pak K zůstane ≥ 1 i v mračnech

3. JE STÁLE NUTNÝ CUTOFF?
   → Závisí na tom, jak rychle α klesá s ρ
   → Pokud screening je slabý v řídkých prostředích, cutoff nemusí být nutný!

POZOROVÁNÍ Z HUSTOT:
- Země:         ρ ~ 5.5×10³ kg/m³
- Slunce:       ρ ~ 1.4×10³ kg/m³  (4× řidší než Země)
- Bílý trpaslík: ρ ~ 1×10⁹ kg/m³   (2×10⁵× hustší než Země!)
- Mračno:       ρ ~ 1×10⁻¹⁸ kg/m³ (5×10⁻²¹× řidší než Země!)
- ISM:          ρ ~ 1×10⁻²¹ kg/m³ (2×10⁻²⁴× řidší než Země!)

Pokud β = 1 (lineární škálování):
- α(mračno) / α(Země) ~ 10⁻²¹
- α(ISM) / α(Země) ~ 10⁻²⁴
→ Prakticky žádný screening v řídkých prostředích!

FYZIKÁLNÍ INTERPRETACE:
α ~ ρ by mohlo znamenat, že neutrino-gravitace coupling závisí na:
- Lokální hustotě barionů
- Počtu rozptylových center
- Efektivní interakční průřez

To by vysvětlilo:
✓ Silný screening v hustých objektech (Země, bílí trpaslíci)
✓ Slabý/žádný screening v řídkých prostředích (mračna, ISM)
✓ Normální gravitace na astrofyzikálních škálách
""")

print("="*100)
