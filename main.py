import streamlit as st
from groq import Groq
import asyncio
import edge_tts
import os

st.set_page_config(page_title="Gojo Sensi REAL AI", page_icon="🟣", layout="centered")

with st.sidebar:
    st.title("🟣 Gojo Control")
    if "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]
        st.success("Six Eyes Are watching you ✅")
    else:
        api_key = st.text_input("Enter Groq API Key", type="password")
    if st.button("Clear Chat / Domain Expansion"):
        st.session_state.messages = []
        st.rerun()

GOJO_PROMPT = """You are Gojo Satoru, the strongest. Cocky, playful. Call user 'my weak student'. Use 'Nah I'd Win', 'I alone am the honored one'. Mix Bangla+English. Short, funny."""

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("Gojo Sensi - REAL AI 🟣")
st.caption("Powered by openai/gpt-oss-20b + Natural Voice")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

async def make_voice(text, voice="en-US-GuyNeural"):
    # Gojo er jonno cool guy voice
    communicate = edge_tts.Communicate(text, voice, rate="+10%", pitch="+5Hz")
    await communicate.save("gojo_voice.mp3")

if prompt := st.chat_input("Ask your Sensei..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        client = Groq(api_key=api_key)
        chat_completion = client.chat.completions.create(
            messages=[{"role": "system", "content": GOJO_PROMPT}, *st.session_state.messages],
            model="openai/gpt-oss-20b",
        )
        full_response = chat_completion.choices[0].message.content
        st.markdown(full_response)

        # NATURAL VOICE
        try:
            asyncio.run(make_voice(full_response[:500]))
            st.audio("gojo_voice.mp3", format="audio/mp3")
        except Exception as e:
            st.write(f"voice error: {e}")

    st.session_state.messages.append({"role": "assistant", "content": full_response})
