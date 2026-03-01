# Bakalárska práca - Tvorba Datasetu pre Tréning Modelov Umelej Inteligencie v Agronómii

Tento repozitár obsahuje zdrojové súbory mojej bakalárskej práce na tému "Tvorba Datasetu pre Tréning Modelov Umelej Inteligencie v Agronómii".

## Štruktúra repozitára

```
.
├── thesis/              # LaTeX zdrojové súbory práce
│   ├── main.tex        # Hlavný súbor
│   ├── chapters/       # Kapitoly práce
│   ├── figures/        # Obrázky a grafy
│   └── bibliography/   # Bibliografické zdroje
├── src/                # Zdrojový kód (implementácia)
├── data/               # Dáta a datasety
├── docs/               # Doplnková dokumentácia
└── Makefile           # Build skripty
```

## Kompilácia práce

Pre kompiláciu LaTeX dokumentu do PDF:

```bash
make build
```

Pre vyčistenie pomocných súborov:

```bash
make clean
```

Pre zobrazenie výsledného PDF:

```bash
make view
```

## Požiadavky

Pre kompiláciu práce je potrebné mať nainštalované:
- LaTeX distribúciu (napr. TeX Live, MiKTeX)
- pdflatex
- biber (pre bibliografiu)

## Obsah práce

### Abstrakt
Práca sa zaoberá tvorbou datasetu pre tréning modelov umelej inteligencie v oblasti agronómie.

### Kapitoly
1. **Úvod** - Motivácia a ciele práce
2. **Teoretické základy** - AI v agronómii a datasety pre ML
3. **Metodológia** - Návrh a proces tvorby datasetu
4. **Implementácia** - Technológie a nástroje
5. **Výsledky a diskusia** - Vyhodnotenie vytvoreného datasetu
6. **Záver** - Zhrnutie a možnosti ďalšieho výskumu

## Autor

Váš Meno  
Univerzita  
Rok obhajoby: 2024

## Licencia

Tento repozitár je určený pre akademické účely. 
