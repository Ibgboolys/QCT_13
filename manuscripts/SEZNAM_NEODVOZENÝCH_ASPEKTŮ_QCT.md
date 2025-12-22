# SEZNAM ASPEKTŮ KTERÉ NEJSOU DOSTATEČNĚ ODVOZENY V MONOGRAFII QCT

**Datum:** 2025-12-21
**Analyzovaný dokument:** `manuscripts/monografie_QCT_munipress.tex`
**Metoda:** Systematický průchod všech klíčových parametrů a tvrzení

---

## SHRNUTÍ

Monografie obsahuje **11 kritických oblastí** s nedostatečnými odvozeními, rozdělených do 4 kategorií:

1. **Primární fitované parametry** (4 položky)
2. **Diskrepance a nesrovnalosti** (3 položky)
3. **Post-hoc vzorce bez odvození** (3 položky)
4. **Cirkulární závislosti** (1 položka)

**Celkem:** 11 aspektů vyžadujících další teoretickou práci

---

## KATEGORIE 1: PRIMÁRNÍ FITOVANÉ PARAMETRY

### 1.1 ❌ α_νG (neutrino-gravitační vazba)

**Status:** Fenomenologická konstanta kalibrovaná k experimentům

**Hodnota:** α_νG ≈ -9 × 10^11

**Problém:**
- Mikroskopické odvození dává: α_micro ≈ -2 × 10^15
- Fenomenologická kalibrace: α_phenom ≈ -9 × 10^11
- **Diskrepance: faktor ~2200** (3 řády velikosti!)

**Navrhovaná vysvětlení (NEJSOU kvantitativně odvozena):**
1. Renormalizace škálou Λ_baryon/Λ_micro ≈ 9.7 × 10^4
   - ❌ **CHYBÍ:** Spojení poměru škál s poměrem α
   - ❌ **CHYBÍ:** RG beta-funkce β(g)
2. Časová evoluce od freeze-outu
   - ❌ **CHYBÍ:** Kvantitativní výpočet α(z)
   - ❌ **CHYBÍ:** Konzistentní evoluce E_pair(z)
3. Nelineární efekty GP rovnice
   - ❌ **CHYBÍ:** Neperturbativní řešení

**Lokace v monografii:**
- Hlavní text: ř. 668-689 (nyní transparentně přiznáno)
- Appendix: appendix_microscopic_derivation_rev_cz.tex:582

**Dopad:** α je používán v CELÉ teorii (screening length, evoluce koherence), ale je primárně fenomenologický!

---

### 1.2 ❌ E_pair (vazebná energie neutrinového páru)

**Status:** Kalibrován na současnou hodnotu G_eff

**Hodnota:** E_pair = 5.38 × 10^18 eV

**Problém:** DVĚ METODY výpočtu se liší o **faktor 10^16**!

**Metoda 1: Logaritmický integral**
```
E_pair ~ ∫ κ_conf d ln(1+z) ~ 10^18 eV ✓ (používaná hodnota)
```

**Metoda 2: Konformní scaling**
```
E_pair ~ Ω_QCT^4 × (...) ~ 10^34 eV ❌ (NESROVNALOST!)
```

**Navrhované řešení (NENÍ rigorózně odvozeno):**
- Saturace kondenzátu při z_sat ~ 10^6
- Nonlineární matching conditions
- ❌ **CHYBÍ:** Explicitní odvození saturačního mechanismu

**Lokace:** Sekce 3.670-3.678 (otevřené otázky)

**Dopad:** E_pair je KLÍČOVÝ parametr - ovlivňuje Λ_QCT, G_eff, celou kosmologickou evoluci!

---

### 1.3 ⚠️ σ²_max (saturovaná fázová variance)

**Status:** Fitováno z astrofyzikálních dat

**Hodnota:** σ²_max = 0.2

**Problém:**
- Mikroskopický výpočet (volný prostor): σ²_max ≈ 3.1
- Fenomenologická hodnota (Země): σ²_max ≈ 0.2
- **Diskrepance: faktor 15**

**Navrhované řešení (semi-odvozeno):**
```
σ²_max(K) = σ²_cosmo + σ²_baryon / K^β
```
kde:
- σ²_cosmo ≈ 0.21 (ireducibilní kosmický šum)
- σ²_baryon,0 ≈ 2.89 (baryonový baseline)
- β ≈ 1.37 (BCS suppression exponent)
- K = 1 + α_νG Φ/c²

