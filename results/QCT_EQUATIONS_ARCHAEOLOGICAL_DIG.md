# ARCHEOLOGICKÝ VÝKOP: Odkud pocházejí QCT rovnice?

## Cíl: Najít ODVOZENÍ numerických hodnot α ~ 0.25, γ < 0.02

---

## 1. STRANGENESS ENHANCEMENT (Λ/p FIT)

### Rovnice v kódu (`strangeness_fit.py:24-29`):

```python
Y(m) ∝ exp(-Ω(dN/dη) · m / T_fo)
R_Λ/p(dN/dη) = exp(-Ω(dN/dη) · (m_Λ - m_p) / T_fo)
Ω(x) = 1 - α · x/(x + x₀)
```

### Konstanty:
```python
M_PROTON = 0.938 GeV
M_LAMBDA = 1.115 GeV
T_FREEZE = 0.160 GeV
DELTA_M = 0.177 GeV
```

### Otázka: ODKUD Ω(x) = 1 - α·x/(x+x₀)?

**Hledání v equations.json:**
- ❌ Žádná rovnice přímo pro Ω(x) strangeness!
- ✓ eq_qct_conformal (4.2): `g_μν = Ω²(x) η_μν` (acoustic metric)
- ✓ eq_hubble_from_coherence (7.2): `H(t) = (1/2) d/dt ln(Ω⁻²)`

**Závěr:**
```
Ω je CONFORMAL FACTOR z acoustic metric teorie.
Ale funkční forma Ω(x) = 1 - α·x/(x+x₀) JE FENOMENOLOGICKÝ ANSATZ!

Není odvozena z fundamentálních rovnic!
Je to GUESS inspirovaný saturation behavior.
```

### Fyzikální interpretace (z kódu):
```
α = 0: žádná dilucekoherence (vacuum zůstává čistý)
α → 1: silná diluce při vysoké multiplicitě
x₀: škála přechodu pp → heavy-ion
```

**KRITICKÉ:**
- Žádné odvození α ~ 0.25 z m_ν, Λ_QCT, nebo jiných fundamentálních parametrů
- x₀ ~ 10-30 je ODHAD bez kalibrace
- **Jsou to VOLNÉ FITOVACÍ PARAMETRY, ne teoretické predikce!**

---

## 2. RIDGE v₂ FIT

### Rovnice v kódu (`ridge_fit.py:12-14`):

```python
v₂(x) = A · ln(1 + x) · exp(-γ)

kde:
  x = dN/dη (multiplicity)
  A = source strength
  γ = vacuum dissipation
```

### Otázka: ODKUD ln(1+x)?

**Hledání v equations.json:**
- ❌ ŽÁDNÁ rovnice pro v₂ vs multiplicity!
- ✓ eq_gw_damping (7.8): `h(t) ~ exp(-γ_GW t)` (GW útlum)
- ✓ eq_gw_dispersion (7.7): `ω² = c²k² + αk⁴/Λ²` (disperze)

**Derivace γ_GW:**
```json
"derivation_steps": [
  "Zahrň disipaci kondenzátu do vlnové rovnice.",
  "Identifikuj útlumový koeficient."
]
```

**KRITICKÉ:**
- Kvalitativní exp(-γt) forma ✓
- Numerická hodnota γ? **❌ NENÍ ODVOZENA!**
- Jen říká "identifikuj koeficient" - TO NENÍ VÝPOČET!

### Logaritmická forma v₂ ~ ln(1+x):

**Fyzikální odůvodnění (pokud existuje):**
```
Akustický model:
1. Perturbace hustoty δρ v kondenzátu
2. Vlnová rovnice: ∇²δρ - (1/c_s²)∂²δρ/∂t² = source
3. Multipole expansion → v₂ z quadrupole
4. Integration over k → ???
```

**Realita:**
```
❌ Žádné odvození ln(1+x) z wave equation
❌ Žádný výpočet proč logaritmický růst
❌ Žádné spojení s acoustic metric perturbations

✓ Je to FENOMENOLOGICKÝ GUESS
✓ Inspirováno tím, že ln roste pomalu (saturation)
```

---

## 3. GAMMA < 0.02 CONSTRAINT

### Tvrzení v docs (`QCT_NEUTRINO_CONDENSATE_COMPLETE.md:307`):

```markdown
γ_GW < 0.02 (horní mez z pozorování)
```

### Hledání teoretického odvození:

**V equation database:**
```json
eq_gw_damping (7.8):
  latex: "h(t) \\sim e^{-\\gamma_{\\rm gw} t}"
  derivation: ["Zahrň disipaci", "Identifikuj koeficient"]
```

**Kalibrace (`cal_lambda_qct_numeric`, C.1):**
```json
"Použij m_ν a v_EW."
"Porovnej s kosmologickými a GW omezeními."
```

