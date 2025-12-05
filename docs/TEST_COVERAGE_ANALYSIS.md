# QCT Test Coverage Analysis and Recommendations

**Date:** 2025-11-17
**Status:** No formal test infrastructure exists
**Priority:** HIGH - Critical scientific issues require systematic validation

---

## Executive Summary

The QCT repository currently has **ZERO formal test coverage**. Given the critical issues identified in peer review (10^16 E_pair discrepancy, G_eff = 0.9 G_N conflict, circular reasoning), systematic testing is essential before publication.

**Current State:**
- ❌ No unit tests
- ❌ No integration tests
- ❌ No regression tests
- ❌ No CI/CD pipeline
- ⚠️ Only 6 ad-hoc verification scripts
- ⚠️ ~25 simulation scripts without validation

---

## 1. PRIORITY 1: Physics Consistency Tests

### 1.1 Parameter Consistency Tests

**Purpose:** Catch the 10^16 E_pair evolution discrepancy and similar issues

**Test File:** `tests/test_parameter_consistency.py`

**What to test:**
```python
def test_epair_evolution_consistency():
    """Verify E_pair(z) conformal vs logarithmic forms agree"""
    # CRITICAL: Currently differ by 10^16! (preprint.tex:1800-1832)
    E_conformal = calculate_epair_conformal(z=1e6)
    E_logarithmic = calculate_epair_logarithmic(z=1e6)

    assert abs(E_conformal - E_logarithmic) / E_logarithmic < 0.1, \
        f"E_pair forms disagree by {abs(E_conformal/E_logarithmic - 1)*100:.1f}%"

def test_geff_planetary_ephemerides():
    """Verify G_eff doesn't violate planetary motion constraints"""
    # CRITICAL: QCT predicts G_eff = 0.9 G_N, but observations constrain to 10^-8 precision
    G_eff_qct = calculate_geff()
    G_newton = 6.67430e-11

    deviation = abs(G_eff_qct - G_newton) / G_newton
    assert deviation < 1e-8, \
        f"G_eff deviates by {deviation:.2e}, violates ephemerides (< 10^-8 required)"

def test_lambda_qct_circular_reasoning():
    """Detect circular calibration: Λ_QCT ↔ E_pair ↔ G_eff"""
    # Ensure E_pair is derived independently from BCS, NOT from G_eff
    E_pair_bcs = calculate_epair_from_bcs()
    Lambda_from_epair = calculate_lambda_qct(E_pair_bcs)

    # Then check if G_eff prediction is consistent
    G_eff_predicted = predict_geff(E_pair_bcs, Lambda_from_epair)

    # Should NOT use G_eff as input to E_pair calculation
    assert not depends_on(E_pair_bcs, 'G_eff'), \
        "Circular reasoning: E_pair depends on G_eff which is 'predicted' from E_pair"

def test_parameter_count_honesty():
    """Verify claimed 4 free parameters vs actual 11 fitted"""
    free_params = count_free_parameters()
    fitted_params = count_fitted_parameters()

    # Document actual parameter count
    total = free_params + fitted_params
    assert total == 11, f"Actual parameters: {total}, not 4 as claimed"

    # Ensure manuscript matches reality
    manuscript_claim = parse_manuscript_parameter_claim()
    assert manuscript_claim >= total, \
        f"Manuscript claims {manuscript_claim}, actual is {total}"
```

**Files to create:**
- `tests/test_parameter_consistency.py`
- `tests/test_circular_reasoning.py`
- `qct/core/parameter_validator.py` (shared validation logic)

---

## 2. PRIORITY 2: Dimensional Analysis Tests

### 2.1 Unit Consistency

**Purpose:** Catch unit errors that lead to 10^16 discrepancies

**Test File:** `tests/test_dimensional_analysis.py`

