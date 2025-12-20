# ❓ Potřebuji Objasnění Integrální Formule E_pair(z)

**Datum:** 2025-12-20
**Status:** IMPLEMENTACE - NUMERICKÉ PROBLÉMY

---

## Co jsem implementoval

Na základě tvé reformulace jsem vytvořil:

```python
E_pair(z) = E_0 + κ_conf × ∫_z^{z_start} [f_turnon(z', z_start) / (1+z')] dz'
```

S parametry:
- E_0 = 0.1 eV
- κ_conf = 0.48×10¹⁸ eV (0.48 EeV)
- z_start = 10⁸
- k = 2.0

---

## Problémy, které vidím

### 1. **Numerické výsledky nesedí s tvými tvrzeními**

**Moje výsledky:**
```
E_pair(0) = 8.68×10¹⁸ eV   (target: 5.38×10¹⁸ eV) ❌
E_pair(BBN)/E_pair(0) = ~0  (target: 0.84) ❌
```

**Tvé tvrzení:**
```
"Numerické ověření: E_pair(BBN)/E_pair(0) ≈ 0.84"
```

### 2. **Problém se směrem f_turnon**

Tvrdíš: f_turnon(10⁹, 10⁸) ≈ 0.84

**Můj test s KLADNÝM znaménkem:**
```python
f(z, z_start) = 1 / [1 + exp(+k × ln((1+z)/(1+z_start)))]

f(10⁹, 10⁸) = 1 / [1 + exp(+2 × ln(10))]
            = 1 / [1 + exp(4.6)]
            = 1 / [1 + 100]
            ≈ 0.01  ❌ (ne 0.84!)
```

**Můj test se ZÁPORNÝM znaménkem:**
```python
f(z, z_start) = 1 / [1 + exp(-k × ln((1+z)/(1+z_start)))]

f(10⁹, 10⁸) = 1 / [1 + exp(-2 × ln(10))]
            = 1 / [1 + exp(-4.6)]
            = 1 / [1 + 0.01]
            ≈ 0.99  ❌ (taky ne 0.84!)
```

**S log₁₀ místo ln (záporné znaménko):**
```python
f(z, z_start) = 1 / [1 + exp(-k × log10((1+z)/(1+z_start)))]

f(10⁹, 10⁸) = 1 / [1 + exp(-2 × log10(10))]
            = 1 / [1 + exp(-2 × 1)]
            = 1 / [1 + exp(-2)]
            = 1 / [1 + 0.135]
            ≈ 0.88  ✓ (blízko 0.84!)
```

**→ Používáš log₁₀ místo ln?**

### 3. **Problém s integrálovými mezemi**

Pro z = 10⁹ (BBN) a z_start = 10⁸:

```python
Integrál ∫_{10⁹}^{10⁸} [f(z') / (1+z')] dz' = -0.34  (ZÁPORNÝ!)
```

To dává:
```
E_pair(10⁹) = 0.1 + 0.48×10¹⁸ × (-0.34) < 0  ❌ (záporné!)
```

**Možná řešení:**
- Použít |integrál|?
- Integrovat od z do nějakého z_max místo z_start?
- Jiná formulace?

### 4. **Problém s E_pair(0)**

S integrálem od 0 do 10⁸:
```
∫_0^{10⁸} [f(z') / (1+z')] dz' ≈ 18.07  (blízko ln(1+10⁸) = 18.42)
```

To dává:
```
E_pair(0) = 0.1 + 0.48×10¹⁸ × 18.07 = 8.67×10¹⁸ eV
```

Ale target je 5.38×10¹⁸ eV!

**→ Potřebuji jiné κ_conf?**
```
κ_conf = (5.38×10¹⁸ - 0.1) / 18.07 ≈ 2.98×10¹⁷ eV (0.298 EeV)
```

---

## Co potřebuji objasnit

### ❓ Otázka 1: Přesný vzorec f_turnon

