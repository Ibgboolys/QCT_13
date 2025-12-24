# Kvantitativní odvození faktoru α_micro / α_phenom ≈ 2200

**Datum:** 2025-12-21
**Autor:** Systematická analýza QCT parametrů
**Status:** PRACOVNÍ DOKUMENT - vyžaduje peer review

---

## ÚVOD

V české monografii QCT (ř. 668-683) je konstatována diskrepance mezi mikroskopickým odhadem a fenomenologickou kalibrací parametru α:

```
α_micro / α_phenom ≈ 2,2 × 10³
```

Jsou uvedeny TŘI spekulativní důvody:
1. Efektivní renormalizace v baryonovém prostředí
2. Časová evoluce od elektroslabyého freeze-outu
3. Limitace poruchové teorie

**ALE:** Žádný z těchto důvodů není kvantitativně odvozen v monografii.

**CÍL TOHOTO DOKUMENTU:** Vytvořit explicitní kvantitativní výpočet faktoru ~2200 z prvních principů, nebo identifikovat PŘEKÁŽKY, které brání takovému výpočtu.

---

## PŘEHLED PROBLÉMU

### Mikroskopický odhad (z monografie ř. 658-666)

```latex
α_micro ~ -(E_pair / m_ν c²) / (n_ν V_proj)
α_micro ~ -5,38 × 10^19 / (2,4 × 10^4) ≈ -2 × 10^15
```

### Fenomenologická kalibrace (ř. 639-654)

```latex
α_phenom = (K_⊕ - 1) / (Φ_⊕/c²)
         = 624 / (-6,95 × 10^-10)
         ≈ -9 × 10^11
```

### Poměr
```
α_micro / α_phenom ≈ 2,2 × 10³
```

---

## POKUS 1: Renormalizace škálou Λ_baryon

### Hypotéza

V appendix_microscopic_derivation_rev_cz.tex (ř. 544-549) je odvozeno:

```
Λ_baryon / Λ_micro = √(m_p / m_ν) ≈ 9,7 × 10^4
```

**Pokus:** Spojit tento poměr škál s poměrem α.

### Analýza dimenzí

α má dimenze **bezrozměrné** (vstupuje do rovnice n_ν(r) = n_ν,0 × [1 + α Φ/c²])

Λ má dimenze **[energie]**

**Problém:** Není zřejmé, jak bezrozměrný poměr energetických škál přímo dá bezrozměrný poměr α.

### Možná cesta: Renormalizační grupa (RG)

V efektivní teorii pole běžící vazba může být:

```
α(μ) = α(μ₀) × [1 + β log(μ/μ₀) + ...]
```

kde β je beta-funkce.

**Pro QCT:**
- μ₀ = Λ_micro (mikroskopická škála kondenzátu)
- μ = Λ_baryon (škála interakce s baryony)

Poměr:
```
log(Λ_baryon / Λ_micro) = log(9,7 × 10^4) ≈ 11,48
```

**Potřebný faktor:**
```
α_micro / α_phenom ≈ 2200

→ Pokud α(Λ_baryon) / α(Λ_micro) = 1/2200

→ β × 11,48 ≈ -log(2200) ≈ -7,7

→ β ≈ -0,67
```

### ❌ PŘEKÁŽKA 1: Záporná beta-funkce není standardní

- V QCD, β > 0 (asymptotická volnost)
- V QED, β > 0 (screening)
- β < 0 by znamenalo **anti-screening** (neobvyklé)

### ❌ PŘEKÁŽKA 2: Chybí odvození beta-funkce

Monografie neobsahuje:
- Explicitní Lagrangián pro neutrino-baryonovou interakci
- Feynmanovy diagramy 1-loop korekcí
- Výpočet beta-funkce β(g) pro vazbu α

**ZÁVĚR POKUSU 1:** Hypotéza možná, ale **NENÍ KVANTITATIVNĚ ODVOZENA** v monografii.

---

## POKUS 2: Časová evoluce od freeze-outu

### Hypotéza

Parametr α mohl být odlišný při elektroslabyém freeze-outu (T ~ 100 GeV, z ~ 10^15) a evolvoval do současné hodnoty.

### Mechanismus

Hustota neutrin škáluje s redshiftem:
```
n_ν(z) = n_ν,0 × (1 + z)³
```

Chemický potenciál:
```
μ(z) = g × n_ν(z) × m_ν
```

**Možná evoluce α:**
```
α(z) ~ -E_pair(z) / [m_ν c² × n_ν(z) × V_proj(z)]
```

### Problém: Jak evolvuje E_pair?

Z monografie (sekce 7, kosmologická evoluce):
```
E_pair(z) ~ κ_conf × ln(1 + z)
```

Pro z → 0:
```
E_pair(0) ~ κ_conf × ln(1) = 0 ❌ Nefyzikální!
```

**Správnější** (z appendixu):
```
E_pair(z) = E_pair(0) - κ_conf × ln(1 + z)
```

