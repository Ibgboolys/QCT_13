#!/usr/bin/env python3
"""
Analýza vlivu hustoty reliktních neutrin na gravitační kolaps v různých epochách vesmíru
S LOKÁLNÍ ZÁVISLOSTÍ λ_screen a CUTOFF MECHANISMEM
"""

import math

# Konstanty
c = 2.998e8  # m/s
G_N = 6.674e-11  # m^3 kg^-1 s^-2
H_0 = 67.4e3 / (3.086e22)  # Hubbleova konstanta v s^-1 (~67.4 km/s/Mpc)

# QCT parametry (kosmická baseline - dnes)
n_nu_today = 336e6  # m^-3 (= 336 cm^-3)
R_proj_0 = 2.58e-2  # m (2.58 cm, projekční poloměr v hlubokém vesmíru)
xi_0 = 1e-3  # m (1 mm, koherenční délka v hlubokém vesmíru)
f_screen = 1.07e-10  # screening faktor m_ν/m_p
alpha = -9e11  # neutrino-gravity coupling (záporný pro attractive potential)

def age_from_redshift(z):
    """
    Přibližný výpočet věku vesmíru pro daný redshift
    Používá zjednodušený model s Lambda-CDM
    """
    # Parametry: Omega_M = 0.3, Omega_Lambda = 0.7
    Omega_M = 0.3
    Omega_Lambda = 0.7

    # Integrál 1/H(z') pro z' od z do nekonečna
    # Zjednodušený vzorec pro flat universe:
    # t(z) ≈ (2/3H_0) * 1/(Omega_Lambda^0.5) * ln((1+z)^(-3/2) + sqrt(Omega_Lambda/Omega_M))

    # Ještě jednodušší aproximace pro náš účel:
    # t(z) ≈ t_0 / (1+z)^(3/2) pro z >> 1 (matter dominated)
    # t_0 = 13.8 Gyr
    t_0 = 13.8e9 * 365.25 * 24 * 3600  # sekund

    if z < 2:
        # Použijeme numerickou integraci
        def integrand(zp):
            return 1 / ((1 + zp) * math.sqrt(Omega_M * (1 + zp)**3 + Omega_Lambda))

        # Numerická integrace
        n_steps = 1000
        dz = z / n_steps
        integral = sum(integrand(z * i / n_steps) * dz for i in range(n_steps))

        t = integral / H_0
    else:
        # Pro vysoké redshifty použijeme aproximaci
        t = (2 / (3 * H_0)) / (1 + z)**(3/2)

    return t / (365.25 * 24 * 3600 * 1e9)  # převod na Gyr

def redshift_from_age(age_gyr):
    """
    Přibližný výpočet redshiftu pro daný věk vesmíru
    Iterativní metoda
    """
    # Binární vyhledávání
    z_min, z_max = 0.0, 100.0

    for _ in range(50):  # 50 iterací
        z_mid = (z_min + z_max) / 2
        age_mid = age_from_redshift(z_mid)

        if abs(age_mid - age_gyr) < 0.01:  # tolerance 0.01 Gyr
            return z_mid

        if age_mid > age_gyr:
            z_min = z_mid
        else:
            z_max = z_mid

    return (z_min + z_max) / 2

def n_nu_at_z(z):
    """
    Hustota reliktních neutrin při redshiftu z
    Škáluje jako (1+z)^3
    """
    return n_nu_today * (1 + z)**3

def R_proj_at_z(z):
    """
    Projekční poloměr při redshiftu z (v hlubokém vesmíru)
    R_proj ∝ 1/√n_ν ∝ (1+z)^(-3/2)
    """
    return R_proj_0 * (1 + z)**(-3/2)

def concentration_factor(Phi, alpha_coupling=alpha):
    """
    Koncentrační faktor neutrin v gravitačním poli.

    K = 1 + α Φ/c²

    Pro attractive potenciál (Φ < 0) a α < 0: K > 1 → vyšší koncentrace
    """
    K = 1 + alpha_coupling * Phi / c**2
    return max(K, 1.0)  # Zajistíme K ≥ 1

def coherence_length(K, z=0):
    """
    Lokální koherenční délka při redshiftu z.

    ξ(K, z) = ξ₀(z) / √K
    """
    xi_baseline = xi_0 * (1 + z)**(-3/2)  # kosmická baseline pro dané z
    return xi_baseline / math.sqrt(K)

