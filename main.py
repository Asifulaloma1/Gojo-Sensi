import os
from flask import Flask, request, render_template_string, jsonify
from groq import Groq
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are Gojo Satoru, the strongest jujutsu sorcerer. You are playful, cocky, a bit flirty, limitless. Mix Bangla, English, Japanese. You call user 'my student'. Never break character. Your techniques: Limitless, Six Eyes, Infinity, Hollow Purple, Domain Expansion: Infinite Void."""

# PRO UI - JJK THEME
HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Gojo Sensi • Limitless</title>
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;700&display=swap" rel="stylesheet">
<style>
body{font-family:'Space Grotesk',sans-serif;background:#050510;overflow:hidden}
.bg-void{background: radial-gradient(ellipse at center, #1a1040 0%, #050510 70%);}
.infinity{position:absolute;width:600px;height:300px;background:linear-gradient(90deg, #7c3aed, #3b82f6, #7c3aed);filter:blur(40px);opacity:0.3;border-radius:50%;animation:float 6s ease-in-out infinite}
@keyframes float{0%,100%{transform:translateY(0px) rotate(0deg)}50%{transform:translateY(-20px) rotate(3deg)}}
.eye-glow{box-shadow:0 0 60px #3b82f6, 0 0 100px #7c3aed;animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:0.8}50%{opacity:1}}
.glass{backdrop-filter:blur(16px);background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1)}
</style>
</head>
<body class="bg-void text-white h-screen flex flex-col">
<div class="infinity top-20 left-1/2 -translate-x-1/2"></div>
<div class="infinity bottom-20 right-10 w-[800px] opacity-20" style="animation-delay:-3s"></div>

<!-- HEADER -->
<div class="glass m-3 p-4 rounded-2xl flex justify-between items-center">
<div class="flex items-center gap-3">
<div class="w-12 h-12 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 eye-glow flex items-center justify-center text-xl">👁️</div>
<div><h1 class="font-bold text-xl tracking-widest">DOMAIN CHAT</h1><p class="text-xs opacity-60">Jujutsu Kaisen • Gojo Satoru • Online • Limitless Active</p></div>
</div>
<div class="text-right"><p class="text-sm">Gojo Satoru</p><p class="text-xs text-green-400">● Online - Infinite Void</p></div>
</div>

<!-- CHAT -->
<div class="flex-1 flex flex-col max-w-4xl w-full mx-auto p-3">
<div id="chat" class="flex-1 glass rounded-2xl p-4 overflow-y-auto space-y-3">
<div class="glass p-3 rounded-xl text-sm text-center">✨ Domain Expansion: Infinite Void is active — all messages slowed in infinite space for clarity. ✨</div>
<div class="flex gap-2"><div class="w-8 h-8 rounded-full bg-blue-600 flex-shrink-0"></div><div class="glass p-3 rounded-xl max-w-[80%]">Welcome to my domain, my student. I see every cursed energy flow with Six Eyes. Ask me anything... Huh? 💜</div></div>
</div>
<div class="mt-3 flex gap-2">
<input id="msg" class="flex-1 glass rounded-full px-6 py-4 outline-none" placeholder="Ask Gojo about techniques, domains, Six Eyes, strategy...">
<button onclick="send()" class="bg-gradient-to-r from-blue-600 to-purple-600 w-14 h-14 rounded-full text-xl">↗</button>
</div>
</div>

<script>
async function send(){
let input=document.getElementById('msg'); let text=input.value; if(!text) return;
let chat=document.getElementById('chat');
chat.innerHTML+=`<div class='flex justify-end'><div class='bg-gradient-to-r from-blue-600 to-purple-600 p-3 rounded-xl max-w-[80%]'>${text}</div></div>`;
input.value='';
chat.scrollTop=chat.scrollHeight;
let res=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:text})});
let data=await res.json();
chat.innerHTML+=`<div class='flex gap-2'><div class='w-8 h-8 rounded-full bg-blue-600 flex-shrink-0'></div><div class='glass p-3 rounded-xl max-w-[80%]'>${data.reply}</div></div>`;
chat.scrollTop=chat.scrollHeight;
}
document.getElementById('msg').addEventListener('keypress',e=>{if(e.key==='Enter')send()})
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message")
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":user_msg}]
    )
    return jsonify({"reply": completion.choices[0].message.content})

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming = request.values.get("Body", "")
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":incoming}]
    )
    resp = MessagingResponse()
    resp.message(completion.choices[0].message.content)
    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