**What to test:**
```python
def test_all_equations_dimensionally_consistent():
    """Every equation in simulations must have [LHS] = [RHS]"""

    # E_pair evolution
    assert check_dimensions(
        "E_pair(z) = E_0 + kappa_conf * ln(1+z)",
        E_0='eV', kappa_conf='eV', result='eV'
    )

    # Lambda_QCT relation
    assert check_dimensions(
        "Lambda_QCT = sqrt(E_pair * m_nu)",
        E_pair='eV', m_nu='eV', result='eV'
    )

    # G_eff calculation
    assert check_dimensions(
        "G_eff = (c^2 / M_Pl^2) * (rho_eff * V_proj / R_proj)",
        result='m^3 / (kg * s^2)'  # SI units for G
    )

def test_conversion_factors():
    """Verify eV ↔ GeV ↔ TeV conversions are correct"""
    eV_to_J = 1.602176634e-19
    assert abs(convert_units(1, 'eV', 'J') - eV_to_J) < 1e-28
    assert convert_units(1, 'TeV', 'eV') == 1e12

def test_energy_density_units():
    """ρ has 3 definitions (GeV^4, GeV/m^3, J/m^3) - verify conversions"""
    # CRITICAL: Appendix has ρ_ent differing by 35 orders of magnitude!
    rho_natural = 1.0  # GeV^4
    rho_hybrid = convert_energy_density(rho_natural, 'GeV4', 'GeV/m3')
    rho_SI = convert_energy_density(rho_natural, 'GeV4', 'J/m3')

    # Cross-check
    assert abs(rho_SI / rho_hybrid - 1.602e-10 * 1e9) < 1e-15
```

**Files to create:**
- `tests/test_dimensional_analysis.py`
- `qct/utils/dimension_checker.py` (automated dimension tracking)
- `qct/utils/unit_converter.py` (centralized unit conversions)

---

## 3. PRIORITY 3: Mathematical Relations Tests

### 3.1 Mathematical Constants Validation

**Purpose:** Detect look-elsewhere effect and arbitrary combinations

**Test File:** `tests/test_mathematical_constants.py`

**What to test:**
```python
def test_mathematical_constants_statistical_significance():
    """Verify claimed P_random ~ 10^-11 includes look-elsewhere effect"""
    # CRITICAL: appendix_mathematical_constants.tex:32 ignores multiple testing

    # Number of tested combinations
    n_combinations = count_tested_combinations()  # Should be documented!

    # Bonferroni correction
    P_single = 1e-11
    P_corrected = P_single * n_combinations

    assert P_corrected < 0.05, \
        f"After {n_combinations} tests, P = {P_corrected:.2e} not significant"

def test_stot_21_ratio():
    """S_tot/21 ≈ e: Why 21 = 3×7? Test if other denominators work"""
    S_tot = 58
    e = 2.71828

    # Test denominator 21
    error_21 = abs(S_tot/21 - e) / e

    # Test other plausible denominators
    for denom in [20, 21, 22, 3*6, 3*7, 3*8]:
        error = abs(S_tot/denom - e) / e
        if error < error_21:
            pytest.fail(f"Denominator {denom} gives better fit than 21!")

    # If 21 is arbitrary, this is not a prediction
    assert denominator_has_theoretical_justification(21), \
        "Denominator 21 appears arbitrary (3×7), not fundamental"

def test_coulomb_constant_postdiction():
    """k_e ≈ √(E_pair)/e found AFTER E_pair calibration"""
    # Mark as POSTDICTION, not prediction

    discovery_date = get_relation_discovery_date("coulomb_epair")
    epair_calibration_date = get_parameter_calibration_date("E_pair")

    assert discovery_date > epair_calibration_date, \
        "This is a POSTDICTION (relation found after calibration)"

    # Manuscript must label correctly
    manuscript_label = parse_manuscript_claim("coulomb_constant")
    assert "postdiction" in manuscript_label.lower() or "post-hoc" in manuscript_label.lower(), \
        "Manuscript incorrectly labels postdiction as prediction"
```

**Files to create:**
- `tests/test_mathematical_constants.py`
- `tests/test_postdiction_labeling.py`
- `qct/analysis/bayesian_validation.py` (proper statistical framework)

---

## 4. Golden Ratio Tests

### 4.1 Baryon Mass Ratio Validation

**Purpose:** Test selective fitting of φ to only 3/38 baryons

**Test File:** `tests/test_golden_ratio.py`

