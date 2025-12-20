# 📋 Manuscript Sections Requiring E_pair(z) Formula Corrections

**Date:** 2024-12-20
**Issue:** E_pair(z) evolution formula has sign error and incompatible boundary conditions
**Impact:** 25+ files affected across manuscript

---

## Summary of Issues

### Issue 1: Sign Error in ln(1+z) Term
- **Current formula:** `E_pair(z) = E_0 + κ × f(z) × ln(1+z)`
- **Problem:** Gives E_pair growing with z (backward evolution)
- **Expected:** E_pair should decrease with z (grow with cosmic time)

### Issue 2: Wrong Boundary Condition at z=0
- **Current formula gives:** E_pair(0) = E_0 = 0.1 eV
- **Should give:** E_pair(0) = 10¹⁹ eV

### Issue 3: Incompatible Numerical Claims
- **Manuscript claims:** f_turnon(10⁹, 10⁸) ≈ 0.84
- **Formula with ln gives:** f ≈ 0.99
- **Formula with log₁₀ gives:** f ≈ 0.88

---

## Files Requiring Corrections (Grouped by Priority)

### 🔴 CRITICAL - Core Formula Definitions

#### 1. `appendix_microscopic_derivation_rev.tex`
**Lines requiring correction:**
- **328-329:** E_pair(z) formula definition
  ```latex
  WRONG: E_{\rm pair}(z) = E_0 + \kappa_{\rm conf} \cdot f_{\rm turn-on}(z, z_{\rm start}) \cdot \ln(1+z)
  ```
- **357-361:** κ_conf value derived from E_pair(z=0) = 10¹⁹ eV
  - Derivation is correct but based on wrong formula
- **400:** BBN ratio claim
  ```latex
  E_{\rm pair}(z_{\rm BBN}) \approx 0.84 \times E_{\rm pair}(z=0)
  ```
  - This is OPPOSITE to what current formula gives

**What needs to change:**
1. Fix formula at line 328-329 with correct sign/form
2. Re-derive κ_conf at lines 357-361 with new formula
3. Verify BBN ratio at line 400 matches corrected formula
4. Update all subsequent numerical examples

---

#### 2. `appendix_cosmological_evolution_REPLACEMENT.tex`
**Lines requiring correction:**
- **97-98:** E_pair(z) formula (identical to original)
  ```latex
  WRONG: E_{\rm pair}(z) = E_0 + \kappa_{\rm conf} \cdot f_{\rm turn-on}(z, z_{\rm start}) \cdot \ln(1+z)
  ```
- **132:** Claims E_0 ~ 0.1 eV at decoupling → E_pair ~ 10¹⁹ eV today
  - Contradicts formula which gives opposite
- **200:** f_turnon numerical claim
  ```latex
  f(10^9, 10^8) ≈ 0.84
  ```
  - ln gives 0.99, not 0.84 (possible log₁₀ confusion)

**What needs to change:**
1. Fix formula at line 97-98
2. Clarify E_0 vs E_max terminology at line 132
3. Fix f_turnon value at line 200 or change to log₁₀
4. Update G_eff evolution discussion (currently correct formula at line 146-148)

---

#### 3. `cosmological_corrections.tex` (Czech)
**Lines requiring correction:**
- **17-19:** Derivation from QCD confinement
  ```latex
  E_{\rm pair}(t) = E_0 + \kappa_{\rm conf}\,\ln\!\left(\frac{a(t)}{a_0}\right)
  ```
  - This is CORRECT in time variable (a(t)/a_0)
  - But conversion to z is WRONG at line 41
- **41:** Conversion to redshift
  ```latex
  WRONG: E_{\rm pair}(z) = E_0 + \kappa_{\rm conf}\,\ln(1+z)
  ```
  - Should have MINUS sign: a(t)/a_0 = 1/(1+z) → ln(a/a_0) = -ln(1+z)

**What needs to change:**
1. **Keep line 17-19** (correct in terms of a(t))
2. **Fix line 41** with proper a→z conversion:
   ```latex
   E_{\rm pair}(z) = E_0 + \kappa_{\rm conf}\,\ln(a(z)/a_{\rm dec})
                   = E_0 + \kappa_{\rm conf}\,[\ln(1+z_{\rm dec}) - \ln(1+z)]
   ```
3. Update numerical examples in lines 27-36

---

### 🟡 HIGH PRIORITY - Dependent Cosmological Sections

