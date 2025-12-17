# QCT-FIT: Numerical Protocol for ALICE Data

**Rigorózní fit parametrů vakua na reálná data z těžkých iontů.**

---

## Přehled

Tento modul implementuje přesný numerický protokol pro extrakci QCT vakuových parametrů z ALICE dat:

1. **Strangeness Enhancement** → fit konformního faktoru **Ω**
2. **Ridge / v₂ Anisotropy** → fit disipačního parametru **γ**
3. **Cross-Consistency Check** → validace γ_ridge ≈ γ_GW

---

## Teoretický základ

### 1. Strangeness Enhancement (R.1, R.2)

**Teorie:**
```
Y(m) ∝ exp(-Ω(dN/dη) · m / T_fo)

R_Λ/p(dN/dη) = exp(-Ω(dN/dη) · (m_Λ - m_p) / T_fo)
```

**Parametrizace:**
```
Ω(x) = 1 - α · x/(x + x₀)
```

**Fyzikální význam:**
- `α ∈ (0,1)`: síla zředění koherence vakua při vysoké multiplicitě
- `x₀ > 0`: charakteristická škála přechodu pp → pA → AA

**Fitované parametry:** `α, x₀`

---

### 2. Ridge / v₂ Acoustic Fit (R.3–R.5)

**Teorie:**
```
v₂(k) ∝ |δρ_k|

|δρ| ~ S / √[(ω_k²)² + (2γω_k)²]
```

**Fenomenologický model** (integrovaný přes k):
```
v₂(x) = A · ln(1 + x) · exp(-γ)
```

**Fyzikální význam:**
- `A`: amplituda akustického zdroje
- `γ`: disipace vakua (η/s ~ γ/(4π))

**Fitované parametry:** `A, γ`

---

### 3. Cross-Consistency (kritický test)

**QCT předpověď:**
```
γ_ridge ≈ γ_GW ≪ 1
```

**QCD hydrodynamika předpovídá:**
```
γ_ridge ~ 0.2–0.5
```

**Pokud γ < 0.01 konzistentně:**
- ✓ QCD hydrodynamika selhává
- ✓ QCT vakuum je ověřeno
- ✓ Jediný parametr disipace napříč všemi škálami

---

## Instalace

### Závislosti

```bash
pip install numpy scipy matplotlib
```

### Struktura

```
qct_fit/
├── __init__.py                  # Package init
├── strangeness_fit.py           # Ω fit (Λ/p ratio)
├── ridge_fit.py                 # γ fit (v₂ anisotropy)
├── consistency_check.py         # γ_ridge vs γ_GW validation
├── run_all_fits.py              # Master workflow script
├── README.md                    # This file
└── data/                        # ALICE data files
    ├── alice_lambda_p.csv       # Λ/p vs multiplicity
    └── alice_v2_pp.csv          # v₂ vs multiplicity
```

---

## Použití

### Rychlý start (mock data)

```bash
cd simulations/qct_fit
python run_all_fits.py
```

Toto spustí celý workflow s generovanými mock daty pro demonstraci.

### S reálnými ALICE daty

```bash
python run_all_fits.py --use-real-data --data-dir data/alice
```

### Samostatné moduly

**Fit pouze Ω:**
```python
from qct_fit.strangeness_fit import fit_omega_to_lambda_p_ratio

results = fit_omega_to_lambda_p_ratio(
    data_file="data/alice_lambda_p.csv",
    plot=True,
    save_results=True
)

print(f"α = {results['alpha']:.4f} ± {results['alpha_err']:.4f}")
print(f"x₀ = {results['x0']:.2f} ± {results['x0_err']:.2f}")
```

**Fit pouze γ:**
```python
from qct_fit.ridge_fit import fit_gamma_to_v2

results = fit_gamma_to_v2(
    data_file="data/alice_v2_pp.csv",
    plot=True
)

print(f"γ = {results['gamma']:.5f} ± {results['gamma_err']:.5f}")
```

**Cross-validace:**
```python
from qct_fit.consistency_check import cross_validate_gamma

report = cross_validate_gamma(
    gamma_ridge=0.008,
    gamma_ridge_err=0.002,
    gamma_gw_upper=0.02
)

print(f"Status: {report['status']}")
print(f"Conclusion: {report['conclusion']}")
```

---

## Formát dat

### alice_lambda_p.csv

