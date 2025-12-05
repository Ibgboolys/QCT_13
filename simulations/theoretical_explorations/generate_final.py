#!/usr/bin/env python3
"""
QCT GRAVITAČNÍ SONIFIKACE - FINÁLNÍ GENERATOR
Pouze poslední soubor - kosmické fade
"""

import numpy as np
import soundfile as sf
import warnings
warnings.filterwarnings('ignore')

# Audio parametry
SAMPLE_RATE = 44100
DURATION_SHORT = 3.0

def generate_cosmic_fade(duration=DURATION_SHORT):
    """Generuje úvodní kosmické fade (1000 Hz → 40 Hz)"""
    print("Generuji kosmicke fade (1000 Hz k 40 Hz)...")

    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))

    # Frekvence sweep (vysoká → nízká)
    f_start = 1000.0
    f_end = 40.0
    f_inst = f_start + (f_end - f_start) * (t / duration)

    # Fázová integrace
    phase = 2 * np.pi * np.cumsum(f_inst) / SAMPLE_RATE

    # Amplituda s fade
    amplitude = np.exp(-t / (duration * 0.8))

    # Signál
    cosmic = amplitude * np.sin(phase)

    # Normalizace
    cosmic = np.clip(cosmic, -1, 1)

    return cosmic, t

def main():
    """Generuje pouze kosmické fade"""
    print("="*80)
    print("QCT GRAVITAČNÍ SONIFIKACE - KOSMICKÉ FADE")
    print("="*80)
    print()

    # Generuj pouze poslední soubor
    cosmic, t = generate_cosmic_fade()

    # Ulož WAV
    sf.write("qct_cosmic_fade.wav", cosmic, SAMPLE_RATE)
    print("ULOZENO: qct_cosmic_fade.wav")
    print("  Popis: Uvodni kosmicke fade: 1000 Hz k 40 Hz")
    print("  Delka: 3.0 sekund")
    print("  Vzorku: 132300")
    print("-" * 50)

    print()
    print("="*80)
    print("VSECHNY WAV SOUBORY VYGENEROVANY!")
    print("="*80)
    print()
    print("Vygenerovane soubory:")
    print("  • qct_screening_drone.wav    - 40 Hz gravitační drone")
    print("  • qct_gw_chirp.wav          - Gravitační vlna chirp")
    print("  • qct_gravity_chord.wav     - Kompletní gravitační akord")
    print("  • qct_environment_beat.wav  - ISS vs Země interference")
    print("  • qct_coherence_pulse.wav  - 1 Hz koherenční pulz")
    print("  • qct_cosmic_fade.wav       - Kosmický úvod")
    print()
    print("Muzete si je prehrat jakymkoli audio prehravacem!")
    print("Doporuceno poslouchat s basy (subwoofer) pro plny zazitek!")

if __name__ == "__main__":
    main()