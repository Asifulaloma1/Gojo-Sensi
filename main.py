import os
from flask import Flask, request, jsonify, send_from_directory
from groq import Groq
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
SYSTEM_PROMPT = "You are Gojo Satoru, strongest sorcerer. Cocky, playful, wise."

@app.route("/gojo.png")
def serve_gojo():
    return send_from_directory(".", "gojo.png")

@app.route("/")
def home():
    GOJO = "/gojo.png"
    return f"""
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>DOMAIN CHAT - Gojo</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}body{{background:#08061a;color:#e0e0ff;font-family:sans-serif;min-height:100vh}}
.header{{margin:12px 20px;display:flex;justify-content:space-between;align-items:center;background:rgba(15,10,35,0.9);border:1px solid #6d28d9;border-radius:16px;padding:14px 20px}}
.main{{display:grid;grid-template-columns:220px 1fr 340px;gap:16px;margin:16px 20px;height:calc(100vh - 90px)}}
.sidebar,.chat-panel{{background:rgba(12,8,30,0.92);border:1px solid #6d28d9;border-radius:16px;padding:14px;display:flex;flex-direction:column}}
#chat{{flex:1;overflow-y:auto;padding:10px;display:flex;flex-direction:column;gap:14px}}
.msg{{display:flex;gap:10px;max-width:85%}}.msg.user{{align-self:flex-end}}
.avatar{{width:36px;height:36px;border-radius:50%;overflow:hidden;border:1px solid #6d28d9}}.avatar img{{width:100%;height:100%;object-fit:cover}}
.bubble{{padding:12px 14px;border-radius:14px;background:rgba(255,255,255,0.08)}}.msg.user.bubble{{background:#6d28d9;color:white}}
.input-wrap{{display:flex;background:rgba(0,0,0,0.6);border:1px solid #6d28d9;border-radius:22px;padding:6px 12px;margin-top:10px}}
.input-wrap input{{flex:1;background:transparent;border:none;color:white;outline:none;padding:10px}}
.send{{width:40px;height:40px;background:linear-gradient(135deg,#6d28d9,#3b82f6);border-radius:50%;border:none;color:white;cursor:pointer}}
.gojo-art{{border-radius:16px;overflow:hidden;border:1px solid #6d28d9;background:radial-gradient(ellipse at center, rgba(109,40,217,0.4), #0a0820);display:flex;align-items:end;justify-content:center}}
.gojo-art img{{width:100%;height:100%;object-fit:cover;object-position:top center}}
</style></head><body>
<div class="header"><div style="display:flex;gap:14px;align-items:center"><div style="width:48px;height:48px;border-radius:50%;background:#000;border:1px solid #6d28d9;display:grid;place-items:center">∞</div><div><div style="font-weight:700;font-size:20px">DOMAIN CHAT</div><div style="font-size:11px;opacity:0.6">Gojo Satoru</div></div></div><img src="{GOJO}" style="width:42px;height:42px;border-radius:10px;object-fit:cover"></div>
<div class="main">
<div class="sidebar"><div style="font-weight:600;font-size:12px">+ CHANNELS</div><div style="margin-top:10px;padding:9px;border-radius:8px;background:rgba(109,40,217,0.35);border:1px solid #6d28d9"># general</div></div>
<div class="chat-panel"><div style="font-weight:600;padding-bottom:12px;border-bottom:1px solid #6d28d9">Chat with Gojo Satoru • Infinite Void Active</div><div id="chat"><div class="msg"><div class="avatar"><img src="{GOJO}"></div><div class="bubble">Welcome to my domain. I see every cursed energy with Six Eyes ~ ✨</div></div></div><div class="input-wrap"><input id="msg" placeholder="Ask Gojo..." onkeypress="if(event.key==='Enter')send()"><button class="send" onclick="send()">➤</button></div></div>
<div class="gojo-art"><img src="{GOJO}"></div>
</div>
<script>
async function send(){{let i=document.getElementById('msg');if(!i.value.trim())return;let c=document.getElementById('chat');let txt=i.value;c.innerHTML+=`<div class="msg user"><div class="bubble">${{txt}}</div></div>`;i.value='';c.scrollTop=c.scrollHeight;let r=await fetch('/chat',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{message:txt}})}});let d=await r.json();c.innerHTML+=`<div class="msg"><div class="avatar"><img src="{GOJO}"></div><div class="bubble">${{d.reply}}</div></div>`;c.scrollTop=c.scrollHeight;}}
</script></body></html>
"""

@app.route("/chat", methods=["POST"])
def chat():
    try:
        msg=request.json.get("message","")
        comp=client.chat.completions.create(model="openai/gpt-oss-20b", messages=[{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":msg}])
        return jsonify({"reply": comp.choices[0].message.content})
    except Exception as e: return jsonify({"reply": f"Error: {e}"})

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    inc=request.values.get("Body","")
    comp=client.chat.completions.create(model="openai/gpt-oss-20b", messages=[{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":inc}])
    r=MessagingResponse(); r.message(comp.choices[0].message.content); return str(r)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