Ale to dává **KLESAJÍCÍ** E_pair v minulosti, ne rostoucí!

### ❌ PŘEKÁŽKA 3: Nejasná evoluce E_pair

Monografie obsahuje **rozporuplné** rovnice pro E_pair(z):
- Sekce 3.3.2 (ř. 1734): E_pair = κ_conf × ln(1+z) / něco
- Appendix kosmologické evoluce: E_pair(z) = E_pair(0) - ΔE

**CHYBĚJÍCÍ:** Konzistentní odvození evoluce E_pair od freeze-outu do dnes.

### Pokus o odhad

Předpokládejme (spekulativně):
- Při freeze-outu: n_ν(z_fo) ~ 10^15 × n_ν,0
- Dnes: n_ν(0) = n_ν,0

Poměr:
```
α(z_fo) / α(0) ~ n_ν(0) / n_ν(z_fo) ~ 1 / 10^15 ❌
```

To je **OPAČNÝ směr** než potřebujeme! (α_micro > α_phenom, ne <)

**ZÁVĚR POKUSU 2:** Časová evoluce **NEMŮŽE** vysvětlit faktor 2200 směrem "holá vazba větší než efektivní".

---

## POKUS 3: Limitace poruchové teorie

### Hypotéza

Vztah α_micro ~ -E_pair / (m_ν n_ν V_proj) je pouze **první řád** poruchové teorie.

Vyšší řády mohou obsahovat potlačující faktory.

### Možné korekce

**1. Faktor F_proj místo n_ν × V_proj:**

Z appendixu:
- F_proj (empirický) = 2,43 × 10^4
- n_ν × V_proj = 336 × 72,3 = 2,43 × 10^4 ✓

(Stejné, žádná korekce)

**2. Fázový koherenční faktor:**

Z monografie:
```
f_coh ~ exp(-σ²/2) ~ 0,37
```

Pro σ² ~ 2. To dává redukci faktorem **0,37**, ne **1/2200**!

**3. Screening faktor f_screen:**

```
f_screen = m_ν / m_p ~ 10^-10
```

ALE tento faktor už JE v odvození G_eff (appendix, eq. G_eff_final), ne v α!

### ❌ PŘEKÁŽKA 4: Žádný známý QFT mechanismus pro faktor ~10³

V standardní kvantové teorii pole:
- 1-loop korekce: faktory ~(1 + α log μ) ~ O(1-10)
- 2-loop: ~ α² ~ O(0,01)
- Neperturbativní efekty (instanton): ~ exp(-1/g²)

**Faktor 2200 je příliš velký** pro běžné radiační korekce, ale **příliš malý** pro neperturbativní potlačení.

**ZÁVĚR POKUSU 3:** Standardní mechanismy QFT **NEDÁVAJÍ** faktor ~10³.

---

## POKUS 4: Kombinace efektů

### Hypotéza "3 faktory"

Co pokud všechny TŘI efekty přispívají multiplikativně?

```
Faktor celkem = f_renorm × f_evoluce × f_PT
Cíl: 2200
```

**Potřebný rozklad:**

Například:
```
2200 ≈ 10 × 10 × 22
```

nebo:
```
2200 ≈ 47 × 47 × 1
```

### Problém: Ad hoc rozklad

**Pokud NENÍ ODVOZENO**, že:
- Renormalizace dává faktor X
- Evoluce dává faktor Y
- PT limitace dává faktor Z

**PAK** tvrzení "kombinace efektů" je **spekulace bez kvantitativního základu**.

### ❌ PŘEKÁŽKA 5: Chybí nezávislé odvození každého faktoru

Monografie neobsahuje:
- Explicitní výpočet f_renorm z RG rovnic
- Explicitní výpočet f_evoluce z kosmologické historie
- Explicitní výpočet f_PT z vyšších řádů GP rovnice

**ZÁVĚR POKUSU 4:** Kombinace je možná hypotéza, ale **NENÍ PODLOŽENA** výpočty.

---

## ALTERNATIVNÍ INTERPRETACE

### Možnost A: α_micro není správný vztah

**Hypotéza:** Poruchový vztah α ~ -E_pair / (m_ν n_ν V_proj) je **kvalitativní odhad řádu velikosti**, ne přesná předpověď.

**Důvod:** GP rovnice s gravitační vazbou je **silně nelineární**:
```
iℏ ∂Ψ/∂t = [-ℏ²∇²/(2m_ν) + g|Ψ|² + m_ν Φ(r)]Ψ
```

V režimu silné vazby (g|Ψ|² >> m_ν Φ), klasická poruchová teorie **selhává**.

**Důsledek:** Faktor 2200 není "chyba", ale odráží **neplatnost poruchového přiblížení**.

### Možnost B: α je primárně fenomenologický parametr

**Alternativa:** Parametr α **NENÍ** odvozený z mikroskopické teorie, ale je **kalibrovaný** k experimentálním datům (Eöt-Wash).

Mikroskopický vztah slouží pouze k **kvalitativnímu pochopení**, ne kvantitativní predikci.

