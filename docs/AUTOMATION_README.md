# QCT Repository Automation System

**Version:** 1.0
**Date:** 2025-11-16
**Status:** Ready for production

---

## 🎯 Overview

Complete automation suite for the Quantum Compression Theory research repository:

- ✅ **Automated data mining** - Extract parameters and equations from LaTeX
- ✅ **GitHub Actions CI/CD** - Validate LaTeX compilation and parameter consistency
- ✅ **GitHub Pages** - Interactive documentation website
- ✅ **Repository organization** - Clean, logical file structure
- ✅ **Consistency checking** - Automatic validation of parameter values

---

## 🚀 Quick Start

### Run All Automation

```bash
# 1. Extract parameters and equations from LaTeX
cd /home/user/QCT_9
python3 tools/data_mining/extract_parameters.py
python3 tools/data_mining/extract_equations.py

# 2. Build documentation site
python3 tools/build_docs_site.py

# 3. View results
ls -lh data/
# - parameters.json          # Parameter database
# - equations.json           # Equation index
# - PARAMETER_REPORT.md      # Human-readable parameter report
# - EQUATION_INDEX.md        # Human-readable equation index

# 4. Open documentation site
firefox docs_site/index.html  # or your preferred browser
```

### Reorganize Repository (Optional)

```bash
# Preview reorganization (dry run)
python3 tools/reorganize_repository.py

# Execute reorganization
python3 tools/reorganize_repository.py --execute
```

---

## 📁 Tool Descriptions

### 1. Parameter Extraction (`tools/data_mining/extract_parameters.py`)

**Purpose:** Automatically mine all physical parameters from LaTeX sources

**Features:**
- Recognizes QCT-specific parameters (Λ_micro, E_pair, κ_conf, etc.)
- Extracts values, units, and uncertainties
- Categorizes as fitted/calibrated/derived/measured
- Detects inconsistencies across files
- Generates JSON database and markdown report

**Output:**
- `data/parameters.json` - Machine-readable database
- `data/PARAMETER_REPORT.md` - Human-readable report with consistency checks

**Usage:**
```bash
python3 tools/data_mining/extract_parameters.py

# Custom paths
python3 tools/data_mining/extract_parameters.py \
    --latex-dir /path/to/latex \
    --output-dir /path/to/output
```

**Example Output:**
```
✓ Database generated: data/parameters.json
  Total parameters: 156
  Unique parameters: 18

✓ Report generated: data/PARAMETER_REPORT.md
```

---

### 2. Equation Extraction (`tools/data_mining/extract_equations.py`)

**Purpose:** Index all equations and validate cross-references

**Features:**
- Extracts from all equation environments (equation, align, etc.)
- Tracks labels and references
- Validates \eqref{} and \ref{eq:} references
- Groups by file and section

**Output:**
- `data/equations.json` - Equation database
- `data/EQUATION_INDEX.md` - Searchable index

**Usage:**
```bash
python3 tools/data_mining/extract_equations.py
```

**Validation:**
Automatically detects broken references:
```
⚠️ BROKEN REFERENCES FOUND:
- preprint.tex:1234: eq:missing_label
```

---

### 3. Documentation Site Builder (`tools/build_docs_site.py`)

**Purpose:** Generate static HTML documentation site

**Features:**
- Interactive parameter browser with search
- Equation index with LaTeX rendering (MathJax)
- Analysis document catalog
- Simulation gallery
- Mobile-responsive design

**Output:**
- `docs_site/` - Complete static website

**Usage:**
```bash
python3 tools/build_docs_site.py

# Open in browser
firefox docs_site/index.html
```

**Pages Generated:**
- `index.html` - Home with overview statistics
- `parameters.html` - Searchable parameter database
- `equations.html` - Searchable equation index
- `analyses.html` - Document catalog
- `simulations.html` - Simulation gallery

---

### 4. Repository Reorganizer (`tools/reorganize_repository.py`)

**Purpose:** Restructure repository into logical hierarchy

**Current Structure (Chaotic):**
```
/
├── *.md (25+ files scattered)
├── *.py (41 files scattered)
└── QCT_7-QCT/
```