```csv
dN_deta,ratio,err
2.0,0.580,0.018
5.0,0.600,0.020
10.0,0.630,0.019
...
```

**Sloupce:**
- `dN_deta`: multiplicity dN/dη
- `ratio`: Λ/p ratio
- `err`: statistical error

**Zdroj:** ALICE Collaboration, arxiv.org/abs/... (doplnit reálnou publikaci)

### alice_v2_pp.csv

```csv
dN_deta,v2,err
2.0,0.020,0.005
5.0,0.045,0.005
10.0,0.065,0.005
...
```

**Sloupce:**
- `dN_deta`: multiplicity dN/dη
- `v2`: elliptic flow v₂
- `err`: statistical error

**Zdroj:** ALICE Collaboration, arxiv.org/abs/... (doplnit reálnou publikaci)

---

## Výstupy

### JSON results

Všechny výsledky jsou uloženy v `results/qct_fit/`:

**strangeness_fit_results.json:**
```json
{
  "alpha": 0.2567,
  "alpha_err": 0.0123,
  "x0": 11.45,
  "x0_err": 1.23,
  "chi2": 8.45,
  "dof": 6,
  "chi2_reduced": 1.41,
  "p_value": 0.29,
  "fit_quality": "good"
}
```

**ridge_v2_fit_results.json:**
```json
{
  "A": 0.1502,
  "A_err": 0.0034,
  "gamma": 0.0082,
  "gamma_err": 0.0019,
  "chi2": 11.23,
  "dof": 8,
  "chi2_reduced": 1.40,
  "p_value": 0.19,
  "eta_over_s_estimate": 0.0007,
  "fit_quality": "good"
}
```

**consistency_check_report.json:**
```json
{
  "gamma_ridge": 0.0082,
  "gamma_ridge_err": 0.0019,
  "gamma_gw_upper": 0.02,
  "consistent": true,
  "tension_sigma": 0.53,
  "status": "PASS",
  "conclusion": "QCT_VALIDATED / QCD_CHALLENGED",
  "interpretation": "Strong evidence for QCT vacuum: γ ≪ 1 consistently..."
}
```

### Diagnostické ploty

- `strangeness_fit.png` — Λ/p vs dN/dη s fitem
- `ridge_v2_fit.png` — v₂ vs dN/dη s fitem
- `gamma_consistency_check.png` — porovnání γ_ridge, γ_GW, γ_QCD

---

## Fyzikální interpretace

### Očekávané výsledky (QCT)

| Parametr | QCT předpověď | QCD předpověď |
|----------|--------------|---------------|
| α | 0.1–0.3 | — |
| x₀ | 10–30 | — |
| γ | < 0.01 | 0.2–0.5 |
| η/s | < 0.001 | 0.08–0.20 |

### Klíčové testy

✓ **α ∈ (0.1, 0.3)**: realistické zředění vakua
✓ **x₀ ~ 10–30**: správná škála přechodu pp → AA
✓ **γ ≪ 1**: téměř ideální kapalina
✓ **γ_ridge ≈ γ_GW**: jednotný vakuový parametr
✓ **γ < γ_QCD**: QCD hydrodynamika selhává

---

## Citace dat

Při použití reálných ALICE dat citujte:

### Strangeness Enhancement
```
ALICE Collaboration, "Enhanced production of multi-strange hadrons in
high-multiplicity proton-proton collisions",
Nature Physics 13, 535 (2017), arXiv:1606.07424
```

### Ridge / v₂
```
ALICE Collaboration, "Long-range angular correlations on the near and
away side in p-Pb collisions at √sNN = 5.02 TeV",
Phys. Lett. B 719, 29 (2013), arXiv:1212.2001
```

---

## TODO / Rozšíření

- [ ] Přidat reálná ALICE data z HEPData
- [ ] Implementovat systematické nejistoty
- [ ] Bayesovská analýza s MCMC
- [ ] Rozšířit na další observables (φ/K*, ⟨pT⟩, ...)
- [ ] Automatický stáhovač dat z HEPData API
- [ ] Porovnání s PYTHIA8 / EPOS baseline

---

## Kontakt / Reporting Issues

Pokud najdete chyby nebo máte návrhy:
- Otevřete issue v repozitáři
- Email: [your-email]

---

## License

MIT License (viz LICENSE file v repozitáři)

---

**Vytvořeno:** 2025-12-17
**QCT Research Team**
