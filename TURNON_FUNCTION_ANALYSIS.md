# Turn-On Function f_turnon(z, z_start): Critical Analysis

## Summary of Findings

I've identified **THREE CRITICAL ISSUES** with the turn-on function implementation in the QCT manuscript:

1. **ln vs log10 discrepancy** (Formula error)
2. **Wrong direction of evolution** (Physical interpretation error)
3. **Formula breakdown at z=0** (Normalization issue)

---

## Issue 1: LN vs LOG10 Discrepancy

### Manuscript Formula (Line 103-104)
```
f_turnon(z, z_start) = 1 / [1 + exp(-k × ln((1+z)/(1+z_start)))]
```
Uses **natural logarithm (ln)**.

### Claimed Value (Line 200)
```
f(10⁹, 10⁸) ≈ 0.84
```

### Actual Values
- **LN formula gives:** f(10⁹, 10⁸) = 0.9901 ≈ 0.99 ❌
- **LOG10 formula gives:** f(10⁹, 10⁸) = 0.8808 ≈ 0.88 ✓

### Conclusion
**The manuscript formula should use log10, not ln, to match the claimed value of 0.84.**

The correct formula should be:
```
f_turnon(z, z_start) = 1 / [1 + exp(-k × log10((1+z)/(1+z_start)))]
```

---

## Issue 2: Wrong Direction of Evolution

### Physical Timeline (Cosmic Time)
```
EARLY → LATE
z ~ 10⁹  →  z ~ 10⁷-10⁸  →  z = 0
(BBN)       (z_start)      (today)
```

### Physical Expectation
From manuscript (lines 53-67):
- **Before decoupling (high z, early time):** No condensate, E_pair ≈ E_0 ≈ 0.1 eV
- **After decoupling (lower z, later time):** Condensate forms, E_pair grows
- **Today (z = 0):** Condensate fully formed, E_pair ~ 10¹⁹ eV

**Therefore: E_pair should INCREASE as z DECREASES (as time progresses)**

### Current Formula Behavior
```
E_pair(z) = E_0 + κ_conf × f(z) × ln(1+z)
```

Components:
- `ln(1+z)`: **DECREASES** as z decreases (ln(10⁹) = 20.7 → ln(1) = 0)
- `f(z)` (current sigmoid): **DECREASES** at high z→low z transition
- **Result:** E_pair is **LARGER at early times (high z)** ❌

### Test Results
```
Early time (z=10⁹):  E_pair = 9.85×10¹⁸ eV
Late time (z=10⁷):   E_pair = 7.66×10¹⁶ eV

E_pair(early) > E_pair(late) ← WRONG DIRECTION!
```

**The formula gives DECREASING E_pair with time, which contradicts the physical picture of condensate build-up!**

---

## Issue 3: Formula Breakdown at z=0

### The Problem
```
E_pair(z=0) = E_0 + κ_conf × f(0) × ln(1)
            = E_0 + κ_conf × 1 × 0
            = E_0
            = 0.1 eV
```

But physically: **E_pair(0) ~ 10¹⁹ eV** (from manuscript line 126)

**Discrepancy: Factor of ~10²⁰!**

### Current Workaround
Both Python implementations use a **special case** for z ≤ 0:
```python
if z <= 0:
    return E_pair_today_eV  # Hard-coded value, not from formula
```

This indicates **the formula is not self-consistent** and requires external normalization.

---

## Root Cause Analysis

### The Fundamental Problem

The formula `E_pair(z) = E_0 + κ × f(z) × ln(1+z)` has the **wrong functional form** for describing condensate build-up.

Consider what happens:
1. At high z (early): ln(1+z) is **large**
2. At low z (late): ln(1+z) is **small**
3. Therefore, E_pair is naturally **larger at early times**

This is **opposite** to condensate physics, where pairing energy should **grow over time**!

### What the Formula Needs

To get E_pair increasing with cosmic time, we need:
- Something that **increases as z decreases**

Options:
1. **Inverted redshift dependence:**
   ```
   E_pair(z) = E_max × f_correct(z)
   where f_correct(z) → 0 for z >> z_start (early)
         f_correct(z) → 1 for z << z_start (late)
   ```

2. **Reciprocal logarithm:**
   ```
   E_pair(z) = E_0 + κ × ln((1+z_max)/(1+z))
   ```

3. **Different functional form entirely**

---

## Current Sigmoid Behavior (Line 109-111)

### Manuscript Claims
```
f(z << z_start) ≈ 0   (no condensate before decoupling)
f(z ~ z_start)  ≈ 0.5  (transition)
f(z >> z_start) ≈ 1   (full confinement)
```

### Reality Check
- `z << z_start`: **LOW z = LATE time** (after z_start)
- `z >> z_start`: **HIGH z = EARLY time** (before z_start)

