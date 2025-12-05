#!/usr/bin/env python3
"""
QCT Data Mining: Parameter Extraction from LaTeX Sources

Automatically extracts all physical parameters, their values, units, and locations
from LaTeX source files. Generates JSON database for automated consistency checking.

Author: AI Assistant
Date: 2025-11-16
"""

import re
import json
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
import argparse


@dataclass
class Parameter:
    """Physical parameter with metadata"""
    name: str
    symbol: str
    value: Optional[str]
    unit: Optional[str]
    uncertainty: Optional[str]
    location: str  # file:line
    context: str  # surrounding text
    category: str  # "fundamental", "derived", "fitted", "calibrated"

    def to_dict(self):
        return asdict(self)


class QCTParameterExtractor:
    """Extract parameters from QCT LaTeX sources"""

    # Known QCT parameters and their patterns
    KNOWN_PARAMETERS = {
        # Primary QCT parameters
        r'\\Lambda_{\\text\{micro\}}|\\Lmicro|\\Lambda_{\\rm\s*micro}': ('Lambda_micro', 'Microscopic cutoff scale'),
        r'\\sigma\^?2_{\\text\{max\}}|\\smax|\\sigma\^?2_{\\rm\s*max}': ('sigma_max_squared', 'Condensate variance'),
        r'E_{\\text\{pair\}}|\\Epair|E_{\\rm\s*pair}': ('E_pair', 'Pairing energy'),
        r'E_0|E_{\\text\{0\}}': ('E_0', 'E_pair present-day value'),
        r'\\kappa_{\\text\{conf\}}|\\kconf|\\kappa_{\\rm\s*conf}': ('kappa_conf', 'Conformal coupling'),
        r'S_{\\text\{tot\}}|\\Stot|S_{\\rm\s*tot}': ('S_tot', 'Total entropy parameter'),

        # Gravitational parameters
        r'G_{\\text\{eff\}}|\\Geff|G_{\\rm\s*eff}': ('G_eff', 'Effective gravitational constant'),
        r'G_N|\\GN|G_{\\text\{N\}}': ('G_N', 'Newton constant'),

        # Neutrino parameters
        r'm_\\nu|m_{\\nu}': ('m_nu', 'Neutrino mass'),
        r'n_{\\nu}|n_\\nu': ('n_nu', 'Neutrino number density'),

        # Coupling constants
        r'\\alpha_{\\nu\s*G}|\\alpha_\{\\nu\s*G\}': ('alpha_nuG', 'Neutrino-gravity coupling'),
        r'\\alpha_{\\text\{conf\}}|\\alpha_{\\rm\s*conf}': ('alpha_conf', 'Conformal coupling alpha'),
        r'\\alpha_{\\text\{cosmo\}}|\\alpha_{\\rm\s*cosmo}': ('alpha_cosmo', 'Cosmological alpha'),
        r'\\alpha_{\\text\{EM\}}|\\alpha_{\\rm\s*EM}': ('alpha_EM', 'Electromagnetic fine structure'),

        # Energy scales and cutoffs
        r'\\Lambda_{\\text\{QCT\}}|\\LambdaQCT|\\Lambda_{\\rm\s*QCT}': ('Lambda_QCT', 'QCT cutoff scale'),
        r'z_{\\text\{sat\}}|z_{\\rm\s*sat}': ('z_sat', 'Saturation redshift'),

        # Density parameters
        r'\\rho_{\\text\{ent\}}|\\rho_{\\rm\s*ent}': ('rho_ent', 'Entanglement density'),
        r'\\rho_{\\text\{vac\}}|\\rho_{\\rm\s*vac}': ('rho_vac', 'Vacuum energy density'),
        r'\\rho_{\\text\{eff\}}|\\rho_{\\rm\s*eff}': ('rho_eff', 'Effective energy density'),

        # Screening parameters
        r'f_{\\text\{screen\}}|f_{\\rm\s*screen}': ('f_screen', 'Screening fraction'),
        r'f_c|f_{\\text\{c\}}': ('f_c', 'Critical screening fraction'),
        r'\\lambda_{\\text\{screen\}}|\\lambda_{\\rm\s*screen}': ('lambda_screen', 'Screening length'),
        r'R_{\\text\{proj\}}|R_{\\rm\s*proj}': ('R_proj', 'Projection radius'),

        # Cosmological parameters
        r'H_0|H_{\\text\{0\}}': ('H_0', 'Hubble constant'),
        r'\\Omega_{\\Lambda}|\\Omega_\{\\Lambda\}': ('Omega_Lambda', 'Dark energy density parameter'),
        r'\\Omega_m|\\Omega_{\\text\{m\}}': ('Omega_m', 'Matter density parameter'),

        # Particle physics parameters
        r'v_{\\text\{EW\}}|v_{\\rm\s*EW}': ('v_EW', 'Higgs VEV'),
        r'm_H|m_{\\text\{H\}}': ('m_H', 'Higgs mass'),
        r'm_t|m_{\\text\{t\}}': ('m_t', 'Top quark mass'),

        # Golden ratio
        r'\\phi|\\varphi': ('phi', 'Golden ratio'),

        # Other QCT-specific
        r'K\\(z\\)|K_{\\text\{ent\}}': ('K_z', 'Entanglement kernel'),
        r'\\lambda_{\\text\{micro\}}|\\lambda_{\\rm\s*micro}': ('lambda_micro', 'Microscopic wavelength'),
    }

    # Value patterns with units
    VALUE_PATTERNS = [
        # Scientific notation: 1.23e45 GeV
        r'(?P<value>[\d.]+\s*\\times\s*10\^{?[\d-]+}?)\s*(?P<unit>eV|GeV|TeV|EeV|m|km|pc|Mpc)?',
        # Decimal: 0.123 eV
        r'(?P<value>[\d.]+)\s*(?P<unit>eV|GeV|TeV|EeV|m|km|μm|pc|Mpc|s|yr|Gyr)?',
        # Fractions: 1/137
        r'(?P<value>[\d]+/[\d]+)',
    ]

    # Category keywords
    CATEGORY_KEYWORDS = {
        'fitted': ['fitted', 'fit', 'free parameter', 'adjustable'],
        'calibrated': ['calibrated', 'calibration', 'matched to'],
        'derived': ['derived', 'calculated', 'computed', 'follows from'],
        'measured': ['measured', 'observed', 'experimental'],
        'predicted': ['predicted', 'predicts', 'prediction'],
    }

    def __init__(self, latex_dir: Path):
        self.latex_dir = Path(latex_dir)
        self.parameters: List[Parameter] = []

    def extract_from_file(self, filepath: Path) -> List[Parameter]:
        """Extract parameters from a single LaTeX file"""
        params = []

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            return params

        for line_num, line in enumerate(lines, 1):
            # Skip comments
            if line.strip().startswith('%'):
                continue

            # Check each known parameter
            for pattern, (param_name, description) in self.KNOWN_PARAMETERS.items():
                if re.search(pattern, line):
                    # Extract context (surrounding lines)
                    context_start = max(0, line_num - 2)
                    context_end = min(len(lines), line_num + 2)
                    context = ''.join(lines[context_start:context_end])

                    # Try to extract value
                    value, unit = self._extract_value(line)

                    # Determine category
                    category = self._categorize_parameter(context)

                    param = Parameter(
                        name=param_name,
                        symbol=self._clean_symbol(re.search(pattern, line).group()),
                        value=value,
                        unit=unit,
                        uncertainty=self._extract_uncertainty(line),
                        location=f"{filepath.name}:{line_num}",
                        context=context.strip(),
                        category=category
                    )
                    params.append(param)

        return params

    def _extract_value(self, text: str) -> Tuple[Optional[str], Optional[str]]:
        """Extract numerical value and unit from text"""
        for pattern in self.VALUE_PATTERNS:
            match = re.search(pattern, text)
            if match:
                groups = match.groupdict()
                return groups.get('value'), groups.get('unit')
        return None, None

    def _extract_uncertainty(self, text: str) -> Optional[str]:
        """Extract uncertainty if present (±, \pm)"""
        uncertainty_pattern = r'\\pm\s*(?P<unc>[\d.]+(?:\s*\\times\s*10\^{?[\d-]+}?)?)'
        match = re.search(uncertainty_pattern, text)
        if match:
            return match.group('unc')
        return None

    def _categorize_parameter(self, context: str) -> str:
        """Determine parameter category from context"""
        context_lower = context.lower()

        for category, keywords in self.CATEGORY_KEYWORDS.items():
            if any(kw in context_lower for kw in keywords):
                return category

        return 'unknown'

    def _clean_symbol(self, symbol: str) -> str:
        """Clean LaTeX symbol to readable form"""
        symbol = symbol.replace('\\', '')
        symbol = symbol.replace('{', '').replace('}', '')
        symbol = symbol.replace('text', '')
        return symbol.strip()

    def extract_all(self) -> Dict[str, List[Parameter]]:
        """Extract parameters from all LaTeX files"""
        results = {}

        for tex_file in self.latex_dir.glob('*.tex'):
            params = self.extract_from_file(tex_file)
            if params:
                results[tex_file.name] = params
                self.parameters.extend(params)

        return results

    def generate_database(self, output_path: Path):
        """Generate JSON database of all parameters"""
        db = {
            'metadata': {
                'generated': '2025-11-16',
                'source': str(self.latex_dir),
                'total_parameters': len(self.parameters),
            },
            'parameters': {}
        }

        # Group by parameter name
        for param in self.parameters:
            if param.name not in db['parameters']:
                db['parameters'][param.name] = []
            db['parameters'][param.name].append(param.to_dict())

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(db, f, indent=2, ensure_ascii=False)

        print(f"✓ Database generated: {output_path}")
        print(f"  Total parameters: {len(self.parameters)}")
        print(f"  Unique parameters: {len(db['parameters'])}")

    def check_consistency(self) -> Dict[str, List[Dict]]:
        """Check for inconsistent parameter values"""
        inconsistencies = {}

        # Group by parameter name
        param_groups = {}
        for param in self.parameters:
            if param.name not in param_groups:
                param_groups[param.name] = []
            param_groups[param.name].append(param)

        # Check each group for value consistency
        for name, params in param_groups.items():
            values = [p.value for p in params if p.value]
            if len(set(values)) > 1:
                inconsistencies[name] = [
                    {
                        'value': p.value,
                        'location': p.location,
                        'context': p.context[:100] + '...'
                    }
                    for p in params if p.value
                ]

        return inconsistencies

    def generate_report(self, output_path: Path):
        """Generate human-readable parameter report"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# QCT Parameter Extraction Report\n\n")
            f.write(f"**Generated:** 2025-11-16\n")
            f.write(f"**Source:** {self.latex_dir}\n")
            f.write(f"**Total occurrences:** {len(self.parameters)}\n\n")

            # Group by category
            by_category = {}
            for param in self.parameters:
                cat = param.category
                if cat not in by_category:
                    by_category[cat] = []
                by_category[cat].append(param)

            for category, params in sorted(by_category.items()):
                f.write(f"## {category.upper()} Parameters ({len(params)})\n\n")

                # Group by name within category
                by_name = {}
                for p in params:
                    if p.name not in by_name:
                        by_name[p.name] = []
                    by_name[p.name].append(p)

                for name, instances in sorted(by_name.items()):
                    f.write(f"### {name}\n\n")
                    for inst in instances:
                        f.write(f"- **Location:** `{inst.location}`\n")
                        if inst.value:
                            f.write(f"  - Value: {inst.value}")
                            if inst.unit:
                                f.write(f" {inst.unit}")
                            if inst.uncertainty:
                                f.write(f" ± {inst.uncertainty}")
                            f.write("\n")
                        f.write(f"  - Symbol: `{inst.symbol}`\n")
                    f.write("\n")

            # Consistency check
            f.write("## Consistency Check\n\n")
            inconsistencies = self.check_consistency()

            if inconsistencies:
                f.write("⚠️ **INCONSISTENCIES FOUND:**\n\n")
                for name, conflicts in inconsistencies.items():
                    f.write(f"### {name}\n\n")
                    for conflict in conflicts:
                        f.write(f"- `{conflict['location']}`: {conflict['value']}\n")
                    f.write("\n")
            else:
                f.write("✓ All parameter values are consistent across files.\n\n")

        print(f"✓ Report generated: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Extract QCT parameters from LaTeX sources'
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

    # Create output directory
    args.output_dir.mkdir(parents=True, exist_ok=True)

    # Extract parameters
    print(f"Extracting parameters from: {args.latex_dir}")
    extractor = QCTParameterExtractor(args.latex_dir)
    extractor.extract_all()

    # Generate outputs
    extractor.generate_database(args.output_dir / 'parameters.json')
    extractor.generate_report(args.output_dir / 'PARAMETER_REPORT.md')

    print("\n✓ Data mining complete!")


if __name__ == '__main__':
    main()
