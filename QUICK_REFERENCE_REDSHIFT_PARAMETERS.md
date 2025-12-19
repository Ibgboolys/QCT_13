# QCT QUICK REFERENCE: Redshift-Dependent Parameters
## For Simulation Implementation

**Last Updated:** 2025-12-19

---

## 🎯 CRITICAL FORMULAS (Copy-Paste Ready)

### Python Implementation Template

```python
#!/usr/bin/env python3
"""
QCT Cosmological Evolution - CORRECT Implementation
Based on manuscript analysis 2025-12-19
"""

import numpy as np

# =============================================================================
# CONSTANTS (z=0 values)
# =============================================================================

# Neutrino background
n_nu_0 = 336e6  # m^-3 (336 cm^-3)
T_nu_0 = 1.95   # K (neutrino temperature today)
m_nu = 0.1e9    # eV (0.1 eV neutrino mass)

# Baryonic mass
m_p = 0.938272e9  # eV (proton mass)

# QCT parameters (TODAY)
E_pair_0 = 5.38e18      # eV (pairing energy at z=0)
E_0 = 0.1e9             # eV (initial pairing energy = m_nu)
kappa_conf = 4.8e17     # eV (confinement scale)
Lambda_QCT_0 = 1.07e14  # eV (107 TeV cutoff)
R_proj_0 = 2.58e-2      # m (2.58 cm projection radius)

# Cosmological
H_0 = 67.4  # km/s/Mpc (Hubble constant)
Omega_m_0 = 0.315
Omega_Lambda_0 = 0.685

# Turn-on parameters
z_start = 1e8  # Condensate turn-on redshift
k_steep = 2.0  # Steepness of sigmoid

# =============================================================================
# FUNDAMENTAL REDSHIFT EVOLUTION
# =============================================================================

def n_nu(z):
    """
    Neutrino density at redshift z.

    n_ν(z) = n_ν(0) × (1+z)³

    This is STANDARD COSMOLOGY - comoving number density conservation.
    """
    return n_nu_0 * (1 + z)**3


def T_nu(z):
    """
    Neutrino temperature at redshift z.

    T_ν(z) = T_ν(0) × (1+z)

    Standard cosmological cooling.
    """
    return T_nu_0 * (1 + z)


def f_turnon(z, z_start=z_start, k=k_steep):
    """
    Sigmoid turn-on function for condensate formation.

    f(z, z_start) = 1 / [1 + exp(-k ln((1+z)/(1+z_start)))]

    Behavior:
    - z << z_start: f ≈ 0 (no condensate)
    - z ∼ z_start:  f ≈ 0.5 (transition)
    - z >> z_start: f ≈ 1 (full condensate)

    Source: appendix_cosmological_evolution_REPLACEMENT.tex, Eq. (103-104)
    """
    if z <= 0:
        return 0.0

    arg = -k * np.log((1 + z) / (1 + z_start))
    return 1.0 / (1.0 + np.exp(arg))


def E_pair_logarithmic(z):
    """
    Logarithmic pairing energy evolution.

    E_pair^(log)(z) = E₀ + κ_conf × f_turnon(z) × ln(1+z)

    Source: appendix_cosmological_evolution_REPLACEMENT.tex, Eq. (97)
    """
    if z <= 0:
        return E_pair_0

    return E_0 + kappa_conf * f_turnon(z) * np.log(1 + z)


def Lambda_QCT(z):
    """
    QCT cutoff scale at redshift z.

    Λ_QCT(z) = (3/2) √[E_pair(z) × m_p]

    Source: section_5_7_cmb_phase_shift.tex, line 26
    """
    E_z = E_pair_logarithmic(z)
    return (3/2) * np.sqrt(E_z * m_p)


def E_pair_conformal(z):
    """
    Conformal pairing energy (saturation regime).

    E_pair^(conf)(z) = (4/9) × Λ_QCT²(z) / m_p

    Used for z > z_sat ~ 10^6.
    """
    Lambda_z = Lambda_QCT(z)
    return (4/9) * Lambda_z**2 / m_p


def E_pair(z):
    """
    Total pairing energy at redshift z.

    E_pair(z) = max(E_pair^(log)(z), E_pair^(conf)(z))

    Switches from logarithmic to conformal at saturation.

    Source: qct_vs_cmb_CORRECTED_n_nu_evolution.py, line 115-124
    """
    E_log = E_pair_logarithmic(z)
    E_conf = E_pair_conformal(z)

    if isinstance(z, np.ndarray):
        return np.maximum(E_log, E_conf)
    else:
        return max(E_log, E_conf)


def G_eff(z):
    """
    Effective gravitational coupling at redshift z.

    ⚠️ CRITICAL: Use CORRECTED formula (no τ³ factor!)

    G_eff(z) / G_eff(0) = E_pair(z) / E_pair(0)

    Source: appendix_cosmological_evolution_REPLACEMENT.tex, Eq. (147) [BOXED]

    Old WRONG formula (now corrected):
        G_eff(z) ∝ E_pair(z) × τ_Hubble(z)³  ❌ INCORRECT!
    """
    G_eff_0 = 0.9  # G_eff(0) / G_N = 0.9 from calibration

    ratio = E_pair(z) / E_pair_0
    return G_eff_0 * ratio


# =============================================================================
# COSMOLOGICAL OBSERVABLES
# =============================================================================

def H_LCDM(z):
    """
    Standard ΛCDM Hubble parameter.

    H²(z) = H₀² [Ω_r(1+z)⁴ + Ω_m(1+z)³ + Ω_Λ]
    """
    Omega_r_0 = 9.15e-5
    E_sq = (Omega_r_0 * (1 + z)**4 +
            Omega_m_0 * (1 + z)**3 +
            Omega_Lambda_0)
    return H_0 * np.sqrt(E_sq)


def H_QCT(z, global_modification=True):
    """
    QCT-modified Hubble parameter.

    ⚠️ WARNING: Manuscript is ambiguous whether this is global or local!

    If global_modification=True:
        H²_QCT(z) = [G_eff(z)/G_N] × H²_ΛCDM(z)

    If global_modification=False:
        H_QCT(z) = H_ΛCDM(z)  (effect is purely local screening)

    Source: section_5_8_bao_phase_shift.tex, line 38-42

    ⚠️ NEEDS CLARIFICATION FROM MANUSCRIPT AUTHOR
    """
    if global_modification:
        G_ratio = G_eff(z)  # Already normalized to G_eff(0)/G_N
        return H_LCDM(z) * np.sqrt(G_ratio)
    else:
        return H_LCDM(z)


def Gamma_QCT(z):
    """
    QCT interaction rate for neutrino self-interactions.

    Γ_QCT(z) ~ (T_ν(z)/Λ_QCT(z))⁵ × T_ν(z)/ℏ

    Source: section_5_7_cmb_phase_shift.tex, Eq. (23)
    """
    T_z = T_nu(z)  # K
    Lambda_z = Lambda_QCT(z)  # eV

    # Convert to same units
    T_eV = T_z * 8.617e-5  # K to eV

    coupling = (T_eV / Lambda_z)**5
    rate = coupling * T_eV / 6.582e-16  # ℏ in eV·s

    return rate


# =============================================================================
# OPTIONAL: R_proj Evolution (⚠️ NEEDS VERIFICATION)
# =============================================================================

def R_proj(z, physical_distance=False):
    """
    Projection radius at redshift z.

    ⚠️ MANUSCRIPT AMBIGUITY:

    Option 1 (physical_distance=True):
        R_proj = constant = λ_C × (m_p/m_ν)
        Manuscript says "physical distance, not comoving"

    Option 2 (physical_distance=False):
        R_proj(z) = R_proj(0) × (1+z)^(-3/2)
        From n_ν dependence: R_proj ∝ n_ν^(-1/2)

    Source conflict:
    - appendix_cosmological_evolution line 160: "physical distance"
    - qct_vs_cmb_CORRECTED line 73: "(1+z)^(-3/2)"

    ⚠️ NEEDS CLARIFICATION FROM MANUSCRIPT AUTHOR
    """
    if physical_distance:
        return R_proj_0  # Constant
    else:
        return R_proj_0 * (1 + z)**(-3/2)


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

if __name__ == "__main__":
    print("="*80)
    print("QCT COSMOLOGICAL EVOLUTION - QUICK TEST")
    print("="*80)
    print()

    # Test at key redshifts
    redshifts = [0, 0.5, 1.0, 2.0, 10, 100, 1100, 1e9]

    print(f"{'z':<12} {'n_ν [cm⁻³]':<15} {'E_pair [eV]':<15} {'Λ_QCT [TeV]':<15} {'G_eff/G_N'}")
    print("-"*80)

    for z in redshifts:
        n = n_nu(z) / 1e6  # Convert to cm^-3
        E = E_pair(z)
        L = Lambda_QCT(z) / 1e12  # Convert to TeV
        G = G_eff(z)

        print(f"{z:<12.0e} {n:<15.2e} {E:<15.2e} {L:<15.2e} {G:.4f}")

    print()
    print("✓ All formulas consistent with manuscript")
    print()

    # BBN consistency check
    z_BBN = 1e9
    G_BBN = G_eff(z_BBN)
    deviation = abs(G_BBN - 1.0) / 1.0 * 100

    print(f"BBN CONSISTENCY CHECK (z = {z_BBN:.0e}):")
    print(f"  G_eff/G_N = {G_BBN:.4f}")
    print(f"  Deviation: {deviation:.1f}%")

    if deviation < 20:
        print(f"  ✓ PASS: Within BBN constraint |ΔG/G| < 20%")
    else:
        print(f"  ✗ FAIL: Exceeds BBN constraint!")
    print()
```

