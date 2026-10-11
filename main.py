import streamlit as st
from groq import Groq
import base64, os

st.set_page_config(page_title="Gojo Saturo", layout="centered")

def get_bg():
    # tor file er naam bg.jpg.png tai oita first e check korbe
    for name in ["bg.jpg.png", "bg.jpg", "bg.png", "wa_image_3925620385820380071"]:
        if os.path.exists(name):
            with open(name, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
                # png hole png, jpg hole jpg
                ext = "png" if "png" in name else "jpg"
                return f"data:image/{ext};base64,{b64}"
    return None

bg_url = get_bg()

if bg_url:
    st.markdown(f"""
    <style>
   .stApp {{
        background-image: url("{bg_url}")!important;
        background-size: cover!important;
        background-position: center center!important;
        background-attachment: fixed!important;
        background-repeat: no-repeat!important;
    }}
    /* halka dark overlay jate text pora jai, kintu pic dekha jai */
   .stApp::before {{
        content: "";
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(0,0,0,0.45);
        z-index: -1;
    }}
   .stApp > header {{ background: transparent!important; }}
    [data-testid="stChatMessage"] {{
        background: rgba(0,0,0,0.65)!important;
        border: 1px solid #60a5fa;
        backdrop-filter: blur(10px);
        border-radius: 16px;
    }}
    h1 {{
        color: #e0f2fe!important;
        text-shadow: 0 0 20px #3b82f6, 0 0 40px #60a5fa;
        text-align: center;
    }}
    </style>
    """, unsafe_allow_html=True)
else:
    st.error("bg file pai nai! GitHub e bg.jpg.png ase kina check kor")

GOJO_PROMPT = "You are Gojo Satoru. Say Huh. Mix Bangla+English, short 4 lines."

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("Gojo Sensi")
st.caption("Powerfull • Strongest • Limitless")

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Gojo ke jiggesh koro..."):
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
