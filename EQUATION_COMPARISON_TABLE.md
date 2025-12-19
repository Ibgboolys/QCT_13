# QCT Redshift Evolution: Equation Comparison Table

**Purpose:** Side-by-side comparison of manuscript equations vs simulation implementations
**Date:** 2025-12-19

---

## TABLE 1: Core Redshift Dependencies

| Parameter | Manuscript Formula | Manuscript Source | Simulation Status | Notes |
|-----------|-------------------|-------------------|-------------------|-------|
| **n_ν(z)** | n_ν(0) × (1+z)³ | Standard cosmology, derivation_fermi_blocking line 24 | ✅ CORRECTED (CMB), ⚠️ CHECK (BAO) | CRITICAL: Was using constant n_ν(0) |
| **T_ν(z)** | T_ν(0) × (1+z) | Standard thermodynamics | ✅ IMPLEMENTED | Standard result |
| **E_pair(z)** | E₀ + κ_conf f(z,z_start) ln(1+z) | appendix_cosmological_evolution Eq. 97 | ⚠️ PARTIAL (no turn-on function) | Need to add f_turnon sigmoid |
| **Λ_QCT(z)** | (3/2)√[E_pair(z) × m_p] | section_5_7_cmb line 26 | ✅ IMPLEMENTED | Logarithmic form correct |
| **G_eff(z)** | G_eff(0) × E_pair(z)/E_pair(0) | appendix_cosmological_evolution Eq. 147 [BOXED] | ✅ CORRECTED | Old τ³ formula removed |
| **R_proj(z)** | CONSTANT (physical) OR (1+z)⁻³/² | AMBIGUOUS! Lines 160 vs simulations | ❓ UNCLEAR | **NEEDS CLARIFICATION** |

---

## TABLE 2: Wrong vs Correct Formulas

### G_eff Evolution (CRITICAL CORRECTION!)

| Version | Formula | Result at z=10⁹ | Status |
|---------|---------|-----------------|--------|
| **OLD (WRONG)** | G_eff(z)/G_N = [E_pair(z)/E_pair(0)] × [τ_H(z)/τ_H(0)]³ | G_BBN/G_N ~ 10⁻⁴² | ❌ UNPHYSICAL |
| **NEW (CORRECT)** | G_eff(z)/G_N = E_pair(z)/E_pair(0) | G_BBN/G_N ~ 0.84 | ✅ WITHIN BBN CONSTRAINTS |

**Manuscript Note (line 8):** "Corrected G_eff evolution formula (removed incorrect τ³ factor)"

---

### Λ_QCT Evolution (Logarithmic vs Conformal)

| Formula Type | Expression | At z=1100 | Use For |
|--------------|-----------|-----------|---------|
| **Logarithmic** | (3/2)√[(E₀ + κ_conf ln(1+z)) × m_p] | ~98 TeV | ✅ NUMERICAL SIMULATIONS |
| **Conformal** | Λ_QCT(0) × (1+z)^(3/4) | ~3500 TeV | ❌ GEOMETRIC INTERPRETATION ONLY |

**Recommendation:** Use ONLY logarithmic form in numerical codes.

---

## TABLE 3: Turn-On Function Details

| Regime | z range | f_turnon value | E_pair behavior | Physical State |
|--------|---------|---------------|-----------------|----------------|
| **Before decoupling** | z < z_start ~ 10⁸ | f ≈ 0 | E_pair ≈ E₀ = 0.1 eV | No condensate |
| **Transition** | z ~ z_start | f ≈ 0.5 | E_pair growing | Condensate forming |
| **Full confinement** | z > z_start | f ≈ 1 | E_pair = E₀ + κ_conf ln(1+z) | Mature condensate |
| **Saturation** | z > z_sat ~ 10⁶ | f = 1 | E_pair → E_conf (conformal) | UV physics dominates |

**Function:**
```
f(z, z_start) = 1 / [1 + exp(-k ln((1+z)/(1+z_start)))]
```
with k ≈ 2

**Source:** appendix_cosmological_evolution_REPLACEMENT.tex, Eq. 103-104

---

## TABLE 4: Cosmological Observables

| Observable | ΛCDM Formula | QCT Modification | Manuscript Source |
|------------|--------------|------------------|-------------------|
| **H(z)** | H₀√[Ω_r(1+z)⁴ + Ω_m(1+z)³ + Ω_Λ] | H_ΛCDM × √[G_eff(z)/G_N] ? | section_5_8_bao line 40 (⚠️ AMBIGUOUS) |
| **Ω_m(z)** | Ω_m,0 (1+z)³ / E²(z) | Same with E_QCT(z) | bao_phase_shift_geff_step2.py line 69 |
| **f(z)** | Ω_m(z)^γ, γ≈0.55 | Ω_m^QCT(z)^γ | step2.py line 83 |
| **D(z)** | E(z) ∫[z,∞] (1+z')/E³(z') dz' | Same with E_QCT | step2.py line 101 |
| **r_s** | ∫[z_drag,∞] c_s(z)/H(z) dz | With H_QCT(z) | section_5_8_bao line 34 |

