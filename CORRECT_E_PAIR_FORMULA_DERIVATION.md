# ✅ CORRECT E_pair(z) Formula Derivation

**Date:** 2024-12-20
**Purpose:** Derive the physically correct E_pair(z) evolution from QCD-like confinement

---

## Physical Setup

### Boundary Conditions (from manuscript claims)

1. **Today (z=0):**
   - E_pair(0) ≈ 10¹⁹ eV (LARGEST - cosmic evolution has maximized pairing)
   - G_eff(0) = G_N (Newton's constant as measured)

2. **BBN (z ~ 10⁹):**
   - E_pair(10⁹) ≈ 0.84 × E_pair(0) (SMALLER - less cosmic evolution)
   - G_eff(10⁹) ≈ 0.84 × G_N (constraint: |ΔG/G| < 20%)

3. **Neutrino decoupling (z ~ 4×10⁹):**
   - E_pair(z_dec) ≈ E_0 ~ m_ν ≈ 0.1 eV (SMALLEST - condensate just forming)

### Evolution Direction

**E_pair INCREASES with cosmic time (DECREASES with z):**
- Early universe (large z): Small E_pair ~ 0.1 eV
- Today (z=0): Large E_pair ~ 10¹⁹ eV

**This is 10¹⁹ eV / 0.1 eV = 10²⁰ growth factor over cosmic history!**

---

## Step 1: Derivation from Scale Factor

### QCD-like Confinement Integral

From `cosmological_corrections.tex:17-18`, the pairing energy grows as:

```
E_pair(t) = E_0 + κ_conf × ∫₀ᵗ H(t') dt'
```

where H(t) is the Hubble parameter.

### Integral Evaluation

The integral of H(t) over cosmic time:

```
∫₀ᵗ H(t') dt' = ∫₀ᵗ (1/a)(da/dt') dt' = ∫ᵃ⁽ᵗ⁾ da/a = ln(a(t)/a_initial)
```

where a_initial is the scale factor at some reference time (e.g., decoupling).

### Formula in Terms of a(t)

```
E_pair(t) = E_0 + κ_conf × ln(a(t)/a_dec)
```

where:
- **E_0** = E_pair at decoupling ≈ m_ν ≈ 0.1 eV
- **a_dec** = scale factor at decoupling

---

## Step 2: Conversion to Redshift

### Scale Factor Relations

The scale factor relates to redshift as:
```
a(z) = a_0 / (1+z)
a_dec = a_0 / (1+z_dec)
```

where a_0 is the scale factor today (typically normalized to 1).

### Scale Factor Ratio

```
a(z) / a_dec = [a_0/(1+z)] / [a_0/(1+z_dec)]
              = (1+z_dec) / (1+z)
```

### Logarithm

```
ln(a(z)/a_dec) = ln[(1+z_dec)/(1+z)]
                = ln(1+z_dec) - ln(1+z)
```

---

## Step 3: The Correct Formula

### Without Turn-On Function

Substituting into E_pair(t):

```
E_pair(z) = E_0 + κ_conf × [ln(1+z_dec) - ln(1+z)]
```

Rearranging:

```
E_pair(z) = [E_0 + κ_conf × ln(1+z_dec)] - κ_conf × ln(1+z)
```

Define **E_max = E_0 + κ_conf × ln(1+z_dec) = E_pair(z=0)**, then:

```
✅ E_pair(z) = E_max - κ_conf × ln(1+z)
```

### With Turn-On Function

Including the sigmoid turn-on function for gradual condensate formation:

```
✅ E_pair(z) = E_max - κ_conf × f_turnon(z, z_start) × ln(1+z)
```

where:
```
f_turnon(z, z_start) = 1 / [1 + exp(-k ln((1+z)/(1+z_start)))]
```

---

## Step 4: Verification of Boundary Conditions

### Parameters

From manuscript:
- E_max = E_pair(0) ≈ 10¹⁹ eV
- κ_conf ≈ 4.8×10¹⁷ eV
- z_dec ~ 4×10⁹
- z_start ~ 10⁸ (turn-on redshift)
- E_0 = E_pair(z_dec) ≈ 0.1 eV

### Check: E_max consistency

From definition:
```
E_max = E_0 + κ × ln(1+z_dec)
      = 0.1 eV + 4.8×10¹⁷ eV × ln(1 + 4×10⁹)
      = 0.1 + 4.8×10¹⁷ × ln(4×10⁹)
      = 0.1 + 4.8×10¹⁷ × 22.4
      ≈ 1.08×10¹⁹ eV ✓
```

Matches E_pair(0) ~ 10¹⁹ eV!

### Check: z = 0 (today)

```
E_pair(0) = E_max - κ × f(0, z_start) × ln(1)
          = E_max - κ × f(0, z_start) × 0
          = E_max
          = 10¹⁹ eV ✓
```

### Check: z = z_dec (decoupling, large z)

For z >> z_start, f_turnon(z, z_start) → 1:

```
E_pair(z_dec) = E_max - κ × 1 × ln(1+z_dec)
              = [E_0 + κ ln(1+z_dec)] - κ ln(1+z_dec)
              = E_0
              = 0.1 eV ✓
```

### Check: z = 10⁹ (BBN)

Calculate f_turnon(10⁹, 10⁸):
```
f(10⁹, 10⁸) = 1 / [1 + exp(-2 × ln(10¹⁰/10⁸))]
            = 1 / [1 + exp(-2 × ln(100))]
            = 1 / [1 + exp(-9.2)]
            ≈ 0.999 ≈ 1
```

Then:
```
E_pair(10⁹) = E_max - κ × 1 × ln(1+10⁹)
            = 10¹⁹ - 4.8×10¹⁷ × ln(10¹⁰)
            = 10¹⁹ - 4.8×10¹⁷ × 23.03
            = 10¹⁹ - 1.1×10¹⁹
            = -1×10¹⁸ eV ❌ NEGATIVE!
```

**PROBLEM: This gives negative E_pair at BBN!**

---

## Step 5: Issue with Large z_dec

The problem is that if z_dec = 4×10⁹ is used as the reference, then:
- ln(1+z_dec) = 22.4
- At BBN (z=10⁹): ln(1+z) = 23.0

So ln(1+z_BBN) > ln(1+z_dec), which makes the subtraction negative!

### Resolution: Use z_start as Reference

The turn-on redshift z_start ~ 10⁸ is when the condensate becomes dynamically significant, not z_dec. Use this as reference:

```
E_pair(z) = E_max - κ_conf × f_turnon(z, z_start) × [ln(1+z_start) - ln(1+z)]
```

Wait, this doesn't help either...

### Alternative: Two-Component Formula

Maybe the formula needs TWO components:

1. **Baseline growth** from decoupling to today:
   ```
   E_base(z) = E_0 + κ_conf × [ln(1+z_dec) - ln(1+z)]
   ```

2. **Turn-on suppression** at high z:
   ```
   E_pair(z) = E_0 + κ_conf × f_turnon(z, z_start) × [ln(1+z_dec) - ln(1+z)]
   ```

Let me verify this form:

**At z = 0:**
```
E_pair(0) = E_0 + κ × 1 × [ln(1+z_dec) - 0]
          = E_0 + κ × ln(1+z_dec)
          = E_max ✓
```

**At z = z_dec (with f → 1):**
```
E_pair(z_dec) = E_0 + κ × 1 × [ln(1+z_dec) - ln(1+z_dec)]
              = E_0 ✓
```

**At z = 10⁹ (BBN, with f ≈ 1):**
```
E_pair(10⁹) = E_0 + κ × 1 × [ln(1+z_dec) - ln(1+10⁹)]
            = 0.1 + 4.8×10¹⁷ × [ln(4×10⁹) - ln(10¹⁰)]
            = 0.1 + 4.8×10¹⁷ × [22.4 - 23.0]
            = 0.1 + 4.8×10¹⁷ × (-0.6)
            = 0.1 - 2.9×10¹⁷
            ≈ -2.9×10¹⁷ eV ❌ STILL NEGATIVE!
```

---

## Step 6: The Real Issue - Wrong Reference Point

The issue is that **z_start and z_dec are TOO CLOSE to z_BBN!**

If condensate forms at z_start ~ 10⁸ and BBN is at 10⁹, then at BBN:
- ln(1+10⁹) = 23.0
- ln(1+10⁸) = 18.4
- ln(1+10⁷) = 16.1

So the condensate is STILL FORMING at BBN, not fully formed!

### Correct Physical Picture

The formula should represent energy growth AFTER condensate formation:

```
E_pair(z) = E_sat - [E_sat - E_0] × (1 - f_turnon(z, z_start))
```

where:
- **E_sat** = saturation energy ≈ 10¹⁹ eV (fully formed condensate)
- **E_0** = seed energy ≈ 0.1 eV (no condensate)
- **f_turnon** = 0 at z << z_start (no condensate yet)
- **f_turnon** = 1 at z >> z_start (full condensate)

Simplifying:
```
E_pair(z) = E_0 + [E_sat - E_0] × f_turnon(z, z_start)
```

### With Logarithmic Growth

Including logarithmic cosmic evolution within each epoch:

```
E_pair(z) = E_0 + κ_eff(z) × ln[(1+z_max)/(1+z)]
```

where:
```
κ_eff(z) = κ_conf × f_turnon(z, z_start)
```

and z_max is some UV cutoff (e.g., Planck scale or saturation).

---

## Step 7: FINAL CORRECT FORMULA (Proposed)

### Preferred Form

```
✅ E_pair(z) = E_sat × f_turnon(z, z_start) + E_0 × [1 - f_turnon(z, z_start)]
```

where:
- **E_sat ≈ 10¹⁹ eV** (saturation value, today)
- **E_0 ≈ 0.1 eV** (seed value, decoupling)
- **z_start ~ 10⁸** (condensate turn-on redshift)

### Equivalent Form

```
✅ E_pair(z) = E_0 + [E_sat - E_0] × f_turnon(z, z_start)
```

### Turn-On Function (INVERTED from manuscript)

The manuscript's f_turnon has the wrong direction. It should be:

```
f_turnon(z, z_start) = 1 / [1 + exp(+k ln((1+z)/(1+z_start)))]
```

**NOTE THE POSITIVE SIGN!** This gives:
- f(z << z_start) → 1 (low z, recent times, full condensate)
- f(z ~ z_start) → 0.5 (transition)
- f(z >> z_start) → 0 (high z, early times, no condensate)

---

## Verification with Proposed Formula

### Parameters
- E_sat = 10¹⁹ eV
- E_0 = 0.1 eV
- z_start = 10⁸
- k = 2

### At z = 0 (today)

```
f(0, 10⁸) = 1 / [1 + exp(+2 × ln(1/10⁸))]
          = 1 / [1 + exp(-36.8)]
          ≈ 1

E_pair(0) = 0.1 + (10¹⁹ - 0.1) × 1
          ≈ 10¹⁹ eV ✓
```

### At z = 10⁹ (BBN)

```
f(10⁹, 10⁸) = 1 / [1 + exp(+2 × ln(10))]
            = 1 / [1 + exp(4.6)]
            = 1 / [1 + 99.5]
            ≈ 0.01

E_pair(10⁹) = 0.1 + (10¹⁹ - 0.1) × 0.01
            ≈ 10¹⁷ eV

E_pair(10⁹) / E_pair(0) = 10¹⁷ / 10¹⁹ = 0.01 ❌
```

**This gives 1%, not 84%!**

---

## Step 8: Correct Turn-On Function Behavior

The manuscript claims f(10⁹, 10⁸) ≈ 0.84, meaning condensate is 84% formed at BBN.

This requires a DIFFERENT functional form. Try:

```
f_turnon(z, z_start) = 1 - 1 / [1 + (z/z_start)^k]
```

### Verification

```
At z = 0: f(0, 10⁸) = 1 - 1/[1 + 0] = 1 - 1 = 0 ❌
At z → ∞: f(∞, 10⁸) → 1 - 1/[1 + ∞] = 1 ✓
```

This is inverted!

Try:
```
f_turnon(z, z_start) = 1 / [1 + (z_start/z)^k]
```

```
At z = 0: f(0, 10⁸) = 1 / [1 + ∞] = 0 ❌ Want 1
At z → ∞: f(∞, 10⁸) → 1 / [1 + 0] = 1 ❌ Want 0
```

Still wrong!

---

## Conclusion: Need User Input

There are **incompatible requirements:**

1. **E_pair(0) = 10¹⁹ eV** (today, large)
2. **E_pair(z_dec) = 0.1 eV** (decoupling, small)
3. **E_pair(BBN) = 0.84 × E_pair(0)** (BBN is 84% of today)
4. **z_BBN = 10⁹**, **z_start = 10⁸**, **z_dec = 4×10⁹**

With z_BBN > z_start, condensate should be LESS formed at BBN than today, giving E_pair(BBN) < E_pair(0). But the growth from z_dec to BBN is SMALL (only factor ~4 in z), while growth from BBN to today is LARGE (factor ~10⁹ in z).

**This suggests the logarithmic evolution cannot explain the factor 10¹⁹/0.1 = 10²⁰ growth!**

### Possible Resolutions

1. **Different functional form** (not logarithmic)
2. **Different reference redshifts** (z_dec is NOT 4×10⁹)
3. **Two-stage evolution** (different physics at different epochs)
4. **Manuscript error in numerical values** (0.84 is wrong, or E_0 ≠ 0.1 eV)

**RECOMMENDATION:** Return to physical derivation and re-examine assumptions.

---

## Next Steps

1. Search manuscript for original physical motivation of logarithmic form
2. Check if there are alternative forms in early drafts
3. Verify numerical claims (0.84, 10¹⁹ eV, etc.) against raw calculations
4. Consider consulting original author for clarification

**STATUS: Cannot proceed with simulation fixes until this is resolved.**
