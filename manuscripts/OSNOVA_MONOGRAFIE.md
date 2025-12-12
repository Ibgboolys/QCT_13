# DETAILNÍ OSNOVA MONOGRAFIE QCT
## Mapování: preprint.tex → Monografie (český překlad)

**Datum:** 2025-12-12
**Zdroj:** `manuscripts/latex_source/preprint.tex` (Revision 5.6, 2853 řádků)
**Cíl:** `manuscripts/monografie_QCT_munipress.tex` (book class, česky)

---

## PŘEDNÍ ČÁST (Frontmatter) ✅ HOTOVO

### ✅ Titulní strana
- Název: *Teorie kvantové komprese: Mikroskopické odvození emergentní gravitace z neutrinového kondenzátu*
- Autoři: Boleslav Plhák, Marek Novák
- Status: **HOTOVO**

### ✅ Předmluva
- Filozofická motivace: "Prázdná metrika se nemůže zakřivovat"
- Proč neutrina jako substrát prostoročasu
- Struktura knihy, poděkování
- Status: **HOTOVO** (~4 strany)

### ✅ Obsah
- Automaticky generovaný z `\tableofcontents`
- Status: **HOTOVO**

---

## HLAVNÍ ČÁST (Mainmatter) - KAPITOLY 1-9

### KAPITOLA 1: Základy teorie kvantové komprese
**Zdroj:** preprint.tex, řádky 135-350 + 351-868
**Appendixy:**
- `appendix_microscopic_derivation_rev.tex` (34K)
- `QCT_hossenfelder_section_2_2_5_screening_conformal.tex` (7.2K)

**Obsah:**
1. **Úvod do QCT** (překlad z Abstract + řádky 135-230)
   - Základní hypotéza: prostoročas = neutrinový kondenzát
   - Analogová gravitace (Barceló, Visser)
   - Konformní rescaling a screening
   - Klíčové parametry (Tabulka 1, řádky 239-349)

2. **Konvence a jednotky** (řádky 145-229)
   - Přirozené jednotky ℏ=c=1
   - Konverzní faktory SI ↔ natural units
   - Notace: α_νG, α_conf, α_cosmo, α_EM
   - Notace: ρ_ent různé škály

3. **Neutrinový kondenzát Ψ_νν** (řádky 351-485)
   - Fundamentální pole: Ψ_νν(x,t) = |Ψ|e^(iθ)
   - Gross-Pitaevskiiho popis
   - Makroskopická vlnová funkce
   - Kosmické neutrinové pozadí (CνB)

**Odhadovaný rozsah:** 15-20 stran

---

### KAPITOLA 2: Odvození Einsteinových rovnic
**Zdroj:** preprint.tex, řádky 486-794
**Appendixy:**
- `appendix_kernel_eft_mapping.tex` (24K)
- `QCT_hossenfelder_section_4_3_acoustic_metric.tex` (11K)
- `QCT_hossenfelder_section_2_2_6_overdetermination.tex` (8.3K)

**Obsah:**
1. **Emergentní prostoročasová geometrie** (řádky 486-567)
   - Od kondenzátu ke geometrii
   - Prostorové korelace neutrinových párů
   - Abstrakcní entanglement space

2. **Gravitační konstanta a fázová koherence** (řádky 568-641)
   - G_eff = (|α|/2) G_N
   - Projekční objem V_proj ~ 70 cm³
   - Fázová koherence: ⟨e^(iφ)⟩ ~ 10^(-10)

3. **Submilimetrové stínění** (řádky 642-716)
   - f_screen = m_ν/m_p ≈ 10^(-10)
   - λ_screen^⊕ ≈ 40 μm (Země)
   - λ_screen^(space) ≈ 1 mm
   - Validace: Eöt-Wash experiment

4. **Geometrický původ screeningu** (řádky 717-836)
   - Konformní faktor Ω_QCT(r)
   - Akustická metrika g_μν^acoustic
   - Souvislost s analogovou gravitací

5. **Řešení paradoxu předeterminace** (řádky 837-931)
   - Hossenfelderův paradox
   - Kvantová koherence vs. klasická konformní parametrizace

6. **Mikroskopické odvození kernelu K_μνρσ** (řádky 932-998)
   - Mapování na EFT

**Odhadovaný rozsah:** 20-25 stran

---

### KAPITOLA 3: Odvození Maxwellových rovnic
**Zdroj:** preprint.tex, řádky 795-868
**Appendixy:**
- `appendix_vacuum_decomposition_56_2.tex` (16K)
- Část z `appendix_mathematical_constants.tex` (20K)

**Obsah:**
1. **Elektromagnetismus jako emergentní jev** (řádky 795-838)
   - Goldstoneův boson z U(1) breaking
   - A_μ = (ℏ/e_eff) ∂_μθ
   - Amplifikace efektivního náboje: e_eff² ~ 10^17

