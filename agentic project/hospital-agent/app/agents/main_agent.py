import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.groq import Groq

# Import tool functions
from app.agents.fees_agent import get_doctor_fee
from app.agents.timings_agent import get_doctor_timings
from app.agents.specialization_agent import get_doctors_by_specialization
from app.agents.name_agent import get_doctor_details

# Load environment variables (GROQ_API_KEY must be in .env)
load_dotenv()

# Initialize Groq model (Agno v2.1.4 style)
llm = Groq(id="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))

# Create the Hospital Agent
hospital_agent = Agent(
    name="HospitalAgent",
    description=(
        "You are an intelligent hospital assistant. "
        "Use reasoning and the available tools to answer questions "
        "about doctors, fees, timings, and specializations from the CSV file."
    ),
    model=llm,
    tools=[
        get_doctor_fee,
        get_doctor_timings,
        get_doctors_by_specialization,
        get_doctor_details,
    ],
)

# CLI fallback (optional - not used by Streamlit but kept for testing)
if __name__ == "__main__":
    print("✅ Hospital Agent (Groq + Agno) ready. Type 'exit' to quit.\n")
    while True:
        query = input("Ask your hospital agent: ")
        if query.lower() in ["exit", "quit"]:
            print("👋 Exiting system.")
            break
        response = hospital_agent.run(query)

        # Print brief summary and final answer safely
        print("\n" + "─" * 60)
        print("🧠 Reasoning Summary:")
        if hasattr(response, "tools") and response.tools:
            for t in response.tools:
                print(f"• Used tool → {t.tool_name} with arguments {t.tool_args}")
        else:
            print("• No external tool was needed.")

        print("\n🩺 Final Answer:")
        if hasattr(response, "content") and isinstance(response.content, str):
            print(response.content.strip())
        elif hasattr(response, "output") and hasattr(response.output, "content"):
            print(response.output.content.strip())
        else:
            print(str(response).strip())
        print("─" * 60 + "\n")
