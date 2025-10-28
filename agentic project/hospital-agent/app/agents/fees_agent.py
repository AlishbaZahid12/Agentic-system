from agno.tools import tool
import pandas as pd
from pathlib import Path

CSV_PATH = Path(__file__).resolve().parents[2] / "data" / "final_hospital_data.csv"

@tool(name="get_doctor_fee", description="Return the consultation fee of a specific doctor.")
def get_doctor_fee(doctor_name: str) -> str:
    """Return the consultation fee of a specific doctor."""
    try:
        df = pd.read_csv(CSV_PATH)
        df = df.dropna(subset=["Name", "Fees"])
        row = df[df["Name"].str.lower().str.contains(doctor_name.lower(), na=False)]
        if row.empty:
            return f"No doctor found named '{doctor_name}'."
        d = row.iloc[0]
        return f"The consultation fee for {d['Name']} is {d['Fees']}."
    except Exception as e:
        return f"Error reading data: {e}"
