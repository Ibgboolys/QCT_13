# QCT Neutrino Condensate — Complete Definition

**Kompletní formální definice neutrinového kondenzátu v rámci QCT**

---

## Přehled

Tento dokument poskytuje úplnou formální definici neutrinového kondenzátu jako základu Quantum Coherence Theory (QCT). Zahrnuje:

1. **Matematickou databázi** — 49 vzájemně propojených rovnic
2. **Numerický fitting protokol** — extrakce vakuových parametrů z ALICE dat
3. **Experimentální validaci** — testovatelné predikce napříč škálami

---

## 1. Matematická Struktura

### 1.1 Equation Database

Kompletní databáze rovnic je uložena v:
```
docs/qct_neutrino_condensate/neutrino_condensate_equations.json
```

**Struktura:**
- **49 equations** organizovaných do 30+ sekcí
- Každá rovnice obsahuje:
  - `latex`: LaTeX reprezentace
  - `equation_number`: číslování (např. "1.1", "2.1", ...)
  - `section`: sekce monografie
  - `derivation_steps`: kroky odvození
  - `phys_interp`: fyzikální interpretace
  - `dependencies`: závislosti na jiných rovnicích
  - `units`: fyzikální jednotky (kde relevantní)
  - `source`: zdroj (monografie, axiomy, kalibrace, ...)

### 1.2 Hierarchie rovnic

**Axiomy (A.1–A.3):**
- A.1: `Ψ_{νν} ≠ 0` — vakuum je koherentní médium
- A.2: `g_{μν} = g_{μν}(ρ_ent, θ)` — geometrie je odvozená
- A.3: `částice ↔ topologické defekty`

**Kondenzát (1.1–1.2):**
- 1.1: `Ψ_{νν}(x) = ⟨ν(x) ν(x)⟩` — párová korelace neutrin
- 1.2: `ρ_ent = |⟨Ψ_{νν}⟩|²` — hustota entanglementu

**Efektivní teorie (2.1–3.5):**
- 2.1: Gross-Pitaevskii lagrangián
- 2.2: GP pohybová rovnice
- 3.1–3.4: Madelungova transformace, kontinuita, rychlostní pole, kvantový tlak
- 3.5: Rychlost zvuku v kondenzátu

**Akustická geometrie (4.1–4.6):**
- 4.1: Akustická metrika `ds² = (ρ/c_s)[-(c_s²-v²)dt² - 2v·dx dt + dx²]`
- 4.2: Konformní limit `g_{μν} = Ω²(x) η_{μν}`
- 4.3: Geodetická rovnice
- 4.4–4.5: Newtonovský limit, efektivní G_eff
- 4.6: Vlnová rovnice pro fonony

**BCS mechanismus (5.1–5.7):**
- 5.1: Slabá interakce jako kontaktní člen
- 5.2–5.3: Hustota stavů, BCS vazba
- 5.4: BCS gap `Δ ~ 2ω_c exp(-1/λ)`
- 5.5–5.6: Vazebná energie páru, spojení s Higgsem
- 5.7: Fundamentální škála `Λ_QCT ~ E_pair`

**Topologie a náboj (6.1–6.7):**
- 6.1–6.2: Fáze–gauge korespondence, emergentní Maxwell
- 6.3: Efektivní proud
- 6.4: Topologický náboj `Q = (1/2π) ∮∇θ·dl`
- 6.5: Spin jako cirkulace
- 6.6–6.7: Proton jako defekt, prostorové rozložení spinu

**Kosmologie (7.1–7.9):**
- 7.1–7.2: Emergentní FLRW metrika, Hubbleův parametr
- 7.3–7.4: Temná hmota jako koherenční skořápka, Tully-Fisher
- 7.5: Temná energie jako tlak kondenzátu
- 7.6: Gravitační screening `f_screen ~ m_ν/m_p`
- 7.7–7.8: Gravitační vlny — disperze a útlum
- 7.9: Experimentální signatury

**Validace a kalibrace (V.1–C.2):**
- V.1–V.2: Rozměrová analýza
- C.1: `Λ_QCT ≈ 10⁷ TeV`
- C.2: `f_screen ≈ 10⁻¹⁰`

