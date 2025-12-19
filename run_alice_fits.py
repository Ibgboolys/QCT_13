#!/usr/bin/env python3
"""
Run ALICE heavy-ion collision fits with real HEPData
"""

import sys
sys.path.insert(0, '/home/user/QCT_13')

from simulations.qct_fit.strangeness_fit import fit_omega_to_lambda_p_ratio

print("="*70)
print("ALICE HEAVY-ION COLLISION DATA FITTING")
print("="*70)
print()

# Run strangeness enhancement fit
print("STEP 1: Strangeness Enhancement (Λ/p ratio)")
print("-" * 70)

data_file = "simulations/qct_fit/data/REAL_alice_lambda_p_HEPData.csv"

try:
    results = fit_omega_to_lambda_p_ratio(
        data_file=data_file,
        plot=True,
        save_results=True,
        output_dir="results/alice_fits/"
    )

    print("\n✅ FIT COMPLETED SUCCESSFULLY")
    print(f"\nBest-fit parameters:")
    print(f"  α = {results['alpha']:.4f} ± {results['alpha_err']:.4f}")
    print(f"  x₀ = {results['x0']:.2f} ± {results['x0_err']:.2f}")
    print(f"  χ²/dof = {results['chi2_dof']:.2f}")
    print(f"  p-value = {results.get('p_value', 'N/A')}")

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

print()
print("="*70)
