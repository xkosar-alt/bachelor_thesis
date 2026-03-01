import pandas as pd

CSV_IN  = "results_sentinelhub_imagery_png.csv"
CSV_OUT = "results_sentinelhub_imagery_updated.csv"

candidate_cols = [
    "intensity",
]

positive_values = {
    "slabý výskyt",
    "škodlivý výskyt",
}

def norm_text(x: str) -> str:
    if pd.isna(x):
        return ""
    return str(x).strip().lower()

df = pd.read_csv(CSV_IN)

lower_map = {c.lower(): c for c in df.columns}
target_col = None
for cand in candidate_cols:
    if cand in lower_map:
        target_col = lower_map[cand]
        break

df[target_col] = df[target_col].apply(
    lambda v: "s výskytom" if norm_text(v) in positive_values else v
)

df.to_csv(CSV_OUT, index=False)
