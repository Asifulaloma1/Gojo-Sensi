import os
from flask import Flask, request, render_template_string, jsonify
from groq import Groq
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are Gojo Satoru. Strongest sorcerer, Six Eyes, Limitless, Infinity. Playful, cocky, call user 'my student'. Mix Bangla + English. You are inside Domain Chat UI."""

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Gojo Sensi • Limitless</title>
<script src="https://cdn.tailwindcss.com"></script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&display=swap');
body{font-family:'Space Grotesk',sans-serif;background:#070711;color:white;overflow:hidden}
.bg-main{background: radial-gradient(ellipse at top, #1b1050 0%, #0a0a20 45%, #050510 100%)}
.glass{background:rgba(22,18,60,0.75);backdrop-filter:blur(18px);border:1px solid rgba(130,110,255,0.25)}
.glow{box-shadow:0 0 40px rgba(124,92,255,0.6)}
::-webkit-scrollbar{width:5px}::-webkit-scrollbar-thumb{background:#5b4bd5;border-radius:10px}
</style>
</head>
<body class="bg-main h-screen p-2 md:p-3 flex flex-col">

<!-- HEADER -->
<div class="glass rounded-2xl px-4 py-3 flex items-center justify-between">
<div class="flex items-center gap-3">
<div class="w-10 h-10 rounded-full bg-black border border-violet-500 flex items-center justify-center glow text-lg">☯</div>
<div><h1 class="text-xl font-bold tracking-widest">DOMAIN CHAT</h1><p class="text-[11px] opacity-60">Jujutsu Kaisen • Gojo Satoru</p></div>
</div>
<div class="hidden md:flex gap-6 text-xs opacity-80"><span>∞ Limitless</span><span class="px-3 py-1 rounded-full bg-violet-500/30 border border-violet-400">◎ Domain Expansion</span><span>✦ Techniques</span></div>
<div class="flex items-center gap-3"><div class="text-right hidden md:block"><p class="text-sm font-bold">Gojo Satoru</p><p class="text-[11px] text-green-400">• Online</p></div><img src="https://i.imgur.com/CzXTtJV.png" class="w-10 h-10 rounded-xl object-cover bg-violet-900"></div>
</div>

<div class="flex-1 flex gap-3 mt-3 overflow-hidden relative">
<!-- LEFT -->
<div class="hidden lg:flex w-[200px] glass rounded-2xl p-4 flex-col">
<p class="text-[11px] font-bold tracking-widest opacity-70">+ CHANNELS</p>
<div class="mt-3 space-y-2 text-sm opacity-70"><p># # general</p><p># techniques</p><p>👁 domain-theory</p><p>💀 cursed-spirits</p></div>
<p class="mt-6 text-[11px] font-bold opacity-50">FAVORITES</p>
<div class="mt-2 px-3 py-2 rounded-xl bg-violet-600/30 border border-violet-400/40 text-sm">☆ Gojo • Six Eyes Guide</div>
<div class="mt-auto glass rounded-xl p-3 text-center">
<p class="text-[10px] opacity-70">LIMITLESS CORE</p><p class="text-2xl my-1">∞</p>
<div class="w-full h-1 bg-black/50 rounded-full overflow-hidden"><div class="h-full w-[94%] bg-gradient-to-r from-blue-500 to-purple-500"></div></div>
<p class="text-[10px] mt-1 flex justify-between"><span>94%</span><span class="opacity-60">Active</span></p>
<p class="text-[9px] mt-2 opacity-50">Infinity: Active • Neutral Space: 94%</p>
</div>
</div>

<!-- CENTER -->
<div class="flex-1 glass rounded-2xl flex flex-col p-3 relative z-10 overflow-hidden">
<!-- Infinity BG -->
<div class="absolute top-[60px] left-1/2 -translate-x-1/2 w-[700px] h-[200px] opacity-40 pointer-events-none">
<svg viewBox="0 0 700 200" class="w-full h-full"><path d="M50 100 Q150 -20 250 100 T450 100 Q550 220 650 100 Q550 -20 450 100 T250 100 Q150 220 50 100" stroke="#8b5cf6" stroke-width="4" fill="none" opacity="0.9"/></svg>
</div>

<div class="flex items-center gap-3"><div class="w-8 h-8 rounded-full bg-black border border-violet-500 flex items-center justify-center text-xs">◎</div><div><p class="text-sm font-bold">Chat with Gojo Satoru</p><p class="text-[10px] opacity-50">AI Sorcerer • Active • Domain: Infinite Void • Latency: 0ms</p></div></div>
<div class="mt-3 glass rounded-full px-4 py-2 text-[11px] text-center">✦ Domain Expansion: Infinite Void is active — all messages slowed in infinite space for clarity. ✦</div>

<div id="chat" class="flex-1 overflow-y-auto mt-3 space-y-3 pr-1">
<div class="flex gap-2"><img src="https://i.imgur.com/CzXTtJV.png" class="w-8 h-8 rounded-full bg-violet-900"><div class="glass p-3 rounded-xl text-sm max-w-[80%]">Welcome to my domain. Bring your questions. I see every cursed energy flow with the Six Eyes — ask me about jujutsu, techniques, or how Limitless bends reality.<br><span class="text-[10px] opacity-50">Today 21:42 • Read</span></div></div>
</div>

<div class="mt-3 flex gap-2"><input id="msg" class="flex-1 glass rounded-full px-5 py-3 text-sm outline-none" placeholder="Ask Gojo about techniques, domains, Six Eyes, strategy..."><button onclick="send()" class="w-12 h-12 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-xl">↗</button></div>

<div class="mt-3 grid grid-cols-3 gap-2 text-[11px]">
<div class="glass rounded-xl p-2 cursor-pointer hover:bg-violet-500/20" onclick="document.getElementById('msg').value='Explain Red';send()"><b>✦ Explain Red</b><br><span class="opacity-60">Cursed Technique Reversal</span></div>
<div class="glass rounded-xl p-2 cursor-pointer hover:bg-violet-500/20" onclick="document.getElementById('msg').value='Explain Blue';send()"><b>✦ Explain Blue</b><br><span class="opacity-60">Cursed Technique Lapse</span></div>
<div class="glass rounded-xl p-2 cursor-pointer hover:bg-violet-500/20" onclick="document.getElementById('msg').value='Explain Hollow Purple';send()"><b>∞ Hollow Purple:</b><br><span class="opacity-60">Explained</span></div>
</div>
</div>

<!-- RIGHT GOJO BIG -->
<div class="hidden xl:block w-[300px] relative rounded-2xl overflow-hidden">
<div class="absolute inset-0 bg-gradient-to-t from-[#070711] via-transparent to-transparent z-10"></div>
<div class="absolute top-6 right-2 opacity-20 text-2xl z-20" style="writing-mode:vertical-rl">無量空処</div>
<img src="https://i.imgur.com/CzXTtJV.png" class="absolute bottom-0 right-0 w-full h-[90%] object-contain object-bottom drop-shadow-[0_0_40px_#7c5cff]">
<div class="absolute bottom-8 right-4 z-20 text-right"><p class="text-[12px] tracking-[0.4em] opacity-60">INFINITY</p><p class="text-3xl font-bold opacity-80">無下限</p></div>
<!-- Six Eyes glow lines -->
<div class="absolute top-1/2 left-0 w-full h-[300px] -translate-y-1/2 opacity-50 pointer-events-none"><svg viewBox="0 0 200 300"><path d="M100 10 Q140 80 100 150 Q60 220 100 290 M100 10 Q60 80 100 150 Q140 220 100 290" stroke="#7c5cff" stroke-width="3" fill="none"/></svg></div>
</div>
</div>

<script>
async function send(){
 let input=document.getElementById('msg'); let t=input.value.trim(); if(!t) return;
 let chat=document.getElementById('chat');
 chat.innerHTML+=`<div class='flex justify-end'><div class='bg-gradient-to-r from-violet-600 to-blue-600 p-3 rounded-xl max-w-[75%] text-sm'>${t}</div></div>`;
 input.value=''; chat.scrollTop=chat.scrollHeight;
 let typing=document.createElement('div'); typing.id='typing'; typing.className='flex gap-2 opacity-60'; typing.innerHTML=`<div class='w-8 h-8 rounded-full bg-violet-600'></div><div class='glass p-3 rounded-xl text-sm'>Gojo is channeling Limitless...</div>`; chat.appendChild(typing);
 let res=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:t})});
 let data=await res.json();
 document.getElementById('typing')?.remove();
 chat.innerHTML+=`<div class='flex gap-2'><img src='https://i.imgur.com/CzXTtJV.png' class='w-8 h-8 rounded-full bg-violet-900'><div class='glass p-3 rounded-xl text-sm max-w-[80%]'>${data.reply}</div></div>`;
 chat.scrollTop=chat.scrollHeight;
}
document.getElementById('msg').addEventListener('keypress',e=>{if(e.key==='Enter')send()})
</script>
</body>
</html>
"""

@app.route("/")
def home(): return render_template_string(HTML)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_msg = request.json.get("message","")
        if not os.environ.get("GROQ_API_KEY"):
            return jsonify({"reply": "❌ GROQ_API_KEY missing! Render > Environment e add koro"})
        completion = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":user_msg}])
        return jsonify({"reply": completion.choices[0].message.content})
    except Exception as e:
        print(f"ERROR: {e}")
        return jsonify({"reply": f"⚠️ Error: {str(e)[:250]}"})

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    try:
        incoming = request.values.get("Body", "")
        completion = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":incoming}])
        resp = MessagingResponse(); resp.message(completion.choices[0].message.content); return str(resp)
    except Exception as e:
        resp = MessagingResponse(); resp.message(f"Error: {e}"); return str(resp)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