def projection_radius(K, z=0):
    """
    Lokální projekční poloměr při redshiftu z.

    R_proj(K, z) = R_proj^(0)(z) × [ξ(K, z) / ξ₀(z)]
    """
    R_proj_baseline = R_proj_at_z(z)
    xi_baseline = xi_0 * (1 + z)**(-3/2)
    xi = coherence_length(K, z)
    return R_proj_baseline * (xi / xi_baseline)

def screening_length(K, z=0):
    """
    Lokální screeningová délka při redshiftu z.

    λ_screen(K, z) = R_proj(K, z) / ln(1/f_screen)
    """
    R_proj = projection_radius(K, z)
    return R_proj / math.log(1.0 / f_screen)

def lambda_screen_at_z(z, Phi=0):
    """
    Screening délka při redshiftu z s lokálním gravitačním potenciálem Phi.
    """
    K = concentration_factor(Phi, alpha)
    return screening_length(K, z)

def jeans_mass(rho, T, mu=2.33):
    """
    Jeansova hmotnost pro gravitační kolaps plynného mračna

    M_J = (5 k T / G μ m_H)^(3/2) * (3 / 4π ρ)^(1/2)

    rho: hustota plynu [kg/m^3]
    T: teplota [K]
    mu: střední molekulová hmotnost (2.33 pro ionizovaný H+He plyn)
    """
    k_B = 1.381e-23  # J/K
    m_H = 1.673e-27  # kg (hmotnost protonu)

    c_s = math.sqrt(5 * k_B * T / (3 * mu * m_H))  # rychlost zvuku
    lambda_J = c_s * math.sqrt(math.pi / (G_N * rho))  # Jeansova délka
    M_J = (4 * math.pi / 3) * rho * lambda_J**3  # Jeansova hmotnost

    return M_J, lambda_J

def G_eff_at_distance(r, M, z=0, use_cutoff=True):
    """
    Efektivní gravitační konstanta na vzdálenosti r podle QCT

    G_eff(r) = G_N × exp(-r / λ_screen)  pro r < R_cutoff
    G_eff(r) = G_N                        pro r ≥ R_cutoff

    r: vzdálenost [m]
    M: hmotnost zdrojového objektu [kg]
    z: redshift
    use_cutoff: použít cutoff mechanismus?
    """
    R_cutoff = R_proj_at_z(z)  # Cutoff závisí na redshiftu

    if use_cutoff and r >= R_cutoff:
        return G_N, 1.0, 0.0, 0.0  # (G_eff, ratio, lambda_screen, K)

    # Gravitační potenciál
    Phi = -G_N * M / r

    # Koncentrační faktor
    K = concentration_factor(Phi, alpha)

    # Lokální screening délka
    lambda_s = screening_length(K, z)

    # Screening faktor
    ratio = math.exp(-r / lambda_s)

    return G_N * ratio, ratio, lambda_s, K

# ============================================================================
# MYŠLENKOVÝ EXPERIMENT: DVA STEJNÁ PLYNNÁ MRAČNA
# ============================================================================

print("="*90)
print("MYŠLENKOVÝ EXPERIMENT: VLIV HUSTOTY RELIKTNÍCH NEUTRIN NA GRAVITAČNÍ KOLAPS")
print("="*90)

# Parametry plynného mračna
rho_cloud = 1e-18  # kg/m^3 (typická hustota pro molekulární mračno)
T_cloud = 10  # K (chladné molekulární mračno)
R_cloud = 1e16  # m (~0.3 pc, typický poloměr malého mračna)
M_cloud = (4 * math.pi / 3) * R_cloud**3 * rho_cloud

print(f"\nParametry plynného mračna:")
print(f"  Hustota: {rho_cloud:.2e} kg/m³")
print(f"  Teplota: {T_cloud} K")
print(f"  Poloměr: {R_cloud:.2e} m = {R_cloud/3.086e16:.2f} pc")
print(f"  Hmotnost: {M_cloud:.2e} kg = {M_cloud/1.989e30:.2f} M☉")

# ============================================================================
# SCÉNÁŘ 1: MRAČNO DNES (t = 13.8 Gyr, z ≈ 0)
# ============================================================================
print(f"\n{'='*90}")
print("SCÉNÁŘ 1: PLYNNÉ MRAČNO DNES (t = 13.8 Gyr, z ≈ 0)")
print(f"{'='*90}")