**What to test:**
```python
def test_golden_ratio_not_selective():
    """If φ is fundamental, ALL ground-state baryons should show it"""
    # CRITICAL: Only 3 Σ baryons fit, excited states show 14-29% errors

    phi = (1 + np.sqrt(5)) / 2

    ground_state_baryons = get_baryon_masses(state='ground')
    excited_state_baryons = get_baryon_masses(state='excited')

    ground_fits = count_phi_matches(ground_state_baryons, tolerance=0.01)
    excited_fits = count_phi_matches(excited_state_baryons, tolerance=0.01)

    # If fundamental, excited states should ALSO show φ
    fraction_ground = ground_fits / len(ground_state_baryons)
    fraction_excited = excited_fits / len(excited_state_baryons)

    assert abs(fraction_ground - fraction_excited) < 0.1, \
        f"φ appears in {fraction_ground*100:.1f}% ground vs {fraction_excited*100:.1f}% excited - selective fitting!"

def test_golden_ratio_statistical_significance():
    """Test if Λ/m ≈ 1/φ is chance or fundamental"""
    # 3 out of 38 baryons show match
    # Is this statistically significant?

    P_random = binomial_probability(
        n_trials=38,
        n_successes=3,
        p_single=0.01  # 1% tolerance
    )

    assert P_random < 0.05, \
        f"3/38 matches not statistically significant (P = {P_random:.3f})"

def test_await_lattice_qcd():
    """Golden ratio must be validated by lattice QCD (appendix_lattice_qcd.tex)"""
    # This is a placeholder - actual test requires external data

    lattice_data_available = check_lattice_qcd_data_exists()

    if not lattice_data_available:
        pytest.skip("Lattice QCD validation not yet available")
    else:
        # When data available, test predictions
        lattice_phi_ratios = get_lattice_qcd_phi_ratios()
        qct_predictions = predict_phi_ratios()

        assert agreement(lattice_phi_ratios, qct_predictions, tolerance=0.05)
```

**Files to create:**
- `tests/test_golden_ratio.py`
- `tests/test_golden_ratio_statistics.py`
- `qct/baryon/phi_validator.py`

---

## 5. Cosmological Evolution Tests

### 5.1 E_pair(z) Evolution

**Purpose:** Catch the 10^16 discrepancy between conformal and logarithmic

**Test File:** `tests/test_cosmological_evolution.py`

**What to test:**
```python
def test_epair_saturation_mechanism():
    """E_pair(z) must saturate at z_sat ~ 10^6 to avoid 10^16 discrepancy"""

    z_sat = 1e6

    # Logarithmic regime (z < z_sat)
    z_low = 1e3
    E_log = calculate_epair_logarithmic(z_low)

    # Conformal regime (z > z_sat) - should saturate
    z_high = 1e9
    E_conf = calculate_epair_conformal(z_high)

    # At EW scale (z ~ 10^15), should NOT reach 10^35 eV
    z_EW = 1e15
    E_at_EW = calculate_epair_with_saturation(z_EW, z_sat=z_sat)

    assert E_at_EW < 1e23, \
        f"E_pair at EW scale = {E_at_EW:.2e} eV, too high! Needs saturation."

    # Match at transition
    E_log_at_sat = calculate_epair_logarithmic(z_sat)
    E_conf_at_sat = calculate_epair_conformal(z_sat)

    assert abs(E_log_at_sat - E_conf_at_sat) / E_log_at_sat < 0.1, \
        "Logarithmic and conformal forms must match at z_sat"

def test_lambda_qct_running():
    """Λ_QCT(z) runs logarithmically with redshift"""

    # Test at different epochs
    epochs = {
        'BBN': 1e9,
        'Recombination': 1100,
        'Today': 0
    }

    for name, z in epochs.items():
        Lambda_z = calculate_lambda_qct(z)
        # Should be order 100 TeV ± factor 2-3
        assert 30e12 < Lambda_z < 300e12, \
            f"Λ_QCT({name}) = {Lambda_z/1e12:.1f} TeV outside reasonable range"

def test_neutrino_density_scaling():
    """n_ν(z) ∝ (1+z)^3 (standard cosmology)"""

    n_nu_0 = 336e6  # m^-3 today

    for z in [0, 1, 10, 100, 1000]:
        n_nu_z = calculate_neutrino_density(z)
        expected = n_nu_0 * (1 + z)**3

        assert abs(n_nu_z - expected) / expected < 0.01, \
            f"n_ν(z={z}) deviates from (1+z)^3 scaling"
```

