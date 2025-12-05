#!/usr/bin/env python3
"""
QCT Data Mining: Equation Extraction and Indexing

Automatically extracts all equations from LaTeX sources, validates cross-references,
and generates searchable equation database.

Author: AI Assistant
Date: 2025-11-16
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import argparse


@dataclass
class Equation:
    """Mathematical equation with metadata"""
    label: Optional[str]
    content: str
    location: str  # file:line
    references: List[str]  # Other equations referenced
    is_numbered: bool
    section: Optional[str]

    def to_dict(self):
        return asdict(self)


class QCTEquationExtractor:
    """Extract and index equations from LaTeX sources"""

    EQUATION_ENVS = [
        'equation', 'align', 'multline', 'gather',
        'eqnarray', 'displaymath'
    ]

    def __init__(self, latex_dir: Path):
        self.latex_dir = Path(latex_dir)
        self.equations: List[Equation] = []
        self.labels: Dict[str, Equation] = {}
        self.current_section = None

    def extract_from_file(self, filepath: Path) -> List[Equation]:
        """Extract equations from a single file"""
        eqs = []

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            return eqs

        lines = content.split('\n')

        # Track section
        for line_num, line in enumerate(lines, 1):
            # Update current section
            section_match = re.search(r'\\section\{([^}]+)\}', line)
            if section_match:
                self.current_section = section_match.group(1)

            # Find equation environments
            for env in self.EQUATION_ENVS:
                # Check for \begin{equation}
                if f'\\begin{{{env}}}' in line or f'\\begin{{{env}*}}' in line:
                    is_numbered = '*' not in line
                    eq_content, eq_lines = self._extract_equation_block(
                        lines, line_num - 1, env
                    )

                    if eq_content:
                        # Extract label
                        label = self._extract_label(eq_content)

                        # Extract referenced equations
                        references = self._extract_references(eq_content)

                        eq = Equation(
                            label=label,
                            content=eq_content.strip(),
                            location=f"{filepath.name}:{line_num}",
                            references=references,
                            is_numbered=is_numbered,
                            section=self.current_section
                        )

                        eqs.append(eq)

                        if label:
                            self.labels[label] = eq

        return eqs

    def _extract_equation_block(
        self, lines: List[str], start_idx: int, env: str
    ) -> tuple[str, int]:
        """Extract full equation block from start to end"""
        content_lines = []
        starred = '*' in lines[start_idx]
        end_pattern = f'\\end{{{env}{"*" if starred else ""}}}'

        for i in range(start_idx + 1, len(lines)):
            if end_pattern in lines[i]:
                return '\n'.join(content_lines), i - start_idx + 1
            content_lines.append(lines[i])

        return '', 0

    def _extract_label(self, eq_content: str) -> Optional[str]:
        """Extract \label{...} from equation"""
        match = re.search(r'\\label\{([^}]+)\}', eq_content)
        return match.group(1) if match else None

    def _extract_references(self, eq_content: str) -> List[str]:
        """Extract all \eqref{...} and \ref{eq:...} references"""
        refs = []

        # \eqref{label}
        refs.extend(re.findall(r'\\eqref\{([^}]+)\}', eq_content))

        # \ref{eq:label}
        refs.extend(re.findall(r'\\ref\{(eq:[^}]+)\}', eq_content))

        return list(set(refs))

    def extract_all(self) -> Dict[str, List[Equation]]:
        """Extract equations from all LaTeX files"""
        results = {}

        for tex_file in sorted(self.latex_dir.glob('*.tex')):
            self.current_section = None
            eqs = self.extract_from_file(tex_file)
            if eqs:
                results[tex_file.name] = eqs
                self.equations.extend(eqs)

        return results

    def validate_references(self) -> Dict[str, List[str]]:
        """Check for broken equation references"""
        broken = {}

        for eq in self.equations:
            for ref in eq.references:
                if ref not in self.labels:
                    if eq.location not in broken:
                        broken[eq.location] = []
                    broken[eq.location].append(ref)

        return broken

    def generate_database(self, output_path: Path):
        """Generate JSON equation database"""
        db = {
            'metadata': {
                'generated': '2025-11-16',
                'source': str(self.latex_dir),
                'total_equations': len(self.equations),
                'labeled_equations': len(self.labels),
            },
            'equations': [eq.to_dict() for eq in self.equations],
            'labels': {label: eq.to_dict() for label, eq in self.labels.items()}
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(db, f, indent=2, ensure_ascii=False)

        print(f"✓ Equation database: {output_path}")
        print(f"  Total equations: {len(self.equations)}")
        print(f"  Labeled: {len(self.labels)}")

    def generate_index(self, output_path: Path):
        """Generate human-readable equation index"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# QCT Equation Index\n\n")
            f.write(f"**Generated:** 2025-11-16\n")
            f.write(f"**Total equations:** {len(self.equations)}\n")
            f.write(f"**Labeled equations:** {len(self.labels)}\n\n")

            # By file
            by_file = {}
            for eq in self.equations:
                filename = eq.location.split(':')[0]
                if filename not in by_file:
                    by_file[filename] = []
                by_file[filename].append(eq)

            for filename, eqs in sorted(by_file.items()):
                f.write(f"## {filename} ({len(eqs)} equations)\n\n")

                for eq in eqs:
                    if eq.label:
                        f.write(f"### `{eq.label}` ({eq.location})\n\n")
                    else:
                        f.write(f"### Unlabeled ({eq.location})\n\n")

                    if eq.section:
                        f.write(f"**Section:** {eq.section}\n\n")

                    # Show first line of equation
                    first_line = eq.content.split('\n')[0]
                    if len(first_line) > 80:
                        first_line = first_line[:77] + '...'
                    f.write(f"```latex\n{first_line}\n```\n\n")

                    if eq.references:
                        f.write(f"**References:** {', '.join(eq.references)}\n\n")

            # Validation
            f.write("## Reference Validation\n\n")
            broken = self.validate_references()

            if broken:
                f.write("⚠️ **BROKEN REFERENCES FOUND:**\n\n")
                for location, refs in broken.items():
                    f.write(f"- `{location}`: {', '.join(refs)}\n")
            else:
                f.write("✓ All equation references are valid.\n")

        print(f"✓ Equation index: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Extract and index equations from QCT LaTeX sources'
    )
    parser.add_argument(
        '--latex-dir',
        type=Path,
        default=Path(__file__).parent.parent.parent / 'QCT_7-QCT' / 'latex_source',
        help='Path to LaTeX source directory'
    )
    parser.add_argument(
        '--output-dir',
        type=Path,
        default=Path(__file__).parent.parent.parent / 'data',
        help='Output directory for generated files'
    )

    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Extracting equations from: {args.latex_dir}")
    extractor = QCTEquationExtractor(args.latex_dir)
    extractor.extract_all()

    extractor.generate_database(args.output_dir / 'equations.json')
    extractor.generate_index(args.output_dir / 'EQUATION_INDEX.md')

    print("\n✓ Equation extraction complete!")


if __name__ == '__main__':
    main()
