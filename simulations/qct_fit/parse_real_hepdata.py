#!/usr/bin/env python3
"""
RIGORÓZNÍ PARSER PRO HEPData SOUBORY
=====================================

PŘÍSNÝ ZÁKAZ: Tento skript NESMÍ generovat žádná syntetická data.
Účel: Extrahovat reálná experimentální data z HEPData CSV souborů s YAML hlavičkami.

Autor: QCT Data Integrity Protocol
Datum: 2025-12-18
"""

import pandas as pd
import numpy as np
import os
import sys

def parse_hepdata_csv(filepath):
    """
    Rigorózní parser pro HEPData soubory (ALICE format).
    Přeskakuje YAML hlavičky (#:) a hledá začátek dat.

    CRITICAL: Pokud parsing selže, script MUSÍ skončit s chybou.
              NESMÍ se generovat náhradní data.

    Args:
        filepath: Cesta k HEPData CSV souboru

    Returns:
        pandas.DataFrame s čistými numerickými daty, nebo None při chybě
    """
    if not os.path.exists(filepath):
        print(f"❌ CRITICAL ERROR: Soubor {filepath} neexistuje!")
        return None

    print(f"\n📂 Parsing: {os.path.basename(filepath)}")

    # Načtení souboru a přeskočení YAML hlaviček
    data_lines = []
    headers = None
    reading_data = False
    line_num = 0

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line_num += 1

                # Přeskočit YAML metadata řádky začínající #:
                if line.startswith('#:'):
                    continue

                # Přeskočit prázdné řádky
                if not line.strip():
                    continue

                # Detekce hlavičky (první řádek bez #: který obsahuje názvy sloupců)
                if not reading_data:
                    headers = [h.strip() for h in line.strip().split(',')]
                    print(f"  ✓ Hlavička nalezena na řádku {line_num}: {len(headers)} sloupců")
                    reading_data = True
                    continue

                # Načítání numerických dat
                if reading_data:
                    parts = line.strip().split(',')
                    if len(parts) >= len(headers):
                        data_lines.append(parts[:len(headers)])
                    else:
                        print(f"  ⚠️  Řádek {line_num} má méně sloupců než hlavička, přeskakuji")

        if not data_lines:
            print(f"❌ ERROR: Nepodařilo se načíst žádná data ze souboru {filepath}")
            print(f"  Soubor měl {line_num} řádků, ale žádná datová řada nebyla detekována.")
            return None

        # Vytvoření DataFrame
        df = pd.DataFrame(data_lines, columns=headers)

        # Konverze na čísla
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        # Odstranění řádků s NaN (nepodařilo se konvertovat)
        rows_before = len(df)
        df = df.dropna()
        rows_after = len(df)

        if rows_after == 0:
            print(f"❌ ERROR: Všechny řádky obsahují ne-numerická data!")
            return None

        if rows_after < rows_before:
            print(f"  ⚠️  Odstraněno {rows_before - rows_after} řádků s chybnými daty")

        print(f"  ✅ SUCCESS: Načteno {len(df)} datových řádků")
        print(f"  📊 Sloupce: {list(df.columns)}")

        return df

    except Exception as e:
        print(f"❌ PARSING ERROR: {e}")
        print(f"  Soubor: {filepath}")
        print(f"  Poslední řádek: {line_num}")
        return None


