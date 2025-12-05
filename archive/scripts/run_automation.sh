#!/bin/bash
# QCT Automation Runner
# Executes complete automation pipeline in one command

set -e  # Exit on error

echo "========================================"
echo "QCT Repository Automation Suite"
echo "========================================"
echo ""

# Check we're in the right directory
if [ ! -f "CLAUDE.md" ]; then
    echo "Error: Must run from repository root"
    exit 1
fi

# Create data directory
echo "[1/5] Creating data directory..."
mkdir -p data

# Extract parameters
echo "[2/5] Extracting parameters from LaTeX..."
python3 tools/data_mining/extract_parameters.py

# Extract equations
echo "[3/5] Extracting equations from LaTeX..."
python3 tools/data_mining/extract_equations.py

# Build documentation site
echo "[4/5] Building documentation site..."
python3 tools/build_docs_site.py

# Generate summary report
echo "[5/5] Generating summary report..."
cat > data/AUTOMATION_SUMMARY.txt <<EOF
QCT Automation Run Summary
==========================
Date: $(date)

Generated Files:
EOF

ls -lh data/ >> data/AUTOMATION_SUMMARY.txt

echo ""
echo "========================================"
echo "✓ Automation Complete!"
echo "========================================"
echo ""
echo "Generated files in data/:"
ls -lh data/
echo ""
echo "Documentation site: docs_site/index.html"
echo ""
echo "Next steps:"
echo "  - Review data/PARAMETER_REPORT.md for consistency issues"
echo "  - Review data/EQUATION_INDEX.md for broken references"
echo "  - Open docs_site/index.html in browser"
echo ""
