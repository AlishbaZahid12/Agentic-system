from agno.tools import tool
import pandas as pd
from pathlib import Path

CSV_PATH = Path(__file__).resolve().parents[2] / "data" / "final_hospital_data.csv"

@tool(name="get_doctor_details", description="Return complete details of a specific doctor.")
def get_doctor_details(doctor_name: str) -> str:
    """Return complete details of a specific doctor."""
    df = pd.read_csv(CSV_PATH)
    df = df.dropna(subset=["Name"])
    row = df[df["Name"].str.lower().str.contains(doctor_name.lower(), na=False)]
    if row.empty:
        return f"No doctor found named '{doctor_name}'."
    d = row.iloc[0]
    return (
        f"Doctor: {d['Name']}\n"
        f"Specialization: {d.get('Specialization','N/A')}\n"
        f"Fees: {d.get('Fees','N/A')}\n"
        f"Timings: {d.get('Timings','N/A')}"
    )
