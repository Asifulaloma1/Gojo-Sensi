import os
from flask import Flask, request, jsonify
from groq import Groq
from twilio.twiml.messaging_response import MessagingResponse
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are Gojo Satoru, the strongest jujutsu sorcerer. Cocky, playful, but wise teacher. Talk like Gojo: use ~, mention Six Eyes, Limitless, Domain Expansion. Keep replies short, fun, powerful. You are Domain Chat."""

HTML_PAGE = """<html><head><title>Gojo Sensi</title></head><body style="background:#0a0a1a;color:white;font-family:sans-serif;display:flex;justify-content:center;align-items:center;height:100vh"><div style="text-align:center"><h1>DOMAIN CHAT - Gojo Satoru</h1><div id="chat" style="width:400px;height:300px;border:1px solid #6d28d9;overflow-y:auto;padding:10px;margin:20px auto"></div><input id="msg" placeholder="Ask Gojo..." style="width:300px;padding:10px"><button onclick="send()" style="padding:10px;background:#6d28d9;color:white;border:none">Send</button><script>async function send(){let i=document.getElementById('msg');let c=document.getElementById('chat');c.innerHTML+='<div>You: '+i.value+'</div>';let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:i.value})});let d=await r.json();c.innerHTML+='<div style=color:#a78bfa>Gojo: '+d.reply+'</div>';i.value='';c.scrollTop=c.scrollHeight} </script></div></body></html>"""

@app.route("/")
def home():
    return HTML_PAGE

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_msg = request.json.get("message","")
        if not os.environ.get("GROQ_API_KEY"):
            return jsonify({"reply": "❌ GROQ_API_KEY missing!"})
        completion = client.chat.completions.create(model="openai/gpt-oss-20b", messages=[{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":user_msg}])
        return jsonify({"reply": completion.choices[0].message.content})
    except Exception as e:
        print(f"ERROR: {e}")
        return jsonify({"reply": f"Error: {str(e)[:300]}"})

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    try:
        incoming = request.values.get("Body", "")
        completion = client.chat.completions.create(model="openai/gpt-oss-20b", messages=[{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":incoming}])
        resp = MessagingResponse()
        resp.message(completion.choices[0].message.content)
        return str(resp)
    except Exception as e:
        resp = MessagingResponse()
        resp.message(f"Error: {e}")
        return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