Která z těchto variant je správná?

**A) Kladné znaménko, přirozený logaritmus (ln):**
```python
f(z, z_start) = 1 / [1 + exp(+k × ln((1+z)/(1+z_start)))]
```

**B) Záporné znaménko, přirozený logaritmus (ln):**
```python
f(z, z_start) = 1 / [1 + exp(-k × ln((1+z)/(1+z_start)))]
```

**C) Záporné znaménko, dekadický logaritmus (log₁₀):**
```python
f(z, z_start) = 1 / [1 + exp(-k × log10((1+z)/(1+z_start)))]
```

**D) Něco jiného:**
```python
f(z, z_start) = ???
```

### ❓ Otázka 2: Meze integrálu

Která z těchto formulí je správná?

**A) Od z do z_start (tvoje původní formulace):**
```python
E_pair(z) = E_0 + κ × ∫_z^{z_start} [f(z') / (1+z')] dz'
```
Problém: Pro z > z_start je integrál ZÁPORNÝ!

**B) Od z do nějakého z_max:**
```python
E_pair(z) = E_0 + κ × ∫_z^{z_max} [f(z') / (1+z')] dz'
```
Kde z_max = ???

**C) Absolutní hodnota:**
```python
E_pair(z) = E_0 + κ × |∫_z^{z_start} [f(z') / (1+z')] dz'|
```

**D) Podmíněně:**
```python
if z < z_start:
    E_pair(z) = E_0 + κ × ∫_z^{z_start} [f(z') / (1+z')] dz'
else:
    E_pair(z) = E_0  # Nebo nějaký jiný vzorec?
```

### ❓ Otázka 3: Hodnota κ_conf

Tvrdíš κ_conf ≈ 0.48 EeV, ale to dává E_pair(0) ≈ 8.7×10¹⁸ eV.

**Měl bych použít:**
- A) κ_conf = 0.48 EeV (tvoje hodnota)
- B) κ_conf ≈ 0.30 EeV (aby E_pair(0) = 5.38×10¹⁸ eV)
- C) Jiná hodnota?

### ❓ Otázka 4: Numerická verifikace

Můžeš mi prosím potvrdit, že s TVÝMI parametry dostáváš:
```
E_pair(0) ≈ 5.38×10¹⁸ eV  ✓
E_pair(10⁹) / E_pair(0) ≈ 0.84  ✓
f_turnon(10⁹, 10⁸) ≈ 0.84  ✓
```

**Jaký přesný Python kód používáš?**

---

## Můj současný kód (pro referenci)

```python
def f_turnon(z, z_start=1e8, k=2.0):
    """Zatím používám KLADNÉ znaménko."""
    arg = +k * np.log((1.0 + z) / (1.0 + z_start))  # ln, ne log10!
    arg = np.clip(arg, -700, 700)
    return 1.0 / (1.0 + np.exp(arg))

def E_pair(z):
    """Integrál od z do z_start."""
    integral, _ = quad(
        lambda z_p: f_turnon(z_p, 1e8, 2.0) / (1.0 + z_p),
        z,          # dolní mez
        1e8,        # horní mez (z_start)
        limit=100
    )
    return 0.1 + 0.48e18 * integral
```

**Výsledky:**
```
E_pair(0) = 8.68×10¹⁸ eV  (ne 5.38!)
E_pair(10⁹) ≈ 0.1 eV  (ratio ~ 0, ne 0.84!)
```

---

## Co mám udělat dál?

1. **Počkat na tvoje objasnění** správného vzorce
2. **Opravit implementaci** podle tvých instrukcí
3. **Znovu spustit validaci** a ověřit boundary conditions
4. **Pokračovat v simulacích** až bude vzorec správný

**Prosím o upřesnění výše uvedených otázek, abych mohl pokračovat!** 🙏

---

**Status:** ⏸️ ČEKÁM NA OBJASNĚNÍ