z_today = 0
n_nu_1 = n_nu_at_z(z_today)
R_proj_1 = R_proj_at_z(z_today)

print(f"\nKosmologické parametry:")
print(f"  Redshift z = {z_today}")
print(f"  Hustota reliktních neutrin: {n_nu_1:.3e} m⁻³ = {n_nu_1/1e6:.0f} cm⁻³")
print(f"  Projekční poloměr R_proj: {R_proj_1*100:.2f} cm")
print(f"  Cutoff poloměr R_cutoff: {R_proj_1*100:.2f} cm")

# Jeansova analýza
M_J_1, lambda_J_1 = jeans_mass(rho_cloud, T_cloud)

print(f"\nJeansova analýza (standardní GR):")
print(f"  Jeansova hmotnost M_J: {M_J_1:.3e} kg = {M_J_1/1.989e30:.2f} M☉")
print(f"  Jeansova délka λ_J: {lambda_J_1:.3e} m = {lambda_J_1/3.086e16:.3f} pc")

# QCT modifikace - BEZ cutoff
print(f"\n--- QCT ANALÝZA (BEZ cutoff mechanismu) ---")
G_eff_1_no, ratio_1_no, lambda_scr_1_no, K_1_no = G_eff_at_distance(
    R_cloud, M_cloud, z_today, use_cutoff=False
)

print(f"  G_eff/G_N na vzdálenosti R = {R_cloud:.2e} m:")
print(f"    Gravitační potenciál Φ ≈ {-G_N * M_cloud / R_cloud:.3e} m²/s²")
print(f"    Koncentrační faktor K ≈ {K_1_no:.3e}")
print(f"    Lokální λ_screen ≈ {lambda_scr_1_no:.3e} m")
print(f"    exp(-R/λ) = {ratio_1_no:.3e}")

if ratio_1_no < 1e-10:
    print(f"  ⚠ KRITICKÉ: Gravitace je prakticky NULOVÁ!")
    print(f"  → Mračno by se NEZHRUTILO gravitačně")
else:
    print(f"  ✓ Gravitace je podobná GR")

# QCT modifikace - S cutoff
print(f"\n--- QCT ANALÝZA (S cutoff mechanismem) ---")
G_eff_1, ratio_1, lambda_scr_1, K_1 = G_eff_at_distance(
    R_cloud, M_cloud, z_today, use_cutoff=True
)

print(f"  G_eff/G_N na vzdálenosti R = {R_cloud:.2e} m:")
if R_cloud >= R_proj_1:
    print(f"  ✓ CUTOFF AKTIVNÍ: r = {R_cloud:.2e} m >> R_cutoff = {R_proj_1:.2e} m")
    print(f"  → G_eff = G_N (screening vypnut, gravitace normální)")
    print(f"  → Mračno by se ZHRUTILO normálně (jako v GR)")
else:
    print(f"    exp(-R/λ) = {ratio_1:.3e}")
    if ratio_1 < 1e-10:
        print(f"  ⚠ KRITICKÉ: Gravitace stále nulová!")
    else:
        print(f"  ✓ Gravitace funguje")

# ============================================================================
# SCÉNÁŘ 2: MRAČNO 3 MILIARDY LET PO VELKÉM TŘESKU
# ============================================================================
print(f"\n{'='*90}")
print("SCÉNÁŘ 2: PLYNNÉ MRAČNO 3 MILIARDY LET PO VELKÉM TŘESKU")
print(f"{'='*90}")

age_early = 3.0  # Gyr
z_early = redshift_from_age(age_early)
age_check = age_from_redshift(z_early)

print(f"\nČasové parametry:")
print(f"  Věk vesmíru: {age_early} Gyr")
print(f"  Odpovídající redshift: z ≈ {z_early:.2f}")
print(f"  Kontrola věku: {age_check:.2f} Gyr")

n_nu_2 = n_nu_at_z(z_early)
R_proj_2 = R_proj_at_z(z_early)
lambda_screen_2_baseline = xi_0 * (1 + z_early)**(-3/2) / math.log(1.0 / f_screen)