2. **Kvantizace náboje** (řádky 839-868)
   - Topologické víry
   - q = (1/2π)∮∇θ·dl = n·e
   - Automatická kvantizace

3. **Fotony jako emergentní excitace** (z Abstract, řádky 106-115)
   - Kolektivní módy kondenzátu
   - Gravitují (přispívají do T_μν), ale zanedbatelně (~10^(-32))

**Odhadovaný rozsah:** 10-12 stran

---

### KAPITOLA 4: Mikroskopické odvození vazebné energie E_pair
**Zdroj:** preprint.tex, řádky 869-1243
**Appendixy:**
- `QCT_hossenfelder_section_3_4_lagrangian_kappa.tex` (9.9K)
- Část z `appendix_cosmological_evolution_REPLACEMENT.tex` (14K)

**Obsah:**
1. **BCS gap equation pro elektroslaabý freeze-out** (řádky 872-927)
   - Slabá interakce mezi neutriny (Z⁰ exchange)
   - Coupling z flavor mixing
   - Gap Δ₀ ~ 100 GeV
   - Selhání standardního BCS: λ_BCS ~ 10^(-52)

2. **Kosmologické stlačování (confinement)** (řádky 928-982)
   - Analogie se strunovým napětím
   - String tension κ ~ Δ₀²
   - Integrace přes kosmologickou expanzi
   - E_pair(z) = E₀ + κ_conf ln(1+z)

3. **Numerický výsledek a semi-predikce** (řádky 983-1009)
   - E_pair(z=0) = 5.38 × 10^18 eV (kalibrovaný)
   - κ_conf ≈ 0.48 EeV
   - Faktor 1.5 shoda s muon g-2

4. **Lagrangeovské odvození konfinem konstanty** (řádky 1010-1243)
   - Efektivní hmotnost z lagrangiánu
   - Konformní evoluce
   - Spojení s κ_conf
   - Numerická evaluace: 4% shoda

**Odhadovaný rozsah:** 18-22 stran

---

### KAPITOLA 5: Efektivní teorie pole (EFT)
**Zdroj:** preprint.tex, řádky 1244-1497
**Appendixy:**
- `appendix_kernel_eft_mapping.tex` (24K) - hlavní zdroj
- `appendix_higgs_vev.tex` (14K)

**Obsah:**
1. **Základní lagrangián** (řádky 1244-1273)
   - Kompletní tabulka Wilsonových koeficientů
   - Parametry QCT

2. **Dynamika entanglement pole φ** (řádky 1274-1293)
   - Bianchiho konzervace

3. **Akustická metrika - interpretace** (řádky 1294-1497)
   - Akustická metrika z GP lagrangiánu
   - Konformní rescaling z modulace hustoty
   - Efektivní gravitační konstanta
   - Entanglement skalár jako konformní pole
   - Implikace pro fifth-force omezení

**Odhadovaný rozsah:** 12-15 stran

---

### KAPITOLA 6: Kosmologická evoluce parametrů
**Zdroj:** preprint.tex, řádky 1536-2288
**Appendixy:**
- `appendix_cosmological_evolution_REPLACEMENT.tex` (14K) - hlavní
- `Časová_evoluce_G_eff.tex` (2.1K)
- `QCT_hossenfelder_section_7_3_geometric_lambda.tex` (13K)

**Obsah:**
1. **Časová evoluce E_pair(t)** (řádky 1539-1667)
   - Decoupling neutrin: z_dec ~ 4×10⁹
   - Turn-on kondenzátu: z_start ~ 10⁷-10⁸
   - Fyzikální původ: neutrino decoupling

2. **Geometrický původ běžícího cutoffu** (řádky 1668-1994)
   - Časově závislý konformní faktor
   - Λ_QCT(z) evoluce z konformního scalingu
   - Numerická verifikace
   - Geometrická interpretace: konformní čas
   - Testovatelné predikce

3. **Příspěvky slabé a silné interakce** (řádky 1995-2017)

4. **Časová evoluce G_eff(t) a konzistence s BBN** (řádky 2018-2073)
   - Ġ/G ~ 10^(-10) yr^(-1)
   - BBN constraints

5. **CνB, evoluce ρ_ent a konzistence BBN/CMB** (řádky 2074-2120)

6. **Srovnání energetických hustot** (řádky 2121-2158)
   - Interpretace vazby hmotnosti

7. **Energetické účtování** (řádky 2159-2266)
   - Paradox nekonzistence
   - Řešení: trojitý mechanismus
   - Celkový výsledek
   - Testovatelné implikace

8. **Hubble tension a lokální variace** (řádky 2267-2288)
   - ACT DR6 a Planck framework
   - CMB neutrino phase-shift measurements
   - Konzistence s QCT