**Meta (M.1–M.2):**
- M.1: Validita oblasti `k ≪ Λ_QCT`
- M.2: Experimentální program

**Export (X.1–X.2):**
- X.1–X.2: Automatická generace LaTeX a grafů

---

## 2. Numerický Fitting Protokol

### 2.1 Motivace

QCT předpovídá, že **vakuum není prázdné**, ale je makroskopicky koherentní neutrinový kondenzát. Tato koherence ovlivňuje:

1. **Hadronovou fenomenologii** (strangeness enhancement)
2. **Akustické excitace** (ridge, v₂)
3. **Gravitační vlny** (slabý útlum)

**Klíčová hypotéza:**
Jediný parametr `γ` (vakuová disipace) popisuje:
- γ_ridge (ALICE)
- γ_GW (LIGO/Virgo)

Pokud `γ ≪ 1` konzistentně → **QCT validována**, QCD hydro selhává.

### 2.2 Implementace

**Umístění:**
```
simulations/qct_fit/
├── __init__.py
├── strangeness_fit.py      # Ω fit (Λ/p ratio)
├── ridge_fit.py            # γ fit (v₂)
├── consistency_check.py    # γ_ridge vs γ_GW
├── run_all_fits.py         # Master script
├── README.md
└── data/
    ├── alice_lambda_p.csv
    └── alice_v2_pp.csv
```

**Použití:**
```bash
cd simulations/qct_fit
python run_all_fits.py
```

Výstup:
- Fitted parametry: `α, x₀, γ, A`
- Fit kvalita: `χ²/dof, p-value`
- Konzistence: `γ_ridge vs γ_GW`
- Diagnostické ploty

### 2.3 Teoretické modely

**Strangeness Enhancement (R.1–R.2):**
```
R_Λ/p(x) = exp(-Ω(x) · (m_Λ - m_p) / T_fo)
Ω(x) = 1 - α · x/(x + x₀)
```
Fitujeme `α, x₀` na ALICE Λ/p data.

**Ridge / v₂ (R.3–R.5):**
```
v₂(x) = A · ln(1 + x) · exp(-γ)
```
Fitujeme `A, γ` na ALICE v₂ data.

**Cross-Consistency:**
```
γ_ridge ≈ γ_GW < 0.02
```
Validujeme konzistenci napříč experimenty.

### 2.4 Očekávané výsledky

| Parametr | QCT | QCD |
|----------|-----|-----|
| α | 0.1–0.3 | — |
| x₀ | 10–30 | — |
| γ | < 0.01 | 0.2–0.5 |
| η/s | < 0.001 | 0.08–0.20 |

**Pokud γ < 0.01:**
- ✓ QCD hydrodynamika vyloučena
- ✓ QCT vakuum validováno
- ✓ Jeden médium pro všechny procesy

---

## 3. Experimentální Predikce

### 3.1 ALICE (LHC)

**Testované observables:**
- `Λ/p(dN/dη)` — strangeness enhancement
- `v₂(dN/dη)` — azimutální anizotropie
- `⟨pT⟩_strange` — průměrný transverse momentum

**Predikce:**
- Plynulý přechod pp → pA → AA (žádný skok!)
- `γ_ridge < 0.01` → téměř ideální kapalina
- Žádná hadronizace v tradičním smyslu

### 3.2 LIGO/Virgo (GW)

**Testované observables:**
- GW útlum `h(t) ~ exp(-γ_GW t)`
- Disperze `ω² = c²k² + αk⁴/Λ_QCT²`

**Predikce:**
- `γ_GW < 0.02` (horní mez z pozorování)
- Slabá disperze na vysokých frekvencích
- **Kritické:** `γ_GW ≈ γ_ridge` (stejné vakuum!)

### 3.3 Lunar Laser Ranging (LLR)

**Testované:**
- Časová variace `G_eff(t)`
- Gravitační screening efekty

**Predikce:**
- `|dG/dt|/G < 10⁻¹³ yr⁻¹`
- Screening `f_screen ~ m_ν/m_p ~ 10⁻¹⁰`

