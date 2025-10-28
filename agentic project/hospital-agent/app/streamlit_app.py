import streamlit as st
import sys, os, re

# 🧭 Add root path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.main_agent import hospital_agent

# 🏥 Streamlit setup
st.set_page_config(page_title="🏥 Hospital Agent", page_icon="🩺", layout="wide")

# 🌟 Header
st.title("🏥 Hospital Agent (Groq + Agno)")
st.markdown(
    """
    💬 **Ask anything about doctors, fees, timings, or specializations!**  
    Type naturally — the agent will reason and fetch answers from your hospital data.
    """
)
st.divider()

# 💾 Session-based chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# 🧠 Display chat messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant"):
            st.markdown(msg["content"])

# 🧍‍♀️ User input box
if user_input := st.chat_input("Ask your hospital agent..."):
    # Store user input
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Process response from the hospital agent
    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            try:
                response = hospital_agent.run(user_input)

                # Extract clean text only
                if hasattr(response, "content") and isinstance(response.content, str):
                    answer = response.content.strip()
                elif hasattr(response, "output") and hasattr(response.output, "content"):
                    answer = response.output.content.strip()
                else:
                    answer = str(response).strip()

                # 🧹 Remove any internal function or tool traces
                answer = re.sub(r"<function=.*?>", "", answer)
                answer = re.sub(r"Used tool.*", "", answer)
                answer = re.sub(r"RunOutput.*", "", answer)
                answer = re.sub(r"\s+", " ", answer).strip()

                # Display and store clean answer
                st.markdown(f"**Agent:** {answer}")
                st.session_state.messages.append({"role": "assistant", "content": f"**Agent:** {answer}"})

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