**Odhadovaný rozsah:** 25-30 stran

---

### KAPITOLA 7: Fenomenologie a testovatelné predikce
**Zdroj:** preprint.tex, řádky 2289-2633
**Appendixy:**
- `Appendix_Galactic_Dynamics.tex` (2.6K)
- Části z různých appendixů

**Obsah:**
1. **Submilimetrová gravitace** (řádky 2291-2358)
   - Environment-dependent screening
   - ISS vs. Země: Δλ ~ 2.5%
   - Eöt-Wash validace

2. **Galaktické rotační křivky** (řádky 2359-2388)
   - KRITICKÝ TEST!
   - V²_vac = √(G M a₀)
   - NGC 1560 a další galaxie
   - Bez temné hmoty!

3. **Astrophysická škála - validace** (řádky 2389-2487)
   - G_eff ≈ 0.9 G_N
   - Black hole shadows: 5% modifikace
   - Gravitační vlny: ringdown frekvence
   - σ₈ tension relief

4. **Equivalence principle** (řádky 2488-2556)
   - Composition-dependent effects
   - η < 10^(-18)

5. **Muon g-2** (řádky 2557-2616)
   - Λ_QCT = 107 TeV z muon anomalie
   - LFUV necessity: T_e/T_μ ≲ 1/60
   - Alternativy

6. **Běžící α(Q²)** (řádky 2617-2620)

7. **Oklo, EDM, spektroskopie** (řádky 2621-2627)

8. **Neutrina a oscilace** (řádky 2628-2630)

9. **Benchmark s nižším cutoffem** (řádky 2631-2633)
   - Λ = 14.85 TeV varianta

**Odhadovaný rozsah:** 20-25 stran

---

### KAPITOLA 8: Temná energie z saturace kondenzátu
**Zdroj:** preprint.tex - není explicitní sekce, ale je v Appendixu!
**Appendixy:**
- `appendix_dark_energy_from_saturation.tex` (19K) - **HLAVNÍ ZDROJ**

**Obsah:**
1. **Motivace: problém kosmologické konstanty**
   - Standardní QFT vs. pozorování
   - 120 řádů rozdíl

2. **Fyzikální mechanismus: saturace**
   - Evoluce E_pair
   - Uvolnění energie
   - Disipace

3. **Trojitý supresorní mechanismus**
   - Suppression 1: Coherence fraction (f_c ~ 10^(-10))
   - Suppression 2: Nonlocal averaging (f_avg)
   - Suppression 3: Topological freezing (f_freeze)

4. **Finální výsledek: ρ_Λ^QCT**
   - Predikce temné energie
   - Srovnání s pozorováním

5. **Řešení problému kosmologické konstanty**
   - Srovnání s naivním QFT očekáváním
   - Absence vacuum energy catastrophe

6. **Testovatelné predikce**
   - Equation of state w(z)
   - Korelace s neutrinovou hmotností
   - CMB constraints

7. **Limitace a otevřené otázky**
   - Mechanismus topological freezing
   - Faktor nonlocal averaging
   - Přesnost z_sat

8. **Srovnání s alternativními modely**

**Odhadovaný rozsah:** 15-18 stran

---

### KAPITOLA 9: Teoretické otázky
**Zdroj:** preprint.tex, řádky 2672-2814
**Appendixy:**
- `appendix_weinberg_witten.tex` (16K) - hlavní
- `appendix_bh.tex` (13K)
- Části z `QCT_hossenfelder_appendix_N_6_black_hole_PG.tex` (12K)

**Obsah:**
1. **Unitarita a platnost EFT** (řádky 2672-2674)
   - Omezení platnosti teorie
   - μ ≲ (0.2-0.3) Λ_QCT

2. **UV outline a Weinberg-Wittenův teorém** (řádky 2675-2681)
   - Motivace a rozsah
   - Formulace WW teorému
   - Klíčové předpoklady
   - QCT evasion mechanismus: nelokalita
   - Stress tensor pouze po průměrování přes V_proj

3. **Černé díry v QCT**
   - Modifikace Schwarzschildovy metriky
   - Event horizon vs. condensate physics
   - No singularities (konečná kompresibilita)

4. **Grand Unification prospects**
   - Zlatý řez ve Yukawa sektorech?
   - CFT s φ-symetrií?
   - Topologický původ (cosmic strings)?

**Odhadovaný rozsah:** 12-15 stran

---

## ZADNÍ ČÁST (Backmatter) ✅ HOTOVO

### ✅ Závěr
- Shrnutí hlavních výsledků
- Empirická validace
- Testovatelné predikce
- Otevřené otázky (E_pair discrepancy, cirkulární logika, post-hoc vzorce)
- Budoucí směry (2025-2035 experimentální program)
- Implikace pro fundamentální fyziku
- Status: **HOTOVO** (~12 stran)

