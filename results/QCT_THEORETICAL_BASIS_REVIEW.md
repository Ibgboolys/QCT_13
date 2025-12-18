# REVIZE TEORETICKÝCH ZÁKLADŮ QCT PREDIKCÍ

## Analýza: Odkud pocházejí očekávané hodnoty?

### 1. γ < 0.02 (Dissipation Parameter)

**Tvrzení v QCT:**
```
γ_ridge ≈ γ_GW < 0.02
```

**Teoretický základ:**
- Rovnice 7.8: `h(t) ~ exp(-γ_GW t)` (GW damping)
- Derivace: "Zahrň disipaci kondenzátu do vlnové rovnice"

**PROBLÉM:**
❌ **Není odvozena numerická hodnota γ!**
- Pouze kvalitativní tvar exponenciálního útlumu
- Hodnota 0.02 je označena jako "(horní mez z pozorování)"
- **Není to teoretická predikce QCT, ale empirický constraint z LIGO/Virgo!**

**Co QCT skutečně říká:**
- "Pokud je vakuum neutrino condensate, pak dissipace by měla být malá"
- "γ_QCT < γ_QCD" (menší než QCD hydrodynamika)
- **Ale konkrétní číslo 0.02 NENÍ odvozeno z prvních principů!**

---

### 2. α ≈ 0.2-0.3 (Strangeness Enhancement)

**Tvrzení v QCT:**
```
α | 0.1–0.3 | — |
x₀ | 10–30 | — |
```

**Teoretický základ:**
- Rovnice pro Λ/p: `R ∝ exp(-Ω(x) · Δm/T)`
- Kde `Ω(x) = 1 - α · x/(x + x₀)` (conformal dilution)

**PROBLÉM:**
❌ **Není odvozeno proč α ~ 0.25!**
- Model má fenomenologickou formu Ω(x)
- Parametry α a x₀ jsou VOLNÉ fitovací parametry
- Očekávané hodnoty 0.1-0.3 a 10-30 nejsou vypočítány
- **Jsou to hrubé odhady, ne teoretické predikce!**

**Co by teoretická predikce potřebovala:**
1. Odvození Ω(x) z dynamiky kondenzátu
2. Výpočet α z fundamentálních parametrů (m_ν, Λ_QCT, T_freeze)
3. Predikce x₀ z koherenční délky ξ

**Realita:**
- α, x₀ jsou EMPIRICKÉ parametry
- Model je FENOMENOLOGICKÝ, ne ab-initio

---

### 3. v₂ Model

**Tvrzení v QCT:**
```python
v₂(x) = A · ln(1 + x) · exp(-γ)
```

**Teoretický základ:**
- Předpokládá acoustic ridge mechanism
- Logaritmický růst z akustické geometrie
- exp(-γ) z dissipace

**PROBLÉM:**
❌ **Funkční forma NENÍ odvozena!**
- Proč ln(1+x)? (Není odvozeno)
- Proč ne ln(x) nebo x^b nebo saturace?
- Model je AD-HOC fenomenologie

**Co by teoretická predikce potřebovala:**
1. Odvození v₂ z perturbací akustické metriky
2. Výpočet multipole response
3. Predikce funkční formy z řešení wave equation

**Realita:**
- Logaritmická forma je GUESS
- Parametry A, γ jsou VOLNÉ
- **Není to první-principiální predikce!**

---

## KRITICKÉ ZJIŠTĚNÍ:

### QCT JAK JE PREZENTOVÁN:

```
"QCT predikuje γ < 0.02 a α ~ 0.25"
```

### QCT REALITA:

```
1. γ < 0.02 je EMPIRICKÝ constraint z LIGO (ne teoretická predikce)
2. α ~ 0.25 je ODHAD, ne výpočet
3. Funkční formy (ln, exp) jsou FENOMENOLOGICKÉ, ne odvozené
```

---

## ČÍM TO JE:

**QCT fitting framework je:**
1. ✅ Konzistentní fenomenologie (jednotná parametrizace)
2. ✅ Testovatelná (porovnání s daty)
3. ❌ **NENÍ ab-initio teoretickou predikcí**
4. ❌ **Parametry jsou volné, ne vypočítané**

**Analogie:**
- QCT je jako "Standard Model effective field theory"
- Má správnou symetrii a konzistenci
- Ale coupling konstanty (α, γ, A) musíš ZMĚŘIT, ne vypočítat

---

## PROČ MODEL SELHAL:

### 1. v₂ ~ konstanta (ne logaritmická)
**Důvod selhání:**
- Předpoklad acoustic ridge mechanism je ŠPATNĚ
- v₂ v pp nemá kolektivní původ
- Logaritmická forma byla GUESS, experimentálně vyvrácena

### 2. Λ/p všechny modely selhávají
**Důvod selhání:**
- Fenomenologická forma Ω(x) je PŘÍLIŠ JEDNODUCHÁ
- Reálná strangeness produkce má:
  - Threshold effects
  - Regeneration
  - Feed-down corrections
  - Které simple exp(-Ω) neumí popsat

---

## ZÁVĚR:

**QCT NENÍ "first-principles theory" jak prezentováno.**

Je to:
- Fenomenologický framework
- S volnými parametry
- Testovatelný na datech
- **Ale numerické hodnoty (0.02, 0.25) NEJSOU teoreticky odvozeny**

**Experimentální selhání znamená:**
1. Funkční formy (ln, exp) jsou ŠPATNĚ volené
2. Fyzikální předpoklady (acoustic ridge) jsou NEPLATNÉ pro pp
3. Framework potřebuje zásadní revizi

**Toto JE poctivá věda:**
- Model byl testován
- Data model nepotvrdila
- Identifikovali jsme chybné předpoklady

---

**Doporučení:**
1. **Přestat prezentovat** α~0.25, γ<0.02 jako "teoretické predikce"
2. **Uznat** že jsou to fenomenologické parametry
3. **Revidovat** funkční formy na základě dat
4. **Publikovat** negativní výsledek jako korektiv k přehnaným tvrzením