### 3.4 CMB (Planck, DESI)

**Testované:**
- Fázový posun v BAO
- Kosmologické parametry

**Predikce:**
- Modifikace H(z) při vysokých z
- Vliv neutrinového kondenzátu na decoupling

### 3.5 Proton Structure (μp scattering)

**Testované:**
- Prostorové rozložení spinu

**Predikce:**
- `⟨r²⟩_S > ⟨r²⟩_charge` (spin distributed beyond proton core)
- Vysvětlení "spin crisis"

---

## 4. Závislostní Graf

```
Axioms (A.1-A.3)
  │
  ├─→ Condensate (1.1-1.2)
  │     │
  │     ├─→ GP Lagrangian (2.1-2.2)
  │     │     │
  │     │     └─→ Madelung (3.1-3.4)
  │     │           │
  │     │           └─→ Sound speed (3.5)
  │     │                 │
  │     │                 └─→ Acoustic metric (4.1)
  │     │                       │
  │     │                       ├─→ Conformal limit (4.2)
  │     │                       │     │
  │     │                       │     └─→ Newtonian (4.4-4.5)
  │     │                       │
  │     │                       ├─→ Geodesics (4.3)
  │     │                       │
  │     │                       └─→ Wave eq (4.6)
  │     │
  │     └─→ BCS mechanism (5.1-5.7)
  │           │
  │           └─→ E_pair, Λ_QCT
  │
  ├─→ Topology (6.1-6.7)
  │     │
  │     └─→ EM, charge, spin
  │
  └─→ Cosmology (7.1-7.9)
        │
        └─→ DM, DE, GW, observables
```

---

## 5. Použití Databáze

### 5.1 Načtení rovnic

```python
import json

with open("docs/qct_neutrino_condensate/neutrino_condensate_equations.json") as f:
    db = json.load(f)

# Přístup k rovnici
psi_def = db["equations"]["eq_psi_def"]

print(psi_def["latex"])
# → "\Psi_{\nu\nu}(x) = \langle \nu(x) \nu(x) \rangle"

print(psi_def["phys_interp"])
# → "Pole Ψ_{νν} popisuje neutrinový kondenzát..."
```

### 5.2 Dependency traversal

```python
def get_dependencies(eq_id, db):
    """Rekurzivně získej všechny závislosti rovnice."""
    eq = db["equations"][eq_id]
    deps = eq["dependencies"]

    all_deps = set(deps)
    for dep in deps:
        all_deps.update(get_dependencies(dep, db))

    return all_deps

# Příklad: všechny závislosti akustické metriky
deps = get_dependencies("eq_acoustic_metric", db)
print(deps)
# → {'eq_sound_speed', 'eq_velocity_field', 'eq_continuity', ...}
```

### 5.3 Export do LaTeX

```python
def export_to_latex(db, section_filter=None):
    """Exportuj rovnice do LaTeX dokumentu."""

    equations = db["equations"]

    if section_filter:
        equations = {k: v for k, v in equations.items()
                     if section_filter in v["section"]}

    latex = "\\documentclass{article}\n\\begin{document}\n\n"

    for eq_id, eq in sorted(equations.items(),
                            key=lambda x: x[1]["equation_number"]):
        latex += f"\\subsection{{{eq['section']}}}\n"
        latex += f"\\begin{{equation}}\n{eq['latex']}\n\\end{{equation}}\n"
        latex += f"\\textit{{{eq['phys_interp']}}}\n\n"

    latex += "\\end{document}"

    return latex

# Export pouze sekce 4 (akustická metrika)
latex_section4 = export_to_latex(db, section_filter="4.")
```

---

## 6. Roadmap

### Completed ✓
- [x] Kompletní equation database (49 rovnic)
- [x] Numerický fitting framework
- [x] Strangeness enhancement fit
- [x] Ridge / v₂ fit
- [x] Cross-consistency check
- [x] Mock data generation
- [x] Dokumentace