**Status řešení:** ✅ Dvou-komponentní model existuje a funguje

**ALE:** β = 1.37 je **fitovaný parametr**!

**Lokace:**
- Tabulka parametrů: ř. 786
- Řešení diskrepance: appendix_kernel_eft_mapping_cz.tex

**Dopad:** Ovlivňuje predikce gravitační síly na různých škálách

---

### 1.4 ⚠️ λ (self-interaction coupling)

**Status:** Fitovaný parametr

**Hodnota:** λ ~ 6 × 10^-2

**Problém:**
- ❌ **NENÍ odvozeno** z mikroskopických principů
- Vstupuje do GP rovnice jako volný parametr
- Ovlivňuje healing length, koherenční vlastnosti

**Lokace:** Uvedeno v tabulce fitovaných parametrů

**Dopad:** Střední závažnost - ovlivňuje detaily kondenzátové dynamiky

---

## KATEGORIE 2: DISKREPANCE A NESROVNALOSTI

### 2.1 ❌ V_proj empirické vs. odvozené (rozdíl 32%)

**Odvozeno z konstant:**
```
V_proj = (4π/3) R_proj³ = 49.4 cm³
```

**Empirické (z fitování):**
```
V_proj = F_proj / n_ν = 72.3 cm³
```

**Diskrepance:** 31.6% (faktor 1.46)

**Navrhovaná vysvětlení:**
- Vyšší řádové korekce v coarse-graining
- Nehomogenita kondenzátu
- ❌ **CHYBÍ:** Kvantitativní výpočet korekcí

**Lokace:** appendix_units_numerical_audit_cz.tex:15-18

**Dopad:** Ovlivňuje všechny projekční výpočty (G_eff, screening, atd.)

---

### 2.2 ⚠️ F_proj empirické vs. odvozené (rozdíl 32%)

**Odvozeno:**
```
F_proj = n_ν × V_proj_derived = 1.66 × 10^4
```

**Empirické:**
```
F_proj = 2.43 × 10^4 (z fitování na G_N)
```

**Diskrepance:** 31.7%

**Souvisí s V_proj** - stejný problém, jiná forma

**Lokace:** appendix_microscopic_derivation_rev_cz.tex:514-517

---

### 2.3 ⚠️ κ_conf (konformní konstanta) - faktor 1.8

**Lagrangeovská predikce:**
```
κ_conf^predikce = E_pair / 35 ≈ 0.15 EeV
```

**Kalibrovaná hodnota:**
```
κ_conf^kalibrace = 0.48 EeV
```

**Diskrepance:** Faktor 3.2

**Autor tvrdí:** "Shoda v rámci faktoru 1.04" (ř. 1860)
**REALITA:** To je po přepočtu - původní diskrepance je faktor ~3!

**Lokace:** ř. 1734, 1746, 1858-1860

**Dopad:** Ovlivňuje kosmologickou evoluci E_pair(z)

---

## KATEGORIE 3: POST-HOC VZORCE BEZ ODVOZENÍ

Autor EXPLICITNĚ přiznává (ř. 3692-3705): *"Následující vztahy byly nalezeny PO měřeních (postdikce)"*

### 3.1 ⚠️ Higgs VEV via zlatý řez

**Vzorec:**
```
v = Λ_micro × φ^12.088 = 246.18 GeV
```

kde φ = (1+√5)/2 = 1.6180... (zlatý řez)

**Přesnost:** 0.015% (experimentální v = 246.22 GeV)

**Problém:**
- ❌ **NENÍ odvozeno** PROČ zlatý řez
- ❌ **NENÍ odvozeno** PROČ exponent 12.088
- Nalezeno POST-HOC (po měření Higgse 2012)

**Status:** **POSTDIKCE**, ne predikce!

**Navrhované směry (NEJSOU vypracovány):**
- Geometrický původ φ v Higgsově potenciálu
- Skupina-teoretická interpretace exponentu
- Testovatelnost: kosmologická evoluce v(z)

**Lokace:** ř. 3694, Appendix Higgs VEV

---

### 3.2 ⚠️ Celková entropie S_tot = n_ν/6 + 2

**Vzorec:**
```
S_tot = n_ν/6 + 2 = 336/6 + 2 = 58 (přesně!)
```

**Další vzor:**
```
S_tot / 21 ≈ e (Eulerovo číslo, 1.6% přesnost)
```

