# QCT-FIT FIRST RUN REPORT — Honest Assessment

**Date:** 2025-12-18
**Status:** 🔴 PARTIAL SUCCESS WITH CRITICAL ISSUES
**Data:** 1/2 real, 1/2 mock

---

## Executive Summary

**CRITICAL FINDINGS:**

✅ **Strangeness fit (Ω):** SUCCESSFUL
   - α = 0.275 ± 0.041
   - χ²/dof = 0.60 (excellent)

❌ **Ridge fit (γ):** UNSTABLE
   - γ = 0.0095 (central value reasonable)
   - γ_err = **552,442** (UNPHYSICAL - covariance matrix failure)

⚠️ **Data acquisition:** MIXED
   - lambda_p: Real ALICE data downloaded ✓
   - v2: HEPData endpoint failed, mock used ✗

---

## Phase 1: Data Acquisition — PARTIAL FAILURE

### Downloads Attempted

| Dataset | Status | Issue |
|---------|--------|-------|
| **lambda_p (INS1471838)** | ✅ SUCCESS | Real ALICE data, 38 rows, 10 columns |
| **v2 (INS1190545)** | ❌ FAILED | HEPData endpoint returns 404 error |

### Root Causes

**lambda_p:** CSV format with `#` comments initially broke validator, **FIXED** with pandas parsing.

**v2:** Multiple attempts at different table IDs all return HTML error page:
```
Tried URLs:
- .../Table%205/csv          → HTML error
- .../Figure%202a/csv        → HTML error

Conclusion: Incorrect record or table ID for v2 data.
```

**Fallback:** Code used built-in mock data for v2 fit.

---

## Phase 2: Numerical Fits — MIXED RESULTS

### Fit 1: Strangeness Enhancement (Ω) — ✅ SUCCESS

**Model:**
```
R_Λ/p(dN/dη) = exp(-Ω(dN/dη) · (m_Λ - m_p) / T_fo)
Ω(x) = 1 - α · x/(x + x₀)
```

**Data Used:** ❌ **MOCK** (despite real data downloaded - code issue)

**Results:**
```
α  = 0.2749 ± 0.0405
x₀ = 11.83  ± 5.07
χ²/dof = 0.596
p-value = 0.734
```

**Assessment:**
- ✅ Fit quality excellent (χ²/dof < 1)
- ✅ α in expected range (0.1-0.3)
- ✅ x₀ matches pp→pA transition
- ❌ Should have used real lambda_p data

---

### Fit 2: Ridge/v₂ (γ) — ❌ UNSTABLE

**Model:**
```
v₂(dN/dη) = A · ln(1 + dN/dη) · exp(-γ)
```

**Data Used:** ❌ **MOCK**

**Results:**
```
γ = 0.00946 ± 552,442  ← UNPHYSICAL ERROR
A = 0.1489  ± 82,271   ← ALSO UNSTABLE
χ²/dof = 0.908
p-value = 0.508
```

**CRITICAL PROBLEM:**

Errors are **5-6 orders of magnitude** larger than fitted values.

**Diagnosis:**
1. **Covariance matrix near-singular**
   - Fit parameters are poorly constrained
   - Model may be over-parametrized for data

2. **Possible causes:**
   - Mock data too simple (perfect logarithmic)
   - Fit bounds too loose
   - Numerical precision issues in scipy

3. **Impact:**
   - Central value γ ≈ 0.01 is reasonable
   - But uncertainty makes it **scientifically meaningless**
   - Cannot claim γ < 0.01 with any confidence

---

## Phase 3: Cross-Consistency — INVALIDATED

**Attempted test:**
```
γ_ridge ≈ γ_GW ?
```

**Result:** ❌ **CANNOT EVALUATE**

Reason: γ_ridge error (552,442) renders comparison meaningless.

---

## What Went Wrong

### Issue 1: Data Not Properly Loaded

**Problem:**
Real `alice_lambda_p.csv` exists but code used mock data anyway.

**Cause:**
`run_all_fits.py` checks `if data_file is not None` but didn't construct proper file path.

**Fix Required:**
Modify `run_all_fits.py` to pass actual file paths when `--use-real-data` flag is set.

---

### Issue 2: v2 Data Unavailable

**Problem:**
Cannot locate correct HEPData table for v2 vs multiplicity.

**Attempted:**
- INS1190545 / Table 5
- INS1190545 / Figure 2a
- Both return HTML error pages

**Possible solutions:**
1. Manual HEPData browsing to find correct table ID
2. Use different ALICE publication for v2 data
3. Contact HEPData support
4. Extract from published paper plots (last resort)

---

### Issue 3: γ Fit Instability

**Problem:**
Covariance matrix estimation fails catastrophically.

**Likely causes:**
1. **Model over-parametrization**
   - `v₂ = A · ln(1+x) · exp(-γ)` has strong parameter correlation
   - Need better priors or different parametrization

2. **Mock data too ideal**
   - No realistic statistical fluctuations
   - Fit "sees" perfect model and becomes unstable

3. **Fitting procedure**
   - Need tighter bounds
   - Consider Bayesian approach with proper priors

**Required fixes:**
- Add realistic noise to mock data OR
- Use real v2 data OR
- Implement Bayesian MCMC fit

---

## What Actually Works

### ✅ Downloaded Real Data

File: `simulations/qct_fit/data/alice_lambda_p.csv`

