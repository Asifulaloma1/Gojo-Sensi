import os
from flask import Flask, request, jsonify
from groq import Groq
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
SYSTEM_PROMPT = "You are Gojo Satoru, the strongest sorcerer. Cocky, playful, wise. Short cool replies."

# REAL GOJO IMAGE - stable link
GOJO_IMG = "https://static.wikia.nocookie.net/jujutsukaisen/images/5/56/Gojo_Satoru_%28Anime%29_2.png"

HTML_PAGE = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DOMAIN CHAT - Gojo Satoru</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#08061a;color:#e0e0ff;font-family:'Space Grotesk',sans-serif;min-height:100vh;overflow:hidden}}
body::before{{content:'';position:fixed;inset:0;background:radial-gradient(ellipse at 50% 0%, rgba(109,40,217,0.6), transparent 70%), url('https://images.unsplash.com/photo-1534796636912-3b95b3ab5986?w=1920');background-size:cover;opacity:0.2;z-index:-1}}
.header{{margin:12px 20px;display:flex;justify-content:space-between;align-items:center;background:rgba(15,10,35,0.9);backdrop-filter:blur(20px);border:1px solid rgba(109,40,217,0.5);border-radius:16px;padding:14px 20px}}
.main{{display:grid;grid-template-columns:220px 1fr 340px;gap:16px;margin:16px 20px;height:calc(100vh - 90px)}}
.sidebar,.chat-panel{{background:rgba(12,8,30,0.92);backdrop-filter:blur(20px);border:1px solid rgba(109,40,217,0.4);border-radius:16px;padding:14px;display:flex;flex-direction:column}}
.channel{{padding:9px 10px;border-radius:8px;font-size:13px;margin:4px 0;opacity:0.7}}.channel.active{{background:rgba(109,40,217,0.35);border:1px solid #6d28d9;opacity:1}}
#chat{{flex:1;overflow-y:auto;padding:10px;display:flex;flex-direction:column;gap:14px}}
.msg{{display:flex;gap:10px;max-width:85%}}.msg.user{{align-self:flex-end;flex-direction:row-reverse}}
.avatar{{width:36px;height:36px;border-radius:50%;overflow:hidden;flex-shrink:0;border:1px solid #6d28d9}}.avatar img{{width:100%;height:100%;object-fit:cover}}
.bubble{{padding:12px 14px;border-radius:14px;font-size:13.5px;line-height:1.5;background:rgba(255,255,255,0.08)}}.msg.user.bubble{{background:#6d28d9;color:white}}
.input-wrap{{display:flex;background:rgba(0,0,0,0.6);border:1px solid rgba(109,40,217,0.4);border-radius:22px;padding:6px 12px;margin-top:10px}}
.input-wrap input{{flex:1;background:transparent;border:none;color:white;outline:none;padding:10px}}
.send{{width:40px;height:40px;background:linear-gradient(135deg,#6d28d9,#3b82f6);border-radius:50%;border:none;cursor:pointer;color:white;font-size:16px}}
.gojo-art{{border-radius:16px;overflow:hidden;position:relative;border:1px solid rgba(109,40,217,0.4);background:radial-gradient(ellipse at center, rgba(109,40,217,0.4), rgba(2,2,16,1)), #0a0820; display:flex; align-items:end; justify-content:center}}
.gojo-art img{{height:95%;width:auto;object-fit:contain;filter:drop-shadow(0 0 30px #6d28d9)}}
.gojo-art::after{{content:'INFINITY 無下限';position:absolute;bottom:18px;left:20px;right:20px;font-size:22px;font-weight:700;letter-spacing:2px;text-shadow:0 0 20px #6d28d9;text-align:right}}
@media(max-width:1000px){{.main{{grid-template-columns:1fr}}.gojo-art{{display:none}}}}
</style>
</head>
<body>
<div class="header"><div style="display:flex;gap:14px;align-items:center"><div style="width:48px;height:48px;border-radius:50%;background:#000;border:1px solid #6d28d9;display:grid;place-items:center">∞</div><div><div style="font-weight:700;letter-spacing:2px;font-size:20px">DOMAIN CHAT</div><div style="font-size:11px;opacity:0.6">Jujutsu Kaisen • Gojo Satoru</div></div></div><img src="{GOJO_IMG}" style="width:42px;height:42px;border-radius:10px;object-fit:cover;object-position:top"></div>
<div class="main">
<div class="sidebar"><div style="font-weight:600;font-size:12px">+ CHANNELS</div><div class="channel active"># general</div><div class="channel"># techniques</div><div class="channel">👁 domain-theory</div></div>
<div class="chat-panel"><div style="font-weight:600;padding-bottom:12px;border-bottom:1px solid rgba(109,40,217,0.3)">Chat with Gojo Satoru • Infinite Void Active</div><div id="chat"><div class="msg"><div class="avatar"><img src="{GOJO_IMG}"></div><div class="bubble">Welcome to my domain. Bring your questions. I see every cursed energy flow with the Six Eyes ~ ✨</div></div></div><div class="input-wrap"><input id="msg" placeholder="Ask Gojo about techniques..." onkeypress="if(event.key==='Enter')send()"><button class="send" onclick="send()">➤</button></div></div>
<div class="gojo-art"><img src="{GOJO_IMG}"><div style="position:absolute;top:20px;right:20px;font-size:120px;opacity:0.15;color:#8b5cf6">∞</div></div>
</div>
<script>
async function send(){{let i=document.getElementById('msg');if(!i.value.trim())return;let c=document.getElementById('chat');let txt=i.value;c.innerHTML+=`<div class="msg user"><div class="bubble">${{txt}}</div></div>`;i.value='';c.scrollTop=c.scrollHeight;let r=await fetch('/chat',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{message:txt}})}});let d=await r.json();c.innerHTML+=`<div class="msg"><div class="avatar"><img src="{GOJO_IMG}"></div><div class="bubble">${{d.reply}}</div></div>`;c.scrollTop=c.scrollHeight;}}
</script>
</body>
</html>
"""

@app.route("/")
def home(): return HTML_PAGE

@app.route("/chat", methods=["POST"])
def chat():
    try:
        msg=request.json.get("message","")
        comp=client.chat.completions.create(model="openai/gpt-oss-20b", messages=[{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":msg}])
        return jsonify({"reply": comp.choices[0].message.content})
    except Exception as e: return jsonify({"reply": f"Six Eyes glitched: {e}"})

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    inc=request.values.get("Body","")
    comp=client.chat.completions.create(model="openai/gpt-oss-20b", messages=[{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":inc}])
    r=MessagingResponse(); r.message(comp.choices[0].message.content); return str(r)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
