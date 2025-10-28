# app/utils.py
import pandas as pd
from typing import List, Dict

DATA_PATH = "../data/final_hospital_data.csv"

def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    # Basic cleaning: strip whitespace
    for c in ["Name", "Specialization", "Fees", "Timings"]:
        if c in df.columns:
            df[c] = df[c].astype(str).str.strip()
        else:
            df[c] = ""
    return df

def find_doctors_by_specialization(df: pd.DataFrame, specialization: str) -> List[Dict]:
    s = specialization.strip().lower()
    matched = df[df["Specialization"].str.lower().str.contains(s, na=False)]
    return matched.to_dict(orient="records")
