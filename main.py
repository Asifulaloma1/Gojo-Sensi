import streamlit as st
from groq import Groq
import requests

st.set_page_config(page_title="Gojo Sensi REAL AI", page_icon="🟣")

GOJO_PROMPT = "You are Gojo Satoru from JJK. Cocky, strongest, serious like video ZHVuXN4DHkE. Say Nah I'd Win. Mix Bangla+English. Short 2 lines max."

FISH_API_KEY = st.secrets["FISH_API_KEY"]
MODEL_ID = st.secrets["FISH_MODEL_ID"]

def get_gojo_voice(text):
    url = "https://api.fish.audio/v1/tts"
    headers = {
        "Authorization": f"Bearer {FISH_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "reference_id": MODEL_ID,
        "format": "mp3",
        "mp3_bitrate": 128
    }
    r = requests.post(url, json=data, headers=headers)
    if r.status_code == 200:
        return r.content
    else:
        st.error(f"Fish Error: {r.text}")
        return None

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🟣 Gojo Sensi - REAL VOICE")
st.caption("Satoru Gojo 46K • Fish Audio S2.1 Pro")

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Omae wa mou... ask something"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        res = client.chat.completions.create(
            messages=[{"role":"system","content":GOJO_PROMPT}, *st.session_state.messages],
            model="openai/gpt-oss-20b"
        )
        ans = res.choices[0].message.content
        st.markdown(ans)

        # REAL GOJO VOICE
        audio_bytes = get_gojo_voice(ans[:250])
        if audio_bytes:
            st.audio(audio_bytes, format="audio/mp3")
            st.success("Gojo is speaking! 🟣")

    st.session_state.messages.append({"role": "assistant", "content": ans})
