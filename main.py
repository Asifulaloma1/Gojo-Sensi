import os
from flask import Flask, request, jsonify
from groq import Groq
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = "You are Gojo Satoru, the strongest sorcerer. Cocky, playful, wise. Talk about Six Eyes, Limitless, Infinity, Domain Expansion: Infinite Void. Use ~ and ✨. Keep replies short, cool, powerful. Explain jujutsu if asked."

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DOMAIN CHAT - Gojo Satoru</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=JetBrains+Mono&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#020210;color:#e0e0ff;font-family:'Space Grotesk',sans-serif;overflow-x:hidden;min-height:100vh;position:relative}
body::before{content:'';position:fixed;inset:0;background:radial-gradient(ellipse at 30% 10%, rgba(109,40,217,0.4) 0%, transparent 50%), radial-gradient(ellipse at 80% 90%, rgba(59,130,246,0.3) 0%, transparent 50%), url('https://images.unsplash.com/photo-1534796636912-3b95b3ab5986?w=1920'); background-size:cover; opacity:0.15; z-index:-2}
.infinity-bg{position:fixed;inset:0;z-index:-1;overflow:hidden}
.inf{position:absolute;font-size:400px;opacity:0.05;color:#6d28d9;filter:blur(2px)}
.header{margin:12px 20px;display:flex;justify-content:space-between;align-items:center;background:rgba(15,10,35,0.8);backdrop-filter:blur(20px);border:1px solid rgba(109,40,217,0.5);border-radius:16px;padding:14px 20px}
.logo{display:flex;align-items:center;gap:14px}
.logo-icon{width:52px;height:52px;background:radial-gradient(circle, #1a0a40, #000);border:1px solid #6d28d9;border-radius:50%;display:grid;place-items:center;box-shadow:0 0 20px #6d28d9}
.nav{display:flex;gap:20px;align-items:center}
.nav span{font-size:13px;opacity:0.8;display:flex;align-items:center;gap:6px}
.user-badge{display:flex;align-items:center;gap:10px}
.main{display:grid;grid-template-columns:220px 1fr 320px;gap:16px;margin:16px 20px}
.sidebar,.chat-panel{background:rgba(12,8,30,0.85);backdrop-filter:blur(20px);border:1px solid rgba(109,40,217,0.4);border-radius:16px;padding:14px}
.sidebar h4{font-size:12px;letter-spacing:1px;opacity:0.5;margin:18px 0 10px}
.channel{padding:8px 10px;border-radius:8px;font-size:13px;margin:4px 0;cursor:pointer;display:flex;gap:8px;align-items:center;opacity:0.7}
.channel.active{background:rgba(109,40,217,0.3);border:1px solid #6d28d9;opacity:1}
.fav{border:1px solid #a78bfa;background:rgba(109,40,217,0.2);padding:10px;border-radius:10px;margin-top:10px;display:flex;gap:8px;font-size:13px}
.core{margin-top:16px;background:rgba(0,0,0,0.4);border:1px solid rgba(109,40,217,0.3);border-radius:12px;padding:12px;text-align:center}
.core.inf-icon{font-size:40px;color:#60a5fa}
.bar{height:4px;background:linear-gradient(90deg,#6d28d9,#60a5fa);border-radius:4px;margin-top:8px;width:94%}
.chat-header{padding:12px;border-bottom:1px solid rgba(109,40,217,0.3);display:flex;gap:12px;align-items:center}
.status{font-size:11px;opacity:0.6;font-family:'JetBrains Mono'}
.domain-banner{background:rgba(109,40,217,0.15);border:1px solid rgba(109,40,217,0.4);border-radius:20px;padding:8px 14px;font-size:12px;text-align:center;margin:12px}
#chat{height:52vh;overflow-y:auto;padding:10px;display:flex;flex-direction:column;gap:14px}
.msg{display:flex;gap:10px;max-width:85%}
.msg.gojo{align-self:flex-start}.msg.user{align-self:flex-end;flex-direction:row-reverse}
.avatar{width:32px;height:32px;border-radius:50%;background:#1a1040;flex-shrink:0;overflow:hidden}
.avatar img{width:100%;height:100%;object-fit:cover}
.bubble{padding:12px 14px;border-radius:14px;font-size:13.5px;line-height:1.5}
.gojo.bubble{background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.1)}
.user.bubble{background:#6d28d9;color:white;border-radius:14px 14px 0 14px}
.time{font-size:10px;opacity:0.5;margin-top:4px}
.input-wrap{display:flex;align-items:center;background:rgba(0,0,0,0.5);border:1px solid rgba(109,40,217,0.4);border-radius:20px;padding:6px 12px;margin-top:10px}
.input-wrap input{flex:1;background:transparent;border:none;color:white;outline:none;padding:10px;font-size:13px}
.send{width:40px;height:40px;background:linear-gradient(135deg,#6d28d9,#3b82f6);border-radius:50%;border:none;display:grid;place-items:center;cursor:pointer}
.quick{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-top:12px}
.q{font-size:11px;padding:10px;border-radius:10px;background:rgba(109,40,217,0.15);border:1px solid rgba(109,40,217,0.3);cursor:pointer}
.gojo-art{position:relative;border-radius:16px;overflow:hidden;height:100%;min-height:600px;background:radial-gradient(ellipse at center, rgba(109,40,217,0.3), transparent), url('https://i.imgur.com/8Km9tLL.jpg'); background-size:cover; background-position:top; border:1px solid rgba(109,40,217,0.4)}
.gojo-art::after{content:'INFINITY\\A無下開';white-space:pre;position:absolute;bottom:20px;right:20px;font-size:28px;font-weight:700;letter-spacing:3px;opacity:0.9;text-shadow:0 0 20px #6d28d9}
.inf-r{position:absolute;right:-20px;top:40%;font-size:180px;opacity:0.6;color:#8b5cf6;transform:rotate(-10deg);text-shadow:0 0 30px #6d28d9}
@media(max-width:1000px){.main{grid-template-columns:1fr}.gojo-art{display:none}.sidebar{display:none}}
</style>
</head>
<body>
<div class="header">
<div class="logo"><div class="logo-icon">∞</div><div><div style="font-weight:700;letter-spacing:2px;font-size:22px">DOMAIN CHAT</div><div style="font-size:11px;opacity:0.6">Jujutsu Kaisen • Gojo Satoru</div></div></div>
<div class="nav"><span>∞ Limitless</span><span>◍ Domain Expansion</span><span>✦ Techniques</span></div>
<div class="user-badge"><div style="text-align:right"><div style="font-size:13px">Gojo Satoru</div><div style="font-size:11px;color:#22c55e">• Online ●</div></div><img src="https://i.imgur.com/8Km9tLL.jpg" style="width:40px;height:40px;border-radius:10px;object-fit:cover"></div>
</div>
<div class="main">
<div class="sidebar">
<div style="font-weight:600;font-size:12px;letter-spacing:1px">+ CHANNELS</div>
<div class="channel active"># # general</div>
<div class="channel"># # techniques</div>
<div class="channel">👁 domain-theory</div>
<div class="channel">💀 cursed-spirits</div>
<h4>FAVORITES</h4>
<div class="fav">☆ Gojo • Six Eyes Guide</div>
<div class="core"><div style="font-size:10px;opacity:0.6">LIMITLESS CORE</div><div class="inf-icon">∞</div><div style="font-size:12px">94%</div><div class="bar"></div><div style="font-size:9px;margin-top:6px;opacity:0.5">Infinity: Active • Neutral Space: 94%</div></div>
</div>
<div class="chat-panel">
<div class="chat-header"><div class="logo-icon" style="width:36px;height:36px">∞</div><div><div style="font-weight:600">Chat with Gojo Satoru</div><div class="status">AI Sorcerer • Active • Domain: Infinite Void • Latency: 0ms</div></div></div>
<div class="domain-banner">✦ Domain Expansion: Infinite Void is active — all messages slowed in infinite space for clarity. ✦</div>
<div id="chat">
<div class="msg gojo"><div class="avatar"><img src="https://i.imgur.com/8Km9tLL.jpg"></div><div><div class="bubble">Welcome to my domain. Bring your questions. I see every cursed energy flow with the Six Eyes — ask me about jujutsu, techniques, or how Limitless bends reality.<div class="time">Today 21:42 • Read</div></div></div></div>
</div>
<div class="input-wrap"><span>✨</span><input id="msg" placeholder="Ask Gojo about techniques, domains, Six Eyes, strategy..." onkeypress="if(event.key==='Enter')send()"><button class="send" onclick="send()">➤</button></div>
<div class="quick">
<div class="q" onclick="ask(this)">✦ Explain Red<br><span style="opacity:0.6">Cursed Technique Reversal</span></div>
<div class="q" onclick="ask(this)">✦ Explain Blue<br><span style="opacity:0.6">Cursed Technique Lapse</span></div>
<div class="q" onclick="ask(this)">∞ Hollow Purple:<br><span style="opacity:0.6">Explained</span></div>
</div>
</div>
<div class="gojo-art"><div class="inf-r">∞</div></div>
</div>
<script>
async function send(){
 let i=document.getElementById('msg'); if(!i.value.trim())return;
 let c=document.getElementById('chat'); let txt=i.value;
 c.innerHTML+=`<div class="msg user"><div class="avatar"><img src="https://i.pravatar.cc/100"></div><div class="bubble">${txt}<div class="time">Today 21:43</div></div></div>`;
 i.value=''; c.scrollTop=c.scrollHeight;
 let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:txt})});
 let d=await r.json();
 c.innerHTML+=`<div class="msg gojo"><div class="avatar"><img src="https://i.imgur.com/8Km9tLL.jpg"></div><div><div class="bubble">${d.reply}<div class="time">Now • Read</div></div></div></div>`;
 c.scrollTop=c.scrollHeight;
}
function ask(el){document.getElementById('msg').value=el.innerText; send();}
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
    try:
        inc=request.values.get("Body","")
        comp=client.chat.completions.create(model="openai/gpt-oss-20b", messages=[{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":inc}])
        from twilio.twiml.messaging_response import MessagingResponse
        r=MessagingResponse(); r.message(comp.choices[0].message.content); return str(r)
    except Exception as e:
        r=MessagingResponse(); r.message(f"Error: {e}"); return str(r)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
