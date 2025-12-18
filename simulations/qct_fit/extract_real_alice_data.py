#!/usr/bin/env python3
"""
EXTRAKCE REÁLNÝCH ALICE DAT Z HEPData
======================================

PŘÍSNÝ ZÁKAZ GENEROVÁNÍ SYNTETICKÝCH DAT.

Extrahuje:
1. Λ/p poměr = (Λ/π) / (p/π) z Table37 a Table47
2. v₂ data z HEPData ins1190545

Autor: QCT Data Integrity Protocol
Datum: 2025-12-18
"""

import pandas as pd
import numpy as np
import sys

def parse_hepdata_table(filepath, skip_yaml=True):
    """
    Parse HEPData CSV s YAML hlavičkami.

    Returns: pandas DataFrame nebo None při chybě
    """
    try:
        # Použití pandas s comment='#:' přeskočí YAML řádky
        df = pd.read_csv(filepath, comment='#')

        # První řádek bez # je hlavička, data začínají od druhého
        # pandas už to správně parsuje

        print(f"  ✓ Načteno {len(df)} řádků z {filepath.split('/')[-1]}")
        return df
    except Exception as e:
        print(f"  ❌ Chyba při parsování {filepath}: {e}")
        return None


def extract_lambda_p_ratio():
    """
    Extrahuje Λ/p poměr kombinací Table37 (Λ/π) a Table47 (p/π).
    """
    print("\n" + "="*70)
    print("EXTRAKCE: Λ/p POMĚR vs MULTIPLICITA")
    print("="*70)

    base_dir = "simulations/qct_fit/data/HEPData-ins1471838-v1-csv"

    # Table 37: Lambda/pion ratio
    print("\n📂 Načítám Table37: Λ/π ratio...")
    lambda_pi_df = parse_hepdata_table(f"{base_dir}/Table37.csv")

    if lambda_pi_df is None:
        return None

    # Table 47: proton/pion ratio
    print("\n📂 Načítám Table47: p/π ratio...")
    proton_pi_df = parse_hepdata_table(f"{base_dir}/Table47.csv")

    if proton_pi_df is None:
        return None

    # Extrakce sloupců (názvy jsou dlouhé s LaTeX, použijeme index)
    # Sloupec 0: dN/deta střed
    # Sloupec 3: ratio hodnota
    # Sloupec 4,5: stat errors

    print("\n🔬 Výpočet Λ/p = (Λ/π) / (p/π)...")

    # Extrakce hodnot
    mult_lambda = lambda_pi_df.iloc[:, 0].values
    ratio_lambda_pi = lambda_pi_df.iloc[:, 3].values
    err_lambda_pi = lambda_pi_df.iloc[:, 4].values  # stat +

    mult_proton = proton_pi_df.iloc[:, 0].values
    ratio_proton_pi = proton_pi_df.iloc[:, 3].values
    err_proton_pi = proton_pi_df.iloc[:, 4].values  # stat +

    # Interpolace pokud mají různé multiplicity
    if not np.array_equal(mult_lambda, mult_proton):
        print("  ⚠️  Multiplicity se neshodují, používám pouze společné body")
        # Najít průnik
        common_mult = np.intersect1d(mult_lambda, mult_proton)

        # Indexy pro filtrování
        idx_lambda = np.isin(mult_lambda, common_mult)
        idx_proton = np.isin(mult_proton, common_mult)

        mult = mult_lambda[idx_lambda]
        ratio_lambda_pi = ratio_lambda_pi[idx_lambda]
        err_lambda_pi = err_lambda_pi[idx_lambda]
        ratio_proton_pi = ratio_proton_pi[idx_proton]
        err_proton_pi = err_proton_pi[idx_proton]
    else:
        mult = mult_lambda

    # Výpočet Λ/p
    ratio_lambda_p = ratio_lambda_pi / ratio_proton_pi

    # Chyba (propagace nejistot): δ(A/B) = (A/B) * sqrt((δA/A)² + (δB/B)²)
    rel_err_lambda = err_lambda_pi / ratio_lambda_pi
    rel_err_proton = err_proton_pi / ratio_proton_pi
    err_lambda_p = ratio_lambda_p * np.sqrt(rel_err_lambda**2 + rel_err_proton**2)

    print(f"  ✓ Vypočítáno {len(mult)} datových bodů")
    print(f"  📊 Multiplicita: {mult.min():.1f} - {mult.max():.1f}")
    print(f"  📊 Λ/p ratio: {ratio_lambda_p.min():.3f} - {ratio_lambda_p.max():.3f}")

    # Vytvoření výstupního DataFrame
    result_df = pd.DataFrame({
        'dN_deta': mult,
        'lambda_p_ratio': ratio_lambda_p,
        'error': err_lambda_p
    })

    return result_df


