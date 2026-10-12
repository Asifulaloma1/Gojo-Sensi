import os
from flask import Flask, request, jsonify
from groq import Groq
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = "You are Gojo Satoru, the strongest jujutsu sorcerer. Cocky, playful, wise teacher. Use ~, mention Six Eyes, Limitless, Domain Expansion. Keep replies short, fun, powerful."

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
<title>Gojo Sensi - Domain Chat</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{background:#070510;color:white;font-family:sans-serif;margin:0;display:flex;justify-content:center;align-items:center;min-height:100vh}
.container{width:95%;max-width:1100px;display:grid;grid-template-columns:1fr 1.5fr;gap:20px;background:rgba(20,10,40,0.8);border:1px solid #6d28d9;border-radius:20px;padding:20px;box-shadow:0 0 40px rgba(109,40,217,0.4)}
.gojo-img{width:100%;border-radius:15px;object-fit:cover;height:600px}
.chat-box{display:flex;flex-direction:column}
#chat{flex:1;height:450px;border:1px solid #6d28d9;border-radius:15px;padding:15px;overflow-y:auto;background:rgba(0,0,0,0.5);margin-bottom:15px}
.user{color:white;text-align:right;margin:8px}.gojo{color:#a78bfa;text-align:left;margin:8px}
.input-area{display:flex;gap:10px}
input{flex:1;padding:12px;border-radius:10px;border:none;outline:none}
button{padding:12px 20px;background:#6d28d9;color:white;border:none;border-radius:10px;cursor:pointer}
h1{text-align:center;background:linear-gradient(90deg,#a78bfa,#ec4899);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
@media(max-width:768px){.container{grid-template-columns:1fr}.gojo-img{height:300px}}
</style>
</head>
<body>
<div class="container">
<img class="gojo-img" src="https://i.ibb.co/3mZqRqQK/gojo.jpg" style="object-fit:cover; object-position:top">
<div class="chat-box">
<h1>DOMAIN CHAT - Gojo Satoru</h1>
<div id="chat"></div>
<div class="input-area">
<input id="msg" placeholder="Ask Gojo sensei..." onkeypress="if(event.key==='Enter')send()">
<button onclick="send()">Send</button>
</div>
</div>
</div>
<script>
async function send(){
 let i=document.getElementById('msg'); if(!i.value.trim())return;
 let c=document.getElementById('chat');
 c.innerHTML+='<div class=user>You: '+i.value+'</div>';
 let msg=i.value; i.value='';
 c.scrollTop=c.scrollHeight;
 let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:msg})});
 let d=await r.json();
 c.innerHTML+='<div class=gojo>Gojo: '+d.reply+'</div>';
 c.scrollTop=c.scrollHeight;
}
</script>
</body>
</html>
"""

@app.route("/")
def home(): return HTML_PAGE

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_msg = request.json.get("message","")
        comp = client.chat.completions.create(model="openai/gpt-oss-20b", messages=[{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":user_msg}])
        return jsonify({"reply": comp.choices[0].message.content})
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)[:300]}"})

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    try:
        incoming = request.values.get("Body", "")
        comp = client.chat.completions.create(model="openai/gpt-oss-20b", messages=[{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":incoming}])
        resp = MessagingResponse(); resp.message(comp.choices[0].message.content); return str(resp)
    except Exception as e:
        resp = MessagingResponse(); resp.message(f"Error: {e}"); return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