**Files to create:**
- `tests/test_cosmological_evolution.py`
- `tests/test_hubble_tension.py`
- `qct/cosmology/evolution.py` (centralized evolution equations)

---

## 6. Numerical Precision Tests

### 6.1 Uncertainty Propagation

**Purpose:** Track how m_ν uncertainty (factor 2-3) affects all derived quantities

**Test File:** `tests/test_uncertainty_propagation.py`

**What to test:**
```python
def test_mnu_uncertainty_propagates():
    """m_ν ~ 0.1 eV with ±factor 2-3 uncertainty affects Λ_QCT, f_screen, R_proj"""

    m_nu_nominal = 0.1  # eV
    m_nu_min = 0.033  # eV (lower bound from cosmology)
    m_nu_max = 0.3    # eV (upper bound)

    # Calculate derived quantities
    Lambda_nominal = calculate_lambda_qct(m_nu=m_nu_nominal)
    Lambda_min = calculate_lambda_qct(m_nu=m_nu_min)
    Lambda_max = calculate_lambda_qct(m_nu=m_nu_max)

    # Propagation: Λ ~ √(E_pair * m_ν) → δΛ/Λ ~ 0.5 * δm/m
    relative_uncertainty = (Lambda_max - Lambda_min) / Lambda_nominal
    expected_uncertainty = 0.5 * (m_nu_max - m_nu_min) / m_nu_nominal

    assert abs(relative_uncertainty - expected_uncertainty) < 0.1, \
        "Uncertainty propagation incorrect"

    # Document uncertainty in all results
    assert Lambda_nominal_has_error_bars(), \
        "Λ_QCT must include ±50-200% error bars due to m_ν uncertainty!"

def test_screening_length_uncertainty():
    """λ_screen ~ R_proj ~ 1/m_ν → large uncertainty"""

    m_nu_nominal = 0.1  # eV
    m_nu_uncertainty = 2.5  # factor

    lambda_screen_nominal = calculate_screening_length(m_nu_nominal)
    lambda_screen_min = calculate_screening_length(m_nu_nominal * m_nu_uncertainty)
    lambda_screen_max = calculate_screening_length(m_nu_nominal / m_nu_uncertainty)

    # λ ∝ 1/m_ν → factor 2.5 uncertainty in m_ν → factor 2.5 in λ
    ratio = lambda_screen_max / lambda_screen_min

    assert abs(ratio - m_nu_uncertainty**2) < 1.0, \
        f"Screening length uncertainty: factor {ratio:.1f}, expected ~{m_nu_uncertainty**2:.1f}"
```

**Files to create:**
- `tests/test_uncertainty_propagation.py`
- `qct/utils/error_propagation.py` (automatic uncertainty tracking)

---

## 7. Regression Tests

### 7.1 Prevent Breaking Changes

**Purpose:** Ensure fixes don't break other results

**Test File:** `tests/test_regression.py`

**What to test:**
```python
def test_known_good_values():
    """Lock in validated results to prevent regressions"""

    # After E_pair discrepancy is fixed, lock the correct value
    E_pair_validated = 1.8e19  # eV (update after fix!)
    assert abs(calculate_epair(z=0) - E_pair_validated) < 1e17, \
        "E_pair(z=0) changed unexpectedly - regression!"

    # After G_eff conflict is resolved, lock the solution
    G_eff_validated = 6.674e-11  # m^3/(kg s^2) (should match G_N!)
    assert abs(calculate_geff() - G_eff_validated) < 1e-13, \
        "G_eff changed - check if this breaks planetary ephemerides"

    # Lock Higgs VEV relation (even though it's postdiction)
    v_higgs = 246.22  # GeV
    Lambda_micro = 0.733  # GeV
    phi_exponent = calculate_phi_exponent(v_higgs, Lambda_micro)
    assert abs(phi_exponent - 12.088) < 0.01, \
        "Higgs VEV relation changed"

def test_cosmological_predictions_unchanged():
    """Cosmological predictions should not change unless explicitly revised"""

    # Hubble tension prediction
    H_qct = calculate_hubble_constant_qct()
    assert 72 < H_qct < 75, \
        f"QCT Hubble constant changed: {H_qct} km/s/Mpc"

    # BBN predictions
    Y_p_qct = calculate_helium_abundance_qct()
    assert abs(Y_p_qct - 0.245) < 0.01, \
        "BBN prediction changed"
```

