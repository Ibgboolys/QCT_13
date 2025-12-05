# Quantum Compression Theory (QCT): Computational Framework

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## Overview

This repository contains the computational implementation and validation code for the **Quantum Compression Theory (QCT)** framework, submitted to **Progress of Theoretical and Experimental Physics (PTEP)**.

**Authors:** Boleslav Plhák, Marek Novák
**Affiliation:** Independent Researchers, Czech Republic
**Paper Status:** Under peer review at PTEP

## Purpose

This repository is provided to **PTEP reviewers** to verify the reproducibility of all numerical results, figures, and predictions reported in the manuscript. All analysis scripts, data files, and figure generation code are included with clear documentation.

---

## 🚀 Quick Start

### Requirements
```bash
pip install -r requirements.txt
```

**Python 3.8+** required. Core dependencies: `numpy`, `scipy`, `matplotlib`, `pandas`

### Running Core Analyses

**1. Generate QCT Framework Predictions:**
```bash
python simulations/core/qct_complete_framework.py
```

**2. Validate Against Experimental Data:**
```bash
python simulations/validation/validate_k_formula.py
python simulations/validation/verify_coulomb_connection.py
python simulations/validation/verify_dark_energy_calculation.py
```

**3. Reproduce Manuscript Figures:**
```bash
python simulations/core/qct_visualization_for_publication.py
```

**4. Run Full Validation Suite:**
```bash
cd simulations/validation
for script in verify_*.py validate_*.py; do python "$script"; done
```

---

## 📁 Repository Structure

```
QCT_13/
├── simulations/        # All analysis & simulation scripts (categorized)
│   ├── core/          # Core QCT framework (5 scripts)
│   ├── particle_physics/  # Mass spectra, neutrino physics (8 scripts)
│   ├── cosmology/     # Cosmological predictions & BBN (24+ scripts)
│   │   └── bao_phase_shift/  # BAO analysis pipeline (5 scripts)
│   ├── validation/    # Experimental verification (11 scripts)
│   ├── codata_analysis/  # Statistical analysis vs CODATA (5 scripts)
│   ├── constants_checks/  # Hidden constants tests (3 scripts)
│   ├── astrophysics/  # Galaxy rotation curves (5 scripts)
│   ├── golden_ratio/  # φ hierarchy in masses (3 scripts)
│   ├── rg_flow/       # Renormalization group (3 scripts)
│   ├── smeft/         # Wilson coefficients (1 script)
│   ├── theoretical_explorations/  # Exploratory calculations
│   └── tests/         # Unit tests & mocks
│
├── results/           # Output data & publication figures
│   ├── data/         # CSV result files (7 files)
│   └── figures/      # Publication-ready figures (11 PNG files)
│
├── manuscripts/       # LaTeX source for the paper
│   ├── latex_source/  # Main manuscript + 22 appendices
│   ├── integration_TEX/  # Integration documents
│   └── literature/    # Bibliography analysis
│
├── docs/             # Theoretical background & analysis notes
│   ├── theory/       # Theory overview documents
│   ├── analysis/     # Key analysis reports
│   ├── equations/    # Complete equation index
│   └── paper_notes/  # Manuscript development notes
│
├── tools/            # Utility scripts for data extraction
│
└── archive/          # Development artifacts (not for review)
```

See [`simulations/README.md`](simulations/README.md) for detailed script catalog.

---

## 🔬 Key Results Files

| File | Description | Manuscript Reference |
|------|-------------|---------------------|
| `results/data/qct_results.csv` | Core QCT predictions vs experimental values | Tables 1-2 |
| `results/figures/k_agreement_precision.png` | k-formula validation | Figure 2 |
| `results/figures/dark_energy_from_saturation.png` | Dark energy prediction | Figure 4 |
| `results/data/smeft_results.csv` | SMEFT Wilson coefficients | Table 3 |
| `results/figures/bao_phase_shift_full_spectrum.png` | BAO phase shift analysis | Figure 7 |

---

## ✅ Validation Tests

All predictions in the manuscript can be verified by running scripts in `simulations/validation/`:

- **k-formula validation:** `validate_k_formula.py` → Reproduces Table 1 (k from constants)
- **Dark energy prediction:** `verify_dark_energy_calculation.py` → Reproduces Section 4.2 (Ω_Λ)
- **Coulomb connection:** `verify_coulomb_connection.py` → Reproduces Eq. (23) (k ↔ k_Coulomb)
- **G_F correlation:** `verify_gf_rproj_correlation.py` → Reproduces Figure 5 (G_F ∝ R_proj³)

**Quick validation suite (<5 min):**
```bash
python simulations/core/qct_complete_framework.py
python simulations/validation/validate_k_formula.py
python simulations/cosmology/dark_energy_saturation.py
```

---

## 📊 Reproducibility

Each simulation script:
1. Outputs numerical results to `results/data/*.csv`
2. Generates figures to `results/figures/*.png`
3. Prints step-by-step calculations to console

**Runtime:** Most scripts complete in <1 minute on standard hardware (Intel i5/Ryzen 5 equivalent, 8GB RAM).

**Python Environment:** Tested on Python 3.8-3.11 (Linux, macOS, Windows)

---

## 📚 Documentation

- **Theory Overview:** `docs/theory/qct_framework.md` - Mathematical foundation of QCT
- **Equation Index:** `docs/equations/EQUATION_INDEX.md` - All equations used in analyses (164KB)
- **Parameter Reference:** `docs/equations/PARAMETER_REPORT.md` - Complete parameter catalog (225KB)
- **Analysis Reports:** `docs/analysis/` - Key consistency checks and correlations

---

## 🔗 Related Resources

- **Manuscript LaTeX Source:** `manuscripts/latex_source/preprint.tex`
- **Appendices:** `manuscripts/latex_source/appendix_*.tex` (22 appendices)
- **Literature Analysis:** `manuscripts/literature/` (CODATA, Hossenfelder correlations)

---

## 📄 Citation

If you use this code or reference the theory, please cite:

```bibtex
@article{plhak2025qct,
  title={Quantum Compression Theory: Emergent Gravity from Neutrino Condensate Dynamics},
  author={Plh{\'a}k, Boleslav and Nov{\'a}k, Marek},
  journal={Progress of Theoretical and Experimental Physics},
  year={2025},
  note={Submitted, under review}
}
```

---

## 📧 Contact

**For reviewers:** Questions about code reproducibility or technical issues:
- Open an issue on GitHub: https://github.com/Ibgboolys/QCT_13/issues
- Email: kelob.31415@gmail.com

**For collaboration inquiries:**
- Primary contact: Boleslav Plhák (ORCID: 0009-0003-7469-5212)

---

## 📜 License

MIT License - See [LICENSE](LICENSE) file

---

## 🙏 Acknowledgments

We thank the PTEP editorial team and anonymous reviewers for their valuable feedback and time invested in evaluating this work.

---

**For Reviewers:** All analysis scripts are documented with clear comments explaining the physics and mathematics. Start with `simulations/README.md` for a guided tour of the codebase. The validation suite in `simulations/validation/` provides independent verification of all key results.

**Repository Organization:** This repository was reorganized in December 2025 specifically for peer review, with focus on clarity, reproducibility, and professional structure. All development artifacts have been archived.
