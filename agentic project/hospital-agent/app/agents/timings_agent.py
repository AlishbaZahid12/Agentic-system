from agno.tools import tool
import pandas as pd
from pathlib import Path

CSV_PATH = Path(__file__).resolve().parents[2] / "data" / "final_hospital_data.csv"

@tool(name="get_doctor_timings", description="Return the availability timings of a specific doctor.")
def get_doctor_timings(doctor_name: str) -> str:
    """Return the availability timings of a specific doctor."""
    df = pd.read_csv(CSV_PATH)
    df = df.dropna(subset=["Name", "Timings"])
    row = df[df["Name"].str.lower().str.contains(doctor_name.lower(), na=False)]
    if row.empty:
        return f"No doctor found named '{doctor_name}'."
    d = row.iloc[0]
    return f"{d['Name']} is available at {d['Timings']}."