**New Structure (Organized):**
```
/
├── docs/analyses/          # Categorized analyses
│   ├── critical/
│   ├── theoretical/
│   ├── numerical/
│   └── ...
├── src/                    # Source files
│   ├── latex/
│   ├── simulations/
│   └── literature/
├── tools/                  # Development tools
│   ├── data_mining/
│   ├── validation/
│   └── visualization/
└── data/                   # Generated data
```

**Usage:**
```bash
# Dry run (preview only)
python3 tools/reorganize_repository.py

# Execute reorganization
python3 tools/reorganize_repository.py --execute
```

**⚠️ Important:** Creates `docs/REORGANIZATION_GUIDE.md` with all path mappings

---

## 🔄 GitHub Actions Workflows

### LaTeX Validation (`.github/workflows/latex-validation.yml`)

**Triggers:**
- Push to any branch modifying LaTeX files
- Pull requests to main/QCT branches

**Actions:**
1. Check LaTeX syntax (brace matching, etc.)
2. Extract and validate parameters
3. Extract and validate equation references
4. Attempt compilation (warns on errors)
5. Upload artifacts (PDF, logs, reports)
6. Comment on PR with validation results

**Artifacts:**
- `preprint.pdf` (if compilation succeeds)
- `preprint.log`
- `PARAMETER_REPORT.md`
- `EQUATION_INDEX.md`

---

### Python Simulation Tests (`.github/workflows/simulation-tests.yml`)

**Triggers:**
- Push to any branch modifying Python files
- Pull requests to main/QCT branches

**Actions:**
1. Run syntax validation on all scripts
2. Execute key simulations (with timeout)
3. Check for hardcoded parameter inconsistencies
4. Run code quality checks (flake8, black)
5. Upload simulation outputs

**Artifacts:**
- Generated plots (PNG, PDF)
- Data files (CSV)

---

### GitHub Pages Deployment (`.github/workflows/github-pages.yml`)

**Triggers:**
- Push to main or QCT branch
- Manual workflow dispatch

**Actions:**
1. Extract parameters and equations
2. Build documentation site
3. Deploy to GitHub Pages

**Result:**
Live documentation at: `https://<username>.github.io/QCT_9/`

---

## 📊 Data Outputs

### Parameter Database (`data/parameters.json`)

**Structure:**
```json
{
  "metadata": {
    "generated": "2025-11-16",
    "total_parameters": 156,
    "unique_parameters": 18
  },
  "parameters": {
    "Lambda_micro": [
      {
        "name": "Lambda_micro",
        "symbol": "Λ_micro",
        "value": "6 × 10^13",
        "unit": "eV",
        "uncertainty": null,
        "location": "preprint.tex:456",
        "category": "fitted",
        "context": "..."
      }
    ]
  }
}
```

**Uses:**
- Machine processing
- Consistency validation
- Documentation generation
- Research queries

---

### Equation Database (`data/equations.json`)

**Structure:**
```json
{
  "metadata": {
    "generated": "2025-11-16",
    "total_equations": 287,
    "labeled_equations": 134
  },
  "equations": [
    {
      "label": "eq:pairing_energy",
      "content": "E_{\\text{pair}} = ...",
      "location": "preprint.tex:1234",
      "references": ["eq:cutoff_scale"],
      "is_numbered": true,
      "section": "Microscopic Framework"
    }
  ],
  "labels": {
    "eq:pairing_energy": { ... }
  }
}
```

**Uses:**
- Reference validation
- Equation search
- Cross-reference mapping
- Documentation

---

## 🧪 Testing

### Test Parameter Extraction

```bash
cd /home/user/QCT_9
python3 tools/data_mining/extract_parameters.py

# Check output
cat data/PARAMETER_REPORT.md | grep "INCONSISTENCIES"
# Should show: ✓ All parameter values are consistent
# OR list specific inconsistencies to fix
```

### Test Equation Extraction

```bash
python3 tools/data_mining/extract_equations.py

# Check for broken references
cat data/EQUATION_INDEX.md | grep "BROKEN REFERENCES"
# Should show: ✓ All equation references are valid
# OR list broken references to fix
```

### Test Documentation Site

```bash
python3 tools/build_docs_site.py

# Open in browser
firefox docs_site/index.html

# Check all pages load:
# - index.html
# - parameters.html
# - equations.html
# - analyses.html
# - simulations.html
```

### Test GitHub Actions Locally

```bash
# Install act (GitHub Actions local runner)
# https://github.com/nektos/act

act push -j validate-latex
act push -j test-simulations
```

