import streamlit as st
from groq import Groq
import base64

st.set_page_config(page_title="A1X - Gojo Sensi", page_icon="🪽", layout="centered")

# --- A1X BACKGROUND WITH YOUR IMAGE ---
def get_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

try:
    bg_b64 = get_base64("bg.jpg") # tor upload kora image
    bg_css = f'data:image/jpg;base64,{bg_b64}'
except:
    bg_css = "" # fallback

st.markdown(f"""
<style>
.stApp {{
    background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.75)), url("{bg_css}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}
.stApp > header {{ background: transparent; }}
[data-testid="stChatMessage"] {{
    background: rgba(10, 20, 40, 0.75)!important;
    border: 1px solid #60a5fa;
    backdrop-filter: blur(12px);
    border-radius: 15px;
    box-shadow: 0 0 20px rgba(96,165,250,0.3);
}}
h1 {{ color: #dbeafe!important; text-shadow: 0 0 25px #3b82f6; text-align: center; letter-spacing: 2px; }}
.stChatInput {{ background: rgba(10,20,40,0.85)!important; border: 1px solid #3b82f6!important; border-radius: 25px!important; }}
</style>
""", unsafe_allow_html=True)

GOJO_PROMPT = "You are Gojo Satoru from JJK + A1X brand guardian. Strongest, cool, angelic like the logo. Say Nah I'd Win. Mix Bangla+English. Short 2 lines."

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🪽 A1X • Gojo Sensi")
st.markdown("<p style='text-align:center;color:#93c5fd;'>Angelic • Strongest • Limitless</p>", unsafe_allow_html=True)

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("A1X Gojo ke kichu jiggesh kor..."):
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