**Files to create:**
- `tests/test_regression.py`
- `tests/fixtures/validated_results.json` (reference values)

---

## 8. Integration Tests

### 8.1 End-to-End Workflows

**Purpose:** Test complete calculation pipelines

**Test File:** `tests/test_integration.py`

**What to test:**
```python
def test_full_geff_calculation_pipeline():
    """From microscopic parameters to G_eff prediction"""

    # Input: BCS parameters
    lambda_micro = 0.733  # GeV
    sigma_max_sq = 0.2

    # Step 1: Calculate E_pair from BCS
    E_pair = calculate_epair_from_bcs(lambda_micro, sigma_max_sq)

    # Step 2: Calculate Λ_QCT
    m_nu = 0.1  # eV
    Lambda_QCT = calculate_lambda_qct(E_pair, m_nu)

    # Step 3: Calculate screening
    f_screen = calculate_screening_factor(m_nu)

    # Step 4: Calculate G_eff
    G_eff = calculate_geff(E_pair, Lambda_QCT, f_screen)

    # Verify each step is dimensionally consistent
    assert check_dimensions(E_pair, 'eV')
    assert check_dimensions(Lambda_QCT, 'eV')
    assert check_dimensions(f_screen, 'dimensionless')
    assert check_dimensions(G_eff, 'm^3/(kg*s^2)')

    # Verify result
    G_newton = 6.67430e-11
    assert abs(G_eff - G_newton) / G_newton < 0.1, \
        "Full pipeline gives wrong G_eff"

def test_full_cosmological_evolution():
    """From early universe to today"""

    epochs = generate_epoch_grid(z_max=1e9, n_points=100)

    for epoch in epochs:
        # Calculate all evolving quantities
        E_pair_z = calculate_epair(epoch.z)
        Lambda_z = calculate_lambda_qct(epoch.z)
        n_nu_z = calculate_neutrino_density(epoch.z)

        # Check physical consistency at each epoch
        assert E_pair_z > 0, f"E_pair negative at z={epoch.z}"
        assert Lambda_z > 0, f"Λ_QCT negative at z={epoch.z}"
        assert n_nu_z > 0, f"n_ν negative at z={epoch.z}"

        # Check causality
        if epoch.z > 1e6:
            # Should be in saturation regime
            dE_dz = derivative(calculate_epair, epoch.z)
            assert abs(dE_dz) < 1e10, "E_pair growing too fast - violates UV cutoff"
```

**Files to create:**
- `tests/test_integration.py`
- `tests/test_workflows.py`

---

## 9. Experimental Prediction Tests

### 9.1 Testable Claims Validation

**Purpose:** Verify claimed experimental predictions are realistic

**Test File:** `tests/test_experimental_predictions.py`

