import pandas as pd
from sklearn.model_selection import train_test_split
import os


INPUT_CSV = 'dataset_filtered.csv'

TRAIN_CSV = 'data_train.csv'
VAL_CSV   = 'data_val.csv'
TEST_CSV  = 'data_test.csv'

TEST_SIZE = 0.15
VAL_SIZE  = 0.15
# Zvyšok je testovacia množina, takže 70%

RANDOM_SEED = 42

def split_data():


    df = pd.read_csv(INPUT_CSV, sep=';', encoding='cp1250')

    # Oddelenie testovacej množiny
    # stratify zabezpečí pomer
    df_train_val, df_test = train_test_split(
        df, 
        test_size=TEST_SIZE, 
        random_state=RANDOM_SEED, 
        stratify=df['intensity']
    )

    # Rozdelenie na trénovaciu a validačnú množinu
    relative_val_size = VAL_SIZE / (1 - TEST_SIZE)

    df_train, df_val = train_test_split(
        df_train_val,
        test_size=relative_val_size,
        random_state=RANDOM_SEED,
        stratify=df_train_val['intensity']
    )

    df_train.to_csv(TRAIN_CSV, sep=';', index=False, encoding='cp1250')
    df_val.to_csv(VAL_CSV, sep=';', index=False, encoding='cp1250')
    df_test.to_csv(TEST_CSV, sep=';', index=False, encoding='cp1250')

if __name__ == "__main__":
    split_data()