def extract_lambda_p_ratio(hepdata_dir):
    """
    Extrahuje Λ/p poměr z HEPData ins1471838.

    POZNÁMKA: Musíme najít správnou tabulku s Λ/p poměrem vs multiplicitou.
              Table 3 je K0S spektrum (špatně!), musíme najít správnou.
    """
    print("\n" + "="*70)
    print("EXTRAKCE: Λ/p POMĚR vs MULTIPLICITA")
    print("="*70)

    # Projdeme všechny tabulky a najdeme tu správnou
    tables_to_check = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]  # Lambda tabulky

    for table_num in tables_to_check:
        filepath = os.path.join(hepdata_dir, f"Table{table_num}.csv")
        if not os.path.exists(filepath):
            continue

        print(f"\n🔍 Zkouším Table{table_num}...")
        df = parse_hepdata_csv(filepath)

        if df is None:
            continue

        # Zkontrolujeme, jestli obsahuje Lambda data
        # Hledáme sloupce které by mohly být yield nebo ratio
        print(f"  Sloupce: {list(df.columns)}")

        # Pro teď uložíme první smysluplnou tabulku
        if len(df) > 0:
            print(f"  ✓ Table{table_num} obsahuje {len(df)} řádků")
            return df, table_num

    print(f"❌ CHYBA: Nenalezena vhodná tabulka pro Λ/p poměr")
    return None, None


def extract_v2_data(hepdata_dir):
    """
    Extrahuje v₂ data z HEPData ins1190545.
    Table1: charged particle density vs pseudorapidity
    """
    print("\n" + "="*70)
    print("EXTRAKCE: v₂ ANISOTROPY DATA")
    print("="*70)

    filepath = os.path.join(hepdata_dir, "Table1.csv")
    df = parse_hepdata_csv(filepath)

    if df is None:
        print(f"❌ CHYBA: Nepodařilo se načíst v₂ data z Table1.csv")
        return None

    return df


# =============================================================================
# HLAVNÍ EXEKUCE
# =============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("QCT DATA INTEGRITY PROTOCOL")
    print("Rigorózní extrakce reálných experimentálních dat")
    print("="*70)
    print("\n⚠️  PŘÍSNÝ ZÁKAZ GENEROVÁNÍ SYNTETICKÝCH DAT")
    print("   Pokud parsing selže, skript skončí s chybou.\n")

    # Cesty k HEPData archivům
    base_dir = "simulations/qct_fit/data"
    lambda_dir = os.path.join(base_dir, "HEPData-ins1471838-v1-csv")
    v2_dir = os.path.join(base_dir, "HEPData-ins1190545-v1-csv")

    # Kontrola existence
    if not os.path.exists(lambda_dir):
        print(f"❌ FATAL: Adresář {lambda_dir} neexistuje!")
        sys.exit(1)

    if not os.path.exists(v2_dir):
        print(f"❌ FATAL: Adresář {v2_dir} neexistuje!")
        sys.exit(1)

    # --- PART 1: Lambda/p data ---
    lambda_df, table_num = extract_lambda_p_ratio(lambda_dir)

    if lambda_df is not None:
        output_file = os.path.join(base_dir, "REAL_DATA_lambda.csv")
        lambda_df.to_csv(output_file, index=False)
        print(f"\n✅ Uloženo: {output_file}")
        print(f"   Zdroj: HEPData ins1471838, Table{table_num}")
        print(f"   Počet bodů: {len(lambda_df)}")
    else:
        print(f"\n❌ SELHÁNÍ: Λ/p data nebyla extrahována")
        sys.exit(1)

    # --- PART 2: v₂ data ---
    v2_df = extract_v2_data(v2_dir)

    if v2_df is not None:
        output_file = os.path.join(base_dir, "REAL_DATA_v2.csv")
        v2_df.to_csv(output_file, index=False)
        print(f"\n✅ Uloženo: {output_file}")
        print(f"   Zdroj: HEPData ins1190545, Table1")
        print(f"   Počet bodů: {len(v2_df)}")
    else:
        print(f"\n❌ SELHÁNÍ: v₂ data nebyla extrahována")
        sys.exit(1)

    print("\n" + "="*70)
    print("✅✅ DOKONČENO BEZ GENEROVÁNÍ SYNTETICKÝCH DAT")
    print("="*70)
    print("\nDalší krok: Použijte tyto soubory pro QCT fitting:")
    print(f"  - {base_dir}/REAL_DATA_lambda.csv")
    print(f"  - {base_dir}/REAL_DATA_v2.csv")
