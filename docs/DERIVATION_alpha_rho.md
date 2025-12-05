# ODVOZENÍ α(ρ) ZÁVISLOSTI Z WEAK INTERACTIONS

**Datum:** 2025-11-06
**Cíl:** Odvodit hustotní závislost coupling konstanty α z neutrino-baryon interakcí

---

## 1. VÝCHOZÍ BOD: MANUSCRIPT ODVOZENÍ

Z manuscriptu (preprint.tex, řádek 336-342):

```
α = -E_pair / (m_ν c²) × 1 / (n_ν V_proj)
  ≈ -9.2 × 10¹¹
```

Kde:
- E_pair = 5.38 × 10¹⁸ eV = vazebná energie páru
- m_ν ≈ 0.1 eV = hmotnost neutrina
- n_ν = 336 cm⁻³ = kosmická hustota neutrin
- V_proj ≈ 72.3 cm³ = projekční objem

**Fyzikální interpretace:**
α popisuje jak silně neutrina "cítí" gravitační potenciál Φ.

---

## 2. PROČ BY α MĚLA ZÁVISET NA ρ_baryon?

### Fyzikální mechanismus:

**A) Neutrino-baryon scattering**

Neutrina interagují s baryony přes slabou sílu (Z⁰ boson):

```
ν + p/n → ν + p/n  (neutral current)
```

Cross-section:
```
σ_νN ≈ G_F² s / π ≈ 10⁻⁴⁴ cm²  (at E_ν ~ MeV)
```

kde G_F = Fermi konstanta ≈ 1.17 × 10⁻⁵ GeV⁻².

**B) Mean free path**

V médiu s hustotou barionů ρ:

```
λ_mfp = 1 / (n_baryon × σ_νN)
      = m_p / (ρ × σ_νN)
```

Numericky pro Zemi (ρ ≈ 5500 kg/m³):

```
n_baryon = ρ / m_p ≈ 5500 / (1.67×10⁻²⁷) ≈ 3.3 × 10³⁰ m⁻³

λ_mfp ≈ 1 / (3.3×10³⁰ × 10⁻⁴⁸) ≈ 3 × 10¹⁷ m ≈ 30 světelných let!
```

→ Přímá slabá interakce je PŘÍLIŠ SLABÁ!

**C) Kolektivní efekt v kondenzátu**

ALE: Neutrina jsou v KONDENZÁTU (pairované stavy)!

Analogie: Cooperovy páry v supravodiči
- Jednotlivé elektrony: weak coupling
- Cooperovy páry: KOLEKTIVNÍ efekt → silnější coupling

V QCT:
- Jednotlivá neutrina: σ_νN ~ 10⁻⁴⁴ cm²
- Párovaná neutrina: efektivní coupling ~ (enhancement factor) × σ_νN

---

## 3. BCS ENHANCEMENT MECHANISMUS

### V BCS teorii supravodičů:

Energie gap:
```
Δ = 2ℏω_D exp(-1 / [λ N(0)])
```

kde:
- ω_D = Debye frequency
- λ = coupling strength
- N(0) = density of states at Fermi surface

**Klíč:** N(0) ~ ρ (hustota elektronů)

→ Silnější coupling v hustším médiu!

### V QCT analogicky:

Gap (binding energy):
```
E_pair ~ E_0 × f(n_ν, n_baryon)
```

kde f obsahuje hustotní závislost.

**Fyzikální obraz:**
- Více barionů → více "rozptylových center"
- Kondenzát se "přizpůsobuje" → stronger response
- Efektivní α roste s ρ

---

## 4. MEAN-FIELD ODVOZENÍ

### A) Kondenzát v baryonickém médiu

GP rovnice s baryony jako background:

```
iℏ ∂Ψ/∂t = [Ĥ₀ + V_baryon(ρ)] Ψ
```

kde:
```
V_baryon = κ × ρ_baryon
```

### B) Chemický potenciál

V mean-field aproximaci:

```
μ = g × n_ν × m_ν + κ × ρ_baryon
```

Druhý člen je **nový** - interakce s baryony!

### C) Odpověď na gravitační potenciál

Gravitační potenciál Φ ovlivňuje obě komponenty:

1. **Neutrina přímo:**
   ```
   δμ_ν = m_ν × Φ/c²
   ```

2. **Přes baryony:**
   ```
   δμ_baryon = κ × δρ_baryon
               = κ × ρ₀ × (Φ/c²)  [hydrostatická rovnováha]
   ```

### D) Celková změna

```
δμ_total = δμ_ν + δμ_baryon
         = m_ν Φ/c² + κ ρ₀ Φ/c²
         = (m_ν + κ ρ₀) × Φ/c²
```

