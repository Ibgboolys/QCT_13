# ALICE Data Files

## Přehled

Tento adresář obsahuje ALICE heavy-ion data pro QCT-FIT analýzu.

---

## Required Files

### 1. alice_lambda_p.csv

**Popis:** Λ/p poměr jako funkce multiplicity dN/dη

**Formát:**
```csv
dN_deta,ratio,err
2.0,0.580,0.018
5.0,0.600,0.020
...
```

**Zdroj:** ALICE Collaboration, Nature Physics 13, 535 (2017), arXiv:1606.07424

**Jak získat:**
- HEPData: https://www.hepdata.net/record/ins1471838
- Tabulka 3: Λ/p ratio vs multiplicity (pp collisions at √s = 7 TeV)

---

### 2. alice_v2_pp.csv

**Popis:** Elliptic flow v₂ jako funkce multiplicity dN/dη

**Formát:**
```csv
dN_deta,v2,err
2.0,0.020,0.005
5.0,0.045,0.005
...
```

**Zdroj:** ALICE Collaboration, Phys. Lett. B 719, 29 (2013), arXiv:1212.2001

**Jak získat:**
- HEPData: https://www.hepdata.net/record/ins1190545
- Tabulka: v₂ vs multiplicity (p-Pb collisions)

---

## Instalace dat

### Automatický download (TODO)

```bash
python download_alice_data.py
```

### Manuální download

1. Navštivte HEPData odkazy výše
2. Stáhněte CSV soubory
3. Přejmenujte a umístěte do tohoto adresáře:
   - `alice_lambda_p.csv`
   - `alice_v2_pp.csv`

---

## Mock Data

Pokud reálná data nejsou k dispozici, QCT-FIT automaticky vygeneruje mock data pro testování.

Mock data jsou konzistentní s QCT předpověďmi:
- α ~ 0.25
- x₀ ~ 12
- γ ~ 0.02
- A ~ 0.15

---

## Data Quality Checks

Před použitím zkontrolujte:
- [ ] Správný formát CSV (3 sloupce)
- [ ] Multiplicity range: 2 < dN/dη < 100
- [ ] Λ/p range: 0.4 < ratio < 0.8
- [ ] v₂ range: 0.01 < v₂ < 0.15
- [ ] Error bars jsou rozumné (1-5%)

---

## Citation

Při publikaci výsledků citujte původní ALICE publikace:

```bibtex
@article{ALICE:2016fzo,
    author = "Acharya, Shreyasi and others",
    collaboration = "ALICE",
    title = "{Enhanced production of multi-strange hadrons in
             high-multiplicity proton-proton collisions}",
    journal = "Nature Phys.",
    volume = "13",
    pages = "535--539",
    year = "2017",
    eprint = "1606.07424",
    archivePrefix = "arXiv",
    primaryClass = "nucl-ex",
    doi = "10.1038/nphys4111"
}

@article{ALICE:2012mte,
    author = "Abelev, Betty and others",
    collaboration = "ALICE",
    title = "{Long-range angular correlations on the near and away
             side in p-Pb collisions at sqrt(s_NN) = 5.02 TeV}",
    journal = "Phys. Lett. B",
    volume = "719",
    pages = "29--41",
    year = "2013",
    eprint = "1212.2001",
    archivePrefix = "arXiv",
    primaryClass = "nucl-ex",
    doi = "10.1016/j.physletb.2013.01.012"
}
```

---

**Last updated:** 2025-12-17
