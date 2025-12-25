# AUDIT VNITŘNÍ KONZISTENCE MONOGRAFIE QCT
**Datum:** 2025-12-25
**Kontrolovaný dokument:** `monografie_QCT_munipress.tex` + všechny \input soubory
**Status:** ⚠️ **NALEZENY KRITICKÉ NEKONZISTENCE**

---

## 🔴 KRITICKÉ PROBLÉMY

### **PROBLÉM 1: DVA PROTICHŮDNÁ PARADIGMATA SOUČASNĚ**

Monografie obsahuje **staré** (fenomenologické) a **nové** (primordial freezeout) paradigma v různých kapitolách, což vytváří **zásadní vnitřní rozpor**.

#### **✅ NOVÉ PARADIGMA (Primordial Freezeout)** - SPRÁVNÉ

**Lokace:**
- Abstract (řádek 274, 278)
- Kapitola 7, sekce "Primordiální zamrznutí a hierarchie škál" (řádek 2489-2507)
- Kapitola 9, sekce "Primordiální zamrznutí a efekt ledovce" (řádek 3056-3069)

**Klíčové tvrzení:**
```latex
E_{\mathrm{cond}} = (2.0 ± 0.5) × 10^{16} GeV  (FIXNÍ od GUT epochy)

G_{\mathrm{eff}} ~ G_N × (m_p/E_{\mathrm{cond}})^2 × f_screen(ρ) × N
```

**Fyzikální interpretace:**
- Vazebná energie kondenzátu zamrzla při GUT fázovém přechodu
- NEEVOLVUJE s redshiftem
- Faktor 10^16 je poměr fundamentálních škál (GUT/QCD), ne chyba

---

#### **❌ STARÉ PARADIGMA (Fenomenologické)** - ZASTARALÉ, MUSÍ SE ODSTRANIT

**Lokace (seznam všech výskytů):**

**Kapitola 5:**
- Řádek 1812: `E_pair(z=0) - E_pair(z_EW) = ∫...`
- Řádek 1922: `E_pair(z) - E_0 ≈ α_0 E_pair(0) × ln(1+z)`
- Řádek 1929: `E_pair(t) = E_0 + κ_conf · ln(1+z)`
- Řádek 2293: `E_pair(t) = E_0 + κ_conf·ln(a(t)/a_0)` **(boxed equation!)**
- Řádek 2311: `E_pair(z) = E_0 + κ_conf · f_turn-on(z, z_start) · ln(1+z)` **(s sigmoidem!)**

**Kapitola 7:**
- Řádek 2402: `Λ_QCT(z) = (3/2)√[E_0+κ_conf·ln(1+z)]·m_p`
- Řádek 2468: "To podporuje logaritmickou formu E_pair(z) ~ ln(1+z)"

**Kapitola 9:**
- Řádek 3141: `E_{\mathrm{pair}}` (bez evoluční závislosti - toto OK)
- Řádek 3830: `E_pair(z) = E_0 + κ_conf ln(1+z)` **(v diskusi konfinem)**
- Řádek 4130: anglická verze téhož

**Klíčové tvrzení (ZASTARALÉ):**
```latex
E_pair(z) = E_0 + κ_conf · f_turn-on(z, z_start) · ln(1+z)
```

**Fyzikální interpretace (NESPRÁVNÁ V NOVÉM PARADIGMATU):**
- Vazebná energie roste logaritmicky s redshiftem
- Parametry E_0 ≈ 0.1 eV, κ_conf ≈ 0.48 EeV
- Sigmoid turn-on funkce f(z, z_start)
- Toto je v PŘÍMÉM ROZPORU s primordial freezeout!

---

### **Proč je to problém?**

1. **Fyzikální rozpor:** Kondenzát nemůže mít současně:
   - Fixní energii E_cond = 2×10^16 GeV (zamrzlou při GUT)
   - A evoluci E_pair(z) ~ ln(1+z) závislou na redshiftu

