# QCT Quick Start Guide

**Get up and running with QCT automation in 5 minutes**

---

## ⚡ Super Quick Start (30 seconds)

```bash
# Clone repository (if not already done)
# cd to QCT_9 directory

# Run complete automation
bash run_automation.sh

# Open documentation
firefox docs_site/index.html
```

**Done!** You now have:
- ✅ Parameter database (`data/parameters.json`)
- ✅ Equation index (`data/equations.json`)
- ✅ Interactive documentation website (`docs_site/`)

---

## 🔧 Installation (First Time Setup)

### 1. Python Dependencies

```bash
# Install Python packages
pip install -r requirements.txt

# Or minimal install:
pip install numpy scipy matplotlib pandas
```

### 2. LaTeX (Optional - only for compilation)

```bash
# Ubuntu/Debian
sudo apt-get install texlive-latex-extra texlive-science texlive-fonts-extra

# macOS
brew install --cask mactex

# Windows
# Download from https://www.tug.org/texlive/
```

### 3. Verify Installation

```bash
# Check Python
python3 --version  # Should be 3.11+

# Check tools
python3 tools/data_mining/extract_parameters.py --help
```

---

## 📖 Common Tasks

### Task 1: Extract Parameters from LaTeX

**Purpose:** Find all physical parameters and check consistency

```bash
# Extract parameters
python3 tools/data_mining/extract_parameters.py

# View report
cat data/PARAMETER_REPORT.md

# Check for inconsistencies
grep "INCONSISTENCIES" data/PARAMETER_REPORT.md
```

**Output:**
- `data/parameters.json` - JSON database
- `data/PARAMETER_REPORT.md` - Human-readable report

**What it finds:**
- All QCT parameters (Λ_micro, E_pair, κ_conf, etc.)
- Parameter values, units, uncertainties
- Locations in LaTeX files (file:line)
- Inconsistencies across files

---

### Task 2: Index Equations

**Purpose:** Create searchable equation database, validate references

```bash
# Extract equations
python3 tools/data_mining/extract_equations.py

# View index
cat data/EQUATION_INDEX.md

# Check for broken references
grep "BROKEN REFERENCES" data/EQUATION_INDEX.md
```

**Output:**
- `data/equations.json` - JSON database
- `data/EQUATION_INDEX.md` - Searchable index

**What it finds:**
- All equations from LaTeX (equation, align, etc.)
- Labels and cross-references
- Broken \eqref{} and \ref{} references
- Section assignments

---

### Task 3: Build Documentation Website

**Purpose:** Create interactive browsable documentation

```bash
# Build site
python3 tools/build_docs_site.py

# Open in browser
firefox docs_site/index.html

# Or serve with Python
cd docs_site
python3 -m http.server 8000
# Visit http://localhost:8000
```

**What you get:**
- 📊 Parameter browser (searchable, filterable)
- 🔢 Equation index (with LaTeX rendering)
- 📝 Analysis catalog (all 25+ documents)
- 🖥️ Simulation gallery (all 40+ scripts)

---

### Task 4: Run Simulations

**Purpose:** Execute numerical simulations

```bash
cd QCT_7-QCT/simulations

# Cosmological evolution
python3 cosmological_evolution.py

# Golden ratio analysis
python3 golden_ratio_deep_analysis.py

# Verify energy budget
python3 verify_cnub_energy.py
```

**Outputs:** PNG plots, CSV data files

---

### Task 5: Validate Consistency

**Purpose:** Check parameter values across all files

```bash
# Check hidden constants
python3 check_hidden_constants.py

# Verify specific calculations
python3 verify_dark_energy_calculation.py
python3 verify_coulomb_connection.py
```

---

### Task 6: Compile LaTeX

**Purpose:** Generate PDF manuscript

```bash
cd QCT_7-QCT/latex_source

# Full compilation
pdflatex preprint.tex
bibtex preprint
pdflatex preprint.tex
pdflatex preprint.tex

# View PDF
evince preprint.pdf  # or your PDF viewer
```

---

## 🎯 Typical Workflows

### Daily Research Workflow

```bash
# 1. Morning: Pull latest changes
git pull origin QCT

# 2. Edit LaTeX files
# ... make changes in QCT_7-QCT/latex_source/ ...

# 3. Check consistency
python3 tools/data_mining/extract_parameters.py
cat data/PARAMETER_REPORT.md

# 4. Fix any inconsistencies found
# ... edit LaTeX files ...

# 5. Verify fixed
python3 tools/data_mining/extract_parameters.py

# 6. Commit changes
git add QCT_7-QCT/latex_source/*.tex
git commit -m "fix: Resolve parameter inconsistencies in section X"
git push
```

---

### Before Submission Workflow

```bash
# 1. Run complete automation
bash run_automation.sh

# 2. Check all reports
cat data/PARAMETER_REPORT.md
cat data/EQUATION_INDEX.md

# 3. Review critical issues
cat PEER_REVIEW_CRITICAL_ANALYSIS.md

# 4. Compile final PDF
cd QCT_7-QCT/latex_source
pdflatex preprint.tex
bibtex preprint
pdflatex preprint.tex
pdflatex preprint.tex

# 5. Review PDF
evince preprint.pdf

# 6. If all OK, tag version
git tag -a v5.6 -m "Revision 5.6 - Pre-submission"
git push --tags
```

---

### Adding New Analysis Workflow

```bash
# 1. Create new analysis document
vim MY_NEW_ANALYSIS.md

# 2. Add content
# ... write analysis ...

# 3. Rebuild documentation site
python3 tools/build_docs_site.py

# 4. Check it appears
firefox docs_site/analyses.html

# 5. Commit
git add MY_NEW_ANALYSIS.md
git commit -m "docs: Add new analysis on [topic]"
git push
```

