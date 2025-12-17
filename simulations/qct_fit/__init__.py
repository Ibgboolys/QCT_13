"""
QCT-FIT: Numerical Protocol for ALICE Data Analysis

This package implements rigorous fitting of QCT vacuum parameters
to real ALICE heavy-ion collision data.

Modules:
    - strangeness_fit: Fits conformal factor Ω to Λ/p ratio data
    - ridge_fit: Fits damping parameter γ to v2 azimuthal anisotropy
    - data_handler: Loads and validates experimental data
    - consistency_check: Cross-checks γ between ALICE and LIGO/Virgo
"""

__version__ = "1.0.0"
__author__ = "QCT Research Team"

from .strangeness_fit import fit_omega_to_lambda_p_ratio
from .ridge_fit import fit_gamma_to_v2
from .consistency_check import cross_validate_gamma

__all__ = [
    'fit_omega_to_lambda_p_ratio',
    'fit_gamma_to_v2',
    'cross_validate_gamma'
]
