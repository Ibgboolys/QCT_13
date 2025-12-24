# 🔧 Instrukce pro merge do main

## ⚠️ Problém s přístupovými právy

Zjistil jsem, že **nemám oprávnění pushovat přímo do main branche** (HTTP 403).
Můžu pushovat pouze do branché začínajících `claude/`.

## ✅ Řešení: Merge provedeš ty

Všechny změny jsou **bezpečně uloženy** na branch:
```
claude/verify-manuscript-predictions-5GzUS
```

Tento branch je již **pushnutý na origin** a obsahuje:
- ✅ Kompletně obnovenou monografii (4597 řádků)
- ✅ Všechny nové implementace (σ²_max, α(ρ), G_eff)
- ✅ 2 nové appendixy
- ✅ 8 dokumentačních souborů

---

## 📋 Postup pro merge (3 kroky)

### Varianta A: Přes GitHub UI (DOPORUČENO)

1. **Otevři GitHub repository** v prohlížeči
2. **Vytvoř Pull Request:**
   - Base: `main`
   - Compare: `claude/verify-manuscript-predictions-5GzUS`
3. **Merguj PR** (Merge pull request button)

GitHub automaticky vyřeší konflikt (použije verzi z mého branche).

---

### Varianta B: Přes příkazovou řádku (pokud máš lokální přístup)

```bash
# 1. Přepni na main
git checkout main

# 2. Mergni můj branch
git merge claude/verify-manuscript-predictions-5GzUS --no-ff

# 3. Vyřeš konflikt (použij verzi z mého branche)
git checkout --theirs manuscripts/monografie_QCT_munipress.tex
git add manuscripts/monografie_QCT_munipress.tex

# 4. Dokončí merge
git commit -m "Merge: Obnovení monografie + implementace 3 řešení QCT"

# 5. Pushni do origin
git push origin main
```

---

## 📊 Co tento merge přinese

### Kritická oprava:
- **Obnoví smazanou monografii** (z 1 řádku na 4597 řádků)

### Nová funkcionalita:
- **σ²_max BCS odvození** → Řeší faktor-15 diskrepanci
- **α(ρ) hustotní škálování** → Řeší K<1 problém
- **G_eff saturační mechanismus** → Řeší astrofyzikální škály
- **Transparentní parametr labeling** → Zlepšuje transparentnost

### Statistiky:
```
12 souborů změněno
+3854 řádků přidáno
-14 řádků odebráno
```

---

## ✅ Verifikace po merge

Po dokončení merge zkontroluj:

```bash
# Ověř že monografie má správný počet řádků
wc -l manuscripts/monografie_QCT_munipress.tex
# Mělo by být: 4597 řádků

# Ověř že nové appendixy existují
ls -la manuscripts/latex_source/appendix_*scaling*.tex
ls -la manuscripts/latex_source/appendix_sigma*.tex

# Zobraz statistiky merge
git show --stat
```

---

## 🎯 Po dokončení merge

Monografie bude připravena k:
1. PDF kompilaci
2. Vizuální kontrole
3. Proofreadu českého textu

**Branch `claude/verify-manuscript-predictions-5GzUS` můžeš po úspěšném merge smazat.**

---

## 📞 Potřebuješ pomoc?

Pokud narazíš na problém, dej mi vědět a pomůžu ti s:
- Vytvořením PR přes GitHub API
- Řešením případných dalších konfliktů
- Verifikací správnosti merge

---

**Status:** Všechny změny jsou bezpečně uloženy na origin
**Action required:** Proveď merge přes GitHub UI nebo lokálně
