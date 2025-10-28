from agno.tools import tool
import pandas as pd
from pathlib import Path

CSV_PATH = Path(__file__).resolve().parents[2] / "data" / "final_hospital_data.csv"

@tool(name="get_doctors_by_specialization", description="List doctors for a given specialization (e.g., dentist).")
def get_doctors_by_specialization(specialization: str) -> str:
    """Return a list of doctors based on specialization."""
    df = pd.read_csv(CSV_PATH)
    df = df.dropna(subset=["Specialization", "Name"])
    matches = df[df["Specialization"].str.lower().str.contains(specialization.lower(), na=False)]
    if matches.empty:
        return f"No doctors found with specialization '{specialization}'."
    names = ", ".join(matches["Name"].tolist()[:50])
    return f"Doctors specialized in {specialization}: {names}."
