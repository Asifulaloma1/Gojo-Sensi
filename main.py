import os
from flask import Flask, request, render_template_string, jsonify
from groq import Groq
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are Gojo Satoru. Strongest sorcerer, playful, cocky, Limitless, Six Eyes, Infinity. Call user 'my student'. Mix Bangla+English. Stay in character."""

HTML = """
<!DOCTYPE html>
<html><head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Gojo Sensi • Limitless</title>
<script src="https://cdn.tailwindcss.com"></script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&display=swap');
body{font-family:'Space Grotesk',sans-serif;background:#060613;color:white;overflow:hidden}
.bg-main{background: radial-gradient(ellipse at 50% 0%, #1e1048 0%, #070714 60%, #04040f 100%);}
.glass{backdrop-filter:blur(20px);background:rgba(18,16,48,0.7);border:1px solid rgba(123,97,255,0.2)}
.glass-strong{backdrop-filter:blur(24px);background:rgba(18,16,48,0.85);border:1px solid rgba(123,97,255,0.3)}
.glow-text{ text-shadow:0 0 20px #7c5cff}
.infinity-bg{position:absolute;top:140px;left:50%;transform:translateX(-50%);width:900px;height:300px;opacity:0.6;pointer-events:none}
</style>
</head>
<body class="bg-main h-screen flex flex-col p-2 md:p-3">

<!-- HEADER -->
<div class="glass rounded-2xl px-5 py-3 flex items-center justify-between">
<div class="flex items-center gap-4">
<div class="w-12 h-12 rounded-full bg-black border border-violet-500/50 flex items-center justify-center shadow-[0_0_30px_#7c5cff]"> <span class="text-[20px]">☯️</span> </div>
<div><h1 class="text-xl md:text-2xl font-bold tracking-widest glow-text">DOMAIN CHAT</h1><p class="text-[11px] opacity-60">Jujutsu Kaisen • Gojo Satoru</p></div>
</div>
<div class="hidden md:flex items-center gap-6 text-xs"><span>∞ Limitless</span><span class="px-3 py-1 rounded-full bg-violet-500/20 border border-violet-500/30">◉ Domain Expansion</span><span>✦ Techniques</span></div>
<div class="flex items-center gap-3"><div class="text-right hidden md:block"><p class="text-sm font-semibold">Gojo Satoru</p><p class="text-[11px] text-green-400">• Online</p></div><img src="https://i.pinimg.com/736x/0c/78/72/0c7872c3e5b9f5a3a3b5e5a7b8c9d0e1f.jpg" onerror="this.src='https://i.imgur.com/8Km9tLL.png'" class="w-10 h-10 rounded-xl object-cover"></div>
</div>

<div class="flex-1 flex gap-3 mt-3 overflow-hidden relative">
<!-- BG Infinity -->
<div class="infinity-bg">
<svg viewBox="0 0 900 200" class="w-full h-full"><defs><linearGradient id="g" x1="0" x2="1"><stop offset="0%" stop-color="#7c3aed"/><stop offset="50%" stop-color="#3b82f6"/><stop offset="100%" stop-color="#7c3aed"/></linearGradient></defs>
<path d="M 100 100 C 100 20, 250 20, 300 100 S 500 180, 450 100 C 400 20, 550 20, 600 100 S 800 180, 800 100" stroke="url(#g)" stroke-width="3" fill="none" opacity="0.8"/><path d="M 100 100 C 100 180, 250 180, 300 100 S 500 20, 450 100 C 400 180, 550 180, 600 100 S 800 20, 800 100" stroke="#7c3aed" stroke-width="2" fill="none" opacity="0.5"/></svg>
</div>

<!-- LEFT SIDEBAR -->
<div class="hidden lg:flex w-[210px] glass-strong rounded-2xl p-4 flex-col gap-4">
<div><p class="text-xs font-bold tracking-widest opacity-80">+ CHANNELS</p><div class="mt-3 space-y-2 text-sm opacity-70"><p># # general</p><p># techniques</p><p>👁 domain-theory</p><p>💀 cursed-spirits</p></div></div>
<div><p class="text-xs font-bold opacity-60">FAVORITES</p><div class="mt-2 px-3 py-2 rounded-xl bg-violet-500/20 border border-violet-500/40 text-sm">☆ Gojo • Six Eyes Guide</div></div>
<div class="mt-auto glass rounded-xl p-3"><p class="text-[10px] text-center">LIMITLESS CORE</p><div class="text-center text-3xl my-1">∞</div><div class="flex justify-between text-xs"><div class="h-1 w-[70%] bg-gradient-to-r from-blue-500 to-purple-500 rounded-full"></div><span>94%</span></div><p class="text-[9px] mt-2 opacity-60">Infinity: Active • Neutral Space: 94%</p></div>
</div>

<!-- CENTER CHAT -->
<div class="flex-1 glass-strong rounded-2xl flex flex-col p-3 md:p-4 relative z-10">
<div class="flex items-center gap-3"><div class="w-9 h-9 rounded-full bg-black border border-violet-400 flex items-center justify-center">◎</div><div><p class="font-bold text-sm">Chat with Gojo Satoru</p><p class="text-[11px] opacity-60">AI Sorcerer • Active • Domain: Infinite Void • Latency: 0ms</p></div></div>
<div class="mt-3 glass rounded-full px-4 py-2 text-[11px] text-center opacity-80">✦ Domain Expansion: Infinite Void is active — all messages slowed in infinite space for clarity. ✦</div>
<div id="chat" class="flex-1 overflow-y-auto mt-3 space-y-3 pr-1">
<div class="flex gap-2"><img src="https://i.imgur.com/8Km9tLL.png" class="w-8 h-8 rounded-full"><div class="glass p-3 rounded-xl text-sm max-w-[85%]">Welcome to my domain. Bring your questions. I see every cursed energy flow with the Six Eyes — ask me about jujutsu, techniques, or how Limitless bends reality.<br><span class="text-[10px] opacity-50">Today 21:42 • Read</span></div></div>
</div>
<div class="mt-3 flex gap-2"><input id="msg" class="flex-1 glass rounded-full px-5 py-3 text-sm outline-none" placeholder="Ask Gojo about techniques, domains, Six Eyes, strategy..."><button onclick="send()" class="w-12 h-12 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">↗</button></div>
<div class="mt-3 grid grid-cols-1 md:grid-cols-3 gap-2 text-[11px]"><div class="glass rounded-xl p-2">✦ <b>Explain Red</b><br><span class="opacity-60">Cursed Technique Reversal</span></div><div class="glass rounded-xl p-2">✦ <b>Explain Blue</b><br><span class="opacity-60">Cursed Technique Lapse</span></div><div class="glass rounded-xl p-2">∞ <b>Hollow Purple:</b><br><span class="opacity-60">Explained</span></div></div>
</div>

<!-- RIGHT GOJO -->
<div class="hidden xl:block w-[320px] relative">
<div class="absolute top-10 right-0 text-right opacity-40 text-3xl" style="writing-mode:vertical-rl">無下限<br>域開</div>
<img src="https://wallpapers.com/images/hd/gojo-satoru-4k-8a7qg7v9p3c7b6z1.jpg" onerror="this.style.display='none'" class="absolute bottom-0 right-0 w-full h-[85%] object-cover object-top opacity-90 mask-gradient" style="-webkit-mask-image: linear-gradient(to bottom, transparent, black 20%, black 80%, transparent);">
<div class="absolute bottom-10 right-0 text-right"><p class="tracking-[0.3em] text-sm opacity-60">INFINITY</p><p class="text-4xl font-bold">無下開</p></div>
<div class="absolute top-1/2 left-0 w-[300px] h-[400px] pointer-events-none opacity-60"><svg viewBox="0 0 200 400"><path d="M100 20 C 160 80, 160 150, 100 200 C 40 250, 40 320, 100 380 M100 20 C 40 80, 40 150, 100 200 C 160 250, 160 320, 100 380" stroke="url(#g)" stroke-width="3" fill="none" filter="url(#glow)"/></svg></div>
</div>

</div>

<script>
async function send(){
 let input=document.getElementById('msg'); let t=input.value.trim(); if(!t) return;
 let chat=document.getElementById('chat');
 chat.innerHTML+=`<div class='flex justify-end'><div class='bg-gradient-to-r from-violet-600 to-blue-600 p-3 rounded-xl max-w-[75%] text-sm'>${t}<br><span class='text-[10px] opacity-70'>Today 21:43</span></div></div>`;
 input.value=''; chat.scrollTop=chat.scrollHeight;
 chat.innerHTML+=`<div id='typing' class='flex gap-2 opacity-60'><div class='w-8 h-8 rounded-full bg-blue-600'></div><div class='glass p-3 rounded-xl text-sm'>Gojo is channeling Limitless...</div></div>`;
 let res=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:t})});
 let data=await res.json();
 document.getElementById('typing')?.remove();
 chat.innerHTML+=`<div class='flex gap-2'><img src='https://i.imgur.com/8Km9tLL.png' class='w-8 h-8 rounded-full'><div class='glass p-3 rounded-xl text-sm max-w-[85%]'>${data.reply}<br><span class='text-[10px] opacity-50'>Today 21:44 • Read</span></div></div>`;
 chat.scrollTop=chat.scrollHeight;
}
document.getElementById('msg').addEventListener('keypress',e=>{if(e.key==='Enter')send()})
</script>
</body></html>
"""

@app.route("/")
def home(): return render_template_string(HTML)

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message")
    completion = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":user_msg}])
    return jsonify({"reply": completion.choices[0].message.content})

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming = request.values.get("Body", "")
    completion = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":incoming}])
    resp = MessagingResponse(); resp.message(completion.choices[0].message.content); return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