**Analogie:** V QCD, strong coupling αs(μ) je měřen experimentálně a pak "běží" podle RG. Ale primární hodnota je **fenomenologická**.

---

## ZÁVĚR ANALÝZY

### Hlavní nálezy

1. ✅ **Poměr škál existuje:** Λ_baryon / Λ_micro ≈ 9,7 × 10^4 (blízko α_micro / α_phenom)

2. ❌ **CHYBÍ spojení:** Není odvozeno, jak poměr škál dává poměr α

3. ❌ **RG beta-funkce:** Není vypočítána pro QCT (PŘEKÁŽKA 1)

4. ❌ **Evoluce E_pair:** Rozporuplné rovnice, nejasný freeze-out (PŘEKÁŽKA 3)

5. ❌ **PT korekce:** Standardní mechanismy nedávají faktor ~10³ (PŘEKÁŽKA 4)

6. ❌ **Kombinace:** Bez nezávislých výpočtů je spekulace (PŘEKÁŽKA 5)

### Identifikované PŘEKÁŽKY pro kvantitativní odvození

| # | Překážka | Popis | Co chybí |
|---|----------|-------|----------|
| 1 | RG beta-funkce | Potřeba β < 0 (neobvyklé) | Explicitní 1-loop výpočet β(g) |
| 2 | Lagrangián interakce | Neutrino-baryon coupling neuspecifikován | L_int s fenomenologickými konstantami |
| 3 | Evoluce E_pair | Rozporuplné rovnice | Konzistentní odvození E_pair(z) |
| 4 | PT selhání | GP nelinearity v silném režimu | Neperturbativní metody (lattice?) |
| 5 | Kombinace efektů | Ad hoc rozklad faktoru | Nezávislé výpočty každého příspěvku |

---

## DOPORUČENÍ

### Pro autory monografie

**VARIANTA A: Rigorózní odvození**

Pokud má být tvrzení o "renormalizaci + evoluce + PT limitace" vědecky podloženo, je NUTNÉ:

1. **Odvodit RG rovnice** pro α(μ) včetně beta-funkce
2. **Vypočítat časovou evoluci** α(z) od freeze-outu s konzistentní E_pair(z)
3. **Kvantifikovat PT korekce** z GP rovnice (nebo lattice simulace)
4. **Ukázat numericky**, že kombinace dává faktor ~2200

**Odhad pracnosti:** Několik měsíců práce, vyžaduje expertízu v:
- Kvantové teorii pole (RG výpočty)
- Kosmologii (freeze-out termodynamika)
- Kondenzovaných látek (nelineární GP dynamika)

**VARIANTA B: Poctivé přiznání**

Pokud rigorózní odvození není (zatím) možné, transparentnější přístup:

```latex
\textbf{Diskrepance a status:}

Mikroskopický odhad a fenomenologická kalibrace se liší faktorem ~10⁴.

\textbf{Možná vysvětlení (zatím kvalitativní):}
1. Renormalizace škálou Λ_baryon/Λ_micro ~ 10⁴
2. Časová evoluce od elektroslabyého freeze-outu
3. Limitace poruchové teorie v nelineárním režimu GP rovnice

\textbf{Současný status:} Tyto mechanismy jsou fyzikálně plausibilní,
ale NEJSOU kvantitativně odvozeny. Parametr α je proto používán jako
**fenomenologická konstanta** kalibrovaná k experimentům (Eöt-Wash).

Kvantitativní odvození faktoru 2200 je otevřený teoretický problém
vyžadující:
- RG analýzu neutrino-baryonové vazby
- Kosmologickou evoluci α(z)
- Neperturbativní řešení GP rovnice

\textbf{Pro praktické výpočty} používáme α_phenom = -9 × 10^11
(kalibrované).
```

### Pro recenzenty

**POŽADOVAT:**
- Buď kvantitativní odvození faktoru 2200, NEBO
- Poctivé přiznání, že α je primárně fenomenologický parametr

**NEPŘIJÍMAT:** Spekulativní výčet mechanismů bez výpočtů jako "vysvětlení".

---

## POZNÁMKY K VĚDECKÉ POCTIVOSTI

Tento dokument byl vytvořen podle principů:

1. **Transparentnost:** Explicitně uvedeny VŠECHNY pokusy a jejich selhání
2. **Poctivost:** Identifikovány konkrétní PŘEKÁŽKY, ne vágní tvrzení
3. **Falzifikovatelnost:** Navrženy konkrétní výpočty, které by mohly potvrdit/vyvrátit hypotézy
4. **Vědecká metoda:** Od hypotézy → test → závěr (ne od závěru → hledání podpory)

**Výsledek:** Faktor 2200 **NENÍ** v současné monografii kvantitativně odvozen. Je to **otevřený teoretický problém**.

---

**Datum:** 2025-12-21
**Status:** Analýza dokončena
**Další kroky:** Předložit autorům pro response nebo implementaci Varianty B