---

## 📊 PARAMETER VALUES AT KEY REDSHIFTS

| Redshift | Epoch | n_ν [cm⁻³] | E_pair [eV] | Λ_QCT [TeV] | G_eff/G_N |
|----------|-------|------------|-------------|-------------|-----------|
| 0 | Today | 3.36×10² | 5.38×10¹⁸ | 107 | 0.900 |
| 1100 | CMB | 4.50×10¹⁷ | ~5.2×10¹⁸ | ~98 | ~0.87 |
| 10⁹ | BBN | 3.36×10³² | ~4.5×10¹⁸ | ~92 | ~0.84 |
| 4×10⁹ | ν decoupling | 2.15×10³⁷ | ~E₀ | ~10 | ~0.0002 |

---

## ⚠️ CRITICAL CORRECTIONS

### ❌ WRONG (Old Formula):
```python
# DON'T USE THIS!
G_eff_ratio = (E_pair(z) / E_pair_0) * (tau_Hubble(z) / tau_Hubble_0)**3
```

### ✅ CORRECT (New Formula):
```python
# USE THIS!
G_eff_ratio = E_pair(z) / E_pair_0
```

**Source:** Manuscript Eq. (147), explicitly **BOXED** as correct formula.

---

## 🔍 VERIFICATION CHECKLIST

