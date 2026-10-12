import os
from flask import Flask, request, jsonify, send_from_directory
from groq import Groq
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = "You are Gojo Satoru, the strongest sorcerer. Cocky, playful, wise. Talk about Six Eyes, Limitless, Infinity, Domain Expansion: Infinite Void. Use ~ and ✨. Keep replies short, cool, powerful."

# --- Image Serve Routes ---
@app.route("/gojo.jpg.jpeg")
def serve_gojo():
    return send_from_directory(".", "gojo.jpg.jpeg")

@app.route("/bg.jpg.png")
def serve_bg():
    return send_from_directory(".", "bg.jpg.png")

@app.route("/gojo.jpg")
def serve_gojo2():
    # jodi rename koro taholeo kaj korbe
    try:
        return send_from_directory(".", "gojo.jpg")
    except:
        return send_from_directory(".", "gojo.jpg.jpeg")

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DOMAIN CHAT - Gojo Satoru</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=JetBrains+Mono&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#020210 url('/bg.jpg.png') center/cover no-repeat fixed;color:#e0e0ff;font-family:'Space Grotesk',sans-serif;min-height:100vh;position:relative}
body::before{content:'';position:fixed;inset:0;background:radial-gradient(ellipse at 30% 10%, rgba(109,40,217,0.5) 0%, transparent 60%), rgba(2,2,16,0.7);z-index:-1}
.header{margin:12px 20px;display:flex;justify-content:space-between;align-items:center;background:rgba(15,10,35,0.85);backdrop-filter:blur(20px);border:1px solid rgba(109,40,217,0.5);border-radius:16px;padding:14px 20px}
.logo{display:flex;align-items:center;gap:14px}
.logo-icon{width:52px;height:52px;background:radial-gradient(circle, #1a0a40, #000);border:1px solid #6d28d9;border-radius:50%;display:grid;place-items:center;box-shadow:0 0 20px #6d28d9}
.main{display:grid;grid-template-columns:220px 1fr 340px;gap:16px;margin:16px 20px}
.sidebar,.chat-panel{background:rgba(12,8,30,0.9);backdrop-filter:blur(20px);border:1px solid rgba(109,40,217,0.4);border-radius:16px;padding:14px}
.channel{padding:8px 10px;border-radius:8px;font-size:13px;margin:4px 0;cursor:pointer;display:flex;gap:8px;opacity:0.7}
.channel.active{background:rgba(109,40,217,0.3);border:1px solid #6d28d9;opacity:1}
#chat{height:48vh;overflow-y:auto;padding:10px;display:flex;flex-direction:column;gap:14px}
.msg{display:flex;gap:10px;max-width:85%}
.msg.user{align-self:flex-end;flex-direction:row-reverse}
.bubble{padding:12px 14px;border-radius:14px;font-size:13.5px;line-height:1.5}
.msg.gojo.bubble{background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.1)}
.msg.user.bubble{background:#6d28d9;color:white}
.input-wrap{display:flex;background:rgba(0,0,0,0.6);border:1px solid rgba(109,40,217,0.4);border-radius:20px;padding:6px 12px;margin-top:10px}
.input-wrap input{flex:1;background:transparent;border:none;color:white;outline:none;padding:10px}
.send{width:40px;height:40px;background:linear-gradient(135deg,#6d28d9,#3b82f6);border-radius:50%;border:none;cursor:pointer;color:white}
.gojo-art{border-radius:16px;overflow:hidden;min-height:600px;background:url('/gojo.jpg.jpeg') top/cover no-repeat; border:1px solid rgba(109,40,217,0.4); position:relative}
.gojo-art::after{content:'INFINITY\\A無下限';white-space:pre;position:absolute;bottom:20px;right:20px;font-size:26px;font-weight:700;opacity:0.9;text-shadow:0 0 20px #6d28d9}
@media(max-width:1000px){.main{grid-template-columns:1fr}.gojo-art{display:none}}
</style>
</head>
<body>
<div class="header">
<div class="logo"><div class="logo-icon">∞</div><div><div style="font-weight:700;letter-spacing:2px;font-size:22px">DOMAIN CHAT</div><div style="font-size:11px;opacity:0.6">Jujutsu Kaisen • Gojo Satoru</div></div></div>
<div style="display:flex;gap:12px;align-items:center"><img src="/gojo.jpg.jpeg" style="width:40px;height:40px;border-radius:10px;object-fit:cover"></div>
</div>
<div class="main">
<div class="sidebar">
<div style="font-weight:600;font-size:12px">+ CHANNELS</div>
<div class="channel active"># general</div>
<div class="channel"># techniques</div>
<div class="channel">👁 domain-theory</div>
</div>
<div class="chat-panel">
<div style="font-weight:600;padding-bottom:10px;border-bottom:1px solid rgba(109,40,217,0.3)">Chat with Gojo Satoru • Infinite Void Active</div>
<div id="chat"><div class="msg gojo"><img src="/gojo.jpg.jpeg" style="width:32px;height:32px;border-radius:50%"><div class="bubble">Welcome to my domain. Bring your questions. I see every cursed energy flow with the Six Eyes ~</div></div></div>
<div class="input-wrap"><input id="msg" placeholder="Ask Gojo about techniques..." onkeypress="if(event.key==='Enter')send()"><button class="send" onclick="send()">➤</button></div>
</div>
<div class="gojo-art"></div>
</div>
<script>
async function send(){
 let i=document.getElementById('msg'); if(!i.value.trim())return;
 let c=document.getElementById('chat'); let txt=i.value;
 c.innerHTML+=`<div class="msg user"><div class="bubble">${txt}</div></div>`; i.value=''; c.scrollTop=c.scrollHeight;
 let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:txt})});
 let d=await r.json();
 c.innerHTML+=`<div class="msg gojo"><img src="/gojo.jpg.jpeg" style="width:32px;height:32px;border-radius:50%"><div class="bubble">${d.reply}</div></div>`;
 c.scrollTop=c.scrollHeight;
}
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return HTML_PAGE

@app.route("/chat", methods=["POST"])
def chat():
    try:
        msg = request.json.get("message","")
        comp = client.chat.completions.create(model="openai/gpt-oss-20b", messages=[{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":msg}])
        return jsonify({"reply": comp.choices[0].message.content})
    except Exception as e:
        return jsonify({"reply": f"Error: {e}"})

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    try:
        inc = request.values.get("Body","")
        comp = client.chat.completions.create(model="openai/gpt-oss-20b", messages=[{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":inc}])
        r = MessagingResponse(); r.message(comp.choices[0].message.content); return str(r)
    except Exception as e:
        r = MessagingResponse(); r.message(f"Error: {e}"); return str(r)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
