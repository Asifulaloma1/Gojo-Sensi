import streamlit as st
from groq import Groq
import base64

st.set_page_config(page_title="Gojo Sensi", page_icon="🟣", layout="centered")

# --- GOJO BACKGROUND CSS ---
def add_bg():
    st.markdown("""
    <style>
   .stApp {
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.85)), url("https://i.pinimg.com/originals/8f/3b/6a/8f3b6a8b8c5d6b8b8c5d6b8b8c5d6b8b.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
   .stApp > header { background: transparent; }
    [data-testid="stChatMessage"] {
        background: rgba(20, 20, 30, 0.8)!important;
        border: 1px solid #7c3aed;
        backdrop-filter: blur(10px);
        border-radius: 15px;
    }
    h1 { color: #a78bfa!important; text-shadow: 0 0 20px #7c3aed; text-align: center; }
   .stChatInput { background: rgba(20,20,30,0.9)!important; border-radius: 20px!important; }
    </style>
    """, unsafe_allow_html=True)

add_bg()

GOJO_PROMPT = """
You are Gojo Satoru from Jujutsu Kaisen.
The STRONGEST. Cocky, funny, serious when needed.
Say "HUH !" sometimes.
Mix Bangla + English like: "Ki obostha ?, bro"
Short replies, max 4 lines.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🟣 Gojo Sensi")
st.markdown("<p style='text-align:center;color:#c4b5fd;'>The Strongest Sorcerer - Nah, I'd Win</p>", unsafe_allow_html=True)

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Gojo ke kichu jiggesh kor..."):
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

    st.session_state.messages.append({"role": "assistant", "content": ans})
