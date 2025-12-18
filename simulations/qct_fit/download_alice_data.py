#!/usr/bin/env python3
"""
ALICE Data Downloader for QCT-FIT

Downloads reference ALICE data from HEPData for QCT vacuum parameter extraction.

🆕 CRITICAL NOTE (2025 Update):
   ALICE confirmed that light nuclei form via LATE-STAGE COALESCENCE, not thermal
   production. This fundamentally changes the interpretation of hadron yields.

   QCT Interpretation:
   - Coalescence = Phase transition of neutrino condensate
   - B_A factor = Overlap of condensate wavefunctions
   - Not classical phase-space coalescence!

Data Sources:
   1. Λ/p ratio vs multiplicity (pp @ 7 TeV) — for calibration
   2. v₂ vs multiplicity (p-Pb) — for acoustic dissipation γ
   3. 🆕 Light nuclei coalescence B_A — for future ξ extraction

⚠️  TODO (Future Development):
    Current fit uses thermal approximation: Y(m) ∝ exp(-Ωm/T)

    Future fit MUST account for coalescence factor B_A scaling:
        Y_A = B_A · (Y_p)^A · f_coal(ξ)

    where:
        - B_A = measured coalescence parameter
        - ξ = coherence length of neutrino condensate
        - f_coal(ξ) = QCT coalescence enhancement factor

    This is NOT just thermal Boltzmann anymore!
"""

import os
import sys
import urllib.request
import json
from typing import Dict, List, Optional
import time


# HEPData record IDs
HEPDATA_RECORDS = {
    'lambda_p_7tev': {
        'record_id': 'ins1471838',
        'table': 3,
        'description': 'Λ/p ratio vs multiplicity (pp @ 7 TeV)',
        'reference': 'ALICE, Nature Physics 13, 535 (2017), arXiv:1606.07424',
        'url': 'https://www.hepdata.net/record/ins1471838',
        'data_url': 'https://www.hepdata.net/download/table/ins1471838/Table%203/csv',
        'filename': 'alice_lambda_p.csv',
        'note': 'Reference data for Ω(dN/dη) calibration'
    },

    'v2_ppb': {
        'record_id': 'ins1190545',
        'table': 5,
        'description': 'v₂ vs multiplicity (p-Pb @ 5.02 TeV)',
        'reference': 'ALICE, Phys. Lett. B 719, 29 (2013), arXiv:1212.2001',
        'url': 'https://www.hepdata.net/record/ins1190545',
        'data_url': 'https://www.hepdata.net/download/table/ins1190545/Table%205/csv',
        'filename': 'alice_v2_ppb.csv',
        'note': 'Ridge data for γ dissipation extraction'
    },

    # 🆕 2025 UPDATE: Coalescence data for future fits
    'deuteron_coalescence': {
        'record_id': 'TBD_2025',  # Will be assigned when Nature paper published
        'table': 'TBD',
        'description': 'Deuteron coalescence B_2 vs multiplicity',
        'reference': 'ALICE, Nature 2025 (in press), arXiv:TBD',
        'url': 'https://www.hepdata.net/record/TBD',
        'data_url': None,  # Not yet available
        'filename': 'alice_deuteron_coalescence.csv',
        'note': '⚠️  FUTURE: For ξ (coherence length) extraction via B_A ~ ξ³ scaling'
    },

    'antihyperhelium4': {
        'record_id': 'TBD_2025',
        'table': 'TBD',
        'description': 'Anti-⁴He-Λ production cross-section',
        'reference': 'ALICE, 2025 (viral preprint)',
        'url': 'TBD',
        'data_url': None,
        'filename': 'alice_antihyperhelium4.csv',
        'note': '⚠️  FUTURE: CPT symmetry test in condensate'
    }
}


