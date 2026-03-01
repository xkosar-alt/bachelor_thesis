# Návod pre používateľov

## Úvod

Tento návod vás prevedie procesom používania nástrojov vytvorených v rámci bakalárskej práce.

## Rýchly štart

### 1. Príprava prostredia

```bash
# Naklonujte repozitár
git clone https://github.com/xkosar-alt/bachelor_thesis.git
cd bachelor_thesis

# Vytvorte virtuálne prostredie
python -m venv venv
source venv/bin/activate  # Na Windows: venv\Scripts\activate

# Nainštalujte závislosti
pip install -r src/requirements.txt
```

### 2. Nastavenie projektu

```bash
# Vytvorte potrebné adresáre
python src/data_collection.py --setup --output data/
```

### 3. Zber dát

```bash
# Zbierajte dáta z vášho zdroja
python src/data_collection.py --source /path/to/your/data --output data/
```

### 4. Anotácia dát

```bash
# Anotujte zozbierané dáta
python src/annotate.py --data data/raw --output data/annotations
```

### 5. Analýza výsledkov

```bash
# Analyzujte vytvorený dataset
python src/analyze_dataset.py --dataset data/annotations
```

## Podrobný návod

### Zber dát

Skript `data_collection.py` umožňuje zbierať dáta z rôznych zdrojov:

**Parametre:**
- `--source`: Cesta k zdrojovým dátam
- `--output`: Cieľový adresár pre uloženie
- `--setup`: Vytvorí adresárovú štruktúru

**Príklad:**
```bash
python src/data_collection.py \
    --source /mnt/external/agriculture_images \
    --output data/
```

### Anotácia dát

Skript `annotate.py` poskytuje nástroje pre anotáciu obrázkov:

**Parametre:**
- `--data`: Cesta k dátam na anotáciu
- `--output`: Adresár pre uloženie anotácií
- `--batch-size`: Počet obrázkov na spracovanie naraz

**Príklad:**
```bash
python src/annotate.py \
    --data data/raw/images \
    --output data/annotations \
    --batch-size 20
```

### Analýza datasetu

Skript `analyze_dataset.py` vytvorí štatistiky a vizualizácie:

**Parametre:**
- `--dataset`: Cesta k datasetu
- `--output`: Cesta pre uloženie vizualizácií (voliteľné)

**Príklad:**
```bash
python src/analyze_dataset.py \
    --dataset data/annotations \
    --output results/distribution.png
```

## Často kladené otázky

### Aké formáty obrázkov sú podporované?
- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)

### Ako môžem pridať vlastné triedy?
Upravte konfiguračný súbor alebo zadajte triedy priamo v anotačnom nástroji.

### Čo robiť, ak mám veľký dataset?
Spracovávajte dáta v menších dávkach pomocou parametra `--batch-size`.

### Ako exportovať anotácie do iného formátu?
Anotácie sú uložené v JSON formáte, ktorý môžete ľahko konvertovať do iných formátov.

## Tipy a triky

1. **Použite virtuálne prostredie** pre izoláciu závislostí
2. **Zálohujte svoje dáta** pravidelne
3. **Kontrolujte kvalitu anotácií** priebežne
4. **Dokumentujte zmeny** v datasete

## Podpora

Pri problémoch alebo otázkach:
- Skontrolujte dokumentáciu
- Prezrite si issues na GitHub
- Kontaktujte autora práce
