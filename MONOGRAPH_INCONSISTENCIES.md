# ⚠️ Nalezené Nesrovnalosti v Monografii

**Datum:** 2025-12-20
**Kontext:** Systematická kontrola konzistence po dark energy analýze

---

## 🔴 KRITICKÁ CHYBA: E_sat vzorec v preprint.tex

### Soubor: `manuscripts/latex_source/preprint.tex`

**Lines 1895-1896:**
```latex
E_{\rm pair}^{\rm (sat)} \sim \frac{\Lambda_{\rm QCT}^2}{m_p}
                          \approx \frac{(107\,{\rm TeV})^2}{0.938\,{\rm GeV}}
                          \approx 1.2 \times 10^{22}\,{\rm eV}
```

**CHYBA:** Používá **m_p** (proton mass) v jmenovateli!

### Srovnání s Appendixem:

**File:** `appendix_dark_energy_from_saturation.tex` **Line 36:**
```latex
E_{\rm sat} \sim \frac{\Lambda_{\rm QCT}^2}{m_\nu}
             = \frac{(1.07 \times 10^{14}\,{\rm eV})^2}{0.1\,{\rm eV}}
             \approx 1.1 \times 10^{29}\,{\rm eV}
```

**SPRÁVNĚ:** Používá **m_ν** (neutrino mass)!

### Diskrepance:

| Parametr | preprint.tex | appendix (správně) | Poměr |
|----------|--------------|-------------------|-------|
| Jmenovatel | m_p = 938 MeV | m_ν = 0.1 eV | 10¹⁰ |
| E_sat | 1.2×10²² eV | 1.1×10²⁹ eV | 10⁷ |

**DOPAD:** Faktor **10 milionů** chyba v saturační energii!

---

## 🔴 NESROVNALOST: z_sat vzorec

### preprint.tex (line 1891):
```latex
z_{\rm sat} \sim \exp\left(\frac{\Lambda_{\rm QCT}^2}{m_p \kappa_{\rm conf}}\right) - 1 \approx 10^6
```

**Problémy:**
1. Opět používá **m_p** místo m_ν
2. Tvrdí že lze **vypočítat** z_sat z vzorce

### appendix_dark_energy_from_saturation.tex (lines 44-51):

```latex
z_{\rm sat} \sim 10^6
```

Citace (line 48):
> "A naive logarithmic extrapolation to E_sat would yield
> z_sat ~ exp(E_sat/κ_conf) >> 10⁶, which is **unphysical**
> (predating the Big Bang). This breakdown indicates that
> the saturation mechanism involves **UV physics beyond the
> logarithmic regime**."

**SPRÁVNĚ:** z_sat ~ 10⁶ je **FENOMENOLOGICKY ZVOLEN**, nelze vypočítat!

---

## 🔴 NESROVNALOST: Triple suppression factors

### preprint.tex (line 1901):
```latex
\rho_{\Lambda}^{\rm QCT} = \rho_{\rm sat} \times f_c \times f_{\rm avg} \times f_{\rm freeze}
```

**Hodnoty v preprint.tex:**
- f_c ~ 10⁻¹⁰ ✓
- f_avg ~ **10⁻³⁹** ❌
- f_freeze ~ 5×10⁻⁸ ✓

**Celková suprese:** 10⁻⁵⁷

### appendix_dark_energy_from_saturation.tex (lines 100, 144, 177):

**Hodnoty v appendixu:**
- f_c = 1.07×10⁻¹⁰ ✓ (rigorous, line 100)
- f_avg ~ **O(1)** ✓ (order-of-magnitude estimate, line 144)
- f_freeze ~ 6.7×10⁻⁹ ✓ (phenomenological, line 177)

**Celková suprese:** ~10⁻¹⁸

### Diskrepance:

| Faktor | preprint.tex | appendix (správně) | Rozdíl |
|--------|--------------|-------------------|--------|
| f_avg | 10⁻³⁹ | O(1) | **10³⁹!** |

**CHYBA:** preprint.tex má f_avg o **39 řádů** menší!

---

## 🔴 DŮSLEDEK: Nekonzistentní výpočet ρ_Λ

### preprint.tex přístup:
```
ρ_Λ = (n_ν × E_sat) × 10⁻⁵⁷
```

Používá:
- E_sat = 1.2×10²² eV (CHYBNĚ, m_p místo m_ν)
- Celková suprese 10⁻⁵⁷ (CHYBNĚ, f_avg ~ 10⁻³⁹)