### ✅ Summary (anglicky)
- Kompletní anglické shrnutí pro RIV
- Status: **HOTOVO** (~6 stran)

### ⏳ Seznam použité literatury
- Bibliografie dle ČSN ISO 690
- Status: **PŘIPRAVENO** (třeba doplnit citace)

### ⏳ Rejstřík
- Automaticky generovaný
- Status: **PŘIPRAVENO**

---

## APPENDIXY - Volitelně pro monografii

**Dostupné LaTeX appendixy** (můžeme vybrat relevantní):
1. `appendix_microscopic_derivation_rev.tex` (34K) - ✅ použít pro Kap. 1-2
2. `appendix_kernel_eft_mapping.tex` (24K) - ✅ použít pro Kap. 5
3. `appendix_mathematical_constants.tex` (20K) - ✅ příloha A
4. `appendix_dark_energy_from_saturation.tex` (19K) - ✅ použít pro Kap. 8
5. `appendix_golden_ratio.tex` (18K) - ✅ příloha B (zlatý řez)
6. `appendix_weinberg_witten.tex` (16K) - ✅ použít pro Kap. 9
7. `appendix_vacuum_decomposition_56_2.tex` (16K) - ✅ příloha C
8. `appendix_higgs_vev.tex` (14K) - ✅ příloha D
9. `appendix_cosmological_evolution_REPLACEMENT.tex` (14K) - ✅ použít pro Kap. 6
10. Další podle potřeby...

**Doporučené přílohy pro monografii:**
- **Příloha A:** Matematické konstanty v QCT (e, π, ln10)
- **Příloha B:** Zlatý řez a φ^12 hierarchie
- **Příloha C:** Vakuová dekompozice 56+2
- **Příloha D:** Higgs VEV postdikce

---

## SOUHRN ROZSAHU

| Část | Odhadovaný rozsah |
|------|-------------------|
| Předmluva | 4 strany |
| Kapitola 1 | 15-20 stran |
| Kapitola 2 | 20-25 stran |
| Kapitola 3 | 10-12 stran |
| Kapitola 4 | 18-22 stran |
| Kapitola 5 | 12-15 stran |
| Kapitola 6 | 25-30 stran |
| Kapitola 7 | 20-25 stran |
| Kapitola 8 | 15-18 stran |
| Kapitola 9 | 12-15 stran |
| Závěr | 12 stran |
| Summary | 6 stran |
| **CELKEM** | **~180-220 stran** |

---

## POSTUP PSANÍ

### Fáze 1: Překlad hlavních kapitol (priorita)
1. ✅ Předmluva - HOTOVO
2. ⏳ Kapitola 1 (Základy QCT) - **ZAČÍT ZDE**
3. ⏳ Kapitola 2 (Einstein equations)
4. ⏳ Kapitola 3 (Maxwell equations)

### Fáze 2: Technické kapitoly
5. ⏳ Kapitola 4 (E_pair derivation)
6. ⏳ Kapitola 5 (EFT)
7. ⏳ Kapitola 6 (Cosmological evolution)

### Fáze 3: Fenomenologie
8. ⏳ Kapitola 7 (Predictions & tests)
9. ⏳ Kapitola 8 (Dark energy)

### Fáze 4: Závěr a doladění
10. ⏳ Kapitola 9 (Theoretical issues)
11. ✅ Závěr - HOTOVO
12. ✅ Summary - HOTOVO
13. ⏳ Bibliografie (doplnit citace)
14. ⏳ Appendixy (přeložit vybrané)

---

## POZNÁMKY K PŘEKLADU

### Terminologie (EN → CS):
- Quantum Compression Theory → Teorie kvantové komprese
- Neutrino condensate → Neutrinový kondenzát
- Entangled pairs → Zapletené páry
- Screening factor → Screening faktor / Stínicí faktor
- Projection radius → Projekční poloměr
- Phase coherence → Fázová koherence
- Conformal rescaling → Konformní přeškálování
- Acoustic metric → Akustická metrika
- Emergent gravity → Emergentní gravitace
- Binding energy → Vazebná energie
- Confinement → Uvěznění / Konfinement
- Dark energy saturation → Saturace temné energie

### Stylistika:
- Vědecký styl, objektivní jazyk
- Autorský plurál: "Ukázali jsme..."
- České uvozovky: „..."
- České čárky v číslech: 0,2 (ne 0.2)
- Mezery v číslech ≥ 10 000

### Rovnice:
- Zachovat LaTeX notaci
- České popisky: "kde" (ne "where")
- České definice veličin

---

**Datum vytvoření osnovy:** 2025-12-12
**Autor osnovy:** Claude (AI asistent)
**Pro:** Boleslav Plhák, Marek Novák
**Účel:** Monografie QCT pro Nakladatelství Masarykovy univerzity (Munipress)
