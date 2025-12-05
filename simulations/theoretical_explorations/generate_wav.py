#!/usr/bin/env python3
"""
QCT GRAVITAČNÍ SONIFIKACE - GENERATOR WAV SOUBORŮ
Generace skutečných audio souborů podle QCT teorie
"""

import numpy as np
import soundfile as sf
import warnings
warnings.filterwarnings('ignore')

# Audio parametry
SAMPLE_RATE = 44100
DURATION_SHORT = 3.0  # 3 sekundy pro ukázky
DURATION_LONG = 10.0  # 10 sekund pro delší záznamy

def generate_screening_drone(duration=DURATION_SHORT):
    """Generuje screening drone 40 Hz s harmonics"""
    print("Generuji screening drone (40 Hz + harmonics)...")

    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))

    # Základní tón (40 Hz - fundamentál)
    tone = 0.3 * np.sin(2 * np.pi * 40 * t)

    # Harmonické složky (H1-H5)
    harmonics = {
        2: 0.2,   # H2: 80 Hz
        3: 0.15,  # H3: 120 Hz
        5: 0.1,   # H5: 200 Hz
        8: 0.05   # H8: 320 Hz
    }

    for harmonic, amplitude in harmonics.items():
        tone += amplitude * np.sin(2 * np.pi * 40 * harmonic * t)

    # Koherenční modulace (1 Hz pulz)
    coherence_mod = 0.5 * (1 + 0.1 * np.sin(2 * np.pi * 1 * t))
    tone *= coherence_mod

    # Fade in/out
    fade_samples = int(0.1 * SAMPLE_RATE)
    tone[:fade_samples] *= np.linspace(0, 1, fade_samples)
    tone[-fade_samples:] *= np.linspace(1, 0, fade_samples)

    # Normalizace
    tone = np.clip(tone, -1, 1)

    return tone, t

def generate_gw_chirp(duration=DURATION_SHORT):
    """Generuje gravitační vlnu chirp (35-250 Hz sweep)"""
    print("Generuji GW chirp (35-250 Hz sweep)...")

    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    tau = duration

    # Instantní frekvence (exponenciální růst)
    f_start = 35.0
    f_end = 250.0
    f_inst = f_start + (f_end - f_start) * (t / tau)**3

    # Fázová integrace
    phase = 2 * np.pi * np.cumsum(f_inst) / SAMPLE_RATE

    # Amplituda (roste, pak sharp peak a útlum)
    t_peak = 0.7 * tau
    sigma_peak = 0.08 * tau
    amplitude = (t / tau)**2 * np.exp(-(t - t_peak)**2 / sigma_peak**2)

    # Základní chirp
    chirp = amplitude * np.sin(phase)

    # QCT modifikace (screening potlačení vysokých frekvencí)
    lambda_screen = 40e-6  # 40 μm
    c = 3e8  # rychlost světla
    qct_factor = np.exp(-2 * np.pi * f_inst * lambda_screen / c)
    chirp *= qct_factor

    # Přidání kontextu (40 Hz drone na pozadí)
    drone = 0.1 * np.sin(2 * np.pi * 40 * t)
    full_signal = chirp + drone

    # Fade in/out
    fade_samples = int(0.1 * SAMPLE_RATE)
    full_signal[:fade_samples] *= np.linspace(0, 1, fade_samples)
    full_signal[-fade_samples:] *= np.linspace(1, 0, fade_samples)

    # Normalizace
    full_signal = np.clip(full_signal, -1, 1)

    return full_signal, t

def generate_qct_chord(duration=DURATION_SHORT):
    """Generuje kompletní QCT akord (40+80+120+160+200 Hz)"""
    print("Generuji QCT akord (gravitační akord)...")

    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))

    # Kompletní akord s různými amplitudami
    chord = np.zeros_like(t)

    # Frekvence a amplitudy pro "hudebně" bohatý zvuk
    freqs_amps = [
        (40, 0.4),   # H1 - fundamentál
        (80, 0.25),  # H2 - oktáva
        (120, 0.2),  # H3 - kvinta
        (160, 0.15), # H4 - kvartta
        (200, 0.1)   # H5 - velká tercie
    ]

    for freq, amp in freqs_amps:
        chord += amp * np.sin(2 * np.pi * freq * t)

    # Koherenční modulace (jemné 1 Hz vlnění)
    coherence = 0.9 + 0.1 * np.sin(2 * np.pi * 1 * t)
    chord *= coherence

    # Quantum flutter (mírné vibrato)
    flutter = 1 + 0.02 * np.sin(2 * np.pi * 0.5 * t)
    chord *= flutter

    # Fade in/out
    fade_samples = int(0.1 * SAMPLE_RATE)
    chord[:fade_samples] *= np.linspace(0, 1, fade_samples)
    chord[-fade_samples:] *= np.linspace(1, 0, fade_samples)

    # Normalizace
    chord = np.clip(chord, -1, 1)

    return chord, t