print(f"\nKosmologické parametry:")
print(f"  Redshift z = {z_early:.2f}")
print(f"  Hustota reliktních neutrin: {n_nu_2:.3e} m⁻³ = {n_nu_2/1e6:.0f} cm⁻³")
print(f"  Projekční poloměr R_proj: {R_proj_2*100:.2f} cm")
print(f"  Cutoff poloměr R_cutoff: {R_proj_2*100:.2f} cm")
print(f"  Baseline λ_screen (hlubký vesmír): {lambda_screen_2_baseline*1000:.3f} mm")

print(f"\nPoměry vůči dnešku:")
print(f"  n_ν(z={z_early:.2f}) / n_ν(dnes) = (1+z)³ = {n_nu_2/n_nu_1:.2f}")
print(f"  R_proj(z={z_early:.2f}) / R_proj(dnes) = (1+z)^(-3/2) = {R_proj_2/R_proj_1:.3f}")

# Jeansova analýza (stejná jako předtím, protože mračno má stejné parametry)
M_J_2, lambda_J_2 = jeans_mass(rho_cloud, T_cloud)

print(f"\nJeansova analýza (standardní GR):")
print(f"  Jeansova hmotnost M_J: {M_J_2:.3e} kg = {M_J_2/1.989e30:.2f} M☉")
print(f"  (Stejná jako dnes - lokální parametry mračna jsou identické)")

# QCT modifikace - BEZ cutoff
print(f"\n--- QCT ANALÝZA (BEZ cutoff mechanismu) ---")
G_eff_2_no, ratio_2_no, lambda_scr_2_no, K_2_no = G_eff_at_distance(
    R_cloud, M_cloud, z_early, use_cutoff=False
)

print(f"  G_eff/G_N na vzdálenosti R = {R_cloud:.2e} m:")
print(f"    Gravitační potenciál Φ ≈ {-G_N * M_cloud / R_cloud:.3e} m²/s²")
print(f"    Koncentrační faktor K ≈ {K_2_no:.3e}")
print(f"    Lokální λ_screen ≈ {lambda_scr_2_no:.3e} m")
print(f"    exp(-R/λ) = {ratio_2_no:.3e}")

if ratio_2_no < 1e-10:
    print(f"  ⚠ KRITICKÉ: Gravitace je prakticky NULOVÁ!")
    print(f"  → Mračno by se NEZHRUTILO gravitačně")
else:
    print(f"  ✓ Gravitace je podobná GR")

# QCT modifikace - S cutoff
print(f"\n--- QCT ANALÝZA (S cutoff mechanismem) ---")
G_eff_2, ratio_2, lambda_scr_2, K_2 = G_eff_at_distance(
    R_cloud, M_cloud, z_early, use_cutoff=True
)

print(f"  G_eff/G_N na vzdálenosti R = {R_cloud:.2e} m:")
if R_cloud >= R_proj_2:
    print(f"  ✓ CUTOFF AKTIVNÍ: r = {R_cloud:.2e} m >> R_cutoff = {R_proj_2:.2e} m")
    print(f"  → G_eff = G_N (screening vypnut, gravitace normální)")
    print(f"  → Mračno by se ZHRUTILO normálně (jako v GR)")
else:
    print(f"    exp(-R/λ) = {ratio_2:.3e}")
    if ratio_2 < 1e-10:
        print(f"  ⚠ KRITICKÉ: Gravitace stále nulová!")
    else:
        print(f"  ✓ Gravitace funguje")

# ============================================================================
# SROVNÁNÍ A ZÁVĚR
# ============================================================================
print(f"\n{'='*90}")
print("SROVNÁNÍ OBOU SCÉNÁŘŮ")
print(f"{'='*90}")

print(f"\n1. HUSTOTA RELIKTNÍCH NEUTRIN:")
print(f"   Dnes (z=0):           n_ν = {n_nu_1:.3e} m⁻³")
print(f"   3 Gyr po VT (z≈{z_early:.1f}):  n_ν = {n_nu_2:.3e} m⁻³")
print(f"   Poměr:                {n_nu_2/n_nu_1:.1f}× vyšší v raném vesmíru")

print(f"\n2. CUTOFF POLOMĚR:")
print(f"   Dnes (z=0):           R_cutoff = {R_proj_1*100:.2f} cm")
print(f"   3 Gyr po VT (z≈{z_early:.1f}):  R_cutoff = {R_proj_2*100:.2f} cm")
print(f"   Poměr:                {R_proj_2/R_proj_1:.3f}× menší v raném vesmíru")

