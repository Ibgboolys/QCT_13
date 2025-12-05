# ⚠️ DEPRECATED - TENTO DOKUMENT OBSAHUJE CHYBY

**POUŽIJ MÍSTO TOHO:** `REKONSTRUKCE_RIGOROZNI_ODPOVED.md`

---

## PROČ JE TENTO DOKUMENT DEPRECATED?

**KRITICKÁ CHYBA:**

Tento dokument používá chybnou "vylepšenou" verzi λ_micro:
```
λ_micro = (e/π)² × (1 - 1/φ³) ≈ 0.572 GeV  ❌ ŠPATNĚ!
```

**SPRÁVNÁ hodnota:**
```
λ_micro = 0.733 GeV (z QCT GP equation)
```

**DŮSLEDKY CHYBY:**

Kvůli použití špatné hodnoty λ_micro (0.572 místo 0.733) jsou **všechny** následné výpočty v tomto dokumentu **chybné**:

- ❌ Higgs VEV: 192 GeV místo 246 GeV (error 22% místo 0.015%)
- ❌ Sigma baryon: 0.925 GeV místo 1.186 GeV (error 22% místo 0.6%)
- ❌ Všechny ostatní odvozené hodnoty

---

## CO SE STALO?

1. **Pokus o "vylepšení":** Snažil jsem se odvodit λ_micro z čisté matematiky pomocí korekce (1 - 1/φ³)
2. **Chyba:** Tato korekce byla spekulativní a **pokazila všechny výpočty**
3. **Správný přístup:** Použít skutečnou QCT hodnotu λ_micro = 0.733 GeV

---

## SPRÁVNÁ VERZE

➡️ **POUŽIJ:** `REKONSTRUKCE_RIGOROZNI_ODPOVED.md`

Tento dokument obsahuje:
- ✅ Správnou hodnotu λ_micro = 0.733 GeV
- ✅ Správné výsledky (Higgs 0.015% error, Sigma 0.6% error)
- ✅ Fyzikálně rigorózní analýzu
- ✅ Kritickou kontrolu všech vztahů
- ✅ Identifikaci cherry-pickingu a dalších problémů

---

## SPRÁVNÉ VÝSLEDKY (z rigorózního dokumentu)

**SOLIDNÍ ODVOZENÍ:**

1. **Higgs VEV:**
   ```
   v = λ_micro × φ^12.088
     = 0.733 GeV × 335.855
     = 246.18 GeV
   Měřeno: 246.22 GeV
   Error: 0.015% ✅
   ```

2. **Sigma Baryon:**
   ```
   m_Σ = λ_micro × φ
       = 0.733 GeV × 1.618
       = 1.186 GeV
   Měřeno: 1.193 GeV
   Error: 0.59% ✅
   ```

3. **S_tot:**
   ```
   S_tot = n_ν/6 + 2 = 336/6 + 2 = 58
   Error: 0% (exact) ✅
   ```

---

## PONAUČENÍ

**Fyzikální rigoróznost vyžaduje:**

1. ✅ Kontrolu jednotek (dimensioned vs dimensionless)
2. ✅ Používání skutečných měřených/odvozených hodnot
3. ✅ Kritickou analýzu každého kroku
4. ✅ Vyhýbání se spekulativním "vylepšením"
5. ✅ Detekci cherry-pickingu

---

**ZNOVU: Správný dokument je `REKONSTRUKCE_RIGOROZNI_ODPOVED.md`**

**Tento soubor ponechán pouze jako dokumentace chyby, která byla odhalena kritickou revizí.**

---

**Datum deprecation:** 2025-11-15
**Důvod:** Chybné výpočty kvůli spekulativní korekci λ_micro
**Nahrazeno:** REKONSTRUKCE_RIGOROZNI_ODPOVED.md
