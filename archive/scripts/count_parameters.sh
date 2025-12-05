#!/bin/bash
# Count occurrences of key parameters in LaTeX files

echo "========================================="
echo "QCT PARAMETER OCCURRENCE ANALYSIS"
echo "========================================="
echo ""

cd QCT_7-QCT/latex_source 2>/dev/null || exit 1

echo "Counting S_tot = 58..."
count_s=$(grep -r "58" . --include="*.tex" 2>/dev/null | grep -i "s.*tot\|tot.*s" | wc -l)
echo "  Found: $count_s occurrences"
echo ""

echo "Counting E_pair = 5.38..."
count_e=$(grep -r "5\.38" . --include="*.tex" 2>/dev/null | wc -l)
echo "  Found: $count_e occurrences"
echo ""

echo "Counting lambda_micro = 0.733..."
count_lm=$(grep -r "0\.733\|733.*MeV" . --include="*.tex" 2>/dev/null | wc -l)
echo "  Found: $count_lm occurrences"
echo ""

echo "Counting f_screen ~ 10^-10..."
count_fs=$(grep -r "10.*-10\|10\^{-10}" . --include="*.tex" 2>/dev/null | grep -i "screen\|m_nu.*m_p" | wc -l)
echo "  Found: $count_fs occurrences"
echo ""

echo "Counting kappa_conf = 0.48 EeV..."
count_kc=$(grep -r "0\.48\|kappa.*conf" . --include="*.tex" 2>/dev/null | wc -l)
echo "  Found: $count_kc occurrences"
echo ""

echo "========================================="
echo "TOTAL FILES TO CHECK:"
tex_files=$(find . -name "*.tex" | wc -l)
echo "  LaTeX files: $tex_files"
echo "========================================="