### TODO
- [ ] Download reálných ALICE dat z HEPData
- [ ] MCMC Bayesovská analýza
- [ ] Systematické nejistoty
- [ ] Rozšíření na další observables (φ/K*, ⟨pT⟩)
- [ ] Grafová vizualizace dependency structure
- [ ] Export do Neo4j / RDF
- [ ] Automatická generace LaTeX monografie
- [ ] Integration s hlavním QCT frameworkem

---

## 7. Reference

### ALICE Data
```
[1] ALICE Collaboration, "Enhanced production of multi-strange hadrons
    in high-multiplicity proton-proton collisions",
    Nature Physics 13, 535 (2017), arXiv:1606.07424

[2] ALICE Collaboration, "Long-range angular correlations on the near
    and away side in p-Pb collisions at √sNN = 5.02 TeV",
    Phys. Lett. B 719, 29 (2013), arXiv:1212.2001
```

### QCT Theory
```
[3] QCT Monograph (this repository),
    docs/QCT_COMPLETE_MARKDOWN.md

[4] QCT Compact Formalism,
    QCT_COMPACT_FORMALISM.md
```

---

## 8. Kontakt

Pro otázky ohledně:
- **Equation database**: viz JSON metadata
- **Fitting protocol**: viz simulations/qct_fit/README.md
- **Teoretické otázky**: viz QCT monografie

---

**Vytvořeno:** 2025-12-17
**Verze:** 1.0.0
**Status:** Complete and ready for validation

---

## Appendix A: Equation Index

Quick reference for all 49 equations:

### Foundations
- **1.1** `Ψ_{νν}` — Condensate definition
- **1.2** `ρ_ent` — Entanglement density

### Effective Field Theory
- **2.1** `ℒ` — GP Lagrangian
- **2.2** `i∂_t Ψ` — GP equation

### Hydrodynamics
- **3.1** `Ψ = √ρ e^{iθ}` — Madelung
- **3.2** `∂_t ρ + ∇·(ρv) = 0` — Continuity
- **3.3** `v = (ℏ/m)∇θ` — Velocity field
- **3.4** `Q` — Quantum pressure
- **3.5** `c_s²` — Sound speed

### Geometry
- **4.1** `ds²` — Acoustic metric
- **4.2** `g = Ω² η` — Conformal limit
- **4.3** Geodesics
- **4.4** `∇²Φ = 4πG_eff δρ` — Newtonian
- **4.5** `G_eff ~ c_s²/ρ_ent`
- **4.6** `□φ = 0` — Wave equation

### Pairing
- **5.1** `ℒ_eff` — Weak contact
- **5.2** `N(E_F)` — DOS
- **5.3** `λ = G_F N(E_F)` — BCS coupling
- **5.4** `Δ ~ 2ω_c exp(-1/λ)` — Gap
- **5.5** `E_pair` — Binding energy
- **5.6** Higgs connection
- **5.7** `Λ_QCT` — QCT scale

### Topology
- **6.1** `∂θ → ∂θ - A` — Phase-gauge
- **6.2** Maxwell
- **6.3** `J_eff` — Current
- **6.4** `Q = (1/2π)∮∇θ·dl` — Charge
- **6.5** `S ~ ∫r×(ρv)` — Spin
- **6.6** Proton profile
- **6.7** Spin distribution

### Cosmology
- **7.1** FLRW metric
- **7.2** `H(t)` — Hubble
- **7.3** `ρ_DM ~ |∇ρ_ent|` — Dark matter
- **7.4** Tully-Fisher
- **7.5** `p_Λ = -ρc²` — Dark energy
- **7.6** `f_screen ~ m_ν/m_p` — Screening
- **7.7** GW dispersion
- **7.8** GW damping
- **7.9** Observable map

### Validation
- **V.1–V.2** Dimensional checks
- **C.1–C.2** Numerical calibration
- **M.1–M.2** Meta-theory
- **X.1–X.2** Export utilities

### Axioms
- **A.1** `Ψ ≠ 0` — Coherent vacuum
- **A.2** `g = g(ρ,θ)` — Geometry emergent
- **A.3** Particles = defects

---

**END OF DOCUMENT**