#### 4. `section_5_7_cmb_phase_shift.tex`
**Lines requiring correction:**
- **26:** Λ_QCT(z) formula
  ```latex
  \Lambda_{\rm QCT}(z) = \sqrt{E_{\rm pair}(z) \cdot m_p}
  ```
  - Formula structure is correct, but uses wrong E_pair(z)
- **30:** Logarithmic evolution discussion
  - Needs update after E_pair(z) fix

**What needs to change:**
1. No formula change needed (uses E_pair as input)
2. Update numerical predictions after E_pair fix
3. Re-run CMB phase shift calculations

---

#### 5. `section_5_8_bao_phase_shift.tex`
**Lines requiring correction:**
- **109:** G_eff evolution discussion
  ```latex
  E_{\rm pair}(z) = E_0 + \kappa_{\rm conf} \ln(1+z)
  ```
  - Same sign error

**What needs to change:**
1. Fix E_pair formula at line 109
2. Re-calculate 6% evolution claim from z=0 to z=1
3. Update BAO predictions

---

#### 6. `appendix_dark_energy_from_saturation.tex`
**Lines requiring correction:**
- **29:** E_pair formula
  ```latex
  WRONG: E_{\rm pair}(z) = E_0 + \kappa_{\rm conf} \cdot \ln(1+z)
  ```

**What needs to change:**
1. Fix formula at line 29
2. Check if saturation physics changes with corrected evolution

---

### 🟢 MEDIUM PRIORITY - Theoretical Derivations

#### 7. `QCT_hossenfelder_section_3_4_lagrangian_kappa.tex`
**Lines requiring correction:**
- **121:** Alternative form
  ```latex
  E_{\rm pair}(z) - E_0 \approx \alpha_0 E_{\rm pair}(0) \times \ln(1+z)
  ```
- **123:** Reference energy definition
  ```latex
  E_0 = E_{\rm pair}(0) - \alpha_0 E_{\rm pair}(0) \ln(1) = E_{\rm pair}(0)
  ```
  - Confusing: sets E_0 = E_pair(0), contradicts other sections
- **129:** Phenomenological form
  ```latex
  WRONG: E_{\rm pair}(t) = E_0 + \kappa_{\rm conf} \ln(1+z)
  ```

**What needs to change:**
1. Clarify E_0 terminology (is it E_pair(z=0) or E_pair(z_dec)?)
2. Fix formulas at lines 121, 129
3. Re-derive κ_conf at line 133

---

#### 8. `QCT_hossenfelder_section_7_3_geometric_lambda.tex`
**Lines requiring correction:**
- **87, 92, 198:** E_pair formula (3 instances)
  ```latex
  WRONG: E_{\rm pair}(z) = E_0 + \kappa_{\rm conf} \ln(1+z)
  ```
- **266:** w parameter discussion supporting logarithmic form
  - Physics argument may still be valid with corrected sign

**What needs to change:**
1. Fix all 3 formula instances
2. Verify w parameter derivation still holds
3. Check dark energy equation of state predictions

---

#### 9. `appendix_units_numerical_audit.tex`
**Lines requiring correction:**
- **124-126:** κ_conf numerical derivation
  ```latex
  \kappa_{\rm conf} \approx \frac{E_{\rm pair}(t_0) - \Delta_0}{\ln(1+z_{\rm BBN})}
  ```
  - Numerator should be E_pair(t_0) - E_pair(BBN), not E_pair - Δ_0
  - Denominator assumes wrong formula

**What needs to change:**
1. Re-derive κ_conf with correct formula
2. Update value from 2.6×10¹⁷ eV to match corrected calculation
3. Propagate to all dependent calculations

---

#### 10. `Časová_evoluce_G_eff.tex` (Czech)
**Lines requiring correction:**
- **25:** E_pair formula with time-dependent turn-on
  ```latex
  WRONG: E_{\rm pair}(z) = E_0 + \kappa_{\rm conf} \ln(1+z) \times f(t - t_{\rm BBN})
  ```

**What needs to change:**
1. Fix formula at line 25 with correct sign
2. Clarify time vs redshift parameterization

---

### 📘 LOWER PRIORITY - Main Preprint File

#### 11. `preprint.tex`
**Lines requiring correction (8 instances):**
- **948:** E_pair integral form
- **1128, 1136:** E_pair formulas in Section 3.4
- **1545:** BOXED formula (critical!)
  ```latex
  WRONG: \boxed{E_{\rm pair}(t) = E_0 + \kappa_{\rm conf}\,\ln(1+z)}
  ```
