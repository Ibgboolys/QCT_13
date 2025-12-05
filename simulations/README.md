# QCT Simulations: Analysis Scripts Catalog

This directory contains all computational analyses for the QCT manuscript submitted to PTEP.

---

## 📂 Directory Organization

### `core/` - Core QCT Framework (5 scripts)
**Entry point for QCT predictions. Start here.**

- **qct_complete_framework.py** - Complete QCT derivation: mathematical constants → particle masses
- **qct_complete_spectrum.py** - Full particle mass spectrum calculation
- **qct_from_constants_framework.py** - Reconstruction from measured fundamental constants
- **qct_refinement.py** - Refined parameter fitting and optimization
- **qct_visualization_for_publication.py** - Generates all manuscript figures

**Run first:** `python core/qct_complete_framework.py`

---

### `particle_physics/` - Mass Calculations & Neutrino Physics (8 scripts)

- **qct_quark_masses.py** - Quark mass hierarchy from φⁿ patterns
- **neutrino_bcs_gap_equation.py** - Independent BCS gap equation solver for neutrino condensate
- **neutrino_mass_phi58_test.py** - Test of neutrino mass relationships
- **leptogenesis_fermi_blocking.py** - Baryon asymmetry from Fermi blocking mechanism
- **lattice_qcd_simulation.py** - QCD f(m_q) interpolation (lattice QCD style)
- **vacuum_cascade_model.py** - Vacuum energy cascade mechanism
- **vacuum_partition.py** - Vacuum partition function analysis
- **group_theory_analysis.py** - Group theoretical structure of QCT

---

### `cosmology/` - Cosmological Predictions (24+ scripts)

#### Main cosmology analyses:
- **dark_energy_saturation.py** - Dark energy from E_pair saturation (**Manuscript Section 4.2**)
- **dark_energy_simple.py** - Simplified dark energy calculation
- **cosmological_evolution.py** - Full cosmological evolution model
- **cosmological_evolution_with_sigma_max.py** - Evolution with phase saturation
- **neutrino_density_evolution.py** - C𝜈B density evolution with redshift
- **test_bbn_with_physical_zstart.py** - Big Bang Nucleosynthesis with QCT corrections

#### CMB & phase shift analyses:
- **cmb_phase_shift_qct.py** - CMB anisotropy predictions
- **cmb_phase_shift_qct_simple.py** - Simplified CMB analysis

#### G_eff analyses:
- **complete_g_eff_model.py** - Complete gravitational coupling evolution
- **g_eff_analysis.py** - G_eff parameter space analysis

#### E_pair saturation:
- **epair_saturation_complete.py** - Complete E_pair saturation model
- **epair_saturation_simple.py** - Simplified saturation calculation

#### Baryon fraction:
- **spin_weighted_omega_b.py** - Baryon fraction with spin corrections
- **baryon_fraction_monte_carlo.py** - Monte Carlo Ω_b analysis
- **baryon_fraction_monte_carlo_REFINED.py** - Refined Monte Carlo analysis

#### Other:
- **sigma_max_solver.py** - Phase variance saturation solver
- **sigma_squared_calculation.py** - Phase coherence calculations
- **volume_source_analysis.py** - Volume source term analysis
- **cosmo_bounds.py** - Cosmological parameter bounds

#### `bao_phase_shift/` - BAO Analysis Pipeline (5 scripts)
**Run in order: step1 → step4**

- **step1_geff.py** - BAO phase shift from G_eff modification (step 1)
- **step2_geff.py** - BAO G_eff analysis refinement (step 2)
- **step3_neutrino.py** - Neutrino contribution to BAO (step 3)
- **step4_full_pk.py** - Full matter power spectrum P(k) calculation (step 4)
- **nonadiabatic_analysis.py** - Non-adiabatic perturbations in BAO

**Key for reproducibility:** `dark_energy_saturation.py` → Reproduces Eq. (42) in manuscript

---

### `validation/` - Experimental Verification (11+ scripts)
**Cross-checks against CODATA, PDG, and cosmological observations.**

- **validate_k_formula.py** - Core k-formula validation (**Manuscript Table 1**)
- **verify_coulomb_connection.py** - k ↔ Coulomb constant connection (**Eq. 23**)
- **verify_dark_energy_calculation.py** - Independent check of Ω_Λ prediction
- **verify_gf_rproj_correlation.py** - G_F ∝ R_proj³ correlation (**Manuscript Fig. 5**)
- **critical_test_k_formula.py** - High-precision k-formula test
- **verify_coulomb_definition.py** - Coulomb constant verification
- **verify_reconstruction_corrected.py** - Corrected reconstruction verification
- **verify_reconstruction_FINAL.py** - Final reconstruction validation
- **verify_with_critical_checks.py** - Comprehensive critical checks
- **varifikace2.py**, **varifikace3.py**, **varifikaceDM.py** - Additional validation tests

**Run full validation suite:**
```bash
cd validation
for script in verify_*.py validate_*.py; do python "$script"; done
```

---

### `codata_analysis/` - Statistical Analysis (5 scripts)