**What to test:**
```python
def test_iss_vs_earth_gravity_feasibility():
    """ISS vs Earth test claims 2.5% difference on 40 μm scale"""
    # CRITICAL: Current systematics ~10 μm → UNFEASIBLE

    # QCT prediction
    delta_g_qct = calculate_gravity_difference_iss_earth()
    distance = 40e-6  # m (40 μm)
    displacement_predicted = delta_g_qct * distance

    # Current experimental systematics
    systematics = 10e-6  # m (10 μm)

    assert displacement_predicted > 3 * systematics, \
        f"Signal {displacement_predicted*1e6:.1f} μm < 3σ systematics {systematics*1e6:.1f} μm - unfeasible!"

def test_submillimeter_gravity_test():
    """λ_screen ~ 40 μm sub-mm gravity test"""

    lambda_screen = calculate_screening_length()

    # Experimental range where deviations are expected
    r_min = lambda_screen / 10
    r_max = lambda_screen * 10

    # Check if experiments in this range exist
    available_experiments = get_submm_gravity_experiments()

    for exp in available_experiments:
        if r_min < exp.distance < r_max:
            # Compare QCT prediction to experimental limit
            deviation_qct = calculate_qct_deviation(exp.distance)
            deviation_limit = exp.limit

            assert abs(deviation_qct) < deviation_limit, \
                f"{exp.name}: QCT predicts {deviation_qct:.2e}, limit is {deviation_limit:.2e}"

def test_lattice_qcd_golden_ratio_proposal():
    """Lattice QCD can test φ in baryon masses (appendix_lattice_qcd.tex:366)"""

    # Generate testable predictions
    predictions = generate_lattice_qcd_predictions()

    for baryon in ['Σ+', 'Σ0', 'Σ-']:
        # QCT prediction
        Lambda_over_m = predictions[baryon]['Lambda/m']
        phi_inv = 1 / ((1 + np.sqrt(5)) / 2)

        # Should match within lattice QCD precision (~1%)
        error_tolerance = 0.01

        assert abs(Lambda_over_m - phi_inv) / phi_inv < error_tolerance, \
            f"{baryon}: Λ/m = {Lambda_over_m:.6f} ≠ 1/φ = {phi_inv:.6f}"
```

**Files to create:**
- `tests/test_experimental_predictions.py`
- `tests/test_lattice_qcd_proposals.py`
- `qct/experimental/feasibility_checker.py`

---

## 10. Code Quality Tests

### 10.1 Simulation Script Validation

**Purpose:** Ensure all 25+ simulation scripts follow standards

**Test File:** `tests/test_simulation_quality.py`

**What to test:**
```python
def test_all_simulations_have_docstrings():
    """Every simulation script must document purpose"""

    simulation_dir = Path("QCT_7-QCT/simulations")

    for script in simulation_dir.glob("*.py"):
        with open(script) as f:
            content = f.read()

        assert '"""' in content or "'''" in content, \
            f"{script.name} missing docstring"

        # Check for key metadata
        assert 'Author:' in content or 'autor:' in content.lower()
        assert 'Date:' in content or 'datum:' in content.lower()

def test_all_simulations_use_centralized_constants():
    """No hardcoded physics constants - use qct.constants"""

    simulation_dir = Path("QCT_7-QCT/simulations")

    for script in simulation_dir.glob("*.py"):
        with open(script) as f:
            content = f.read()

        # Check for hardcoded constants (bad practice)
        bad_patterns = [
            r'c\s*=\s*2\.998',  # Speed of light
            r'hbar\s*=\s*1\.054',  # Planck constant
            r'G.*=\s*6\.67',  # Gravitational constant
        ]

        for pattern in bad_patterns:
            if re.search(pattern, content):
                pytest.fail(f"{script.name} has hardcoded constant: {pattern}")

        # Should import from centralized location
        assert 'from qct.constants import' in content or 'from scipy.constants import' in content

def test_all_simulations_include_error_bars():
    """Results must include uncertainty estimates"""

    simulation_dir = Path("QCT_7-QCT/simulations")

    for script in simulation_dir.glob("*.py"):
        # Run script and capture output
        result = subprocess.run(['python3', str(script)], capture_output=True, timeout=30)

        output = result.stdout.decode()

        # Check for uncertainty indicators
        has_uncertainty = any([
            '±' in output,
            'uncertainty' in output.lower(),
            'error' in output.lower(),
            'sigma' in output.lower(),
        ])

        assert has_uncertainty, \
            f"{script.name} produces results without uncertainty estimates"
```

**Files to create:**
- `tests/test_simulation_quality.py`
- `tests/test_code_standards.py`
- `qct/constants.py` (centralized physics constants)

---

## 11. LaTeX Consistency Tests

### 11.1 Manuscript-Simulation Agreement

**Purpose:** Ensure LaTeX equations match Python implementations

**Test File:** `tests/test_latex_consistency.py`