---

## 🛠️ Maintenance

### Update Parameter Patterns

Edit `tools/data_mining/extract_parameters.py`:

```python
KNOWN_PARAMETERS = {
    r'\\new_parameter|\\newparam': ('new_param', 'Description'),
    # Add more patterns...
}
```

### Add New Equation Environment

Edit `tools/data_mining/extract_equations.py`:

```python
EQUATION_ENVS = [
    'equation', 'align', 'multline',
    'your_custom_env',  # Add here
]
```

### Customize Documentation Site

Edit `tools/build_docs_site.py`:

- Modify HTML templates in `build_*_page()` methods
- Update CSS in `build_css()`
- Update JavaScript in `build_js()`

---

## 📈 Performance

**Typical execution times:**

| Task | Time | Output Size |
|------|------|-------------|
| Parameter extraction | ~2-5s | 50-100 KB JSON |
| Equation extraction | ~3-7s | 100-500 KB JSON |
| Documentation site build | ~1-2s | 2-5 MB HTML |
| Full automation suite | ~10s | - |

**Scaling:**
- Works with 100+ LaTeX files
- Handles 1000+ equations
- Supports 100+ parameters

---

## 🔧 Troubleshooting

### "Module not found" errors

```bash
# Ensure you're in repository root
cd /home/user/QCT_9

# Run with python3
python3 tools/data_mining/extract_parameters.py
```

### LaTeX compilation fails

```bash
# Check log file
cat QCT_7-QCT/latex_source/preprint.log

# Common issues:
# - Missing \end{environment}
# - Undefined \ref{}
# - Missing package
```

### GitHub Actions fail

1. Check workflow logs in GitHub Actions tab
2. Look for specific error messages
3. Run locally first to debug
4. Verify all paths are correct after reorganization

### Documentation site displays incorrectly

```bash
# Rebuild completely
rm -rf docs_site/
python3 tools/build_docs_site.py

# Check browser console for JavaScript errors
# Open docs_site/index.html in browser, press F12
```

---

## 🎯 Roadmap

### Completed ✅
- [x] Parameter extraction from LaTeX
- [x] Equation indexing and validation
- [x] GitHub Actions CI/CD
- [x] GitHub Pages documentation site
- [x] Repository reorganization tool

### Planned 🔮
- [ ] Parameter uncertainty propagation calculator
- [ ] Automated LaTeX table generation from parameters.json
- [ ] BibTeX reference validation
- [ ] Simulation result database
- [ ] Interactive parameter correlation visualizations
- [ ] Automated consistency reports in LaTeX format
- [ ] Integration with Overleaf (LaTeX collaboration)
- [ ] PDF annotation extraction (from peer reviews)

---

## 📝 Contributing

When adding new automation:

1. **Create tool in `tools/` subdirectory**
   ```bash
   tools/
   └── category/
       └── new_tool.py
   ```

2. **Follow naming conventions:**
   - Functions: `snake_case`
   - Classes: `PascalCase`
   - Files: `snake_case.py`

3. **Add docstrings:**
   ```python
   """
   Tool Name: Brief Description

   Detailed explanation of what this tool does,
   how it works, and what outputs it generates.

   Author: Your Name
   Date: YYYY-MM-DD
   """
   ```

4. **Add to this README:**
   - Tool description
   - Usage examples
   - Output formats

5. **Consider GitHub Action:**
   - Should this run automatically?
   - On what trigger?
   - What artifacts to upload?

---

## 📚 Resources

- **QCT Research:** See `CLAUDE.md` for physics background
- **Critical Issues:** `PEER_REVIEW_CRITICAL_ANALYSIS.md`
- **Git Workflow:** `CLAUDE.md` section "Git Workflow"
- **GitHub Actions Docs:** https://docs.github.com/en/actions
- **GitHub Pages:** https://pages.github.com/

---

## 🙏 Acknowledgments

This automation system was developed to support the Quantum Compression Theory research project by Boleslav Plhák and Marek Novák.

**Tools used:**
- Python 3.11+
- LaTeX (TeX Live)
- GitHub Actions
- MathJax (equation rendering)

---

## 📄 License

Same as main project (MIT License, Copyright 2025 Boleslav Plhák)

---

**Last Updated:** 2025-11-16
**Maintained by:** AI Assistant & QCT Research Team
