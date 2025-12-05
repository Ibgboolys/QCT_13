# Contributing to QCT

Thank you for your interest in contributing to the Quantum Compression Theory project!

---

## 🎯 Ways to Contribute

### For Physicists & Researchers

1. **Review the theory** - Read `PEER_REVIEW_CRITICAL_ANALYSIS.md` and provide feedback
2. **Validate predictions** - Check mathematical derivations and numerical results
3. **Suggest experiments** - Propose testable predictions
4. **Find errors** - Report inconsistencies in equations or parameters
5. **Improve documentation** - Clarify explanations, add context

### For Developers

1. **Improve automation** - Enhance data mining tools
2. **Add validations** - Create new consistency checks
3. **Build visualizations** - Create plots and interactive graphics
4. **Optimize workflows** - Improve CI/CD pipelines
5. **Write tests** - Add unit tests for tools

### For Everyone

1. **Report issues** - Found a bug? Open an issue!
2. **Improve documentation** - Fix typos, add examples
3. **Share feedback** - Suggest improvements
4. **Spread awareness** - Share the project (with appropriate caveats)

---

## 🔧 Development Setup

### 1. Fork & Clone

```bash
# Fork repository on GitHub, then:
git clone https://github.com/YOUR-USERNAME/QCT_9.git
cd QCT_9
```

### 2. Install Dependencies

```bash
# Python packages
pip install -r requirements.txt

# LaTeX (optional)
sudo apt-get install texlive-latex-extra texlive-science
```

### 3. Create Branch

**IMPORTANT:** Branch names must follow the pattern `claude/<description>-<session-id>`

```bash
# Create feature branch
git checkout -b claude/your-feature-name-<unique-id>

# Example:
git checkout -b claude/improve-parameter-extraction-abc123
```

---

## 📝 Making Changes

### Code Style

#### Python

```python
"""
Module/Function docstring

Explain what this does, parameters, and return values.

Author: Your Name
Date: YYYY-MM-DD
"""

def my_function(param1: str, param2: int) -> bool:
    """
    Brief description.

    Args:
        param1: Description
        param2: Description

    Returns:
        Description of return value
    """
    # Use clear variable names
    result = process_data(param1, param2)

    # Add comments for complex logic
    return result


# Follow PEP 8 style guide
# Use black for formatting: black your_file.py
# Use flake8 for linting: flake8 your_file.py
```

#### LaTeX

```latex
% ALWAYS use macros for consistency
\Lmicro    % → Λ_micro
\Epair     % → E_pair
\kconf     % → κ_conf

% Number only key equations
\begin{equation}
  \label{eq:important_result}
  E_{\text{pair}} = \text{formula}
\end{equation}

% Use unnumbered for derivation steps
\begin{equation*}
  \text{intermediate step}
\end{equation*}

% Maintain dimensional consistency
% Always verify [LHS] = [RHS]
```

---

## ✅ Before Committing

### Automated Checks

```bash
# Run parameter extraction
python3 tools/data_mining/extract_parameters.py

# Check for inconsistencies
grep "INCONSISTENCIES" data/PARAMETER_REPORT.md

# Run equation extraction
python3 tools/data_mining/extract_equations.py

# Check for broken references
grep "BROKEN REFERENCES" data/EQUATION_INDEX.md
```

### Manual Checks

- [ ] LaTeX compiles without errors
- [ ] Python scripts have no syntax errors
- [ ] New parameters are documented
- [ ] Equation labels are unique
- [ ] Cross-references are valid
- [ ] Documentation is updated
- [ ] Tests pass (if applicable)

---

## 📦 Commit Guidelines

### Commit Message Format

```
<type>: <subject>

<body>

<impact>
```

### Types

- `feat`: New feature or analysis
- `fix`: Bug fix or correction
- `docs`: Documentation only
- `refactor`: Code restructuring (no behavior change)
- `analysis`: New analysis or review
- `test`: Adding tests
- `ci`: CI/CD changes
- `style`: Formatting (no code change)

### Examples

#### Good Commit Message

```
fix: Resolve E_pair evolution discrepancy

Implement saturation mechanism for E_pair(z):
- Add z_sat ~ 10^6 transition redshift
- Match logarithmic (z < z_sat) to saturated (z > z_sat)
- Derived from UV cutoff Λ_QCT ~ 100 TeV

Impact:
- E_pair(z_EW) now ~ 10^22 eV (was incorrectly 10^35 eV)
- Removes 10^16 discrepancy between conformal/logarithmic forms
- Cosmological predictions (Sec 5.6) need re-validation

Files modified:
- preprint.tex: Section 5.5 E_pair evolution
- cosmological_evolution.py: Updated saturation model
- DARK_ENERGY_ANALYSIS.md: Results documentation
```

#### Bad Commit Message

```
fixed stuff

changed some files
```

### Commit Frequency

- **Small, focused commits** are better than large ones
- Each commit should represent one logical change
- Don't commit broken code (should compile/run)
- Commit related changes together

---

