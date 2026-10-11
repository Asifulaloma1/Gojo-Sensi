import streamlit as st
from groq import Groq
import requests, asyncio
import edge_tts

st.set_page_config(page_title="Gojo Sensi REAL AI", page_icon="🟣")

GOJO_PROMPT = "You are Gojo Satoru. Cocky, strongest, serious like video ZHVuXN4DHkE. Say Nah I'd Win. Mix Bangla+English. Short."

FISH_API_KEY = st.secrets.get("FISH_API_KEY", "")
MODEL_ID = st.secrets.get("FISH_MODEL_ID", "91d1420efb1846afb51ffd1f64c4d538")

def get_gojo_voice_fish(text):
    try:
        url = "https://api.fish.audio/v1/tts"
        headers = {"Authorization": f"Bearer {FISH_API_KEY}", "Content-Type": "application/json"}
        data = {"text": text, "reference_id": MODEL_ID, "format": "mp3"}
        r = requests.post(url, json=data, headers=headers, timeout=15)
        if r.status_code == 200:
            return r.content, True
    except: pass
    return None, False

async def get_gojo_voice_edge(text):
    # Deep Gojo voice - FREE unlimited
    communicate = edge_tts.Communicate(text, "en-US-ChristopherNeural", rate="-8%", pitch="-15Hz")
    await communicate.save("gojo.mp3")
    return "gojo.mp3"

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🟣 Gojo Sensi - REAL VOICE")

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

        # Try Fish first, fail hole Edge
        audio, is_fish = get_gojo_voice_fish(ans[:250])
        if is_fish and audio:
            st.audio(audio, format="audio/mp3")
            st.caption("🔥 Real Gojo Clone (Fish)")
        else:
            awaitable = get_gojo_voice_edge(ans[:300])
            asyncio.run(awaitable)
            st.audio("gojo.mp3")
            st.caption("🟣 Gojo Deep Voice (Free - Unlimited)")
            st.info("Fish API credit sesh, tai free voice bajche. 100% free unlimited!")

    st.session_state.messages.append({"role": "assistant", "content": ans})
