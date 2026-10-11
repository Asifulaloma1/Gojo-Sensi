import streamlit as st
from groq import Groq
import time
from gtts import gTTS

st.set_page_config(page_title="Gojo Sensi REAL AI", page_icon="🟣", layout="centered")

# --- SIDEBAR ---
with st.sidebar:
    st.title("Gojo Control")

    if "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]
        st.success("Six Eyes Are watching you ✅")
    else:
        api_key = st.text_input("Enter Groq API Key", type="password")

    if st.button("Clear Chat / Domain Expansion"):
        st.session_state.messages = []
        st.rerun()

# --- GOJO PROMPT ---
GOJO_PROMPT = """You are Gojo Satoru, the strongest jujutsu sorcerer.
You are cocky, playful, funny. You call user 'my weak student'.
You use phrases like 'Nah I'd Win', 'Throughout Heaven and Earth, I alone am the honored one'.
You roast user but in a friendly sensei way. Mix Bangla and English like a cool Dhaka guy.
Keep answers short, funny, powerful."""

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("Gojo Sensi - REAL AI 🟣")
st.caption("Powered by openai/gpt-oss-20b on Groq - The Strongest")

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ask your Sensei..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        client = Groq(api_key=api_key)
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": GOJO_PROMPT},
                *st.session_state.messages
            ],
            model="openai/gpt-oss-20b",
        )
        full_response = chat_completion.choices[0].message.content
        st.markdown(full_response)

        # --- VOICE ---
        try:
            tts = gTTS(text=full_response[:400], lang='en', tld='com.au')
            tts.save("gojo_voice.mp3")
            with open("gojo_voice.mp3", "rb") as f:
                st.audio(f.read(), format="audio/mp3")
        except:
            pass

    st.session_state.messages.append({"role": "assistant", "content": full_response})