2. **Recenzent okamžitě odhalí:** "Equation (7.23) claims E_cond is fixed at GUT scale, but equation (5.145) shows it evolving with ln(1+z). Which is correct?"

3. **Ztráta věrohodnosti:** Vypadá to, jako by autor neznal vlastní teorii.

---

## 🟡 STŘEDNÍ PROBLÉMY

### **PROBLÉM 2: SIGMOID v APPENDIXU**

**Soubory:**
- `appendix_microscopic_derivation_rev_cz.tex` (řádek 334-343)
- `appendix_microscopic_derivation_rev.tex` (anglická verze)

**Obsah:**
```latex
f_{\rm turn-on}(z, z_{\rm start}) = 1/(1 + exp(-k ln((1+z)/(1+z_start))))
```

**Použití:**
- Tento appendix je aktivní: \input na řádku 4559 hlavní monografie

**Doporučení:**
- BUĎTO: Odstranit celou sekci o sigmoidní funkci z appendixu
- NEBO: Přidat poznámku "Historical note (deprecated): Earlier drafts used..."

---

### **PROBLÉM 3: PREPRINT.TEX (ANGLICKÁ VERZE) NENÍ AKTUALIZOVANÁ**

**Soubor:** `latex_source/preprint.tex`

**Stav:**
- ✅ Abstract je aktualizován (obsahuje primordial freezeout)
- ❌ Tělo textu (Section 7) stále používá STARÉ paradigma:
  - Řádek 2035: "sigmoid turn-on function and physical justification"
  - Řádek 2041-2043: `E_pair(z) = E_0 + κ_conf · f_turn-on(z) · ln(1+z)`
  - Reference na Appendix o neutrino decoupling s sigmoidem

**Doporučení:**
- Aktualizovat tělo preprint.tex tak, aby odpovídalo české monografii
- Kapitoly 5, 7 a 9 v preprint.tex musí být revidovány

---

### **PROBLÉM 4: CHYBĚJÍCÍ INTEGRACE KAPITOLY 12**

**Vytvořené soubory (NEJSOU integrovány):**
- `chapter_12_numerical_intro.tex` - úvod do kapitoly 12
- `section_numerical_verification.tex` - numerická verifikace (3 testy)
- `section_12_4_phenomenology.tex` - Apollo anomálie, dualita QCT

**Aktuální stav:**
- Kapitola 12 v `monografie_QCT_munipress.tex` (řádek 4493) je STARÁ:
  - Název: "Numerické výpočty a validace"
  - Obsah: Hierarchie parametrů, matematické konstanty (zlatý řez!)
  - Toto je PŘED chirurgickými řezy!

**Doporučení:**
- Nahradit starou kapitolu 12 novými soubory:
  ```latex
  \chapter{Numerická verifikace QCT na mřížce}
  \input{latex_source/chapter_12_numerical_intro}
  \input{latex_source/section_numerical_verification}
  \input{latex_source/section_12_4_phenomenology}
  ```

---

## 🟢 CO FUNGUJE DOBŘE

### ✅ Numerologie odstraněna

**Kontrola appendixů:**
```bash
grep -n "\\label{app:golden-ratio" monografie_QCT_munipress.tex
# Výsledek: řádek 4567 zakomentován
```

**Status:**
- Appendix "Zlatý řez v Σ baryonech" - zakomentován ✅
- Appendix "Matematické konstanty" - zakomentován ✅
- Žádné aktivní reference na tyto appendixy ✅

---

### ✅ Exponent ξ = 1 teoreticky fixován

**Soubor:** `appendix_alpha_density_scaling_cz.tex`

**Obsah:**
```latex
ξ = 1  (teoreticky fixní)

V limitě nízkých energií (IR limit), kde je vlnová délka fononů λ >> d,
se kondenzát chová jako nestlačitelná kapalina.
δμ ∝ ρ_baryon^1  ⟹  ξ = 1 (exaktně)
```