### appendix přístup (SPRÁVNĚ):
```
ρ_Λ = ρ_pairs(z=0) × f_c × f_avg × f_freeze
    = (n_ν,0 × E_pair(0)) × (1.07×10⁻¹⁰) × (1) × (6.7×10⁻⁹)
```

Používá:
- E_pair(0) = 5.38×10¹⁸ eV (dnešní hodnota, kalibrovaná)
- f_c rigorózní, f_avg ~ 1, f_freeze fenomenologický

**Klíčový rozdíl:**
- preprint: počítá z **saturační energie** při z_sat
- appendix: počítá z **dnešní energie** při z=0

---

## 📋 Co Je Třeba Opravit

### 1. preprint.tex (lines 1891-1904)

**Oprava line 1896:**
```latex
E_{\rm pair}^{\rm (sat)} \sim \frac{\Lambda_{\rm QCT}^2}{m_\nu}  % OPRAVENO: m_p → m_ν
                          \approx \frac{(107\,{\rm TeV})^2}{0.1\,{\rm eV}}
                          \approx 1.1 \times 10^{29}\,{\rm eV}  % OPRAVENO: 10^22 → 10^29
```

**Oprava line 1891:**
```latex
% Phenomenologically, saturation occurs at:
z_{\rm sat} \sim 10^6  % OPRAVENO: Odstraněn nefyzikální exp() vzorec
```

Přidat poznámku:
```latex
\emph{Note:} A naive extrapolation $z_{\rm sat} \sim \exp(\Lambda^2/(m_\nu \kappa))$
would yield unphysically high redshifts. The value $z_{\rm sat} \sim 10^6$ is
chosen phenomenologically for consistency with BBN/CMB constraints.
```

**Oprava line 1901:**
```latex
\rho_{\Lambda}^{\rm QCT} &= \rho_{\rm pairs}(z=0) \times f_c \times f_{\rm avg} \times f_{\rm freeze} \\
&= (n_{\nu,0} \times E_{\rm pair}(0)) \times (10^{-10}) \times (1) \times (6.7 \times 10^{-9}) \\
&\approx 10^{-47}\,{\rm GeV}^4 \quad \checkmark
```

**NEBO** odkazovat na appendix:
```latex
See Appendix~\ref{app:dark_energy} for complete triple suppression derivation.
```

### 2. Zkontrolovat další odkazy na m_p v kontextu saturace

Hledat všechny instance:
```bash
grep -n "m_p.*sat\|sat.*m_p\|Lambda.*m_p" manuscripts/latex_source/*.tex
```

---

## ✅ Co Je Správně (Appendix)

### appendix_dark_energy_from_saturation.tex:

**SPRÁVNĚ:**
- ✅ E_sat = Λ²/m_ν = 1.1×10²⁹ eV (line 36)
- ✅ z_sat ~ 10⁶ fenomenologický (lines 44-51)
- ✅ f_c = m_ν/m_p rigorózní (line 100)
- ✅ f_avg ~ O(1) odhad (line 144)
- ✅ f_freeze ~ 6.7×10⁻⁹ fenomenologický (line 177)
- ✅ Počítá z ρ_pairs(z=0), ne z_sat (lines 84-90)
- ✅ Otevřeně přiznává co je odvozeno vs fenomenologické (lines 300-337)

**Tento appendix je VZOR** jak to má být!

---

## 🎯 Doporučení

### Priorita 1: Opravit preprint.tex

**Kritické chyby:**
1. m_p → m_ν v E_sat vzorci (line 1896)
2. Odstranit nebo opravit z_sat vzorec (line 1891)
3. f_avg 10⁻³⁹ → O(1) (line 1901)

### Priorita 2: Sjednotit přístup

**Rozhodnout:**
- Používat preprint přístup (z saturace) → vyžaduje velké změny
- **NEBO** používat appendix přístup (z dnešní hodnoty) → jednodušší a správnější

**Doporučuji:** Appendix přístup je správnější a rigoroznější!

### Priorita 3: Prohledat další soubory

Zkontrolovat zda další .tex soubory nemají stejné chyby:
- E_sat s m_p místo m_ν
- Nefyzikální z_sat vzorce
- Nesprávné f_avg hodnoty

---

## 📊 Status

**Identifikováno:** 3 kritické nesrovnalosti v preprint.tex
**Ověřeno správné:** appendix_dark_energy_from_saturation.tex
**Další kontrola:** Ostatní .tex soubory

**Připraveno k opravě** ✓
