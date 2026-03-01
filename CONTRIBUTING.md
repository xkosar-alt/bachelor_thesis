# Príspevky k projektu

Ďakujeme za váš záujem prispieť k tomuto projektu bakalárskej práce!

## Ako prispieť

### Nahlásenie chýb

Ak nájdete chybu:
1. Skontrolujte, či chyba už nie je nahlásená v Issues
2. Vytvorte nový Issue s podrobným popisom
3. Uveďte kroky na reprodukciu problému
4. Pripojte relevantné logy alebo screenshots

### Návrh zmien

Ak chcete navrhnúť zlepšenie:
1. Vytvorte Issue s popisom návrhu
2. Počkajte na diskusiu a schválenie
3. Vytvorte Fork repozitára
4. Implementujte zmenu
5. Otvorte Pull Request

### Pull Request proces

1. **Fork a Clone**
   ```bash
   git clone https://github.com/your-username/bachelor_thesis.git
   cd bachelor_thesis
   ```

2. **Vytvorte novú vetvu**
   ```bash
   git checkout -b feature/my-improvement
   ```

3. **Implementujte zmeny**
   - Dodržiavajte existujúci kódový štýl
   - Pridajte komentáre kde je to potrebné
   - Aktualizujte dokumentáciu

4. **Testujte**
   ```bash
   # Otestujte svoje zmeny
   python src/data_collection.py --help
   python src/annotate.py --help
   python src/analyze_dataset.py --help
   ```

5. **Commit a Push**
   ```bash
   git add .
   git commit -m "Pridaná nová funkcionalita: ..."
   git push origin feature/my-improvement
   ```

6. **Otvorte Pull Request**
   - Popíšte zmeny podrobne
   - Uveďte súvisiace Issues
   - Počkajte na review

## Kódový štýl

### Python
- Používajte PEP 8 štýl
- Používajte type hints kde je to možné
- Dokumentujte funkcie pomocou docstrings

```python
def example_function(param1: str, param2: int) -> bool:
    """
    Krátky popis funkcie.
    
    Args:
        param1: Popis prvého parametra
        param2: Popis druhého parametra
        
    Returns:
        Popis návratovej hodnoty
    """
    pass
```

### LaTeX
- Používajte 4 medzery pre odsadenie
- Jeden príkaz na riadok
- Komentujte komplexné časti

## Štruktúra commit správ

```
Typ: Krátky popis (max 50 znakov)

Podrobnejší popis ak je potrebný.
Môže byť viacriadkový.

Fixes #123
```

**Typy commitov:**
- `feat`: Nová funkcionalita
- `fix`: Oprava chyby
- `docs`: Zmeny v dokumentácii
- `style`: Formátovanie, biele znaky
- `refactor`: Refaktoring kódu
- `test`: Pridanie testov
- `chore`: Údržba, konfigurácia

## Licencia

Prispením do tohto projektu súhlasíte s uvoľnením vášho príspevku pod MIT licenciou.

## Otázky?

Ak máte otázky, vytvorte Issue alebo kontaktujte autora.

Ďakujeme za váš príspevok! 🎓
