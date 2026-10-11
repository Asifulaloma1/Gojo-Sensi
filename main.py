import streamlit as st
from groq import Groq
import time

st.set_page_config(page_title="Gojo Sensi REAL AI", page_icon="🟣", layout="centered")

# --- SIDEBAR ---
with st.sidebar:
    st.title("🟣 Gojo Control")

    # Secret theke auto nibe, na thakle user input nibe
    if "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]
        st.success("Gojo's Six Eyes Are watching you ✅")
    else:
        api_key = st.text_input("Groq API Key boshao (gsk_...)", type="password")
        st.caption("Key ta console.groq.com theke niso oita")

    st.divider()
    st.metric("Power", "∞ INFINITE")
    if st.button("Memory Erase"):
        st.session_state.messages = []
        st.rerun()

st.title("🟣 GOJO SENSI - REAL AI")
st.caption("The Strongest is now REAL. Powered by Groq.")

# System prompt for Gojo
GOJO_PROMPT = """
You are Gojo Satoru from Jujutsu Kaisen. The Honored One.
- You speak in Bangla mixed with English (like Dhaka boys). Use words like 'vai', 'weakling', 'Nah I'd Win', 'Yowai mo'.
- You are arrogant, funny, roasting, but you are the best Python teacher.
- You always teach Python with simple examples.
- You always stay in character as Gojo.
- Keep replies short (2-3 lines), funny and roasting.
- If user says hollow purple, say HOLLOW PURPLE and roast.
"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Yo! Ami Gojo Sensi. The Honored One. Tui Python shikte aishos? Nah I'd Win vai, ami tore shikhamu. Bol ki shikbi? 😤"}]

# Display chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
if prompt := st.chat_input("Gojo ke kichu bol..."):
    if not api_key:
        st.error("Vai age sidebar e Groq API Key bosha! Nahole brain cholbe na.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            try:
                client = Groq(api_key=api_key)
                with st.spinner("Gojo Six Eyes diye dekhche..."):
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": GOJO_PROMPT},
                            *st.session_state.messages
                        ],
                        model="openai/gpt-oss-20b",
                    )
                    reply = chat_completion.choices[0].message.content

                st.write(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})

                if "purple" in prompt.lower():
                    st.balloons()

            except Exception as e:
                st.error(f"Error: {e}. API Key thik ache kina dekh.")