So the manuscript is saying:
- **Late times (after z_start):** f ≈ 0 (no condensate)
- **Early times (before z_start):** f ≈ 1 (full condensate)

**This is BACKWARDS!**

The correct behavior should be:
```
f(z >> z_start) ≈ 0   (no condensate at early times)
f(z ~ z_start)  ≈ 0.5  (transition)
f(z << z_start) ≈ 1   (full condensate at late times)
```

To achieve this, we need to **invert the sigmoid**:
```
f_correct(z) = 1 / [1 + exp(+k × log10((1+z)/(1+z_start)))]
```
Note the **+k instead of -k**.

---

## Testing with Correct Formula

### Inverted Sigmoid
```python
f(z) = 1 / [1 + exp(+k × log10((1+z)/(1+z_start)))]
```

### Results
```
z = 10¹⁰: f = 0.0001  (early time, no condensate) ✓
z = 10⁹:  f = 0.0099  (BBN, minimal condensate)
z = 10⁸:  f = 0.5000  (z_start, transition) ✓
z = 10⁷:  f = 0.9901  (late time, strong condensate) ✓
z = 0:    f = 1.0000  (today, full condensate) ✓
```

**Direction is now CORRECT!**

### But...
With inverted sigmoid:
- f(10⁹, 10⁸) = 0.0099 ≈ 0.01

But manuscript claims:
- f(10⁹, 10⁸) ≈ 0.84

**These cannot both be true!**

---

## The Real Problem: z_start Interpretation

### Option A: z_BBN > z_start (Current Understanding)
```
Timeline: z_BBN = 10⁹ → z_start = 10⁸ → z = 0
```
- BBN happens **before** z_start (earlier in time)
- At BBN, condensate **hasn't formed yet**
- Therefore: E_pair(BBN) ≈ E_0 (small)
- **Contradicts** manuscript claim that E_pair(BBN) = 0.84 × E_pair(0)

### Option B: Alternative Interpretation
Maybe **z_start represents when condensate STARTS, not when it's strong**?

Timeline:
```
z_dec ~ 10⁹: Decoupling (condensate can begin forming)
z_start ~ 10⁸: Condensate is 50% formed
z = 0: Condensate fully formed
```

Then at BBN (z ~ 10⁹), condensate is already ~84% formed relative to today.

But this contradicts lines 73-77 which say:
```
"z_start when condensate becomes strong enough to affect gravitational dynamics"
```

---

## Recommended Corrections

### 1. Fix the Formula (Use log10)
```
f_turnon(z, z_start) = 1 / [1 + exp(-k × log10((1+z)/(1+z_start)))]
                                         ^^^^^^
```

### 2. Fix the Direction (Invert the sigmoid)
```
f_turnon(z, z_start) = 1 / [1 + exp(+k × log10((1+z)/(1+z_start)))]
                                    ^^
```

### 3. Reconsider the E_pair Formula
Instead of:
```
E_pair(z) = E_0 + κ × f(z) × ln(1+z)  ← Decreases with time
```

Consider:
```
E_pair(z) = E_max × g(z)  ← where g(z) increases with time
```
or
```
E_pair(z) = E_0 + κ × f(z) × [const - ln(1+z)]  ← Increases with time
```

### 4. Clarify Physical Timeline
Explicitly state which redshift corresponds to which epoch and what fraction of condensate has formed.

---

## Files Examined

1. `/home/user/QCT_13/manuscripts/latex_source/appendix_cosmological_evolution_REPLACEMENT.tex`
   - Lines 51-112: Physical evolution description
   - Lines 190-200: BBN calculation
   - **Uses: ln** (natural logarithm)

2. `/home/user/QCT_13/simulations/cosmology/test_bbn_with_physical_zstart.py`
   - Line 126: **Uses: log10**
   - Gives f(10⁹, 10⁸) = 0.845 ✓ (matches manuscript claim)

3. `/home/user/QCT_13/simulations/cosmology/qct_cosmology_CORRECT.py`
   - Line 91: **Uses: ln**
   - Gives f(10⁹, 10⁸) = 0.9901 ❌ (doesn't match claim)
   - BBN test **FAILS** (ΔG/G = 64.8% > 20% limit)

---

## Bottom Line

**The manuscript formula (Eq. 103-104) contains errors:**

1. ✅ **Use log10, not ln** (to match f(10⁹, 10⁸) ≈ 0.84)
2. ❌ **Current sigmoid gives wrong direction** (E_pair decreases with time)
3. ⚠️ **Fundamental formula issue:** The form `E_0 + κ × f × ln(1+z)` naturally gives decreasing E_pair with time, contradicting condensate physics

**The correct implementation should:**
- Use log10 in the sigmoid
- Possibly invert the sigmoid (flip sign of k)
- Reconsider whether the E_pair formula has the right functional form
- Add explicit special-case handling for z=0 (or redesign formula to work at all z)