**What to test:**
```python
def test_latex_equations_match_code():
    """Equations in preprint.tex must match simulations/"""

    # Parse LaTeX for key equations
    latex_epair = parse_latex_equation('preprint.tex', label='eq:epair_evolution')

    # Compare to Python implementation
    code_epair = get_function_source('cosmological_evolution.py', 'calculate_epair')

    # Symbolic comparison (requires sympy)
    latex_symbolic = latex_to_sympy(latex_epair)
    code_symbolic = python_to_sympy(code_epair)

    assert latex_symbolic.equals(code_symbolic), \
        "E_pair equation in LaTeX ≠ Python implementation"

def test_all_parameter_values_consistent():
    """Parameter values in LaTeX must match simulation constants"""

    # Parse from parameter_mapping.tex
    latex_params = parse_parameter_table('parameter_mapping.tex')

    # Parse from Python constants
    from qct.constants import E_PAIR, LAMBDA_QCT, M_NU

    code_params = {
        'E_pair': E_PAIR,
        'Lambda_QCT': LAMBDA_QCT,
        'm_nu': M_NU,
    }

    for name, value_latex in latex_params.items():
        if name in code_params:
            value_code = code_params[name]

            # Allow 1% difference (for rounding)
            assert abs(value_latex - value_code) / value_code < 0.01, \
                f"{name}: LaTeX={value_latex:.3e}, Code={value_code:.3e}"

def test_notation_consistency():
    """α, ρ_ent, K(z) must have subscripts throughout"""
    # CRITICAL: α has 4 meanings, ρ_ent has 3 definitions

    latex_files = Path("QCT_7-QCT/latex_source").glob("*.tex")

    for texfile in latex_files:
        with open(texfile) as f:
            content = f.read()

        # Check for bare α (should be α_νG, α_conf, α_cosmo, α_EM)
        bare_alpha = re.findall(r'(?<!\\)alpha(?![_\\{])', content)
        assert len(bare_alpha) == 0, \
            f"{texfile.name}: Found {len(bare_alpha)} instances of bare 'alpha' without subscript"

        # Check for ρ_ent without specification
        bare_rho_ent = re.findall(r'rho_\{?ent\}?(?![\\^_])', content)
        assert len(bare_rho_ent) == 0, \
            f"{texfile.name}: ρ_ent must specify (vac), (pairs), or (cosmo)"
```

**Files to create:**
- `tests/test_latex_consistency.py`
- `tests/test_notation_standards.py`
- `qct/validation/latex_parser.py`

---

## 12. CI/CD Pipeline

### 12.1 Automated Testing

**File:** `.github/workflows/tests.yml`