- **1562:** Formula with turn-on
- **1751, 1756, 1882, 1888:** Additional instances
- **1974:** Dark energy discussion
- **2040:** Formula in cosmological section
- **2694:** Summary/conclusion mention

**What needs to change:**
1. Fix all 8+ formula instances
2. Pay special attention to BOXED formula at line 1545 (highly visible)
3. Update dark energy predictions
4. Verify conclusion at line 2694 matches corrected physics

---

## Additional Files to Check

The following files were not in the Grep results but may reference E_pair(z):

- `section_*.tex` files (Sections 1-6)
- `appendix_*.tex` files (other appendices)
- `QCT_hossenfelder_section_*.tex` files (Hossenfelder review sections)
- `derivation_*.tex` files (derivation supplements)

**Recommendation:** Do a comprehensive search for "E_pair" and "ln(1+z)" across ALL .tex files.

---

## Systematic Correction Strategy

### Phase 1: Core Formula Fix
1. **Decide on correct formula** (needs physical re-derivation or user clarification)
2. **Fix primary definition files:**
   - `appendix_microscopic_derivation_rev.tex:328-329`
   - `appendix_cosmological_evolution_REPLACEMENT.tex:97-98`
3. **Fix derivation file:**
   - `cosmological_corrections.tex:41` (a→z conversion)

### Phase 2: Parameter Updates
1. **Re-derive κ_conf** with correct formula
2. **Update numerical examples:**
   - BBN ratio (should be 0.84 or recalculate?)
   - f_turnon values
   - CMB/BAO predictions
3. **Fix dependent parameters:**
   - Λ_QCT(z) evolution
   - G_eff(z) values
   - w(z) dark energy equation of state

### Phase 3: Simulation Validation
1. **Update all simulation codes** with corrected formula
2. **Re-run cosmological tests:**
   - BBN: Target |ΔG/G| ~ 16%
   - CMB: Target χ² improvement
   - BAO: Target phase shift matching
3. **Compare with experimental data**

### Phase 4: Manuscript Propagation
1. **Update main preprint.tex** (8+ instances)
2. **Update section files** (5_7, 5_8, others)
3. **Update appendix files** (all remaining)
4. **Update theoretical derivations** (Hossenfelder sections)

---

## Testing Checklist

After corrections, verify:

- [ ] E_pair(z=0) = 10¹⁹ eV (today, maximum)
- [ ] E_pair(z_dec) ≈ 0.1 eV (decoupling, minimum)
- [ ] E_pair(z_BBN) / E_pair(0) ≈ 0.84 (BBN ratio)
- [ ] E_pair decreases with z (increases with cosmic time)
- [ ] G_eff(z_BBN) / G_N ≈ 0.84 (ΔG/G ~ -16%)
- [ ] CMB χ² improved from baseline
- [ ] BAO phase shift matches observations
- [ ] Formula is dimensionally consistent
- [ ] Turn-on function gives claimed f(10⁹, 10⁸) value
- [ ] All numerical examples self-consistent

---

## Summary Statistics

- **Total files identified:** 11 primary + unknown secondaries
- **Total formula instances:** 25+ across all files
- **Critical BOXED formulas:** 2 (preprint.tex:1545, appendix line 372 is correct)
- **Numerical values to update:** κ_conf, f_turnon, BBN ratio, CMB/BAO predictions
- **Simulations to re-run:** 5+ (BBN, CMB, BAO, G_eff, dark energy)

---

## Estimated Scope

- **Formula fixes:** ~30 instances across 11+ files
- **Numerical updates:** ~50 values
- **Derivation rewrites:** ~5 sections
- **Simulation updates:** ~10 Python files
- **Validation tests:** ~15 checks

**This is a major manuscript revision affecting core predictions.**

---

## Next Steps

1. ✅ **DONE:** Identify all affected files
2. ⏳ **TODO:** Determine physically correct formula
3. ⏳ **TODO:** Get user/author confirmation on approach
4. ⏳ **TODO:** Implement corrections systematically
5. ⏳ **TODO:** Re-run all simulations
6. ⏳ **TODO:** Update manuscript
7. ⏳ **TODO:** Verify consistency across all sections

**STATUS:** Awaiting decision on correct E_pair(z) formula before proceeding with corrections.