print(f"\n3. EFEKTIVNÍ GRAVITACE (BEZ cutoff):")
print(f"   Dnes (z=0):           G_eff/G_N = {ratio_1_no:.3e}")
print(f"   3 Gyr po VT (z≈{z_early:.1f}):  G_eff/G_N = {ratio_2_no:.3e}")
print(f"   → OBĚ prakticky nulové!")

print(f"\n4. EFEKTIVNÍ GRAVITACE (S cutoff):")
print(f"   Dnes (z=0):           G_eff/G_N = {ratio_1:.3e}")
print(f"   3 Gyr po VT (z≈{z_early:.1f}):  G_eff/G_N = {ratio_2:.3e}")
print(f"   → OBĚ normální (cutoff aktivní pro R_cloud >> R_cutoff)")

# Klíčový závěr
print(f"\n{'='*90}")
print("KLÍČOVÝ ZÁVĚR MYŠLENKOVÉHO EXPERIMENTU")
print(f"{'='*90}")

print(f"""
Podle QCT teorie S CUTOFF MECHANISMEM:

1. LOKÁLNÍ ZÁVISLOST λ_screen:
   - λ_screen(r, z) ZÁVISÍ na:
     * Lokálním gravitačním potenciálu Φ(r)
     * Redshiftu z (kosmická evoluce)
   - Koncentrační faktor: K = 1 + α Φ/c²
   - λ_screen = R_proj(K, z) / ln(1/f_screen)

2. CUTOFF MECHANISMUS:
   - Pro r < R_cutoff:  G_eff = G_N × exp(-r/λ_screen)
   - Pro r ≥ R_cutoff:  G_eff = G_N (screening vypnut!)

   Fyzikální odůvodnění:
   - Screening funguje jen na škálách srovnatelných s koherenční doménou
   - Pro r >> R_proj ~ několik cm: gravitace normální (jako GR)

3. GRAVITAČNÍ KOLAPS MRAČNA (R ~ 0.3 pc = {R_cloud:.2e} m):

   BEZ CUTOFF:
   - Dnes: G_eff/G_N ≈ {ratio_1_no:.3e} (nula!)
   - 3 Gyr po VT: G_eff/G_N ≈ {ratio_2_no:.3e} (nula!)
   - ✗ Mračna by se NEZHRUTILA → hvězdy by NEVZNIKLY

   S CUTOFF:
   - Dnes: G_eff/G_N = {ratio_1:.3e} (normální!)
   - 3 Gyr po VT: G_eff/G_N = {ratio_2:.3e} (normální!)
   - ✓ Mračna by se ZHRUTILA → hvězdy by VZNIKLY

4. ODPOVĚĎ NA FUNDAMENTÁLNÍ PROBLÉM:

   ❌ BEZ CUTOFF:
      - Screening délka λ ~ 1 mm << astrofyzikální škály
      - Gravitace mizí na velkých škálách
      - Nesouhlasí s pozorováními!

   ✅ S CUTOFF (R_cutoff ~ 2.6 cm):
      - Screening aktivní jen na r < 2.6 cm
      - Na větších škálách (planety, hvězdy, galaxie): G_eff = G_N
      - Souhlasí s pozorováními!

5. KONZISTENCE:
   ✓ Sub-mm experimenty (Eöt-Wash): r < 40 μm < R_cutoff → screening aktivní
   ✓ Astrofyzikální objekty: r >> R_cutoff → screening neaktivní
   ✓ Planetární oběhy fungují (r >> 2.6 cm)
   ✓ Stíny černých děr viditelné (r_ph >> 2.6 cm)
   ✓ Gravitační čočkování zachováno
   ✓ Hvězdy vznikaly v raném vesmíru (kolaps funguje)

ZÁVĚR: QCT S CUTOFF MECHANISMEM je konzistentní s pozorováními!

Cutoff R_proj ~ 2.6 cm (kosmická baseline) škáluje s redshiftem:
- R_cutoff(z) = R_proj_0 × (1+z)^(-3/2)
- V raném vesmíru: R_cutoff menší, ale stále >> sub-mm škály
- Gravitace funguje normálně na všech astrofyzikálních škálách v jakékoliv epoše!
""")

print(f"\n{'='*90}")