**Problém:**
- ❌ **NENÍ odvozeno** PROČ n_ν/6
- ❌ **NENÍ odvozeno** PROČ +2
- ❌ **NENÍ odvozeno** spojení s e

**Navrhované směry:**
- Skupinově-teoretická interpretace
- Spojení s flavor symetrií?

**Lokace:** ř. 3695-3696

---

### 3.3 ⚠️ Matematické konstanty v f_screen

**Vzorec:**
```
ln ln(1/f_screen) ≈ π (0.16% přesnost)
```

**Problém:**
- ❌ **NENÍ odvozeno** PROČ π
- Pouze empirické pozorování

**Navrhované směry:**
- Topologický původ π konstant v QCT parametrech

**Lokace:** ř. 3697

---

## KATEGORIE 4: CIRKULÁRNÍ ZÁVISLOSTI

### 4.1 ❌ CIRKULÁRNÍ LOOP: E_pair ↔ Λ_QCT ↔ g-2

**Problém (autor EXPLICITNĚ přiznává, ř. 3682):**

```
1. E_pair je kalibrován na G_eff (současnost)
   ↓
2. Λ_QCT = (3/2)√(E_pair × m_p) se vypočítá z E_pair
   ↓
3. Λ_QCT se shoduje s muon g-2 fitem (107 TeV)
   ↓
4. TVRZENÍ: "Shoda validuje teorii!" ❌ CIRKULÁRNÍ!
```

**Realita:**
- E_pair není nezávisle odvozen
- Shoda s g-2 je **důsledek kalibrace**, ne nezávislá validace

**Navrhované řešení transparentnosti:**
1. Jasně deklarovat kalibrační loop
2. Přeinterpretovat jako "consistency check", ne predikci

**Lokace:** Sekce 3.680-3.688

**Dopad:** **KRITICKÝ** - podkopává tvrzení o prediktivní síle teorie!

---

## DOPLŇUJÍCÍ PROBLEMATICKÉ OBLASTI

### 5.1 ⚠️ Screening length λ_screen = 40 μm

**Status:** Fenomenologická kalibrace (NYNÍ transparentně přiznáno)

**Problém:**
- α_νG je fitován TAK, aby K_⊕ = 625
- S K = 625 vychází λ = 40 μm
- ❌ NENÍ to predikce, ale zpětný fit k Eöt-Wash!

**Opraveno v revizi:** ✅ Nyní označeno jako "fenomenologická kalibrace"

**SKUTEČNÁ testovatelná predikce:**
- ISS vs. Země: λ_ISS/λ_⊕ = √(625/590) = 1.029 (2.9% rozdíl)
- ✅ Toto JE falzifikovatelné!

---

### 5.2 ⚠️ Časová evoluce G_eff(z)

**Tvrzení:** Ġ/G ~ 10^-10 yr^-1

**Problém:**
- Závisí na evoluci E_pair(z)
- E_pair(z) má diskrepanci 10^16 mezi dvěma metodami!
- ❌ **NEJASNÉ** jak spolehlivě počítat G(z)

**Lokace:** Kapitola 7 (kosmologická evoluce)

---

### 5.3 ⚠️ Galaktické rotační křivky - parametr a₀

**Tvrzení:** QCT reprodukuje rotační křivky pomocí V_vac = (G M_bar a₀)^1/4

**Problém:**
- a₀ je **volný parametr** fitovaný k datům
- Není odvozeno z QCT principů
- Podobné MOND (tam je a₀ také fitován)

**Lokace:** Kapitola 8 (fenomenologie)

---

## KATEGORIE PODLE ZÁVAŽNOSTI

### 🔴 KRITICKÉ (vyžadují OKAMŽITOU pozornost)

1. **α_νG diskrepance faktorem 2200** - klíčový parametr celé teorie!
2. **E_pair diskrepance 10^16** - dvě metody dávají naprosto rozdílné hodnoty
3. **Cirkulární loop E_pair ↔ Λ_QCT** - podkopává tvrzení o validaci

### 🟡 VÝZNAMNÉ (vyžadují teoretickou práci)

4. **σ²_max - β parameter fitován** (ale dvou-komponentní model existuje)
5. **V_proj / F_proj rozdíl 32%** - ovlivňuje všechny projekční výpočty
6. **Post-hoc vzorce** (Higgs VEV, S_tot, π konstanty) - fascinující, ale není odvození