Koncentrace neutrin:

```
δn_ν / n_ν = δμ / (g m_ν)
           = (m_ν + κ ρ₀) × Φ / (g m_ν c²)
```

Definice α:
```
n_ν = n_ν₀ × [1 + α Φ/c²]
```

→
```
α = (m_ν + κ ρ₀) / (g m_ν)
  = 1/g + κ ρ₀ / (g m_ν)
```

**První člen:** α₀ = 1/g (nezávislý na ρ)
**Druhý člen:** α₁ = (κ/g) × (ρ₀/m_ν) (proporcionální ρ!)

---

## 5. EXPLICITNÍ FORMA α(ρ)

```
α(ρ) = α₀ + α₁ × (ρ / ρ_ref)
     = α₀ × [1 + β × (ρ / ρ_ref)]
```

kde β = α₁ / α₀.

**Pro β >> 1:** (silná baryon-neutrino coupling)
```
α(ρ) ≈ α₁ × (ρ / ρ_ref)
     = (α_⊕) × (ρ / ρ_⊕)
```

→ **Lineární škálování!**

---

## 6. FENOMENOLOGICKÝ FIT

Z Eöt-Wash (Země, ρ_⊕ = 5515 kg/m³):
```
α_⊕ = -9 × 10¹¹
```

Pro jinou hustotu ρ:
```
α(ρ) = α_⊕ × (ρ / ρ_⊕)^β
```

### Test β = 1 (lineární):

**Země:**
```
ρ = 5515 kg/m³
α = -9 × 10¹¹
K = 1 + α Φ_⊕/c² ≈ 625 ✓
λ_screen ≈ 40 μm ✓
```

**Molekulární mračno:**
```
ρ = 10⁻¹⁸ kg/m³
α = -9 × 10¹¹ × (10⁻¹⁸ / 5515)
  = -9 × 10¹¹ × 1.8 × 10⁻²²
  ≈ -1.6 × 10⁻¹⁰

Φ_cloud ~ -4 × 10⁴ m²/s²
K = 1 + (-1.6×10⁻¹⁰) × (-4×10⁴) / (3×10⁸)²
  = 1 + 7×10⁻⁷
  ≈ 1.0 ✓ FYZIKÁLNÍ!
```

---

## 7. ALTERNATIVNÍ EXPONENTY

### Možnost A: β = 1/2 (difúzní limit)

V některých kolektivních systémech:
```
Response ~ √(density of scatterers)
```

Příklad: Difúze v médiu, thermal conductivity

### Možnost B: β = 2/3 (percolation)

Pokud je baryon distribuce nehomogenní:
```
Effective coupling ~ (volume fraction)^(2/3)
```

### Možnost C: β = 2 (two-body correlations)

Pokud dominují two-body interakce:
```
Energy ~ n²  (collision rate ~ n²)
```

---

## 8. TEORETICKÉ ARGUMENTY PRO β = 1

### Argument 1: Mean-field theory

V mean-field aproximaci (platí pro kondenzáty!):
```
Interakční energie ~ n × U
U ~ ρ_baryon  (external potential)
→ E_int ~ n × ρ → lineární!
```

### Argument 2: Random Phase Approximation (RPA)

V RPA (standardní v many-body physics):
```
Screening ~ linear response χ(q,ω)
χ ~ density of states ~ ρ
```

### Argument 3: Weak coupling režim

Pro slabé neutrino-baryon coupling (G_F malý!):
```
Perturbation theory → linear response v ρ
```

---

## 9. KOREKCE VYŠŠÍCH ŘÁDŮ

Přesněji (včetně nelineárních efektů):

```
α(ρ) = α₀ × [1 + c₁(ρ/ρ₀) + c₂(ρ/ρ₀)² + ...]
```

Pro Zemi (ρ/ρ_ref ~ 1):
```
α_⊕ = α₀ × [1 + c₁ + c₂ + ...]
```

Pro mračno (ρ/ρ_ref ~ 10⁻²²):
```
α_cloud ≈ α₀ × c₁ × (10⁻²²)
```

Pokud c₂, c₃, ... << c₁ → aproximace β = 1 je dobrá!

---

## 10. ZÁVISLOST NA TEPLOTĚ?

V principu by měla být i teplotní závislost:

```
α(ρ, T) = α₀(T) × f(ρ/ρ₀, T/T₀)
```

**Pro T << T_⊕** (kosmické prostředí, T ~ 2.7 K):
- Termální fluktuace zanedbatelné
- α(ρ, T→0) → α(ρ)