---

## TABLE 5: CMB/BAO Phase Shifts

| Effect | Formula | QCT Prediction | Observed | Status |
|--------|---------|----------------|----------|--------|
| **CMB phase** | A_∞ = 1 + O(Γ_QCT/H) | A_∞ = 1.00 | A_∞ > 0.90 (95% CL) | ✅ PASS |
| **BAO r_s** | r_s^QCT / r_s^ΛCDM | 1.054 (+5.4%) | N/A | From G_eff = 0.9 |
| **BAO growth** | f_QCT / f_ΛCDM | 1.060 (+6.0%) | N/A | From Ω_m enhancement |
| **BAO total** | β_φ^QCT | 1.4 ± 0.3 | 2.7 ± 1.7 (DESI) | 0.75σ compatible |

**CMB Constraint (z ~ 1.7×10⁴):**
```
Γ_QCT/H ~ (T_ν/Λ_QCT)⁵ × (T_ν/H) ~ 1.2 × 10⁻²⁷ ≪ 1  →  Free-streaming ✓
```

**Source:** section_5_7_cmb_phase_shift.tex, lines 38-43

---

## TABLE 6: Numerical Values at Key Epochs

### z = 0 (Today)

| Parameter | Value | Units | Source |
|-----------|-------|-------|--------|
| n_ν | 3.36 × 10⁸ | m⁻³ | Standard |
| T_ν | 1.95 | K | Standard |
| E_pair | 5.38 × 10¹⁸ | eV | Calibrated from G_eff |
| Λ_QCT | 1.07 × 10¹⁴ | eV (107 TeV) | Derived |
| G_eff/G_N | 0.9 | - | Calibrated |
| R_proj | 2.58 | cm | Derived |

### z = 1100 (CMB Last Scattering)

| Parameter | Value | Factor Change | Units |
|-----------|-------|--------------|-------|
| n_ν | 4.5 × 10¹⁷ | ×1.3 × 10⁹ | m⁻³ |
| T_ν | 2100 | ×1100 | K |
| E_pair | ~5.2 × 10¹⁸ | ×0.97 | eV |
| Λ_QCT | ~9.8 × 10¹³ | ×0.92 | eV (98 TeV) |
| G_eff/G_N | ~0.87 | ×0.97 | - |
| R_proj | ? | ? | **UNCLEAR** |

### z = 10⁹ (BBN)

| Parameter | Value | Factor Change | Units |
|-----------|-------|--------------|-------|
| n_ν | 3.36 × 10³² | ×10²⁷ | m⁻³ |
| T_ν | ~2×10⁹ | ×10⁹ | K |
| E_pair | ~4.5 × 10¹⁸ | ×0.84 | eV |
| Λ_QCT | ~9.2 × 10¹³ | ×0.86 | eV (92 TeV) |
| G_eff/G_N | ~0.84 | ×0.93 | - |
| ΔG/G | -16% | Within |<20%| |

**BBN Constraint:** |ΔG/G| < 20% at z ~ 10⁹
**QCT Result:** ΔG/G ≈ -16%  ✓ **PASS**

**Source:** appendix_cosmological_evolution_REPLACEMENT.tex, lines 184-212

---

## TABLE 7: Dark Energy Evolution

| Component | Today (z=0) | Saturation (z~10⁶) | Formula |
|-----------|------------|-------------------|---------|
| **Pair density** | ρ_pairs(0) = 1.39 × 10⁻²⁹ GeV⁴ | ρ_pairs^sat = 0.3 GeV⁴ | n_ν(z) × E_pair(z) |
| **Coherence** | f_c = 1.07 × 10⁻¹⁰ | Same | m_ν / m_p |
| **Averaging** | f_avg ∼ 1 | Same | Nonlocal kernel |
| **Topological** | f_freeze = 6.7 × 10⁻⁹ | Set at saturation | Phenomenological |
| **Final ρ_Λ** | 1.0 × 10⁻⁴⁷ GeV⁴ | N/A | ρ_pairs × f_c × f_avg × f_freeze |
| **Observed** | 1.0 × 10⁻⁴⁷ GeV⁴ | - | Planck 2018 |

**Triple Suppression:**
- Factor 10¹⁰ from coherence (m_ν/m_p)
- Factor ~1 from nonlocal averaging
- Factor 10⁸ from topological freezing

**Total:** ~10¹⁸ suppression from saturation value!

**Source:** appendix_dark_energy_from_saturation.tex, lines 154-207

---

## TABLE 8: Implementation Checklist

### ✅ VERIFIED CORRECT