- **analyze_codata_qct_correlations.py** - CODATA cross-correlation analysis
- **advanced_codata_qct_analysis.py** - Advanced statistical analysis vs CODATA
- **deep_codata_qct_analysis.py** - Deep learning-style correlation detection
- **bayesian_model_selection.py** - Bayesian model comparison QCT vs SM
- **monte_carlo.py** - Monte Carlo uncertainty propagation

---

### `golden_ratio/` - Golden Ratio Physics (3 scripts)

- **golden_ratio_deep_analysis.py** - φⁿ hierarchy in particle masses
- **golden_ratio_visualization.py** - Visualization of φ patterns
- **higgs_vev_golden_ratio.py** - Higgs VEV from φ¹² pattern (**Appendix**)

---

### `rg_flow/` - Renormalization Group (3 scripts)

- **rg_flow_solver.py** - RG equations for QCT parameters
- **qct_np_rg.py** - Non-perturbative neutrino-photon RG flow
- **s_tot_neutrino_density_analysis.py** - S_tot from neutrino density

---

### `smeft/` - Standard Model EFT (1 script)

- **smeft_scan.py** - Wilson coefficient predictions (**Manuscript Table 3**)

---

### `astrophysics/` - Astrophysical Applications (5 scripts)

- **rotation_curves_v1.py** - Galaxy rotation curves (NGC 1560, version 1)
- **rotation_curves_v2.py** - Rotation curves refined (version 2)
- **rotation_curves_v3.py** - Rotation curves with screening (version 3)
- **rotation_curves_v4.py** - Latest rotation curve model (version 4)
- **screening_paradox.py** - QCT resolution of screening paradox

---

### `constants_checks/` - Hidden Constants & Calibration (3 scripts)

- **check_hidden_constants.py** - Verify no hidden experimental inputs in QCT
- **check_hidden_constants_simple.py** - Simplified hidden constants check
- **alpha_density_scaling.py** - α_EM density scaling analysis

---

### `theoretical_explorations/` - Exploratory Calculations (4 scripts)
**Preliminary investigations not in main manuscript.**

- **light_interpretation.py** - Alternative interpretations of speed of light
- **speed_of_light_derivation.py** - c derivation attempts
- **generate_wav.py** - Audio visualization of QCT predictions (?)
- **generate_final.py** - Final generation script

---

### `tests/` - Unit Tests & Mock Data

- **demo_test_example.py** - Example test structure
- **mocks/** - Mock implementations for fast testing
  - `calculate_dark_energy_from_saturation_mock.py`
  - `calculate_dark_energy_simple_mock.py`
  - `check_hidden_constants_mock.py`

---

## ⚡ Execution Guide

### Reproduce All Manuscript Results

```bash
# 1. Core predictions
python core/qct_complete_framework.py

# 2. Validation tests
cd validation
for f in verify_*.py validate_*.py; do python "$f"; done
cd ..

# 3. Cosmology
python cosmology/dark_energy_saturation.py
python cosmology/test_bbn_with_physical_zstart.py

# 4. Particle physics
python particle_physics/qct_quark_masses.py
python particle_physics/neutrino_bcs_gap_equation.py

# 5. Generate figures
python core/qct_visualization_for_publication.py
```

### Quick Validation (<5 min total)

```bash
python core/qct_complete_framework.py
python validation/validate_k_formula.py
python validation/verify_dark_energy_calculation.py
```

---

## 📊 Output Locations

- **Data:** `../results/data/*.csv`
- **Figures:** `../results/figures/*.png`
- **Console:** Step-by-step calculation details

---

## 📝 Manuscript Mapping

| Script | Manuscript Reference |
|--------|---------------------|
| `validation/validate_k_formula.py` | Table 1 - k-formula |
| `cosmology/dark_energy_saturation.py` | Section 4.2, Eq. (42) - Dark energy |
| `validation/verify_coulomb_connection.py` | Eq. (23) - Coulomb connection |
| `validation/verify_gf_rproj_correlation.py` | Figure 5 - G_F correlation |
| `cosmology/bao_phase_shift/step4_full_pk.py` | Figure 7 - BAO spectrum |
| `smeft/smeft_scan.py` | Table 3 - Wilson coefficients |
| `particle_physics/qct_quark_masses.py` | Table 2 - Quark masses |
| `golden_ratio/higgs_vev_golden_ratio.py` | Appendix - Higgs VEV |

---

## 💡 Notes for Reviewers

1. **Script naming:**
   - `verify_*.py` = validation against experiments
   - `calculate_*.py` = new predictions
   - `*_simple.py` = pedagogical version
   - `*_complete.py` = full calculation

2. **Version suffixes:** Scripts evolved during development:
   - `v1, v2, v3, v4` = iteration versions (later = more refined)
   - `_REFINED`, `_FINAL` = latest production versions

3. **Czech names:** Some scripts (e.g., `varifikace*.py`) retain Czech names from development. Code and physics are the same.

4. **Dependencies:** All scripts are standalone - no complex dependency chains. Can be run independently.

---

## ❓ Questions?

See `../docs/theory/qct_framework.md` for theoretical background.

For technical issues with scripts, open a GitHub issue: https://github.com/Ibgboolys/QCT_13/issues
