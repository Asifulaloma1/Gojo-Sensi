import streamlit as st
from groq import Groq
import asyncio
import edge_tts

st.set_page_config(page_title="Gojo Sensi REAL AI", page_icon="🟣")

with st.sidebar:
    st.title("🟣 Gojo Control")
    api_key = st.secrets["GROQ_API_KEY"]

GOJO_PROMPT = "You are Gojo Satoru, strongest. Cocky, serious, playful. Call user 'my weak student'. Short reply."

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("Gojo Sensi - REAL Voice 🟣")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

async def gojo_voice(text):
    # Eita oi YouTube er Gojo serious voice er moto
    communicate = edge_tts.Communicate(
        text,
        "en-US-ChristopherNeural", # Deep Gojo type
        rate="-10%",
        pitch="-15Hz"
    )
    await communicate.save("gojo.mp3")

if prompt := st.chat_input("Ask your Sensei..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        client = Groq(api_key=api_key)
        res = client.chat.completions.create(
            messages=[{"role": "system", "content": GOJO_PROMPT}, *st.session_state.messages],
            model="openai/gpt-oss-20b",
        )
        ans = res.choices[0].message.content
        st.markdown(ans)

        asyncio.run(gojo_voice(ans[:400]))
        st.audio("gojo.mp3")

    st.session_state.messages.append({"role": "assistant", "content": ans})
