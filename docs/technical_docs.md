# Technická dokumentácia

## Architektúra systému

Systém pre tvorbu datasetu sa skladá z nasledujúcich komponentov:

### 1. Zber dát (`data_collection.py`)
- Zbieranie obrázkov a metadát z rôznych zdrojov
- Organizácia do štruktúrovaného formátu
- Validácia kvality vstupných dát

### 2. Anotácia (`annotate.py`)
- Nástroje pre manuálnu a semi-automatickú anotáciu
- Podpora pre rôzne typy anotácií (klasifikácia, detekcia, segmentácia)
- Export do štandardných formátov (COCO, YOLO, Pascal VOC)

### 3. Analýza (`analyze_dataset.py`)
- Štatistická analýza datasetu
- Vizualizácia rozloženia tried
- Kontrola kvality a konzistencie

## Technológie

- **Python 3.8+**: Hlavný programovací jazyk
- **PyTorch**: Framework pre strojové učenie
- **OpenCV**: Spracovanie obrázkov
- **Matplotlib/Seaborn**: Vizualizácia dát

## Workflow

```
1. Zber dát → 2. Preprocessing → 3. Anotácia → 4. Validácia → 5. Export
```

## API dokumentácia

### DataCollector

```python
from data_collection import DataCollector

collector = DataCollector(source_path, output_path)
collector.collect()
```

### DataAnnotator

```python
from annotate import DataAnnotator

annotator = DataAnnotator(data_path, output_path)
annotator.process_batch(batch_size=10)
```

### DatasetAnalyzer

```python
from analyze_dataset import DatasetAnalyzer

analyzer = DatasetAnalyzer(dataset_path)
stats = analyzer.compute_statistics()
analyzer.visualize_distribution()
```

## Inštalácia

```bash
# Klonujte repozitár
git clone https://github.com/xkosar-alt/bachelor_thesis.git
cd bachelor_thesis

# Nainštalujte závislosti
cd src
pip install -r requirements.txt

# Nastavte adresárovú štruktúru
python data_collection.py --setup
```

## Použitie

### Zber dát
```bash
python src/data_collection.py --source /path/to/source --output data/
```

### Anotácia dát
```bash
python src/annotate.py --data data/raw --output data/annotations
```

### Analýza datasetu
```bash
python src/analyze_dataset.py --dataset data/annotations --output results/distribution.png
```

## Troubleshooting

### Časté problémy

1. **Chýbajúce závislosti**
   ```bash
   pip install -r requirements.txt
   ```

2. **Chyba pri načítaní dát**
   - Skontrolujte cestu k dátam
   - Overte formát súborov

3. **Problémy s pamäťou**
   - Zmenšite batch_size
   - Použite lazy loading

## Kontakt

Pre technické otázky kontaktujte autora práce.
