# Mohla by sluneční neutrina kompenzovat G_eff = 0.9 konflikt?

**Datum:** 2025-11-19
**Otázka:** Pokud G_eff závisí na hustotě neutrin, mohla by vyšší koncentrace slunečních neutrin ve sluneční soustavě kompenzovat G_eff ~ 0.9 G_N a dostat nás zpět na G_eff ≈ G_N?

---

## 🔢 KVANTITATIVNÍ ANALÝZA

### Cosmic Neutrino Background (CνB)

**Celý vesmír:**
```
Hustota:     n_CνB = 336 cm^-3 (všechny flavory)
             = 112 cm^-3 per flavor (ν_e, ν_μ, ν_τ)
Teplota:     T_CνB = 1.95 K ≈ 1.7×10^-4 eV
Rychlost:    v ~ c (relativistické do z ~ 1)
Původ:       Big Bang (freeze-out při T ~ 1 MeV)
```

### Solar Neutrinos (Sluneční neutrina)

**Ve sluneční soustavě:**
```
Flux na Zemi:  Φ_☉ = 6.5×10^10 cm^-2 s^-1 (celkem všechny reakce)
               Složení:
               - pp chain:    ~6×10^10 (E < 0.42 MeV)
               - pep:         ~1.4×10^8 (E = 1.44 MeV)
               - 7Be:         ~5×10^9 (E = 0.86 MeV)
               - 8B:          ~5×10^6 (E až 15 MeV)
               - hep:         ~8×10^3 (E až 18 MeV)

Rychlost:      v ≈ c (neutrinos are ultrarelativistic)

Efektivní hustota:
n_solar = Φ_☉ / c
        = 6.5×10^10 cm^-2 s^-1 / (3×10^10 cm s^-1)
        ≈ 2.2 cm^-3
```

### Poměr Solar / Cosmic

```
n_solar / n_CνB = 2.2 / 336 ≈ 0.0065 ≈ 0.65%

→ Sluneční neutrina tvoří pouze ~0.65% celkové hustoty!
```

---

## 💡 FYZIKÁLNÍ ZÁVĚR

### Odpověď: **NE, nemohou kompenzovat**

**Důvody:**

1. **Sluneční neutrina jsou ZANEDBATELNÁ:**
   - Contribution: 0.65% z CνB hustoty
   - Pokud G_eff ∝ n_ν: efekt slunečních ν je ~0.65% × (nějaký faktor)
   - To je **řádově 10^-2**, ne korekce na úrovni 10%!

2. **Efekt klesá s vzdáleností:**
   - Flux Φ_☉ ∝ 1/r² (od Slunce)
   - Na Zemi (1 AU): n_solar ~ 2 cm^-3
   - Na Marsu (1.5 AU): n_solar ~ 0.9 cm^-3
   - U Neptuna (30 AU): n_solar ~ 0.002 cm^-3 (zanedbatelné!)

   → Kompenzace by nefungovala na vnějších planetách

3. **Energy scale mismatch:**
   - CνB: E_typ ~ 10^-4 eV (thermal)
   - Solar ν: E_typ ~ 0.5 MeV (pp chain)
   - Rozdíl: 10^6 faktor v energii!

   Pokud QCT závisí na E_ν:
   - High-E solar ν by mohla přispívat více per particle
   - Ale hustota je stále 150× menší
   - Celkový efekt: √(10^6) × 0.0065 ~ 6.5 (kdyby E^(1/2) scaling)

   **To by mohlo být zajímavé!** Ale potřebujeme znát scaling.

---

## 🔍 DETAILNĚJŠÍ ANALÝZA: QCT DEPENDENCE NA n_ν a E_ν

### QCT Framework Recap

```python
G_eff ∝ ρ_eff = n_ν × E_pair

Kde:
- n_ν: neutrino number density
- E_pair: pairing energy (depends on E_ν?)
```

**Klíčová otázka:** Jak E_pair závisí na energii neutrin?

### Scénář A: E_pair nezávisí na E_ν (jen na počtu neutrin)

```
G_eff ∝ n_total = n_CνB + n_solar
                = 336 + 2.2
                = 338.2 cm^-3

Relative change: (338.2 - 336) / 336 = 0.65%

→ ZANEDBATELNÝ efekt (10^-2 level)
```

### Scénář B: E_pair ∝ E_ν (pairing energy scales with neutrino energy)

```
G_eff ∝ Σ_i (n_i × E_i)

CνB contribution:
ρ_CνB = n_CνB × E_CνB
      = 336 cm^-3 × 1.7×10^-4 eV
      ≈ 0.057 eV/cm³

Solar contribution (pp chain dominance):
ρ_solar = n_solar × E_solar
        = 2.2 cm^-3 × 0.5 MeV
        = 2.2 cm^-3 × 5×10^5 eV
        ≈ 1.1×10^6 eV/cm³

Ratio:
ρ_solar / ρ_CνB = 1.1×10^6 / 0.057 ≈ 2×10^7

→ Solar neutrinos DOMINATE energy density by 10^7 factor!!!
```

**ALE POZOR:** Toto předpokládá že high-energy neutrina párují stejně jako thermal CνB.

### Scénář C: Pairing vyžaduje thermal equilibrium (realistický)

**BCS pairing typicky vyžaduje:**
- Fermi surface (degenerate gas)
- Low temperature (T << E_Fermi)
- Coherence over long distances

**Solar neutrinos:**
- Nejsou v thermal equilibriu (beam z reactoru)
- High energy (MeV vs μeV thermal)
- Nízká hustota
- Krátký interaction time (prolétnou během ~500 s)

**→ Solar neutrinos NEPÁRUJÍ!**