## 🚀 Submitting Changes

### 1. Push Your Branch

```bash
# Add files
git add .

# Commit with message
git commit -m "feat: Your descriptive message"

# Push to YOUR fork
git push -u origin claude/your-feature-name-<id>
```

**Note:** Branch name MUST start with `claude/` and end with unique ID, or push will fail.

### 2. Create Pull Request

1. Go to GitHub repository
2. Click "New Pull Request"
3. Select your branch
4. Fill in PR template:

```markdown
## Description
Brief description of changes

## Motivation
Why this change is needed

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
How you tested this:
- [ ] Ran parameter extraction
- [ ] Ran equation validation
- [ ] LaTeX compiles
- [ ] Python scripts run

## Impact
What this affects:
- Section X predictions
- Parameter Y value
- Equation Z references

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No broken references
- [ ] Tests pass (if applicable)
```

### 3. Code Review

- Be open to feedback
- Respond to comments
- Make requested changes
- Push updates to same branch (auto-updates PR)

### 4. Merge

- After approval, maintainer will merge
- Delete your branch after merge (optional)

---

## 🧪 Testing

### Running Tests

```bash
# Automated tests (if implemented)
pytest tests/

# Manual validation
bash run_automation.sh

# Check reports
cat data/PARAMETER_REPORT.md
cat data/EQUATION_INDEX.md
```

### Adding Tests

```python
# tests/test_parameter_extraction.py

import pytest
from tools.data_mining.extract_parameters import QCTParameterExtractor

def test_parameter_extraction():
    """Test parameter extraction from LaTeX"""
    extractor = QCTParameterExtractor(Path("test_data"))
    params = extractor.extract_all()

    assert len(params) > 0
    assert "E_pair" in params
```

---

## 📚 Documentation Standards

### Analysis Documents

```markdown
# Title of Analysis

**Author:** Your Name
**Date:** YYYY-MM-DD
**Purpose:** What question does this answer?

## Summary

Brief overview (2-3 sentences)

## Methodology

How you did this:
1. Step 1
2. Step 2
3. Step 3

## Results

Quantitative findings:
- Result 1: value ± uncertainty
- Result 2: value ± uncertainty

## Discussion

What do these results mean?
How do they affect QCT framework?

## Implications

- Impact on prediction X
- Changes to section Y
- Need for validation Z

## Next Steps

- [ ] TODO 1
- [ ] TODO 2

## References

- Paper 1: citation
- Code: script.py
- Data: file.csv
```

### Code Comments

```python
# Brief description (what)
# Explanation (why)
# TODO: Future improvement
# FIXME: Known issue
# NOTE: Important information
# WARNING: Potential problem
```

---

## 🐛 Reporting Issues

### Bug Report Template

```markdown
## Bug Description
Clear description of the bug

## Steps to Reproduce
1. Run command X
2. Do action Y
3. See error Z

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: Ubuntu 22.04
- Python: 3.11.0
- LaTeX: TeX Live 2023

## Error Messages
```
Paste error messages here
```

## Additional Context
Screenshots, logs, etc.
```

### Feature Request Template

```markdown
## Feature Description
What you want to add

## Motivation
Why this is useful

## Proposed Implementation
How you would implement it

## Alternatives Considered
Other approaches

## Additional Context
Examples, references, etc.
```

---

## 🎓 Resources

### Learning Materials

- **QCT Physics:** Read `CLAUDE.md`
- **Critical Issues:** Read `PEER_REVIEW_CRITICAL_ANALYSIS.md`
- **Automation:** Read `AUTOMATION_README.md`
- **Quick Start:** Read `QUICKSTART.md`

### Tools & Technologies

- **Python:** https://docs.python.org/3/
- **LaTeX:** https://www.latex-project.org/help/documentation/
- **GitHub Actions:** https://docs.github.com/en/actions
- **Git:** https://git-scm.com/doc

---

## 🤝 Code of Conduct

### Be Respectful

- Treat everyone with respect
- Welcome newcomers
- Accept constructive criticism
- Focus on what's best for the project

### Be Professional

- Use clear, professional language
- Avoid personal attacks
- Stay on topic
- Provide constructive feedback

### Be Collaborative

- Share knowledge
- Help others
- Credit contributions
- Work together

---

## 📞 Getting Help

### Questions?

1. **Check documentation** first (README, CLAUDE.md, etc.)
2. **Search issues** - maybe already answered
3. **Ask in discussion** - for general questions
4. **Open issue** - for bugs or feature requests

### Contact

- **Technical questions:** Open GitHub issue
- **Physics questions:** See `CLAUDE.md` for context
- **General questions:** GitHub Discussions

---

## 🏆 Recognition

Contributors are listed in:
- Commit history (automatic)
- Release notes (for significant contributions)
- Acknowledgments section (for major contributions)

---

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License (same as the project).

---

## 🙏 Thank You!

Every contribution, no matter how small, helps improve QCT. Thank you for your time and effort!

---

**Last Updated:** 2025-11-16
**Version:** 1.0