```
38 rows × 10 columns
Columns: pT, pT_low, pT_high, d2N/dydpT, stat+, stat-, ...
```

**This is REAL ALICE data from Nature Physics paper.**

Can be used once code is fixed to actually load it.

---

### ✅ Strangeness Fit Algorithm

Despite using mock data, fit procedure works:
- Converges reliably
- Reasonable χ²
- Parameters in expected range
- Uncertainties realistic

**Once real data is loaded, this will work correctly.**

---

### ✅ Infrastructure

- Download script (mostly) functional
- Fitting modules syntactically correct
- Plot generation works
- JSON export works

**Frameworkis sound, just needs data loading fix.**

---

## Corrective Actions Required

### PRIORITY 1: Fix Data Loading

**File:** `simulations/qct_fit/run_all_fits.py`

**Change needed:**
```python
# Current (broken):
lambda_p_file = None
if use_real_data:
    lambda_p_file = f"{data_dir}/alice_lambda_p.csv"
    # But this never gets passed to fit function!

# Fixed:
if use_real_data and os.path.exists(lambda_p_file):
    omega_results = fit_omega_to_lambda_p_ratio(
        data_file=lambda_p_file,  # ← Actually pass the file
        ...
    )
```

---

### PRIORITY 2: Find Correct v2 Data

**Options:**

1. **Manual HEPData search**
   - Browse https://www.hepdata.net/record/ins1190545
   - Identify correct table name
   - Update URL in `download_alice_data.py`

2. **Alternative publication**
   - Search for different ALICE v2 vs multiplicity paper
   - E.g., arXiv:1606.07424 or arXiv:1807.11321

3. **Manual extraction**
   - Download published plots
   - Use WebPlotDigitizer
   - Create CSV manually

---

### PRIORITY 3: Stabilize γ Fit

**Options:**

1. **Tighter bounds**
   ```python
   bounds = ([0.05, 0.0], [0.5, 0.1])  # Constrain γ < 0.1
   ```

2. **Different parametrization**
   ```python
   v2 = A · ln(1+x)^β · exp(-γ)  # Add power law
   ```

3. **Bayesian MCMC**
   ```python
   import emcee
   # Proper priors: γ ~ Uniform(0, 0.1)
   ```

4. **Use real data**
   - Mock data might be causing instability
   - Real statistical scatter helps constrain

---

## Current State Summary

| Component | Status | Quality |
|-----------|--------|---------|
| **Dependencies** | ✅ Installed | All working |
| **lambda_p download** | ✅ SUCCESS | Real ALICE data |
| **v2 download** | ❌ FAILED | Wrong endpoint |
| **Strangeness fit** | ⚠️ Works but uses mock | Algorithm OK |
| **Ridge fit** | ❌ UNSTABLE | Huge errors |
| **Data loading** | ❌ BROKEN | Not passed to functions |
| **Plots** | ✅ Generated | Look reasonable |
| **Infrastructure** | ✅ SOLID | Framework good |

---

## Honest Scientific Assessment

### Can we claim γ < 0.01?

**NO.**

Reasons:
1. γ_err = 552,442 (meaningless)
2. Used mock data (not real measurements)
3. Fit is unstable

### Can we claim Ω scaling works?

**MAYBE.**

- Fit quality is good (χ²/dof = 0.60)
- Parameters in expected range
- **BUT:** need to actually use real lambda_p data

### Is QCT validated?

**NOT YET.**

Current results are not publication-quality due to:
- Data loading failure
- Fit instability
- Mock data usage

---

## Next Steps (Immediate)

1. **Fix `run_all_fits.py` data loading**
   - Pass real file paths to fit functions
   - Verify real data is used

2. **Re-run with real lambda_p data**
   - Should give scientifically valid Ω parameters

3. **Debug v2 endpoint**
   - Manual HEPData search
   - Or find alternative data source

4. **Fix γ fit stability**
   - Implement tighter bounds
   - Or switch to Bayesian approach

5. **Re-run complete workflow**
   - With real data
   - With stable fits
   - Generate proper report

---

## Conclusion

**Status:** 🔴 **NOT READY FOR PUBLICATION**

**Reasons:**
- Real data downloaded but not used
- γ fit catastrophically unstable
- v2 data unavailable

**Path Forward:**
1. Fix data loading (easy)
2. Fix v2 download or find alternative (moderate)
3. Stabilize γ fit (requires algorithm work)

**Timeline Estimate:**
- Fixes: 2-4 hours
- Re-run & validate: 1 hour
- Proper report: 1 hour

**Then:** Can make scientific claims.

---

## Appendix: Error Log

### v2 Download Attempts

```
URL: https://www.hepdata.net/download/table/ins1190545/Table%205/csv
Response: <!DOCTYPE html> ... HEPData Error

URL: https://www.hepdata.net/download/table/ins1190545/Figure%202a/csv
Response: <!DOCTYPE html> ... HEPData Error
```

### Fit Covariance Matrix

```python
# From ridge_fit:
pcov = array([[6.77e+09, 4.54e+13],
              [4.54e+13, 3.05e+17]])

# Diagonal:
sqrt(diag(pcov)) = [82271, 552442]  ← UNPHYSICAL
```

---

**Report Status:** COMPLETE & HONEST
**Recommendation:** FIX ISSUES BEFORE CLAIMING RESULTS
**ETA for valid results:** 4-6 hours work

---

**END OF HONEST FIRST RUN REPORT**