**Pro T >> T_⊕** (hvězdy):
- Termální excitace narušují páry
- Slabší coupling? (podobně jako supravodič nad T_c)

→ **Otevřená otázka!**

---

## 11. EXPERIMENTÁLNÍ TEST

Jak určit β?

### Experiment 1: Eöt-Wash v různých materiálech

Měřit λ_screen pro:
- Olovo (ρ = 11340 kg/m³)
- Železo (ρ = 7874 kg/m³)
- Voda (ρ = 1000 kg/m³)
- Aerogel (ρ = 100 kg/m³)

Fitovat:
```
λ_screen ~ ρ^(-β/2)  (protože λ ~ 1/√K ~ 1/√α ~ ρ^(-β/2))
```

### Experiment 2: ISS vs. Země

ISS orbit: efektivní ρ menší (mikrogravitace)
→ Měřit změnu λ_screen

### Experiment 3: Deep space probe

Pioneer anomaly, Voyager:
→ Test G_eff v nízkodenzitním prostředí

---

## 12. KONEČNÁ FORMA

Doporučená forma pro manuscript:

```
α(ρ) = α₀ × (ρ / ρ_⊕)^β
```

kde:
- **α₀ = -9 × 10¹¹** (calibrated from Eöt-Wash on Earth)
- **ρ_⊕ = 5515 kg/m³** (mean density of Earth)
- **β = 1** (mean-field prediction, TBD experimentally)

**Fyzikální interpretace:**
- α popisuje efektivní coupling mezi neutriny a gravitačním polem
- Coupling je zprostředkován baryonickou hmotou
- V hustším médiu: více "scattering centers" → silnější coupling

---

## 13. DŮSLEDKY PRO QCT

### Pro hustá prostředí (Země, hvězdy):

```
ρ >> ρ_⊕ → α velké → K >> 1
→ Silná koncentrace neutrin
→ Krátká λ_screen
→ Silný screening na sub-mm škálách
```

### Pro řídká prostředí (mračna, vakuum):

```
ρ << ρ_⊕ → α malé → K ≈ 1
→ Žádná koncentrace neutrin
→ Dlouhá λ_screen ≈ λ_cosmic = 1 mm
→ Slabý/žádný screening
```

**Vyřešený problém:**
- Původní α = konstanta → K < 1 v mračnech ❌
- Nový α(ρ) → K ≈ 1 v mračnech ✓

---

## 14. OTEVŘENÉ OTÁZKY

1. **Přesná hodnota β:**
   - Odvození dává β = 1
   - Ale vyšší řády? Nelineární efekty?
   - Experimentální test nutný!

2. **Teplotní závislost:**
   - Jak se α(ρ,T) chová ve hvězdách?
   - Existuje "kritická teplota" (analogie T_c)?

3. **Flavor dependence:**
   - Manuscript má LFUV (lepton flavor universality violation)
   - Závisí α na flavor (e, μ, τ)?

4. **Časová evoluce:**
   - α(ρ(z), z) v kosmologické evoluci?
   - Ovlivňuje BBN, CMB?

5. **Kvantové korekce:**
   - Loop corrections k α?
   - Renormalizace?

---

## 15. ZÁVĚR

✅ **ODVOZENO Z TEORIE:**
```
α(ρ) = α₀ × (ρ/ρ_⊕)^β
```

✅ **FYZIKÁLNÍ MECHANISMUS:**
- Mean-field coupling kondenzátu s baryonickou hmotou
- Lineární response (β = 1) z perturbation theory

✅ **FENOMENOLOGICKÁ PODPORA:**
- Fituje Eöt-Wash data ✓
- Řeší K < 1 problém ✓
- Predikuje slabý screening v mračnech ✓

✅ **TESTOVATELNÉ:**
- Různé materiály v Eöt-Wash
- ISS experiment
- Deep space probes

❓ **VYŽADUJE EXPERIMENTÁLNÍ VERIFIKACI:**
- β = 1 je teoretický prediction
- Přesné měření nutné!

---

**DOPORUČENÍ PRO MANUSCRIPT:**

Přidat diskusi α(ρ) jako "možný mechanismus" (ne definitivní!):

```latex
\paragraph{Density-dependent coupling (speculative).}
The microscopic derivation (Eq. X) gives α as a constant.
However, mean-field theory suggests possible density dependence:
  α_eff(ρ) ≈ α₀ (ρ/ρ_⊕)^β
with β ≈ 1 from linear response theory.

This would resolve the K < 1 problem in dilute environments
and predict environment-dependent screening lengths.

Experimental test: measure λ_screen in different materials.
```

**NE jako definitivní fact, ale jako theoretical possibility!**
