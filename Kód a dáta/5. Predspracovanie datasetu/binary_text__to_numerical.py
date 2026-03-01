import pandas as pd

INPUT_CSV = 'dataset_integrity_checked.csv'
OUTPUT_CSV = 'dataset_numerical_binary.csv'

def convert_labels():

    df = pd.read_csv(INPUT_CSV, sep=';', encoding='cp1250')
    df['intensity_text'] = df['intensity']

    mapping = {
        'bez výskytu': 0,
        's výskytom': 1,
    }

    df['intensity'] = df['intensity'].map(mapping).fillna(0).astype(int)
    df.to_csv(OUTPUT_CSV, sep=';', index=False, encoding='cp1250')

if __name__ == "__main__":
    convert_labels()