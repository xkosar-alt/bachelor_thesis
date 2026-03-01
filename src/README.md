# Zdrojový kód

Tento adresár obsahuje zdrojový kód a skripty vytvorené v rámci bakalárskej práce.

## Štruktúra

- `data_collection.py` - Skript pre zber dát
- `annotate.py` - Nástroj pre anotáciu dát
- `analyze_dataset.py` - Analýza a vizualizácia datasetu
- `requirements.txt` - Python závislosti

## Použitie

```python
# Príklad použitia
python data_collection.py --source /path/to/data --output ../data
python annotate.py --data ../data/raw --output ../data/annotations
python analyze_dataset.py --dataset ../data/annotations
```

## Požiadavky

```bash
pip install -r requirements.txt
```