def generate_environment_beat(duration=DURATION_LONG):
    """Generuje environment beat (Země 40 Hz vs ISS 41 Hz)"""
    print("Generuji environment beat (Země vs ISS)...")

    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))

    # Dvě frekvence (Země a ISS)
    f_earth = 40.0      # Země
    f_iss = 41.0        # ISS (+2.5%)

    # Jednotlivé tóny
    earth_tone = 0.3 * np.sin(2 * np.pi * f_earth * t)
    iss_tone = 0.3 * np.sin(2 * np.pi * f_iss * t)

    # Beat pattern - interference
    beat = earth_tone + iss_tone

    # Přidání harmonics pro bohatší zvuk
    for harm in [2, 3]:
        beat += 0.1 * np.sin(2 * np.pi * f_earth * harm * t)

    # Fade in/out
    fade_samples = int(0.5 * SAMPLE_RATE)
    beat[:fade_samples] *= np.linspace(0, 1, fade_samples)
    beat[-fade_samples:] *= np.linspace(1, 0, fade_samples)

    # Normalizace
    beat = np.clip(beat, -1, 1)

    return beat, t

def generate_coherence_pulse(duration=DURATION_LONG):
    """Generuje koherenční pulz (1 Hz metronom)"""
    print("Generuji koherenční pulz (1 Hz metronom)...")

    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))

    # Rytmický pulz 1 Hz
    pulse = 0.5 * np.sin(2 * np.pi * 1 * t)

    # Přidání harmonics pro "teplejší" zvuk
    pulse += 0.2 * np.sin(2 * np.pi * 2 * t)  # 2 Hz
    pulse += 0.1 * np.sin(2 * np.pi * 3 * t)  # 3 Hz

    # Exponenciální decay pro přirozenější pulz
    decay = np.exp(-t / (duration * 0.5))
    pulse *= decay

    # Fade in
    fade_samples = int(0.5 * SAMPLE_RATE)
    pulse[:fade_samples] *= np.linspace(0, 1, fade_samples)

    # Normalizace
    pulse = np.clip(pulse, -1, 1)

    return pulse, t

def generate_cosmic_fade(duration=DURATION_SHORT):
    """Generuje úvodní kosmické fade (1000 Hz → 40 Hz)"""
    print("Generuji kosmické fade (1000 Hz → 40 Hz)...")

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

def save_wav_file(data, filename, description):
    """Uloží WAV soubor a zobrazí info"""
    sf.write(filename, data, SAMPLE_RATE)
    print(f"ULOZENO: {filename}")
    print(f"  Popis: {description}")
    print(f"  Delka: {len(data)/SAMPLE_RATE:.1f} sekund")
    print(f"  Vzorku: {len(data)}")
    print("-" * 50)

def main():
    """Hlavní generátor všech WAV souborů"""
    print("="*80)
    print("QCT GRAVITAČNÍ SONIFIKACE - WAV GENERATOR")
    print("="*80)
    print()

    # 1. Screening Drone
    tone, t = generate_screening_drone()
    save_wav_file(tone, "qct_screening_drone.wav",
                 "40 Hz screening drone s harmonics (H1-H8) + koherenční modulace")

    # 2. GW Chirp
    chirp, t = generate_gw_chirp()
    save_wav_file(chirp, "qct_gw_chirp.wav",
                 "Gravitační vlna chirp 35-250 Hz s QCT modifikací")

    # 3. QCT Akord
    chord, t = generate_qct_chord()
    save_wav_file(chord, "qct_gravity_chord.wav",
                 "Kompletní gravitační akord 40+80+120+160+200 Hz")

    # 4. Environment Beat
    beat, t = generate_environment_beat()
    save_wav_file(beat, "qct_environment_beat.wav",
                 "Environment beat: Země (40 Hz) vs ISS (41 Hz) - interference pattern")

    # 5. Koherenční Pulz
    pulse, t = generate_coherence_pulse()
    save_wav_file(pulse, "qct_coherence_pulse.wav",
                 "Koherenční pulz 1 Hz jako metronom vesmíru")

    # 6. Kosmické Fade
    cosmic, t = generate_cosmic_fade()
    save_wav_file(cosmic, "qct_cosmic_fade.wav",
                 "Uvodni kosmicke fade: 1000 Hz k 40 Hz")

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