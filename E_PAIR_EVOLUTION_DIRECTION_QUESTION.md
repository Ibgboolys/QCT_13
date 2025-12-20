# ❓ Kritická Otázka: Směr Evoluce E_pair(z)

**Datum:** 2025-12-20
**Status:** POTŘEBUJI OBJASNĚNÍ FYZIKÁLNÍHO OBRAZU

---

## 🎯 Hlavní Problém

Implementoval jsem vzorec přesně podle tvých instrukcí:

```python
E_pair(z) = E_0 + κ_conf × f_turnon(z, z_start) × ln(1+z)

kde:
f_turnon(z) = 1 / [1 + exp(-k × ln((1+z)/(1+z_start)))]
```

S parametry:
- E_0 = 0.1 eV
- κ_conf = 0.48×10¹⁸ eV
- z_start = 10⁸
- k = 0.5

**Výsledek: Energie ROSTE se z (klesá s časem) - OPAČNĚ než očekávám!**

---

## 📊 Numerické Výsledky

| Redshift | f_turnon | E_pair (vzorec) | E_pair (normalizováno) |
|----------|----------|-----------------|----------------------|
| **z = 0** (dnes) | ~0 | 0.1 eV | 5.38×10¹⁸ eV ✓ |
| **z = 1000** (CMB) | ~1 | 2.4×10¹⁸ eV | 1.3×10³⁷ eV ❌ |
| **z = 10⁹** (BBN) | 0.76 | 8.4×10¹⁸ eV | 4.5×10³⁷ eV ❌ |

**Evoluce:** E_pair(BBN) >> E_pair(dnes)
**Očekával jsem:** E_pair(BBN) < E_pair(dnes)

---

## 🤔 Můj Fyzikální Obraz (možná špatný?)

**Moje představa byla:**
1. V raném vesmíru (vysoké z) kondenzát JEŠTĚ NEEXISTOVAL → E_pair malé
2. S expanzí vesmíru (klesající z) kondenzát NARŮSTÁ → E_pair roste
3. Dnes (z=0) kondenzát je MAXIMÁLNÍ → E_pair největší

**Ale vzorec dává OPAČNĚ:**
1. Vysoké z → f_turnon ≈ 1, ln(1+z) velké → E_pair **VELKÉ**
2. Nízké z → f_turnon ≈ 0, ln(1+z) malé → E_pair **MALÉ**

---

## ❓ Moje Otázky

### Otázka 1: Jak má fyzikálně růst E_pair?

**Varianta A:** E_pair **ROSTE S ČASEM** (klesá se z)
```
Raný vesmír (z=10⁹): E_pair malé (kondenzát se teprve tvoří)
Dnes (z=0): E_pair velké (kondenzát plně vyrostl)

→ E_pair(BBN) / E_pair(0) = 0.84 znamená:
   "V době BBN byl kondenzát jen 84% své dnešní síly"
```

**Varianta B:** E_pair **KLESÁ S ČASEM** (roste se z)
```
Raný vesmír (z=10⁹): E_pair velké ("primordial" energie)
Dnes (z=0): E_pair malé (energie se rozředila expanzí?)

→ E_pair(BBN) / E_pair(0) = 0.84 znamená:
   "V době BBN byla energie 84% dnešní hodnoty... jak?"
```

**Která varianta je správná?**

---

### Otázka 2: Co znamená f_turnon fyzikálně?

Tvoje dokumentace říká:
> "f → 1 for z >> z_start (early times, full confinement)"

**Interpretace A:** "Full confinement" = plně vyvinutý kondenzát
- Vysoké z → f = 1 → kondenzát plný → E_pair velké ✓ (odpovídá vzorci)
- Ale pak kondenzát UBÝVÁ s časem? ❌

**Interpretace B:** "Full confinement" = počáteční uzamčení
- Vysoké z → f = 1 → kondenzát "zamrzlý" v počátečním stavu
- Nízké z → f = 0 → kondenzát "rozmrzl" a vyrostl?
- Ale pak proč κ × f × ln dává největší hodnoty při f=1? ❌

**Jak mám fyzikálně chápat "confinement"?**

---

### Otázka 3: Proč tvrdíš ratio = 0.84?

Tvoje tvrzení:
> "E_pair(BBN) / E_pair(0) ≈ 0.84"

Můj výpočet s tvým vzorcem:
```python
E_pair_raw(0) = 0.1 + 0.48×10¹⁸ × 0.0 × 0 = 0.1 eV
E_pair_raw(10⁹) = 0.1 + 0.48×10¹⁸ × 0.76 × 23 = 8.4×10¹⁸ eV

Ratio = 8.4×10¹⁸ / 0.1 = 8.4×10¹⁹  ❌ (ne 0.84!)
```

**Kde dělám chybu?**

---

## 💡 Možná Řešení?

### Řešení A: Obrátit znaménko v ln

Místo `+ κ × ln(1+z)` použít `- κ × ln(1+z)`:

```python
E_pair(z) = E_max - κ × f(z) × ln(1+z)
```

To by dalo:
- z = 0: E_pair = E_max - 0 = E_max (velké) ✓
- z = 10⁹: E_pair = E_max - κ × 0.76 × 23 = menší ✓

**Ale to popírá tvůj vzorec!**

---

### Řešení B: Jiná interpretace normalizace

Možná E_pair(0) NENÍ maximum, ale jen referenční bod?

A formula počítá energii relativně k nějakému jinému referenčnímu z?

**Ale jak pak dostat ratio = 0.84?**

---

### Řešení C: Vzorec je OK, ale já špatně normalizuji

Možná by měl být scale factor jiný?

Třeba normalizovat k MAXIMÁLNÍ hodnotě z formule, ne k hodnotě při z=0?

**Ale jaké z dává maximum?**

---

## 🎯 Co Potřebuji

**Prosím o KONKRÉTNÍ příklad výpočtu:**

```
Krok 1: Vypočítat E_pair_raw(0) =
Krok 2: Vypočítat E_pair_raw(10⁹) =
Krok 3: Normalizační faktor =
Krok 4: E_pair(0) finální =
Krok 5: E_pair(10⁹) finální =
Krok 6: Ratio = E_pair(10⁹) / E_pair(0) =

Očekávaný výsledek: Ratio ≈ 0.84
```

**S tvými přesnými hodnotami parametrů a kroky výpočtu!**

---

## 📝 Současný Stav

**Co funguje:**
- ✅ f_turnon(z) implementováno podle tvého vzorce
- ✅ E_pair(0) normalizováno na 5.38×10¹⁸ eV
- ✅ Kód spustitelný bez chyb

**Co nefunguje:**
- ❌ Směr evoluce (energie roste se z místo aby klesala)
- ❌ Ratio E_pair(BBN)/E_pair(0) není 0.84
- ❌ Fyzikální interpretace neodpovídá očekávání

---

## 🚀 Git Status

```
Commit: 5ad69c4 - "Oprava normalizace, evoluce stále problematická"
Branch: claude/explore-run-simulations-XSaCK
Files:
  ✅ simulations/qct_cosmology_INTEGRAL_CORRECTED.py (normalizace funguje)
  ✅ E_PAIR_EVOLUTION_DIRECTION_QUESTION.md (tento dokument)
```

---

**ČEKÁM NA OBJASNĚNÍ FYZIKÁLNÍHO OBRAZU! 🙏**