**KRITICKÉ ZJIŠTĚNÍ:**
```
γ < 0.02 NENÍ teoretická predikce QCT!

Je to EMPIRICKÝ CONSTRAINT z:
- LIGO/Virgo pozorování (žádný významný GW útlum pozorován)
- Kosmologická omezení (CMB, BAO)

QCT říká: "γ by mělo být malé (téměř ideální kapalina)"
Ale ČÍSLO 0.02 pochází z EXPERIMENTU, ne teorie!
```

---

## 4. ALPHA ~ 0.25 PREDICTION

### Tvrzení v docs (tabulka):

```markdown
| α | 0.1–0.3 | — |
| x₀ | 10–30 | — |
```

### Hledání odvození:

**Prohledávka celého repository:**
```bash
grep -r "alpha.*0.2\|0.25.*alpha" docs/
```

**Výsledek:** ❌ ŽÁDNÉ ODVOZENÍ!

**Mock data (`strangeness_fit.py:276`):**
```python
alpha_true = 0.25
x0_true = 12.0
```

**KRITICKÉ:**
```
Hodnota 0.25 je HARDCODED v mock data generátoru!
Není odvozena, není kalibr ována, není vypočítána.
Je to GUESS pro testování kódu!
```

---

## 5. CO VLASTNĚ QCT ODVOZUJE?

### Skutečné teoretické výpočty v repository:

**A) BCS Gap Energy (`D_K_BCS_derivation.md`):**
```
Δ ~ 2 ω_c exp(-1/λ)
D(K) ~ D_0 / K^(4/3)  [BCS enhancement in dense environment]
```
✓ Toto JE odvozeno z BCS teorie
✓ Má derivaci krok-za-krokem
✓ Používá fundamentální parametry (λ, ω_c)

**B) Fundamental Scale (`cal_lambda_qct_numeric`):**
```
Λ_QCT ~ 10^7 TeV
```
✓ Odvozeno z E_pair a m_ν
✓ Má fyzikální zdůvodnění

**C) Gravitational Screening (`cal_screening_numeric`):**
```
f_screen ~ 10^{-10}
```
✓ Vypočítáno z m_ν ~ 0.1 eV, m_p ~ 1 GeV

**D) Hubble Parameter (`eq_hubble_from_coherence`):**
```
H(t) = (1/2) d/dt ln(Ω⁻²)
```
✓ Odvozeno z FLRW metriky s conformal factor

---

## ZÁVĚR:

### Co QCT SKUTEČNĚ odvozuje:

1. ✅ **Qualitative forms:**
   - h(t) ~ exp(-γt) ✓
   - Ω(x) existuje ✓
   - BCS enhancement D(K) ~ 1/K^β ✓

2. ✅ **Fundamental scales:**
   - Λ_QCT ~ 10^7 TeV ✓
   - f_screen ~ 10^{-10} ✓

### Co QCT NEODVOZUJE (ale tvrdí):

1. ❌ **Numerical parameters:**
   - α ~ 0.25 → NENÍ odvozeno
   - γ < 0.02 → převzato z LIGO
   - x₀ ~ 10-30 → hrubý odhad

2. ❌ **Functional forms:**
   - Ω(x) = 1 - α·x/(x+x₀) → fenomenologický ansatz
   - v₂ ~ ln(1+x) → guess bez odvození

---

## IMPLIKACE:

### Pro experimentální selhání:

**Původní interpretace:**
```
"QCT predikuje γ = 0.01, data dávají 0.7"
→ Teoretická predikce je špatně
```

**SPRÁVNÁ interpretace:**
```
"QCT hádá funkční formu ln(1+x), data ukazují konstanta"
→ Fenomenologický guess je špatně
→ Fyzikální předpoklad (acoustic ridge v pp) je FALSE
```

### Pro budoucí práci:

**Pokud chceme QCT jako prediktivní teorii:**
1. Odvodit Ω(x) z perturbací acoustic metric
2. Vypočítat α z m_ν, T_freeze, Λ_QCT
3. Odvodit v₂(x) z wave equation řešení
4. Vypočítat γ z condensate viscosity

**Nebo uznat:**
- QCT je fenomenologický framework
- Parametry se FITUJÍ, ne počítají
- Je to validní přístup, ale ne "ab-initio theory"

---

## FINÁLNÍ VERDIKT:

```
QCT JAK JE PREZENTOVÁN:
  "First-principles theory predikující γ<0.02, α~0.25"

QCT VE SKUTEČNOSTI:
  "Phenomenological framework s kvalitativními formami
   a volnými parametry kalibovanými na data"
```

**Toto NENÍ kritika QCT jako vědy.**
**Je to kritika PREZENTACE jako něčeho, čím QCT není.**

Honest physics: Fenomenologie je validní!
Ale nesmíme ji prodávat jako first-principles calculation.
