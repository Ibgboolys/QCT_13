# KOMPLETNÍ SEZNAM MÍST K OPRAVĚ - BBN/G_eff evoluce

**Datum:** 2025-11-18
**Účel:** Promítnout řešení z appendix A.2 do main textu preprint.tex

---

## 🎯 HLAVNÍ PROBLÉMOVÁ MÍSTA

### 1. SEKCE 5.9: Time evolution of G_eff(t) and BBN consistency
**Lokace:** preprint.tex, řádky 1942-1989 (48 řádků)
**Label:** Žádný (jen subsection)

**Současný obsah:**
- Řádek 1944: "\subsubsection{Phasing of condensation and confinement}"
- Řádky 1948-1960: Popis Epoch I/II/III s neurčitou funkcí f(t)
- Řádek 1960: `f` is a smooth "turn-on" function (**NESPECIFIKOVÁNO**)
- Řádky 1962-1982: BBN consistency check s epsilon_early
- Řádky 1984-1989: Testable prediction

**Co chybí:**
- ❌ Žádný odkaz na appendix A.2
- ❌ Žádná zmínka o neutrino decoupling jako fyzikálním původu
- ❌ Žádná konkrétní rovnice pro f(t)
- ❌ Žádná zmínka o z_start ~ 10^7-10^8 odvození
- ❌ Žádná zmínka o opravené G_eff formuli (bez τ³)

**Co je v appendixu A.2 (UŽ HOTOVÉ):**
- ✅ A.2.1 (řádky 256-322): Fyzikální odvození z neutrino decoupling
- ✅ A.2.2 (řádky 323-361): Konkrétní sigmoid funkce
- ✅ A.2.3 (řádky 362-384): Opravená G_eff formule
- ✅ A.2.4 (řádky 385-428): BBN tabulka s z_start rozsahem

**Doporučená akce:** PŘEPSAT celou sekci 5.9 (nebo radikálně zkrátit + silné odkazy)

---

### 2. SEKCE 5.1: Time evolution of binding energy E_pair(t)
**Lokace:** preprint.tex, řádky 1493-1515
**Label:** `\section{sec:cosmo_evolution}` (řádek 1491)
**Equation label:** `eq:E_pair_evolution` (řádek 1498)

**Současný obsah:**
```latex
E_pair(t) = E_0 + κ_conf ln(a(t)/a_0) = E_0 + κ_conf ln(1+z)
```

**Problém:**
- Toto je ZJEDNODUŠENÁ forma (bez turn-on funkce)
- Chybí poznámka, že plná forma je v appendixu
- Equation \ref{eq:E_pair_evolution} se používá na 3 místech (1088, 1697, 1803)

**Doporučená akce:** Přidat poznámku:
```latex
\textbf{Note:} This simplified form applies after condensate formation.
For the complete evolution including turn-on function and BBN consistency,
see Appendix~\ref{subsec:cosmological_evolution}.
```

---

### 3. ODKAZY NA eq:E_pair_evolution
**Lokace:** 4 místa v preprint.tex

**Řádek 1088:**
```latex
Comparing with the phenomenological form (Eq.~\ref{eq:E_pair_evolution}):
```
**Status:** ✅ OK (obecný odkaz)

**Řádek 1472:**
```latex
...which arises from cosmological confinement (see Section~\ref{sec:cosmo_evolution}).
```
**Status:** ✅ OK (obecný odkaz na sekci)

**Řádek 1697:**
```latex
The binding energy E_pair(z) evolves according to Eq.~\ref{eq:E_pair_evolution}:
```
**Status:** ✅ OK (používá zjednodušenou formu)

**Řádek 1803:**
```latex
From logarithmic evolution (Eq.~\ref{eq:E_pair_evolution}):
```
**Status:** ✅ OK (kontext: porovnání s konformní evolucí)

**Doporučená akce:** Žádná změna potřebná (odkazy fungují správně)

---

### 4. ODKAZY NA app:microscopic
**Lokace:** 2 místa v preprint.tex

**Řádek 1537:**
```latex
See Appendix~\ref{app:microscopic} for breaking circular reasoning.
```
**Status:** ✅ OK (odkaz na celý appendix A)

**Řádek 2525:**
```latex
Circular reasoning between Λ_QCT ↔ E_pair explicitly broken
(see Appendix~\ref{app:microscopic}).
```
**Status:** ✅ OK (odkaz na celý appendix A)

**Doporučená akce:** Žádná změna (odkazy fungují)

---

### 5. TABULKA: Predictions Summary
**Lokace:** preprint.tex, řádek 2516
**Kontext:** Table~\ref{tab:predictions_summary}

**Současný text:**
```latex
$G(z)$ evolution & $\Delta G/G \sim 0.1$ (BBN$\to$now) & BBN boundary & delayed confinement \\
```

**Problém:**
- Termín "delayed confinement" je zastaralý (připomíná ad-hoc fine-tuning)
- Chybí odkaz na fyzikální odvození

**Doporučená akce:** Změnit na:
```latex
$G(z)$ evolution & $\Delta G/G \sim 0.1$ (BBN$\to$now) & BBN boundary & neutrino decoupling (App.~A.2) \\
```

---

## 📋 SOUHRN AKCÍ

### PRIORITA 1: Musí se opravit
- ✅ **Akce 1.1:** Přepsat/aktualizovat sekci 5.9 (řádky 1942-1989)
  - Přidat odkazy na appendix A.2.1-A.2.4
  - Specifikovat sigmoid funkci nebo odkázat na appendix
  - Zmínit fyzikální odvození z neutrino decoupling
  - Zmínit opravenou G_eff formuli

### PRIORITA 2: Doporučeno
- ✅ **Akce 2.1:** Přidat poznámku do sekce 5.1 (po řádku 1502)
  - Odkaz na appendix A.2 pro plnou formu s turn-on

- ✅ **Akce 2.2:** Aktualizovat tabulku (řádek 2516)
  - "delayed confinement" → "neutrino decoupling (App. A.2)"

### PRIORITA 3: Volitelné
- ⏸️ **Akce 3.1:** Zkontrolovat cross-references po změnách
- ⏸️ **Akce 3.2:** Přidat \label pro subsekce 5.9 (pro budoucí odkazy)

---

## 🔍 SUBSEKCE APPENDIXU A.2 (Pro odkazy)

**Appendix A má tyto subsekce (z našeho čtení):**

```latex
\subsection{Cosmological Evolution of Parameters}
\label{subsec:cosmological_evolution}  % Řádek 252

\subsubsection{Physical Origin of Condensate Turn-On: Neutrino Decoupling}
\label{subsubsec:neutrino_decoupling}  % Řádek 257

\subsubsection{Time Dependence of E_pair}
% Žádný label (řádek 323)

\subsubsection{Evolution of G_eff: Corrected Formula}
\label{subsubsec:geff_evolution_corrected}  % Řádek 363

\subsubsection{BBN Consistency with Physically Derived Parameters}
\label{subsubsec:bbn_consistency}  % Řádek 386
```

**Poznámka:** Labels jsou převzaté z appendixu - použijeme je pro odkazy!

---

## ✅ STATUS

**Krok 1: Najít všechna místa** - ✅ HOTOVO
**Krok 2: Navrhnout změny** - ČEKÁ (další krok)
**Krok 3: Schválení** - ČEKÁ
**Krok 4: Implementace** - ČEKÁ

---

**Celkem míst k úpravě:** 3 hlavní (sekce 5.9, sekce 5.1 poznámka, tabulka)
**Odhadovaný čas:** 20-30 minut implementace