---

## 🔍 Finding Things

### Find Parameter Value

```bash
# Option 1: Use JSON database
cat data/parameters.json | jq '.parameters.E_pair'

# Option 2: Search markdown report
grep -A5 "E_pair" data/PARAMETER_REPORT.md

# Option 3: Use documentation website
firefox docs_site/parameters.html
# Then use search box
```

---

### Find Equation by Label

```bash
# Option 1: Search JSON
cat data/equations.json | jq '.labels["eq:pairing_energy"]'

# Option 2: Search markdown
grep "eq:pairing_energy" data/EQUATION_INDEX.md

# Option 3: Use documentation website
firefox docs_site/equations.html
```

---

### Find Analysis Document

```bash
# List all analyses
ls -lh *.md

# Search by content
grep -l "dark energy" *.md

# View in documentation site
firefox docs_site/analyses.html
```

---

## 🚨 Troubleshooting

### "Module not found" error

```bash
# Install dependencies
pip install -r requirements.txt

# Or minimal:
pip install numpy scipy matplotlib pandas
```

---

### "Permission denied" error

```bash
# Make scripts executable
chmod +x run_automation.sh
chmod +x tools/data_mining/*.py
chmod +x tools/*.py
```

---

### LaTeX compilation fails

```bash
# Check log file
cat QCT_7-QCT/latex_source/preprint.log

# Common fixes:
# 1. Missing \end{environment}
# 2. Undefined \ref{} - check EQUATION_INDEX.md for broken references
# 3. Missing package - install texlive-latex-extra
```

---

### Generated data is empty

```bash
# Check LaTeX directory exists
ls QCT_7-QCT/latex_source/

# Run with verbose output
python3 tools/data_mining/extract_parameters.py 2>&1 | tee output.log
```

---

### Documentation site doesn't work

```bash
# Rebuild completely
rm -rf docs_site/
python3 tools/build_docs_site.py

# Check browser console (F12) for JavaScript errors
# Most issues are missing JSON data files
```

---

## 📊 Understanding Outputs

### parameters.json Structure

```json
{
  "metadata": {
    "generated": "2025-11-16",
    "total_parameters": 67
  },
  "parameters": {
    "Lambda_micro": [
      {
        "name": "Lambda_micro",
        "value": "6e13",
        "unit": "eV",
        "location": "preprint.tex:456",
        "category": "fitted"
      }
    ]
  }
}
```

---

### equations.json Structure

```json
{
  "metadata": {
    "total_equations": 861,
    "labeled_equations": 58
  },
  "equations": [
    {
      "label": "eq:my_equation",
      "content": "E = mc^2",
      "location": "preprint.tex:123",
      "is_numbered": true
    }
  ]
}
```

---

## 🎓 Next Steps

### Learn More

1. **Complete automation guide:** Read `AUTOMATION_README.md` (4,500 words)
2. **Project overview:** Read `CLAUDE.md` (12,000+ words)
3. **Critical issues:** Read `PEER_REVIEW_CRITICAL_ANALYSIS.md`

### Explore Tools

```bash
# See all available tools
ls tools/

# Read tool documentation
python3 tools/data_mining/extract_parameters.py --help
```

### Join Development

```bash
# Create feature branch
git checkout -b claude/my-feature-<session-id>

# Make changes
# ...

# Commit and push
git add .
git commit -m "feat: My new feature"
git push -u origin claude/my-feature-<session-id>
```

---

## 💡 Tips & Tricks

### Tip 1: Automate Daily Checks

Add to `~/.bashrc`:

```bash
alias qct-check='cd ~/QCT_9 && bash run_automation.sh'
```

Then just run `qct-check` anytime!

---

### Tip 2: Watch for Changes

```bash
# Automatically rebuild on file changes
while inotifywait -e modify QCT_7-QCT/latex_source/*.tex; do
    python3 tools/data_mining/extract_parameters.py
done
```

---

### Tip 3: Quick Parameter Lookup

```bash
# Add to ~/.bashrc
qct-param() {
    cat ~/QCT_9/data/parameters.json | jq ".parameters.$1"
}

# Usage:
qct-param E_pair
```

---

### Tip 4: Generate Daily Report

```bash
# Create custom report
cat > daily_report.sh <<'EOF'
#!/bin/bash
echo "QCT Daily Report - $(date)"
echo "================================"
echo ""
echo "Parameters extracted:"
cat data/parameters.json | jq '.metadata.total_parameters'
echo ""
echo "Equations indexed:"
cat data/equations.json | jq '.metadata.total_equations'
echo ""
echo "Recent commits:"
git log --oneline -5
EOF

chmod +x daily_report.sh
./daily_report.sh
```

---

## 🔗 Quick Reference

| Task | Command |
|------|---------|
| Run all automation | `bash run_automation.sh` |
| Extract parameters | `python3 tools/data_mining/extract_parameters.py` |
| Extract equations | `python3 tools/data_mining/extract_equations.py` |
| Build docs site | `python3 tools/build_docs_site.py` |
| Compile LaTeX | `cd QCT_7-QCT/latex_source && pdflatex preprint.tex` |
| Run simulation | `cd QCT_7-QCT/simulations && python3 <script>.py` |
| Check consistency | `python3 check_hidden_constants.py` |

---

## 📞 Get Help

- **Automation issues:** See `AUTOMATION_README.md` troubleshooting section
- **Physics questions:** See `CLAUDE.md` for context
- **Critical issues:** See `PEER_REVIEW_CRITICAL_ANALYSIS.md`
- **GitHub issues:** Open issue at repository

---

**You're all set!** 🚀

Start with `bash run_automation.sh` and explore from there.
