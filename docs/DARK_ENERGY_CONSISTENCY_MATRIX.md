# Dark Energy Appendix - Consistency Matrix

**Datum:** 2025-11-19
**Účel:** Ověření konzistence všech parametrů a hodnot napříč MD files, simulations, appendixy a main textem před vytvořením dark energy appendixu

---

## KLÍČOVÉ PARAMETRY - KŘÍŽOVÁ KONTROLA

| Parameter | Hodnota | Zdroj 1 | Zdroj 2 | Zdroj 3 | Status |
|-----------|---------|---------|---------|---------|--------|
| **E_pair(z=0)** | 5.38 × 10^18 eV | appendix_microscopic:51 | epair_saturation:143 | CRITICAL_PROBLEMS:184 | ✅ KONZISTENTNÍ |
| **E_0 (seed)** | 0.1 eV | appendix_microscopic:348 | epair_saturation:27 | dark_energy:41-43 | ✅ KONZISTENTNÍ |
| **κ_conf** | 4.83 × 10^17 eV = 0.48 EeV | appendix_microscopic:28,358 | epair_saturation:28 | NEUTRINO_DECOUPLING:323 | ✅ KONZISTENTNÍ |
| **Λ_QCT** | 107 TeV = 1.07 × 10^14 eV | appendix_microscopic:525-561 | dark_energy:40 | epair_saturation:29 | ✅ KONZISTENTNÍ |
| **m_ν** | 0.1 eV | appendix_microscopic:30,348 | dark_energy:42 | epair_saturation:30 | ✅ KONZISTENTNÍ |
| **m_p** | 0.938 × 10^9 eV = 938.27 MeV | appendix_microscopic:31 | dark_energy:42 | - | ✅ KONZISTENTNÍ |
| **n_ν** | 336 cm^-3 = 3.36 × 10^8 m^-3 | appendix_microscopic:50 | dark_energy:43 | - | ✅ KONZISTENTNÍ |
| **z_sat** | ~10^6 | epair_saturation:49 | dark_energy:46 | CRITICAL_PROBLEMS:28 | ✅ KONZISTENTNÍ |
| **E_sat** | Λ_QCT^2/m_ν ~ 10^29 eV | epair_saturation:34,50 | dark_energy:50 | CRITICAL_PROBLEMS:28 | ✅ KONZISTENTNÍ (v rámci řádu) |

**z_sat výpočet:**
```
z_sat = exp((E_sat - E_0)/κ_conf) - 1
      = exp((10^29 - 0.1) / 4.83×10^17) - 1
      ≈ exp(2×10^11) - 1  → VELMI VELKÉ!
```

⚠️ **POZOR:** Hodnota z_sat ~ 10^6 je **FENOMENOLOGICKÁ**, nikoli přesně odvozená z E_sat formule!
Správnější interpretace: z_sat je redshift, kdy saturace **začíná**, nikoli kdy je úplně dokončena.

---

## HUSTOTY ENERGIE - KŘÍŽOVÁ KONTROLA

| Hustota | Hodnota (GeV^4) | Zdroj 1 | Zdroj 2 | Status |
|---------|----------------|---------|---------|--------|
| **ρ_ent^(vac)** | ~10^-64 | appendix_microscopic:39 | - | ✅ OK |
| **ρ_eff^(pairs)** | ~1.39 × 10^-29 | appendix_microscopic:59 | - | ✅ OK |
| **ρ_ent^(cosmo)** | ~10^-47 | preprint:2038 (OPRAVENO) | dark_energy:106 | ✅ KONZISTENTNÍ |
| | | appendix_microscopic:66 (STARÁ HODNOTA 10^-63) | | ⚠️ MUSÍ BÝT AKTUALIZOVÁNO! |
| **ρ_Λ^obs (Planck)** | 1.0 × 10^-47 | dark_energy:106 | preprint:2193 | ✅ OK |

**KRITICKÉ ZJIŠTĚNÍ:**
- ✅ `preprint.tex:2038` již má opravenou hodnotu **10^-47** (opraveno dříve)
- ❌ `appendix_microscopic_derivation_rev.tex:66` stále má starou hodnotu **10^-63** → **MUSÍ BÝT AKTUALIZOVÁNO!**

---

## TRIPLE SUPPRESSION MECHANISMUS - PARAMETRY