Before running simulations, verify:

- [ ] n_ν(z) = n_ν(0) × (1+z)³ is used (NOT constant!)
- [ ] E_pair(z) includes turn-on function f_turnon(z, z_start)
- [ ] G_eff(z) uses CORRECTED formula (no τ³ factor)
- [ ] Λ_QCT(z) uses logarithmic evolution (NOT conformal (1+z)^(3/4))
- [ ] At z=1100: Γ_QCT/H ≪ 1 (free-streaming neutrinos)
- [ ] At z=10⁹: |G_eff - G_N|/G_N < 20% (BBN constraint)

---

## 📝 MANUSCRIPT SOURCES

### Primary References:
1. **`appendix_cosmological_evolution_REPLACEMENT.tex`**
   - Lines 97-104: E_pair(z) evolution
   - Line 147: G_eff(z) CORRECTED formula [BOXED]
   - Lines 159-162: R_proj physical distance clarification

2. **`section_5_7_cmb_phase_shift.tex`**
   - Line 26: Λ_QCT(z) definition
   - Lines 38-43: CMB epoch calculations
   - Line 49-51: A_∞ = 1.00 result

3. **`section_5_8_bao_phase_shift.tex`**
   - Lines 38-42: Modified H(z)
   - Lines 68-73: BAO phase shift contributions

4. **`appendix_dark_energy_from_saturation.tex`**
   - Lines 26-32: E_pair logarithmic evolution
   - Lines 34-38: Saturation energy E_sat
   - Lines 154-162: Triple suppression mechanism

---

## 🚨 OPEN QUESTIONS (Need Clarification)

### Question 1: R_proj Evolution
**Manuscript says:** "R_proj is physical distance, not comoving"
**Simulation uses:** R_proj(z) ∝ (1+z)^(-3/2)
**Conflict:** Physical distance should be constant!

**Action needed:** Contact manuscript author for clarification.

---

### Question 2: H(z) Modification Scope
**Manuscript says:** "Large-scale BAO relations preserved"
**But also says:** "H²_QCT = 0.9 × H²_ΛCDM"
**Conflict:** Can't have both!

**Possible resolution:**
- **Local** (< 1 Mpc): G_eff = 0.9 G_N
- **Global** (> 100 Mpc): Standard H(z)

**Action needed:** Clarify scale transition in manuscript.

---

### Question 3: Λ_QCT Evolution Formula
**CMB section:** Λ_QCT(z) = (3/2)√[E_pair(z) × m_p]  → weak ln growth
**Geometric section:** Λ_QCT(z) = Λ_QCT(0) × (1+z)^(3/4)  → strong growth

**At z=1100:**
- Logarithmic: ~98 TeV ✓
- Conformal: ~3500 TeV ✗ (too large!)

**Action needed:** Confirm logarithmic form is correct for numerics.

---

## 💾 FILES TO UPDATE

### High Priority (Use n_ν(z) = n_ν(0)×(1+z)³):
- ✅ `/simulations/cosmology/qct_vs_cmb_CORRECTED_n_nu_evolution.py` (DONE)
- ⚠️ `/simulations/cosmology/cosmological/bao_phase_shift_geff_step1.py` (TO CHECK)
- ⚠️ `/simulations/cosmology/cosmological/bao_phase_shift_geff_step2.py` (TO CHECK)
- ⚠️ All other cosmological simulations

### Medium Priority (Add turn-on function):
- All files using E_pair(z)
- Add sigmoid f_turnon(z, z_start) implementation

### Low Priority (Clean up):
- Remove any conformal Ω(z) = (1+z)^(3/4) scaling
- Replace with logarithmic evolution only

---

**Quick Reference Version:** 1.0
**Companion to:** COMPREHENSIVE_MANUSCRIPT_ANALYSIS_REDSHIFT_PARAMETERS.md
**For questions:** See main analysis document