**Status:** ✅ Perfektně provedeno

---

### ✅ Abstract konzistentní

**Soubory:**
- `monografie_QCT_munipress.tex` (řádek 271-286)
- `preprint.tex` (abstract sekce)

**Obsah:**
- Primordial freezeout paradigma ✅
- E_cond = 2×10^16 GeV fixní ✅
- Hierarchické potlačení (m_p/E_cond)^2 ✅
- Falsifikovatelná predikce (Pb/Al = 4.2) ✅

---

## 📋 AKČNÍ PLÁN PRO OPRAVU

### **PRIORITA 1: ODSTRANIT STARÉ PARADIGMA Z KAPITOL 5 A 7**

**Kapitola 5 (řádky ~1800-2320):**
1. **Odstranit/upravit:**
   - Všechny rovnice s `E_pair(z) = E_0 + κ·ln(1+z)`
   - Boxed equation (řádek 2293) - nahradit E_cond (fixní)
   - Sigmoid turn-on (řádek 2311)

2. **Nahradit:**
   ```latex
   % PŘED (ZASTARALÉ):
   E_{\mathrm{pair}}(z) = E_0 + \kappa_{\mathrm{conf}} \cdot \ln(1+z)

   % PO (SPRÁVNĚ):
   E_{\mathrm{cond}} = 2 \times 10^{16}\,\mathrm{GeV}
   \quad \text{(fixní od GUT epochy, bez evoluce)}
   ```

**Kapitola 7 (řádky ~2400-2470):**
1. **Odstranit:**
   - Řádek 2402: evoluce Λ_QCT(z) s E_0 + κ·ln(1+z)
   - Řádek 2468: "podporuje logaritmickou formu E_pair(z)"

2. **Zachovat:**
   - BBN konzistence (řádek 2509-2522) - toto je OK
   - Primordial freezeout sekce (2489-2507) - toto je perfektní

---

### **PRIORITA 2: AKTUALIZOVAT APPENDIX**

**Soubor:** `appendix_microscopic_derivation_rev_cz.tex`

**Akce:**
1. Odstranit sigmoid turn-on funkci (řádky 332-343)
2. Přepsat sekci "Evoluce párovací energie":
   ```latex
   \paragraph{Primordiální zamrznutí (2025 Revision).}

   V revidovaném paradigmatu vazebná energie \emph{nezevolvuje}
   s redshiftem. Kondenzát zamrzl při GUT phase transition:

   E_{\mathrm{cond}} = 2 \times 10^{16}\,\mathrm{GeV}
   \quad \text{(konstantní)}
   ```

---

### **PRIORITA 3: AKTUALIZOVAT PREPRINT.TEX**

**Soubor:** `latex_source/preprint.tex`

**Akce:**
1. Kapitola 7 (řádky ~2030-2073):
   - Odstranit reference na sigmoid
   - Nahradit E_pair(z) evolution za E_cond (fixed)
   - Odstranit reference na Appendix o cosmological evolution

2. Template z `monografie_QCT_munipress.tex`:
   - Zkopírovat kapitolu 7 (řádky 2471-2522) do preprint.tex
   - Přeložit do angličtiny

---

### **PRIORITA 4: INTEGROVAT KAPITOLU 12**

**Lokace:** `monografie_QCT_munipress.tex` řádek ~4493

**Akce:**
1. Zakomentovat starou kapitolu 12
2. Vložit nové soubory:
   ```latex
   \chapter{Numerická verifikace QCT na mřížce}
   \label{chap:numerical-verification}

   \input{latex_source/chapter_12_numerical_intro}

   \section{Numerická verifikace na mřížce}
   \label{sec:numerical-verification}
   \input{latex_source/section_numerical_verification}

   \input{latex_source/section_12_4_phenomenology}
   ```

3. Zkopírovat grafy do `figures/`:
   - pb_al_comparison.png
   - osmium_hires.png
   - density_scaling.png
   - phase_diagram.png