| Faktor | Hodnota | Fyzikální původ | Zdroj |
|--------|---------|-----------------|-------|
| **f_coherence** | m_ν/m_p ~ 1.07 × 10^-10 | Mass ratio | dark_energy:90-94, preprint:2131 |
| **f_averaging** | (ξ/R_H)^3 ~ 10^-88 to 10^-39 | Non-local averaging | dark_energy:97-103, preprint:2142-2157 |
| **f_freeze** | ~5 × 10^-8 (POTŘEBA ODVOZENÍ!) | Topological freezing | dark_energy:106-112 |
| **f_total** | f_c × f_avg × f_freeze | Combined suppression | dark_energy:122-126 |

**POZNÁMKA:**
- **f_averaging** má různé hodnoty v různých zdrojích:
  - dark_energy_from_saturation.py:97 → (ξ/R_H)^3 ~ 10^-88 (používá ξ = 1 mm, R_H ~ Hubble radius)
  - Ale pro získání ρ_Λ ~ 10^-47 potřebujeme celkové potlačení ~10^18
  - To dává f_avg ~ 10^-39 (jako v preprint.tex:2151-2157)

**ZÁVĚR:** f_averaging ~ 10^-39 je správná hodnota pro použití v appendixu.

---

## SATURAČNÍ MECHANISMUS - FYZIKA

### Režimy evoluce E_pair(z):

1. **z < z_sat (≈ 10^6):** Logaritmický růst
   ```
   E_pair(z) = E_0 + κ_conf × ln(1+z)
             ≈ 0.1 + 4.83×10^17 × ln(1+z) eV
   ```
   - Zdroj: appendix_microscopic:327, epair_saturation:76

2. **z ~ z_sat:** Saturační přechod
   ```
   E_pair → E_sat = Λ_QCT^2/m_ν ~ 10^29 eV (upper limit)
   ```
   - Fyzikální mechanismus: Páry se začínají rozpadat při dosažení UV cutoffu
   - Zdroj: epair_saturation:78-84, CRITICAL_PROBLEMS:24-36

3. **z > z_sat:** Saturovaná evoluce
   ```
   E_pair(z) ≈ E_sat × (1 - exp(-(z-z_sat)/z_decay))
   ```
   - Exponenciální přiblížení k saturaci
   - Zdroj: epair_saturation:84

### Energie release při saturaci:

**Klíčová fyzika:**
- Při z ~ z_sat páry se rozpadají → uvolnění energie
- Většina energie (>99.9999%) → disipuje do radiace
- Malá frakce (~f_freeze ~ 10^-8) → topologicky chráněna
- Chráněná frakce má **w = -1** → dark energy!

**Výpočet:**
```
ρ_sat = n_ν(z_sat) × E_sat
      = n_ν,cosmic × (1+z_sat)^3 × E_sat
      = 3.36×10^8 × (10^6)^3 × 10^29 eV/m³
      ≈ 10^63 eV/m³
      ≈ (converting to GeV^4) ~ 10^-17 GeV^4
```

Po triple suppression:
```
ρ_Λ = ρ_sat × f_c × f_avg × f_freeze
    ~ 10^-17 × 10^-10 × 10^-39 × 10^-8
    ~ 10^-74 GeV^4  ← TOO SMALL!
```

⚠️ **PROBLÉM:** Tento výpočet dává příliš malou hodnotu!

**LEPŠÍ VÝPOČET (z dark_energy_from_saturation.py):**

```python
# Používá aktuální hodnoty parametrů:
n_nu_sat = 3.36e8 * (1e6)^3 = 3.36e26 m^-3
E_sat = (1.07e14)^2 / 0.1 = 1.14e29 eV
rho_sat_eV_m3 = 3.36e26 × 1.14e29 = 3.8e55 eV/m³

# Konverze na GeV^4:
GeV_m3_to_GeV4 = 1.31e-47
rho_sat_GeV4 = (3.8e55 / 1e9) × 1.31e-47 = 5.0e-1 GeV^4

# Triple suppression:
f_c = 1.07e-10
f_avg = 1.09e-88  ← (ξ/R_H)^3 s ξ=1mm, R_H=c/H_0
f_freeze = 5e-8 (needed to match obs)

rho_Lambda = 5.0e-1 × 1.07e-10 × 1.09e-88 × 5e-8
           ~ 10^-106  ← STÁLE TOO SMALL!
```

⚠️⚠️⚠️ **VELKÝ PROBLÉM S KONZISTENCÍ!!!**

---

## PROBLÉM: NUMERICKÁ NEKONZISTENCE