### 🟢 MENŠÍ (akceptovatelné v EFT kontextu)

7. **λ self-interaction** - standardní EFT parametr
8. **κ_conf faktor 3** - v rámci neperturbativní fyziky přijatelné
9. **a₀ v galaktických křivkách** - fenomenologický model (jako MOND)

---

## STATISTIKA

**Celkem analyzováno:** 15 klíčových aspektů teorie

**Kategorizace:**
- ❌ **Neodvozeno/nesrovnalost:** 11 aspektů (73%)
- ✅ **Odvozeno dostatečně:** 4 aspekty (27%)
  - R_proj z fundamentálních konstant (11.8% rozdíl) ✓
  - f_screen = m_ν/m_p (odvozeno přesně) ✓
  - Zlatý řez v Σ baryonech (numericky OK, ale post-hoc) ⚠️
  - Screening závislost na prostředí (mechanismus OK) ✓

---

## DOPORUČENÍ PRO AUTORY

### Kritická priorita (před publikací NUTNÉ):

1. **Vyřešit α_νG diskrepanci:**
   - Buď odvodit faktor 2200 kvantitativně, NEBO
   - Jasně deklarovat α jako primárně fenomenologický parametr ✅ (HOTOVO v revizi)

2. **Vyřešit E_pair diskrepanci 10^16:**
   - Explicitní odvození saturačního mechanismu
   - Nebo přiznat, že konformní scaling metoda je chybná

3. **Rozpustit cirkulární loop:**
   - Jasně označit E_pair → Λ_QCT jako consistency check
   - Ne jako nezávislou predikci

### Střední priorita (zlepšení teorie):

4. Odvodit β parameter pro σ²_max z BCS teorie (ne fitovat)
5. Vysvětlit 32% diskrepanci V_proj (vyšší řádové korekce?)
6. Teoreticky odvodit post-hoc vzorce (φ, S_tot, π)

### Dlouhodobá výzkumná agenda:

7. UV completion (Weinberg-Witten obchází se přes nelokalitu - OK, ale vyžaduje důkaz)
8. Kvantová verze GP rovnice pro neperturbativní režim
9. Lattice simulace neutrino-baryonové vazby

---

## TRANSPARENTNOST - CO AUTOR UŽ PŘIZNÁVÁ

### ✅ V sekci "Otevřené teoretické otázky" (ř. 3665-3706):

1. ✅ E_pair diskrepance 10^16 (explicitně uvedeno)
2. ✅ Cirkulární loop E_pair ↔ Λ_QCT (explicitně uvedeno)
3. ✅ Post-hoc vzorce vyžadují odvození (explicitně uvedeno)

### ✅ Po naší revizi (nyní přidáno):

4. ✅ α_νG diskrepance 2200 (transparentně přiznáno jako otevřený problém)
5. ✅ λ_screen = 40 μm je kalibrace, ne predikce (opraveno v appendixu)

---

## ZÁVĚR

**Monografie obsahuje 11 aspektů s nedostatečnými odvozeními**, z toho:
- 🔴 **3 kritické** (α_νG, E_pair, cirkulární loop)
- 🟡 **5 významných** (σ²_max, V_proj, post-hoc vzorce)
- 🟢 **3 menší** (λ, κ_conf, a₀)

**Pozitivní:**
- Autor většinu problémů PŘIZNÁVÁ v sekci "Otevřené otázky"
- Po revizi je transparentnost VÝRAZNĚ zlepšena
- Skutečné testovatelné predikce (ISS, M87*) jsou jasně označeny

**Doporučení:**
Monografie je **publikovatelná S EXPLICITNÍM PŘIZNÁNÍM TĚCHTO LIMITACÍ**, které už většinou obsahuje. Kritické je, aby recenzent a čtenář viděli rozdíl mezi:
- ✅ Co JE odvozeno (R_proj, f_screen, screening mechanismus)
- ⚠️ Co je POST-HOC (Higgs VEV, matematické vzorce)
- ❌ Co NENÍ odvozeno (α_νG faktor 2200, E_pair diskrepance)
- 🔄 Co je CIRKULÁRNÍ (E_pair → Λ_QCT → g-2)

---

**Dokument vytvořil:** Claude Code AI Agent
**Datum:** 2025-12-21
**Metoda:** Systematický průchod celé monografie + appendixů
**Status:** Kompletní analýza