---

## 📊 STATISTIKA PROBLÉMŮ

| Kategorie | Počet | Kritičnost |
|-----------|-------|------------|
| Protichůdná paradigmata (E_pair vs E_cond) | 9 míst | 🔴 KRITICKÁ |
| Sigmoid v aktivních souborech | 3 soubory | 🟡 STŘEDNÍ |
| Neaktualizovaný preprint.tex | 1 soubor | 🟡 STŘEDNÍ |
| Chybějící integrace kapitoly 12 | 3 soubory | 🟡 STŘEDNÍ |
| Zastaralé reference | 0 | ✅ OK |
| Numerologie | 0 (odstraněno) | ✅ OK |

---

## 🎯 DOPORUČENÍ

### **SCÉNÁŘ A: Minimální oprava (1-2 hodiny práce)**

Zaměřit se pouze na KRITICKÉ problémy:
1. Projít kapitolu 5 a 7, nahradit všechny výskyty `E_pair(z) = E_0 + κ·ln(1+z)` za:
   ```latex
   E_{\mathrm{cond}} = 2 \times 10^{16}\,\mathrm{GeV}
   \text{(fixní od GUT epochy)}
   ```
2. Odstranit boxed equation (2293) s logaritmickou evolucí
3. Odstranit sigmoid (řádek 2311)

**Výsledek:** Monografie bude konzistentní, ale kapitola 12 chybí

---

### **SCÉNÁŘ B: Kompletní revize (4-6 hodin práce)**

Provést všechny opravy podle Akčního plánu:
1. ✅ Odstranit staré paradigma (Priority 1)
2. ✅ Aktualizovat appendix (Priority 2)
3. ✅ Aktualizovat preprint.tex (Priority 3)
4. ✅ Integrovat kapitolu 12 (Priority 4)

**Výsledek:** Publikaci-ready monografie s kompletní numerickou verifikací

---

## 🔍 METODOLOGIE AUDITU

**Použité nástroje:**
```bash
# Hledání sigmoid
grep -r "sigmoid" manuscripts/latex_source/

# Hledání E_pair evolution
grep -r "E_.*pair.*ln\|ln.*E_.*pair" manuscripts/

# Hledání E_cond
grep -n "E_{.*cond" manuscripts/monografie_QCT_munipress.tex

# Kontrola zakomentovaných appendixů
grep -n "\\label{app:golden-ratio" manuscripts/monografie_QCT_munipress.tex
```

**Kontrolované soubory:**
- `monografie_QCT_munipress.tex` (hlavní dokument, 4900+ řádků)
- `preprint.tex` (anglická verze)
- `appendix_microscopic_derivation_rev_cz.tex`
- `appendix_alpha_density_scaling_cz.tex`
- `section_primordial_stiffness.tex`
- `chapter_12_numerical_intro.tex`
- `section_numerical_verification.tex`
- `section_12_4_phenomenology.tex`

---

## ✍️ ZÁVĚR

Monografie obsahuje **excelentní vědeckou práci** (primordial freezeout mechanismus, numerická verifikace, dualita focusing/screening), ale trpí **nekonzistencí mezi starými a novými sekcemi**.

**Hlavní problém:** Kapitoly 5 a 7 nebyly kompletně aktualizovány po zavedení primordial freezeout paradigmatu. Obsahují protichůdné tvrzení o povaze vazebné energie (fixní vs. evoluční).

**Řešení:** Systematicky nahradit všechny reference na `E_pair(z) = E_0 + κ·ln(1+z)` za `E_cond = 2×10^16 GeV (fixní)`.

**Odhadovaný čas opravy:**
- Minimální (kritické problémy): 1-2 hodiny
- Kompletní (všechny problémy): 4-6 hodin

---

**Audit provedl:** Claude (Sonnet 4.5)
**Datum:** 2025-12-25
**Status:** ⚠️ Nalezeny kritické nekonzistence, doporučena revize před publikací