class ALICEDataDownloader:
    """
    Download and validate ALICE data from HEPData.

    Handles:
    - Automatic retry on network errors
    - Data format validation
    - Metadata storage
    """

    def __init__(self, output_dir: str = "simulations/qct_fit/data"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def download_dataset(
        self,
        dataset_key: str,
        force: bool = False,
        timeout: int = 30
    ) -> bool:
        """
        Download single ALICE dataset.

        Args:
            dataset_key: Key from HEPDATA_RECORDS
            force: Overwrite existing file
            timeout: Download timeout in seconds

        Returns:
            True if successful, False otherwise
        """

        if dataset_key not in HEPDATA_RECORDS:
            print(f"✗ Unknown dataset: {dataset_key}")
            return False

        record = HEPDATA_RECORDS[dataset_key]
        output_path = os.path.join(self.output_dir, record['filename'])

        # Check if already exists
        if os.path.exists(output_path) and not force:
            print(f"✓ {record['filename']} already exists (use --force to overwrite)")
            return True

        # Check if data URL is available
        if record['data_url'] is None:
            print(f"⚠️  {record['filename']} not yet available:")
            print(f"   {record['description']}")
            print(f"   {record['note']}")
            print(f"   Reference: {record['reference']}")
            return False

        # Download
        print(f"\nDownloading: {record['description']}")
        print(f"  Source: {record['url']}")
        print(f"  → {output_path}")

        try:
            urllib.request.urlretrieve(
                record['data_url'],
                output_path,
                reporthook=self._progress_hook
            )
            print(f"\n✓ Downloaded successfully")

            # Validate
            if self._validate_csv(output_path):
                print(f"✓ Validation passed")
                return True
            else:
                print(f"✗ Validation failed")
                os.remove(output_path)
                return False

        except Exception as e:
            print(f"\n✗ Download failed: {e}")
            return False

    def download_all(self, include_future: bool = False):
        """
        Download all available datasets.

        Args:
            include_future: Attempt to download 2025 data (likely to fail until published)
        """

        print("\n" + "="*70)
        print(" "*20 + "ALICE Data Downloader")
        print(" "*15 + "QCT-FIT Reference Data Acquisition")
        print("="*70)

        print("\n🆕 IMPORTANT NOTE (2025):")
        print("   ALICE confirmed late-stage coalescence mechanism for nuclei.")
        print("   Current fit uses thermal approximation for calibration.")
        print("   Future fits MUST include B_A coalescence factor scaling!")
        print("="*70)

        success_count = 0
        total_count = 0

        for key, record in HEPDATA_RECORDS.items():
            # Skip future data unless explicitly requested
            if record['data_url'] is None and not include_future:
                continue

            total_count += 1
            if self.download_dataset(key):
                success_count += 1

            time.sleep(1)  # Be nice to HEPData servers

        print("\n" + "="*70)
        print(f"Download Summary: {success_count}/{total_count} successful")
        print("="*70)

        # Save metadata
        self._save_metadata()

        return success_count == total_count

    def _validate_csv(self, filepath: str) -> bool:
        """
        Validate downloaded CSV file.

        Checks:
        - File is not empty
        - Has at least 3 columns
        - Has at least 5 data rows
        """

        try:
            with open(filepath, 'r') as f:
                lines = [l.strip() for l in f.readlines() if l.strip()]

            if len(lines) < 6:  # header + 5 data rows
                print(f"  ✗ Too few rows: {len(lines)}")
                return False

            # Check columns
            header = lines[0].split(',')
            if len(header) < 3:
                print(f"  ✗ Too few columns: {len(header)}")
                return False

            print(f"  → {len(lines)-1} data rows, {len(header)} columns")
            return True

        except Exception as e:
            print(f"  ✗ Validation error: {e}")
            return False

    def _save_metadata(self):
        """Save dataset metadata to JSON."""

        metadata = {
            'downloaded': time.strftime('%Y-%m-%d %H:%M:%S'),
            'datasets': HEPDATA_RECORDS,
            'note_2025': (
                "ALICE 2025 breaking news: Light nuclei form via late-stage "
                "coalescence, not thermal production. QCT interpretation: "
                "Condensation from neutrino condensate background."
            ),
            'todo_future': (
                "Future fits must account for coalescence factor B_A scaling "
                "with coherence length ξ. Current thermal approximation is "
                "valid for calibration but incomplete."
            )
        }

        metadata_path = os.path.join(self.output_dir, 'alice_data_metadata.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)

        print(f"\n✓ Metadata saved to {metadata_path}")

    def _progress_hook(self, block_num, block_size, total_size):
        """Show download progress."""
        downloaded = block_num * block_size
        if total_size > 0:
            percent = min(100, downloaded * 100 / total_size)
            print(f'\r  Progress: {percent:.1f}% ({downloaded}/{total_size} bytes)', end='')


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Download ALICE reference data for QCT-FIT',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download all available data
  python download_alice_data.py

  # Include future 2025 coalescence data (will likely fail until published)
  python download_alice_data.py --include-future

  # Download specific dataset
  python download_alice_data.py --dataset lambda_p_7tev

  # Force re-download
  python download_alice_data.py --force

⚠️  CRITICAL NOTE (2025):
    ALICE confirmed that nuclei form via COALESCENCE, not thermal production.

    Current fit: Uses thermal approximation for CALIBRATION
    Future fit:  MUST include B_A coalescence factor scaling

    TODO: Implement f_coal(ξ) correction factor once B_A data available.
        """
    )

    parser.add_argument(
        '--dataset',
        type=str,
        choices=list(HEPDATA_RECORDS.keys()),
        help='Download specific dataset only'
    )

    parser.add_argument(
        '--force',
        action='store_true',
        help='Overwrite existing files'
    )

    parser.add_argument(
        '--include-future',
        action='store_true',
        help='Attempt to download 2025 coalescence data (likely unavailable yet)'
    )

    parser.add_argument(
        '--output-dir',
        type=str,
        default='simulations/qct_fit/data',
        help='Output directory (default: simulations/qct_fit/data)'
    )

    args = parser.parse_args()

    downloader = ALICEDataDownloader(output_dir=args.output_dir)

    if args.dataset:
        # Download single dataset
        success = downloader.download_dataset(args.dataset, force=args.force)
        sys.exit(0 if success else 1)
    else:
        # Download all
        success = downloader.download_all(include_future=args.include_future)
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