**What to automate:**
```yaml
name: QCT Test Suite

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Install dependencies
      run: |
        pip install pytest numpy scipy matplotlib sympy
        pip install -e .

    - name: Run Priority 1 tests (physics consistency)
      run: pytest tests/test_parameter_consistency.py -v

    - name: Run dimensional analysis tests
      run: pytest tests/test_dimensional_analysis.py -v

    - name: Run regression tests
      run: pytest tests/test_regression.py -v

    - name: Run all simulation scripts (smoke test)
      run: |
        for script in QCT_7-QCT/simulations/*.py; do
          echo "Testing $script"
          timeout 60s python3 "$script" || echo "FAILED: $script"
        done

    - name: Generate coverage report
      run: |
        pytest --cov=qct --cov-report=html

    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

**Files to create:**
- `.github/workflows/tests.yml`
- `.github/workflows/latex_compile.yml` (test LaTeX compilation)

---

## Implementation Roadmap

### Phase 1: Immediate (1-2 weeks)
1. ✅ Create `tests/` directory structure
2. ✅ Implement `test_parameter_consistency.py` (catch 10^16 discrepancy)
3. ✅ Implement `test_dimensional_analysis.py` (prevent unit errors)
4. ✅ Create `qct/constants.py` (centralize physics constants)
5. ✅ Set up pytest infrastructure

### Phase 2: Critical Issues (2-4 weeks)
6. ✅ Implement `test_circular_reasoning.py` (Λ_QCT ↔ E_pair ↔ G_eff)
7. ✅ Implement `test_cosmological_evolution.py` (E_pair saturation)
8. ✅ Implement `test_uncertainty_propagation.py` (m_ν error bars)
9. ✅ Implement `test_postdiction_labeling.py` (honesty in claims)

### Phase 3: Validation (4-6 weeks)
10. ✅ Implement `test_golden_ratio.py` (statistical significance)
11. ✅ Implement `test_mathematical_constants.py` (look-elsewhere effect)
12. ✅ Implement `test_experimental_predictions.py` (feasibility)
13. ✅ Implement `test_regression.py` (lock validated results)

### Phase 4: Infrastructure (6-8 weeks)
14. ✅ Set up CI/CD pipeline (GitHub Actions)
15. ✅ Implement LaTeX-Python consistency checks
16. ✅ Create automated dimension checker
17. ✅ Generate test coverage reports (aim for >80%)

### Phase 5: Documentation (ongoing)
18. ✅ Document all tests in repository
19. ✅ Create `TESTING.md` guide for contributors
20. ✅ Add test badges to README

---

## Success Metrics

**Coverage Goals:**
- Unit tests: >80% code coverage
- Integration tests: All major workflows tested
- Regression tests: All validated results locked
- Parameter consistency: 100% of critical issues caught

**Quality Gates:**
- All tests pass before merge
- No new code without tests
- Coverage cannot decrease
- LaTeX and Python must agree

**Timeline:**
- Phase 1 complete before ANY further manuscript revisions
- Phase 2 complete before addressing Priority 1 issues
- Phase 3 complete before submission
- Phase 4 complete for long-term maintenance

---

## Appendix: Test File Structure

```
QCT_9/
├── tests/
│   ├── __init__.py
│   ├── conftest.py                          # pytest configuration
│   │
│   ├── test_parameter_consistency.py        # PRIORITY 1
│   ├── test_dimensional_analysis.py         # PRIORITY 1
│   ├── test_circular_reasoning.py           # PRIORITY 1
│   │
│   ├── test_cosmological_evolution.py       # PRIORITY 2
│   ├── test_uncertainty_propagation.py      # PRIORITY 2
│   ├── test_golden_ratio.py                 # PRIORITY 2
│   ├── test_mathematical_constants.py       # PRIORITY 2
│   │
│   ├── test_experimental_predictions.py     # PRIORITY 3
│   ├── test_regression.py                   # PRIORITY 3
│   ├── test_integration.py                  # PRIORITY 3
│   │
│   ├── test_latex_consistency.py            # Quality
│   ├── test_simulation_quality.py           # Quality
│   ├── test_notation_standards.py           # Quality
│   │
│   └── fixtures/
│       ├── validated_results.json
│       ├── reference_calculations.json
│       └── experimental_limits.json
│
├── qct/                                      # New package structure
│   ├── __init__.py
│   ├── constants.py                         # Centralized constants
│   ├── core/
│   │   ├── parameter_validator.py
│   │   └── bcs_solver.py
│   ├── cosmology/
│   │   ├── evolution.py
│   │   └── hubble.py
│   ├── baryon/
│   │   └── phi_validator.py
│   ├── utils/
│   │   ├── dimension_checker.py
│   │   ├── unit_converter.py
│   │   └── error_propagation.py
│   ├── validation/
│   │   ├── latex_parser.py
│   │   └── consistency_checker.py
│   └── experimental/
│       └── feasibility_checker.py
│
├── .github/
│   └── workflows/
│       ├── tests.yml
│       └── latex_compile.yml
│
├── pytest.ini
├── setup.py
└── TESTING.md
```

---

## Conclusion

The QCT repository requires **URGENT implementation of systematic testing** before submission. The identified critical issues (10^16 discrepancies, circular reasoning, postdiction mislabeling) would have been caught by proper test coverage.

**Recommendation:** Implement Phase 1-2 tests (4-6 weeks) BEFORE addressing any Priority 1 issues in PEER_REVIEW_CRITICAL_ANALYSIS.md. This will:

1. Catch regressions when fixing E_pair discrepancy
2. Prevent new circular reasoning when resolving Λ_QCT
3. Ensure fixes don't break other predictions
4. Provide confidence in revised manuscript

**Risk:** Without tests, fixing one issue may break three others.

**Next Steps:**
1. Create `tests/` directory
2. Implement `test_parameter_consistency.py`
3. Run tests and document failures
4. Fix issues systematically
5. Re-run tests until all pass
6. Lock validated results with regression tests
