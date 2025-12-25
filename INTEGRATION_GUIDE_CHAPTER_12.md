# Návod na integraci Kapitoly 12 do monografie

## Soubory k integraci:

1. **chapter_12_numerical_intro.tex** - Úvodní část kapitoly 12
2. **section_numerical_verification.tex** - Sekce 12.3 s numerickou verifikací

## Postup integrace do monografie_QCT_munipress.tex:

### Krok 1: Najít kapitolu 12
Hledejte řádek obsahující:
```latex
\chapter{Numerické výpočty a~validace}
```

### Krok 2: Nahradit/rozšířit obsah
Současný obsah kapitoly 12 nahraďte nebo doplňte:

```latex
% ============================================================================
% KAPITOLA 12: Numerické výpočty a validace
% ============================================================================

\input{latex_source/chapter_12_numerical_intro}

% Sekce 12.1 - Kalibrace na CODATA (pokud existuje, ponechat)
% \input{latex_source/section_codata_calibration}

% Sekce 12.2 - Další sekce (pokud existují, ponechat)

% Sekce 12.3 - Numerická verifikace na mřížce (NOVÉ!)
\input{latex_source/section_numerical_verification}

% Sekce 12.4 - Konzistenční testy (pokud existuje, ponechat)
% \input{latex_source/section_consistency_checks}
```

### Krok 3: Zkopírovat obrázky
Uložte obrázky do složky:
```
results/figures/
  ├─ qct_pb_al_comparison.png       (První obrázek - Pb vs Al)
  ├─ qct_high_res_osmium.png        (Druhý obrázek - Osmium high-res)
  ├─ qct_density_scaling.png        (Třetí obrázek - hustotní závislost)
  └─ qct_phase_transition.png       (Čtvrtý obrázek - fázový diagram)
```

### Krok 4: Kompilace
```bash
cd manuscripts/
pdflatex monografie_QCT_munipress.tex
biber monografie_QCT_munipress
pdflatex monografie_QCT_munipress.tex
pdflatex monografie_QCT_munipress.tex
```

## Kontrolní seznam:

- [ ] Úvodní oddíl (chapter_12_numerical_intro.tex) integrován
- [ ] Sekce 12.3 (section_numerical_verification.tex) integrována
- [ ] Všechny 4 obrázky zkopírovány do results/figures/
- [ ] LaTeX kompiluje bez chyb
- [ ] Obrázky se zobrazují správně
- [ ] Reference fungují (Kapitola 7, 9, Příloha atd.)

## Výsledek:

Kapitola 12 bude obsahovat:
- Profesionální úvod vysvětlující motivaci numerické verifikace
- Kompletní popis metodiky (Split-Step Fourier, GPE)
- 3 klíčové testy (Pb/Al, Osmium, Měsíc)
- 4 grafy s výsledky simulací
- Fázový diagram režimů QCT
- Závěr s predikcemi pro experimenty

Celková délka sekce 12.3: ~6-7 stran
