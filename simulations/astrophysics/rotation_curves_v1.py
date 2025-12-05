import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# 1. GENERICKÁ DATA GALAXIE (Modelová data podobná SPARC)
# ---------------------------------------------------------
# Poloměr (kpc)
r = np.linspace(0.1, 20, 100) 

# Rychlost způsobená viditelnou hmotou (Baryony: Hvězdy + Plyn)
# Modelujeme jako Freemanův disk + Bulge
# V reálné simulaci byste načetli data ze souboru .dat
def v_baryon_model(r):
    # Zjednodušený profil: náběh a pokles (Keplerian)
    return 100 * (r / (r + 2)) * (1 / np.sqrt(1 + (r/5)**2)) * 1.5

v_bar = v_baryon_model(r)

# Pozorovaná rychlost (Data - typicky plochá křivka)
# Toto je to, co chceme trefit naší teorií
v_obs = 200 * (1 - np.exp(-r/2)) # Asymptoticky jde k 200 km/s

# ---------------------------------------------------------
# 2. QCT MODEL: KOMPRESE KONDENZÁTU
# ---------------------------------------------------------
# Myšlenka: Baryonové zrychlení (g_bar) komprimuje vakuum.
# Kde je g_bar malé (okraje), tam je odezva relativně silnější (nebo se projevuje pozadí).

def get_v_QCT(r, v_bar):
    """
    Vypočítá celkovou rychlost včetně QCT příspěvku.
    Použijeme vztah: g_total = g_bar + g_condensate
    """
    # 1. Newtonovské zrychlení od baryonů
    g_bar = (v_bar**2) / r 
    
    # 2. QCT Příspěvek (Zde je fyzika vaší teorie)
    # Parametr a0: Škála zrychlení, kde se efekt zapíná (cca 1.2e-10 m/s2)
    a0 = 1.2e-10  # m/s^2 (Standardní hodnota pro galaxie)
    
    # Model A: Interpolace (jako MOND, ale interpretovaná jako efekt kondenzátu)
    # g_total = g_bar / (1 - exp(-sqrt(g_bar/a0))) - jen příklad funkce
    
    # Model B: QCT specifický ("Vakuová odezva")
    # Předpokládejme, že kondenzát přidává konstantní "tlak" nebo sílu na velkých škálách
    # g_total = sqrt(g_bar * a0) je klasický MOND limit.
    # Zkusme vaši myšlenku "kosmologického průměru":
    # Kondenzát vytváří efektivní potenciál, který dominuje, když g_bar klesne pod a0.
    
    g_QCT_effect = np.sqrt(g_bar * a0) # Toto matematicky funguje na galaxie nejlépe
    
    # Přechodová funkce (aby to fungovalo i ve středu galaxie)
    # g_tot = g_bar pokud g_bar >> a0
    # g_tot = sqrt(g_bar*a0) pokud g_bar << a0
    interpolation = 1 / (1 + g_bar/a0) # Váha efektu
    
    g_total = g_bar + (np.sqrt(g_bar * a0) - g_bar) * interpolation
    # Pozn: Toto je zjednodušená "Simple MOND" funkce pro demonstraci
    
    return np.sqrt(g_total * r)

v_pred = get_v_QCT(r, v_bar)

# ---------------------------------------------------------
# 3. VIZUALIZACE
# ---------------------------------------------------------

plt.figure(figsize=(10, 6))

# Baryony (to co vidíme)
plt.plot(r, v_bar, 'b--', linewidth=2, label='Newton (Baryons only)')

# Data (to co naměřili astronomové)
plt.plot(r, v_obs, 'ko', markersize=4, label='Observation (Data)')

# QCT Predikce
plt.plot(r, v_pred, 'r-', linewidth=3, label='QCT Prediction (Condensed Vacuum)')

plt.xlabel('Radius [kpc]', fontsize=12)
plt.ylabel('Rotation Velocity [km/s]', fontsize=12)
plt.title('Galaxy Rotation Curve: QCT Vacuum Response', fontsize=14)
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)

# Přidání anotace
plt.text(10, 50, r'$G_{eff} \rightarrow$ Dynamic Response', color='red', fontsize=12)

plt.show()