Condensate vzniká z thermal CνB (T ~ 2 K), ne z hot solar neutrinos.

**Analogie:**
```
Jako když:
- Thermal phonons v krystalu → superconductivity ✓
- High-energy gamma rays → superconductivity ✗

Solar ν jsou "gamma rays" neutrino světa!
```

---

## 🎯 FINÁLNÍ ZÁVĚR

### **NE, sluneční neutrina NEMOHOU kompenzovat G_eff = 0.9 konflikt**

**Kvantitativní důvody:**

1. **Hustota příspěvek:** 0.65% (zanedbatelný)

2. **Energie příspěvek:** Potenciálně 10^7× větší, **ALE:**
   - High-energy ν nepárují (ne v thermal equilibriu)
   - BCS condensate vyžaduje low-E, thermal ν
   - Solar ν prolétnou rychle (~8 min od Slunce), nezůstávají

3. **Distance scaling:** Φ ∝ 1/r² znamená efekt mizí na vnějších planetách
   - Mercury: n_solar ~ 8 cm^-3
   - Neptune: n_solar ~ 0.002 cm^-3
   - Would predict different G at different planets → **VYLOUČENO daty!**

4. **Directional dependence:** Solar ν přicházejí ze Slunce (anisotropní)
   - Pokud by ovlivňovaly G: gravitace by závisela na směru!
   - To by narušilo izotropii (Birkhoff theorem)
   - **VYLOUČENO observations**

---

## 🔬 ALTERNATIVNÍ MYŠLENKA: Baryon Density Screening

**Lepší kandidát pro kompenzaci:**

Místo solar neutrinos → **baryon density** ve sluneční soustavě!

```
Sluneční vítr:       n_p ~ 10 cm^-3 (u Země)
Interplanetary medium: n_p ~ 5-10 cm^-3
Galactic cosmic rays: n_cosmic ~ 10^-3 cm^-3

vs.

Cosmology:           n_baryon ~ 10^-7 cm^-3 (průměr vesmíru)
```

**Poměr:** Solar system má ~10^8× vyšší baryon density než cosmic average!

### Physical mechanism (z G_EFF_CONFLICT_RESOLUTION.md):

```python
σ²_max(ρ_baryon) = σ²_vac / (1 + (ρ_baryon/ρ_crit)^n)

High ρ_baryon (solar system):
→ σ²_max → 0 (strong screening)
→ G_eff → G_N ✓

Low ρ_baryon (cosmology):
→ σ²_max → 0.2 (weak screening)
→ G_eff → 0.9 G_N ✓
```

**Toto JE navrhované řešení!** (Environment-dependent screening)

---

## 📊 SROVNÁNÍ MECHANISMŮ

| Mechanismus | Hustota ratio | Energy ratio | Pairing capable? | Distance scaling | Verdict |
|-------------|---------------|--------------|------------------|------------------|---------|
| **Solar neutrinos** | 0.0065 (0.65%) | 10^7 | ❌ NO (high-E, beam) | ∝ 1/r² (bad!) | ❌ **NEFUNGUJE** |
| **Baryon density** | 10^8 | N/A | N/A (disrupts coherence) | ∝ ρ_planet (local) | ✅ **FUNGUJE!** |

---

## 🎓 FYZIKÁLNÍ POZNÁMKY

### Proč high-energy neutrina nepárují:

**Cooper pairing (BCS theory) vyžaduje:**
```
1. Particles near Fermi surface: E ≈ E_F ± δE (δE << E_F)
2. Attractive interaction: V < 0
3. Phase coherence: Δφ << 1 over correlation length
```

**Solar neutrinos:**
```
1. E_solar ~ 0.5 MeV >> E_F ~ T_CνB ~ 10^-4 eV
   → Far above Fermi surface! (by factor 10^9)
2. Pass through in ~500 s → No time to establish coherence
3. Anisotropic (beam) → Breaks isotropy needed for s-wave pairing
```

**Analogie z solid-state:**
```
Superconductor:
- Thermal phonons (meV) → pair electrons ✓
- X-ray photons (keV) → scatter electrons, break pairs ✗

QCT condensate:
- Thermal CνB (0.1 meV) → pair neutrinos ✓
- Solar neutrinos (0.5 MeV) → scatter, don't pair ✗
```

---

## ✅ DOPORUČENÍ PRO QCT

**CO FUNGUJE (navrhované řešení):**
- Environment-dependent σ²_max(ρ_baryon)
- Baryon density disrupts neutrino condensate coherence
- High ρ (solar system) → G_eff ≈ G_N ✓
- Low ρ (cosmology) → G_eff ~ 0.9 G_N ✓

**CO NEFUNGUJE:**
- Solar neutrino compensation
- High-energy neutrino contribution to pairing
- Distance-dependent effects from Sun

---

## 📚 REFERENCE PRO DALŠÍ STUDIUM

1. **Solar neutrino spectrum:**
   - Bahcall, J.N. "Solar Neutrinos" (1989)
   - SNO Collaboration, Phys. Rev. C 81, 055504 (2010)

2. **Neutrino pairing in cosmology:**
   - Lesgourgues & Pastor, Phys. Rept. 429, 307 (2006)
   - Ringwald & Wong, JCAP 12, 005 (2004)

3. **Environment-dependent screening:**
   - Khoury & Weltman, Phys. Rev. D 69, 044026 (2004) - Chameleon fields
   - Vainshtein, Phys. Lett. B 39, 393 (1972) - Vainshtein mechanism

---

**Závěr:** Velmi dobrá fyzikální úvaha, ale bohužel čísla to nedovolují. Baryon density screening je správná cesta!
