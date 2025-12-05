# SOUHRN NAVRHOVANÝCH ZMĚN - BBN/G_eff Reference

**Datum:** 2025-11-18
**Status:** Připraveno ke schválení uživatelem

---

## 📋 PŘEHLED

Našel jsem **3 místa** v preprint.tex vyžadující aktualizaci odkazů na appendix A.2.

**Appendix A.2 (appendix_microscopic_derivation_rev.tex) JIŽ OBSAHUJE:**
- ✅ Fyzikální odvození z neutrino decoupling (z_dec ~ 4×10⁹)
- ✅ Konkrétní sigmoid turn-on funkci
- ✅ Opravenou G_eff formuli (bez τ³)
- ✅ BBN consistency tabulku

**Main text (preprint.tex) POTŘEBUJE AKTUALIZOVAT:**
- ❌ Sekce 5.9: Zmínky o neurčité f(t), žádné odkazy na appendix
- ❌ Sekce 5.1: Chybí poznámka o plné formě v appendixu
- ❌ Tabulka: Zastaralý termín "delayed confinement"

---

## 🎯 NAVRHOVANÉ ZMĚNY

### ZMĚNA 1: Sekce 5.9 - Radikální zkrácení + silné odkazy

**Lokace:** preprint.tex, řádky 1942-1989 (48 řádků)

**Původní:** Epoch I/II/III popis s neurčitou funkcí f(t)

**Nový návrh:**
- Zkráceno na ~35 řádků
- 4 konkrétní odkazy na appendix subsekce
- Zmínka o fyzikálním odvození z neutrino decoupling
- Zmínka o opravené G_eff formuli (bez τ³)
- Zachována BBN konzistence a testovatelné predikce

**Detailní text:** Viz `NAVRHOVA_ZMENA_SEKCE_5_9.txt`

**Odkazy použité:**
```latex
\ref{subsubsec:neutrino_decoupling}
\ref{subsec:cosmological_evolution}
\ref{eq:turnon_function}
\ref{subsubsec:geff_evolution_corrected}
\ref{subsubsec:bbn_consistency}
\ref{tab:bbn_z_start_range}
```

---

### ZMĚNA 2: Sekce 5.1 - Poznámka o plné formě

**Lokace:** preprint.tex, po řádku 1512

**Akce:** Přidat poznámku (~6 řádků)

**Text:**
```latex
\textbf{Note on condensate formation:} Equation~\eqref{eq:E_pair_evolution}
represents the simplified form valid after condensate formation. The complete
evolution includes a turn-on function accounting for gradual condensate
build-up after neutrino decoupling:
\begin{equation}
E_{\rm pair}(z) = E_0 + \kappa_{\rm conf} \cdot f_{\rm turn-on}(z, z_{\rm start}) \cdot \ln(1+z)
\end{equation}
where $z_{\rm start} \sim 10^{7}$--$10^8$ is physically derived from the
neutrino decoupling epoch ($z_{\rm dec} \sim 4 \times 10^9$). For the full
derivation, turn-on function, and BBN consistency, see
Appendix~\ref{subsec:cosmological_evolution}, particularly
\S\ref{subsubsec:neutrino_decoupling}.
```

**Detailní text:** Viz `NAVRHOVA_ZMENA_SEKCE_5_1.txt`

---

### ZMĚNA 3: Tabulka - Aktualizace termínu

**Lokace:** preprint.tex, řádek 2516

**Původní:**
```latex
$G(z)$ evolution & $\Delta G/G \sim 0.1$ (BBN$\to$now) & BBN boundary & delayed confinement \\
```

**Nový:**
```latex
$G(z)$ evolution & $\Delta G/G \sim 0.1$ (BBN$\to$now) & BBN boundary & neutrino decoupling (App.~\ref{subsubsec:neutrino_decoupling}) \\
```

**Detailní text:** Viz `NAVRHOVA_ZMENA_TABULKA.txt`

---

## ✅ DOPADY ZMĚN

### Pozitiva:
- ✅ Main text odkazuje na detailní odvození v appendixu
- ✅ Odstraněna zmínka o neurčité funkci f(t)
- ✅ Zdůrazněno fyzikální odvození (ne ad-hoc fitting)
- ✅ Zmíněna oprava G_eff formule
- ✅ Čtenář má jasné odkazy kde najít detaily

### Rizika:
- ⚠️ Sekce 5.9 je zkrácena o 27% - někomu se může zdát příliš stručná
- ⚠️ Čtenář musí jít do appendixu pro detaily (ale to je standardní)

### Alternativy:
- **Varianta B:** Zachovat délku sekce 5.9, jen přidat odkazy (bez zkrácení)
- **Varianta C:** Minimální změny (jen přidat \ref{} bez změny textu)

---

## 📊 STATISTIKA

| Položka | Hodnota |
|---------|---------|
| Počet změn | 3 |
| Přidané řádky | ~13 (Změna 2: 6, Změna 3: 0, Změna 1: +7 nových odkazů) |
| Odebrané řádky | ~13 (Změna 1: zkrácení o ~13 řádků) |
| Nové odkazy | 6 (\ref na appendix subsekce) |
| Odstraněné problémy | Neurčitá f(t), "delayed confinement", chybějící odkazy |

---

## 🚀 DALŠÍ KROKY

**KROK 3: Získat schválení uživatele**
- [ ] Uživatel zkontroluje návrhy
- [ ] Uživatel schválí/upraví/zamítne

**KROK 4: Implementace (po schválení)**
- [ ] Použít Edit tool pro Změnu 1 (sekce 5.9)
- [ ] Použít Edit tool pro Změnu 2 (sekce 5.1)
- [ ] Použít Edit tool pro Změnu 3 (tabulka)
- [ ] Commitnout a pushnout

**Odhadovaný čas implementace:** 15 minut

---

## ❓ OTÁZKY PRO UŽIVATELE

1. **Sekce 5.9:** Souhlasíte s radikálním zkrácením (Varianta A)?
   - Nebo preferujete zachovat délku a jen přidat odkazy (Varianta B)?

2. **Sekce 5.1:** Je poznámka dostatečně jasná?

3. **Tabulka:** Je změna termínu v pořádku?

4. **Chcete vidět další změny před implementací?**

---

**Připraveno ke schválení!** 🎯
