#!/usr/bin/env python3
"""
QCT Repository Reorganization Script

Reorganizes the QCT repository into a clean, logical structure:

OLD STRUCTURE (chaotic):
    /
    ├── *.md (25+ analysis files scattered)
    ├── *.py (41 Python scripts scattered)
    ├── QCT_7-QCT/
    │   ├── latex_source/
    │   ├── simulations/
    │   └── literature/
    └── documentation/

NEW STRUCTURE (organized):
    /
    ├── docs/
    │   ├── analyses/
    │   │   ├── critical/
    │   │   ├── theoretical/
    │   │   ├── numerical/
    │   │   └── historical/
    │   ├── guides/
    │   └── reports/
    ├── src/
    │   ├── latex/
    │   ├── simulations/
    │   ├── validation/
    │   └── literature/
    ├── tools/
    │   ├── data_mining/
    │   ├── validation/
    │   └── visualization/
    ├── data/
    │   ├── parameters.json
    │   ├── equations.json
    │   └── outputs/
    ├── tests/
    ├── .github/
    │   └── workflows/
    └── [root config files]

Author: AI Assistant
Date: 2025-11-16
"""

import shutil
import re
from pathlib import Path
from typing import Dict, List
import argparse


class QCTReorganizer:
    """Reorganize QCT repository structure"""

    # Analysis file categorization
    ANALYSIS_CATEGORIES = {
        'critical': [
            'PEER_REVIEW_CRITICAL_ANALYSIS.md',
            'COMPREHENSIVE_REVIEWER_ANALYSIS.md',
            'CRITICAL_REVIEW_MATHEMATICAL_RELATIONS.md',
        ],
        'theoretical': [
            'QCT_RIGOROUS_THEORETICAL_ANALYSIS.md',
            'QCT_COMPLETE_RECONSTRUCTION_FROM_MATH.md',
            'theoretical_derivation_of_phi.md',
            'NEUTRINO_ACCUMULATION_MECHANISM.md',
            'REFORMULATION_IMPACT_ANALYSIS.md',
        ],
        'numerical': [
            'DARK_ENERGY_ANALYSIS.md',
            'DARK_ENERGY_CALCULATION_RESULTS.md',
            'E_PAIR_CORRECTION_AUDIT_REPORT.md',
            'STOT_CORRECTION_FACTOR_ANALYSIS.md',
            'VERIFICATION_REPORT.md',
        ],
        'integration': [
            'COMPREHENSIVE_INTEGRATION_ANALYSIS_DETAILED.md',
            'INTEGRATION_REVIEW_FINDINGS.md',
            'INTEGRATION_SUMMARY_MATHEMATICAL_CONSTANTS.md',
            'CONSISTENCY_FIXES_COMPLETE_REPORT.md',
        ],
        'discoveries': [
            'BREAKTHROUGH_COULOMB_SUMMARY_CZ.md',
            'HIDDEN_CONSTANTS_DISCOVERED.md',
            'COULOMB_CONNECTION_ANALYSIS.md',
        ],
        'summaries': [
            'EXECUTIVE_SUMMARY.md',
            'IMPLEMENTATION_SUMMARY.md',
            'RIGOROUS_ANALYSIS_SUMMARY.md',
            'QUICK_REFERENCE_MATHEMATICAL_CONSTANTS.txt',
        ],
        'historical': [
            'FINALNI_SOUHRN_KONZISTENCE_CZ.md',
            'FINALNI_SOUHRN_USPECH_CZ.md',
            'FINAL_INTEGRATION_SUMMARY_CZ.md',
            'REKONSTRUKCE_OD_ZAKLADU_MATEMATICKE_KONSTANTY.md',
            'REKONSTRUKCE_RIGOROZNI_ODPOVED.md',
        ],
    }

    # Script categorization
    SCRIPT_CATEGORIES = {
        'validation': [
            'check_hidden_constants.py',
            'check_hidden_constants_simple.py',
            'verify_coulomb_connection.py',
            'verify_reconstruction_FINAL.py',
            'verify_reconstruction_corrected.py',
            'verify_with_critical_checks.py',
            'verify_dark_energy_calculation.py',
        ],
        'models': [
            'vacuum_cascade_model.py',
            'qct_refinement.py',
            'qct_complete_spectrum.py',
            'qct_from_constants_framework.py',
            'qct_complete_framework.py',
            'qct_quark_masses.py',
        ],
        'calculations': [
            'calculate_dark_energy_from_saturation.py',
            'calculate_dark_energy_simple.py',
            'bayesian_model_selection.py',
            'group_theory_analysis.py',
        ],
        'visualization': [
            'qct_visualization_for_publication.py',
        ],
    }

    def __init__(self, root_dir: Path, dry_run: bool = True):
        self.root_dir = Path(root_dir)
        self.dry_run = dry_run
        self.moves: List[tuple] = []

    def create_new_structure(self):
        """Create new directory structure"""
        new_dirs = [
            'docs/analyses/critical',
            'docs/analyses/theoretical',
            'docs/analyses/numerical',
            'docs/analyses/integration',
            'docs/analyses/discoveries',
            'docs/analyses/summaries',
            'docs/analyses/historical',
            'docs/guides',
            'docs/reports',
            'src/latex',
            'src/simulations',
            'src/literature',
            'tools/data_mining',
            'tools/validation',
            'tools/visualization',
            'data/outputs',
            'tests',
        ]

        for dir_path in new_dirs:
            full_path = self.root_dir / dir_path
            if not self.dry_run:
                full_path.mkdir(parents=True, exist_ok=True)
                print(f"✓ Created {dir_path}/")
            else:
                print(f"[DRY RUN] Would create {dir_path}/")

    def plan_moves(self):
        """Plan all file movements"""
        # Move analysis files
        for category, files in self.ANALYSIS_CATEGORIES.items():
            for filename in files:
                src = self.root_dir / filename
                if src.exists():
                    dst = self.root_dir / 'docs' / 'analyses' / category / filename
                    self.moves.append((src, dst, 'analysis'))

        # Move Python scripts (root level)
        for category, scripts in self.SCRIPT_CATEGORIES.items():
            for filename in scripts:
                src = self.root_dir / filename
                if src.exists():
                    dst = self.root_dir / 'tools' / category / filename
                    self.moves.append((src, dst, 'script'))

        # Move QCT_7-QCT contents
        qct_dir = self.root_dir / 'QCT_7-QCT'
        if qct_dir.exists():
            # LaTeX sources
            latex_src = qct_dir / 'latex_source'
            if latex_src.exists():
                self.moves.append((latex_src, self.root_dir / 'src' / 'latex', 'directory'))

            # Simulations
            sim_src = qct_dir / 'simulations'
            if sim_src.exists():
                self.moves.append((sim_src, self.root_dir / 'src' / 'simulations', 'directory'))

            # Literature
            lit_src = qct_dir / 'literature'
            if lit_src.exists():
                self.moves.append((lit_src, self.root_dir / 'src' / 'literature', 'directory'))

            # Markdown files in QCT_7-QCT
            for md_file in qct_dir.glob('*.md'):
                dst = self.root_dir / 'docs' / 'analyses' / 'historical' / md_file.name
                self.moves.append((md_file, dst, 'analysis'))

        # Move guides
        guides = ['CLAUDE.md']
        for guide in guides:
            src = self.root_dir / guide
            if src.exists():
                dst = self.root_dir / 'docs' / 'guides' / guide
                self.moves.append((src, dst, 'guide'))

    def execute_moves(self):
        """Execute planned moves"""
        print(f"\n{'='*60}")
        print(f"{'DRY RUN MODE' if self.dry_run else 'EXECUTING REORGANIZATION'}")
        print(f"{'='*60}\n")

        # Group by type
        by_type = {}
        for src, dst, move_type in self.moves:
            if move_type not in by_type:
                by_type[move_type] = []
            by_type[move_type].append((src, dst))

        for move_type, items in by_type.items():
            print(f"\n{move_type.upper()} ({len(items)} items)")
            print("-" * 60)

            for src, dst in items:
                rel_src = src.relative_to(self.root_dir)
                rel_dst = dst.relative_to(self.root_dir)

                if self.dry_run:
                    print(f"  {rel_src} → {rel_dst}")
                else:
                    try:
                        # Create parent directory
                        dst.parent.mkdir(parents=True, exist_ok=True)

                        # Move file/directory
                        if src.is_dir():
                            if dst.exists():
                                shutil.rmtree(dst)
                            shutil.copytree(src, dst)
                        else:
                            shutil.copy2(src, dst)

                        print(f"✓ {rel_src} → {rel_dst}")

                    except Exception as e:
                        print(f"✗ Error moving {rel_src}: {e}")

    def generate_migration_guide(self):
        """Generate guide for updating paths"""
        guide_path = self.root_dir / 'docs' / 'REORGANIZATION_GUIDE.md'

        content = """# QCT Repository Reorganization Guide

**Date:** 2025-11-16
**Status:** Migration complete

## Overview

The QCT repository has been reorganized into a cleaner, more logical structure.

## New Structure

```
/
├── docs/                           # All documentation
│   ├── analyses/                   # Analysis documents
│   │   ├── critical/               # Critical reviews
│   │   ├── theoretical/            # Theoretical analyses
│   │   ├── numerical/              # Numerical validations
│   │   ├── integration/            # Integration studies
│   │   ├── discoveries/            # Breakthrough findings
│   │   ├── summaries/              # Executive summaries
│   │   └── historical/             # Historical documents
│   ├── guides/                     # User guides
│   └── reports/                    # Generated reports
├── src/                            # Source files
│   ├── latex/                      # LaTeX manuscript
│   ├── simulations/                # Numerical simulations
│   └── literature/                 # Reference PDFs
├── tools/                          # Development tools
│   ├── data_mining/                # Parameter extraction
│   ├── validation/                 # Consistency checks
│   └── visualization/              # Plotting tools
├── data/                           # Generated data
│   └── outputs/                    # Simulation outputs
├── tests/                          # Test suite
├── .github/workflows/              # CI/CD automation
└── docs_site/                      # GitHub Pages site
```

## Path Updates

### Analysis Documents

"""

        # Add move mappings
        for src, dst, move_type in self.moves:
            rel_src = src.relative_to(self.root_dir)
            rel_dst = dst.relative_to(self.root_dir)
            content += f"- `{rel_src}` → `{rel_dst}`\n"

        content += """

## Updating References

### In Python Scripts

Old imports:
```python
from check_hidden_constants import validate
```

New imports:
```python
from tools.validation.check_hidden_constants import validate
```

### In LaTeX

Old:
```latex
\\input{../some_file.tex}
```

New:
```latex
\\input{some_file.tex}  % All LaTeX in same directory now
```

### In GitHub Actions

Update paths in `.github/workflows/*.yml`:
```yaml
# Old
- QCT_7-QCT/latex_source/**

# New
- src/latex/**
```

## Benefits

1. **Clear separation**: Docs vs Source vs Tools
2. **Easy navigation**: Related files grouped together
3. **Better CI/CD**: Logical workflow triggers
4. **Scalability**: Room for growth in each category

## Rollback

If needed, run:
```bash
git reset --hard <commit-before-reorganization>
```

## Next Steps

1. Update all import paths in Python scripts
2. Update LaTeX compilation scripts
3. Update CI/CD workflow paths
4. Update documentation links
5. Test all automation tools
"""

        if not self.dry_run:
            guide_path.parent.mkdir(parents=True, exist_ok=True)
            with open(guide_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"\n✓ Migration guide created: {guide_path}")
        else:
            print(f"\n[DRY RUN] Would create migration guide at {guide_path}")

    def cleanup_old_structure(self):
        """Remove old empty directories"""
        if not self.dry_run:
            # Remove old QCT_7-QCT if empty
            qct_dir = self.root_dir / 'QCT_7-QCT'
            if qct_dir.exists():
                try:
                    # Check if empty
                    remaining = list(qct_dir.rglob('*'))
                    if len(remaining) <= 1:  # Only directory itself
                        qct_dir.rmdir()
                        print(f"✓ Removed empty {qct_dir}")
                except:
                    print(f"⚠ Could not remove {qct_dir} (not empty)")
        else:
            print("\n[DRY RUN] Would cleanup empty directories")

    def run(self):
        """Execute full reorganization"""
        print("QCT Repository Reorganization")
        print("=" * 60)

        # Create new structure
        print("\n1. Creating new directory structure...")
        self.create_new_structure()

        # Plan moves
        print("\n2. Planning file movements...")
        self.plan_moves()

        # Execute
        print("\n3. Executing moves...")
        self.execute_moves()

        # Generate guide
        print("\n4. Generating migration guide...")
        self.generate_migration_guide()

        # Cleanup
        print("\n5. Cleaning up old structure...")
        self.cleanup_old_structure()

        print("\n" + "=" * 60)
        if self.dry_run:
            print("DRY RUN COMPLETE")
            print("\nTo execute for real, run with --execute flag")
        else:
            print("REORGANIZATION COMPLETE!")
            print("\nNext steps:")
            print("1. Review docs/REORGANIZATION_GUIDE.md")
            print("2. Update import paths in scripts")
            print("3. Update workflow paths in .github/workflows/")
            print("4. Test all tools: python3 -m tools.data_mining.extract_parameters")
        print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description='Reorganize QCT repository structure'
    )
    parser.add_argument(
        '--execute',
        action='store_true',
        help='Actually execute the reorganization (default is dry run)'
    )
    parser.add_argument(
        '--root',
        type=Path,
        default=Path(__file__).parent.parent,
        help='Repository root directory'
    )

    args = parser.parse_args()

    reorganizer = QCTReorganizer(
        root_dir=args.root,
        dry_run=not args.execute
    )

    reorganizer.run()


if __name__ == '__main__':
    main()