| Item | Formula | File | Line |
|------|---------|------|------|
| n_ν(z) evolution | n_ν(0) × (1+z)³ | qct_vs_cmb_CORRECTED_n_nu_evolution.py | 62 |
| G_eff without τ³ | E_pair(z)/E_pair(0) | appendix_cosmological_evolution_REPLACEMENT.tex | 147 |
| Logarithmic Λ_QCT | (3/2)√[E_pair × m_p] | qct_vs_cmb_CORRECTED_n_nu_evolution.py | 93 |
| CMB free-streaming | Γ/H ≪ 1 | section_5_7_cmb_phase_shift.tex | 42 |

### ⚠️ NEEDS UPDATE

| Item | Current Problem | Should Be | Priority |
|------|----------------|-----------|----------|
| BAO simulations | May use constant n_ν | n_ν(0) × (1+z)³ | **HIGH** |
| E_pair evolution | Missing turn-on function | Add f_turnon sigmoid | **MEDIUM** |
| R_proj scaling | Ambiguous in manuscript | Clarify with author | **LOW** |
| H(z) modification | Global vs local unclear | Define scope clearly | **MEDIUM** |

### ❓ AMBIGUOUS (Needs Clarification)

| Item | Manuscript Says | Simulation Does | Resolution Needed |
|------|-----------------|----------------|-------------------|
| R_proj | "Physical distance" (constant?) | Scales as (1+z)⁻³/² | **AUTHOR CLARIFICATION** |
| H(z) scope | "BAO relations preserved" vs "H²∝G_eff" | Uses modified H globally | **AUTHOR CLARIFICATION** |
| Λ_QCT at high z | Logarithmic vs Conformal | Uses logarithmic | Confirm log is correct |

---

## TABLE 9: Manuscript Equation Numbers

| Equation Number | Content | File | Line | Status |
|-----------------|---------|------|------|--------|
| Eq. (97) | E_pair(z) = E₀ + κ_conf f(z) ln(1+z) | appendix_cosmological_evolution | 97 | ✅ VERIFIED |
| Eq. (103-104) | f_turnon sigmoid function | appendix_cosmological_evolution | 103 | ⚠️ NOT IN SIMS |
| Eq. (147) [BOXED] | G_eff(z)/G_eff(0) = E_pair(z)/E_pair(0) | appendix_cosmological_evolution | 147 | ✅ CRITICAL, CORRECTED |
| Eq. (23) | Γ_QCT ∝ T⁵/Λ⁴ | section_5_7_cmb | 23 | ✅ VERIFIED |
| Line 26 | Λ_QCT(z) = (3/2)√[E_pair(z) m_p] | section_5_7_cmb | 26 | ✅ IMPLEMENTED |
| Line 40 | H²_QCT = 0.9 H²_ΛCDM | section_5_8_bao | 40 | ❓ SCOPE UNCLEAR |

---

## TABLE 10: Error History (What Was Fixed)

| Error | Discovered | Impact | Fix | Status |
|-------|-----------|--------|-----|--------|
| **n_ν constant** | 2025-12-19 | CMB calculations wrong by factor ~10⁹ | Use n_ν(z) = n_ν(0)(1+z)³ | ✅ FIXED (CMB) |
| **G_eff with τ³** | Pre-2025 | G_BBN ~ 10⁻⁴² (unphysical) | Remove τ_Hubble³ factor | ✅ MANUSCRIPT CORRECTED |
| **Conformal Λ_QCT** | N/A | Would give Λ ~ 3500 TeV at CMB | Use logarithmic form only | ⚠️ CLARIFY IN SIMS |

---

## SUMMARY: Most Critical Points

### 🔴 HIGHEST PRIORITY

1. **n_ν(z) = n_ν(0) × (1+z)³** - NOT constant!
   - Already fixed in CMB code
   - **MUST CHECK** all BAO codes

2. **G_eff(z) = G_eff(0) × E_pair(z)/E_pair(0)** - NO τ³ factor!
   - Old formula was WRONG
   - Manuscript explicitly corrected this

### 🟡 MEDIUM PRIORITY

3. **Add turn-on function** to E_pair(z)
   - Most codes use simple logarithmic
   - Should add sigmoid for z < z_start

4. **Clarify H(z) modification scope**
   - Is it global or local?
   - Manuscript seems contradictory

### 🟢 LOW PRIORITY

5. **R_proj evolution**
   - Manuscript ambiguous
   - Contact author for clarification

6. **Remove conformal Λ_QCT** from any code
   - Logarithmic form is correct
   - Conformal is geometric illustration only

---

**Document Version:** 1.0
**Last Updated:** 2025-12-19
**Companion Documents:**
- COMPREHENSIVE_MANUSCRIPT_ANALYSIS_REDSHIFT_PARAMETERS.md (detailed analysis)
- QUICK_REFERENCE_REDSHIFT_PARAMETERS.md (code templates)