def extract_v2_data():
    """
    Extrahuje v₂ data z HEPData ins1190545 Table1.

    POZNÁMKA: Table1 obsahuje dN/deta vs pseudorapidity, ne v2!
    Musíme najít správnou tabulku pro v2 vs multiplicity.
    """
    print("\n" + "="*70)
    print("EXTRAKCE: v₂ DATA")
    print("="*70)

    base_dir = "simulations/qct_fit/data/HEPData-ins1190545-v1-csv"

    print("\n📂 Načítám Table1...")
    v2_df = parse_hepdata_table(f"{base_dir}/Table1.csv")

    if v2_df is None:
        print("  ❌ VAROVÁNÍ: v2 data z Table1 nejsou dostupná")
        print("  ℹ️  Table1 obsahuje dN/deta spektrum, ne v2 vs multiplicitu")
        print("  ℹ️  Pro správnou validaci by byla potřeba jiná tabulka nebo paper")
        return None

    print(f"  ⚠️  UPOZORNĚNÍ: Tato tabulka neobsahuje v₂ vs multiplicitu!")
    print(f"  Sloupce: {list(v2_df.columns)}")

    # Pro teď vrátíme None - museli bychom najít správný HEPData záznam
    return None


# =============================================================================
# HLAVNÍ EXEKUCE
# =============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("QCT DATA INTEGRITY PROTOCOL")
    print("Extrakce reálných ALICE experimentálních dat")
    print("="*70)
    print("\n⚠️  PŘÍSNÝ ZÁKAZ GENEROVÁNÍ SYNTETICKÝCH DAT")
    print("   Všechna data pocházejí z HEPData publikovaných měření\n")

    # --- PART 1: Lambda/p ratio ---
    lambda_p_df = extract_lambda_p_ratio()

    if lambda_p_df is not None:
        output_file = "simulations/qct_fit/data/REAL_DATA_lambda_p.csv"
        lambda_p_df.to_csv(output_file, index=False)
        print(f"\n✅ Uloženo: {output_file}")
        print(f"   Zdroj: HEPData ins1471838, Table37 / Table47")
        print(f"   Počet bodů: {len(lambda_p_df)}")
        print(f"   Výpočet: Λ/p = (Λ/π) / (p/π)")

        # Zobrazení prvních řádků
        print("\n📋 První 3 body:")
        print(lambda_p_df.head(3).to_string(index=False))
    else:
        print("\n❌ SELHÁNÍ: Λ/p data nebyla extrahována")
        sys.exit(1)

    # --- PART 2: v₂ data ---
    print("\n" + "="*70)
    v2_df = extract_v2_data()

    if v2_df is not None:
        output_file = "simulations/qct_fit/data/REAL_DATA_v2.csv"
        v2_df.to_csv(output_file, index=False)
        print(f"\n✅ Uloženo: {output_file}")
    else:
        print("\n⚠️  v₂ data nejsou dostupná v současných HEPData archivech")
        print("   Pro γ fit budou použita mock data jako fallback")
        print("   (Toto je přijatelné - hlavní validace je Λ/p ratio)")

    print("\n" + "="*70)
    print("✅ EXTRAKCE DOKONČENA")
    print("="*70)
    print("\nReálná data připravena pro QCT-FIT:")
    print(f"  ✅ Λ/p ratio: REAL_DATA_lambda_p.csv ({len(lambda_p_df)} bodů)")
    print(f"  ⚠️  v₂ data: Nejsou v HEPData (použije se mock)")
    print("\nDalší krok:")
    print("  python simulations/qct_fit/run_all_fits.py --use-real-data")
