import os, base64
from flask import Flask, request, render_template_string
from groq import Groq
from twilio.rest import Client as TwilioClient
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# API Clients
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
twilio_client = TwilioClient(os.getenv("TWILIO_SID"), os.getenv("TWILIO_TOKEN")) if os.getenv("TWILIO_SID") else None

GOJO_PROMPT = "You are Gojo Satoru. The strongest sorcerer. Cocky, funny, savage. Mix Bangla+English, short 4-5 lines max. Say Huh sometimes. Use emojis."

def get_bg():
    for name in ["bg.jpg.png", "bg.jpg", "bg.png"]:
        if os.path.exists(name):
            with open(name, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
                return f"data:image/png;base64,{b64}"
    return None

BG = get_bg()

def get_gojo_reply(user_msg):
    res = groq_client.chat.completions.create(
        messages=[{"role":"system","content":GOJO_PROMPT},{"role":"user","content":user_msg}],
        model="openai/gpt-oss-20b"
    )
    return res.choices[0].message.content

HTML = """
<!DOCTYPE html>
<html>
<head><title>Gojo Sensi</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{
 background: url('{{bg}}') no-repeat center center fixed; background-size: cover;
 color: white; font-family: sans-serif; margin:0;
}
.overlay{ background: rgba(0,0,0,0.6); min-height:100vh; padding:20px; }
.box{ max-width:700px; margin:auto; background: rgba(0,0,0,0.7); padding:20px; border-radius:20px; border:1px solid #60a5fa; backdrop-filter: blur(10px);}
h1{ text-align:center; color:#e0f2fe; text-shadow:0 0 20px #3b82f6; }
input{ width:80%; padding:12px; border-radius:10px; border:none; }
button{ padding:12px 20px; border-radius:10px; background:#3b82f6; color:white; border:none; }
.msg{ margin:10px 0; padding:10px; border-radius:10px; }
.user{ background:#1e40af; text-align:right; }
.assistant{ background:#111827; border:1px solid #3b82f6; }
</style>
</head>
<body><div class="overlay"><div class="box">
<h1>Gojo Sensi - Limitless</h1>
<div id="chat"></div>
<form onsubmit="sendMsg(event)">
<input id="inp" placeholder="Gojo ke jiggesh koro..." autocomplete="off"><button>Send</button>
</form>
<p style="text-align:center; font-size:12px;">WhatsApp Bot: {{wa_status}}</p>
</div></div>
<script>
async function sendMsg(e){
 e.preventDefault();
 let txt=document.getElementById('inp').value;
 if(!txt) return;
 document.getElementById('chat').innerHTML+=`<div class='msg user'>${txt}</div>`;
 document.getElementById('inp').value='';
 let r=await fetch('/chat', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({msg:txt})});
 let d=await r.json();
 document.getElementById('chat').innerHTML+=`<div class='msg assistant'>${d.reply}</div>`;
}
</script>
</body></html>
"""

@app.route("/")
def home():
    wa = "Active ✅" if twilio_client else "Not set"
    return render_template_string(HTML, bg=BG, wa_status=wa)

@app.route("/chat", methods=['POST'])
def chat():
    data = request.get_json()
    reply = get_gojo_reply(data.get('msg',''))
    return {"reply": reply}

@app.route("/whatsapp", methods=['POST'])
def whatsapp():
    incoming = request.values.get('Body', '')
    reply = get_gojo_reply(incoming)
    resp = MessagingResponse()
    resp.message(reply)
    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