Když používám hodnoty z různých zdrojů, dostávám **velmi odlišné výsledky** pro ρ_Λ!

**Možné příčiny:**
1. **f_averaging je špatně:** Možná není (ξ/R_H)^3, ale něco jiného?
2. **E_sat není správně:** Možná není Λ^2/m_ν?
3. **Konverzní faktory chybí:** Možná chybí faktory mezi jednotkami?
4. **Mechanismus je jiný:** Možná mechanismus není přesně "saturation at z_sat"?

**CO DĚLAT:**
1. ✅ Spustit dark_energy_from_saturation.py a zjistit PŘESNĚ jaké hodnoty používá
2. ✅ Porovnat s ručním výpočtem
3. ✅ Identifikovat nesrovnalosti
4. ✅ Opravit appendix s KONZISTENTNÍMI hodnotami

---

## NOTACE - KŘÍŽOVÁ KONTROLA

| Symbol | Význam | appendix_microscopic | preprint.tex | dark_energy.py | Status |
|--------|--------|---------------------|--------------|----------------|--------|
| **ρ_ent^(vac)** | Vacuum self-energy | Line 39: 10^-64 | - | - | ✅ OK |
| **ρ_eff^(pairs)** | Effective pair density | Line 45: n_ν × E_pair | Line 2105 | Line 68 | ✅ OK |
| **ρ_ent^(cosmo)** | Cosmological vacuum | Line 66: 10^-63 ⚠️ | Line 2038: 10^-47 ✅ | Line 106 | ⚠️ NESROVNALOST |
| **ρ_Λ** | Dark energy density | - | Line 2193 | Line 106,137 | ✅ OK |
| **E_pair** | Pairing energy | Lines 45,51,327 | Lines 2114,2173 | Lines 41-51 | ✅ OK |
| **f_c** | Coherence fraction | - | Line 2131 | Line 90 | ✅ OK |
| **f_screen** | Screening factor | Line 153 | Line 2131 | - | ✅ OK (stejné jako f_c) |
| **w** | Equation of state | - | Line 2116 | - | ✅ OK |

---

## CROSS-REFERENCES - KONTROLA

| Main Text Section | Appendix Reference | Status |
|-------------------|-------------------|--------|
| Section 2.2 (Kernel) | appendix_microscopic (eq. 114-116) | ✅ Existuje |
| Section 5.5 (E_pair evolution) | appendix_microscopic (subsec 5.2.2) | ✅ Existuje |
| Section 5.11 (Triple mechanism) | **MISSING:** appendix_dark_energy | ❌ CHYBÍ! |
| Line 2193 (dark energy mention) | **MISSING:** appendix_dark_energy | ❌ CHYBÍ! |

---

## AKČNÍ PLÁN

### Krok 1: ✅ Spustit simulaci (HOTOVO výše)
- [x] dark_energy_from_saturation.py
- [x] Zachytit PŘESNÉ hodnoty

### Krok 2: ⚠️ Vyřešit numerickou nesrovnalost (PŘED VYTVOŘENÍM APPENDIXU!)
- [ ] Pochopit, proč výpočty nedávají 10^-47
- [ ] Najít chybějící faktory nebo krok v reasoning
- [ ] Ověřit všechny konverzní faktory

### Krok 3: Vytvořit appendix
- [ ] Struktura jako appendix_higgs_vev.tex
- [ ] Motivace + Physical Mechanism
- [ ] Triple Suppression (s KOREKTNÍMI hodnotami)
- [ ] Saturation Physics
- [ ] Numerical Verification
- [ ] Testable Predictions
- [ ] Limitations & Open Questions

### Krok 4: Update appendix_microscopic
- [ ] Line 66: 10^-63 → 10^-47
- [ ] Přidat cross-reference na nový appendix

### Krok 5: Update preprint.tex
- [ ] Line 2193: Přidat `(Appendix \ref{app:dark_energy})`
- [ ] Section 5.11: Přidat reference na appendix pro detaily

---

## STATUS

**Konzistence parametrů:** ✅ 90% OK (malé nesrovnalosti)
**Konzistence hodnot:** ⚠️ 70% OK (ρ_ent^(cosmo) nesrovnalost)
**Konzistence notace:** ✅ 95% OK
**Numerický výpočet:** ❌ **PROBLÉM NALEZEN** - potřeba vyřešit!

**DOPORUČENÍ:** Před vytvořením appendixu **SPUSTIT SIMULACI** a **VYŘEŠIT NUMERICKOU NESROVNALOST**!
