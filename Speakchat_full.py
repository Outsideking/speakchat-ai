from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI(title="SpeakChat AI Fullstack")

# =========================
# NLP Engine (ตัวอย่าง)
# =========================
def generate_response(message: str) -> str:
    # Placeholder AI logic
    return f"Echo: {message}"

# =========================
# API Endpoint
# =========================
@app.post("/chat")
async def chat(message: str = Form(...)):
    response = generate_response(message)
    return JSONResponse({"response": response})

# =========================
# Payment API (ตัวอย่าง placeholder)
# =========================
@app.post("/pay")
async def pay(amount: float = Form(...), user: str = Form(...)):
    # ตัวอย่างรับเงิน (จริงต้องต่อ Stripe/PayPal SDK)
    return JSONResponse({"status": "success", "amount": amount, "user": user})

# =========================
# Frontend HTML
# =========================
frontend_html = """
<!DOCTYPE html>
<html>
<head>
<title>SpeakChat AI</title>
<style>
body { font-family: Arial; max-width:600px; margin:auto; padding:20px; }
#chatbox { border:1px solid #ccc; padding:10px; height:300px; overflow:auto; margin-bottom:10px; }
input[type=text] { width:80%; padding:5px; }
button { padding:5px 10px; }
</style>
</head>
<body>
<h2>SpeakChat AI Demo</h2>
<div id="chatbox"></div>
<input type="text" id="msg"/>
<button onclick="sendMsg()">Send</button>

<h3>Payment (Demo)</h3>
<input type="text" id="user" placeholder="User"/>
<input type="number" id="amount" placeholder="Amount"/>
<button onclick="pay()">Pay</button>

<script>
async function sendMsg(){
    const msg = document.getElementById('msg').value;
    const formData = new FormData();
    formData.append('message', msg);
    const res = await fetch('/chat', {method:'POST', body: formData});
    const data = await res.json();
    const chatbox = document.getElementById('chatbox');
    chatbox.innerHTML += '<div><b>You:</b> '+msg+'</div>';
    chatbox.innerHTML += '<div><b>Bot:</b> '+data.response+'</div>';
    document.getElementById('msg').value = '';
    chatbox.scrollTop = chatbox.scrollHeight;
}

async function pay(){
    const user = document.getElementById('user').value;
    const amount = document.getElementById('amount').value;
    const formData = new FormData();
    formData.append('user', user);
    formData.append('amount', amount);
    const res = await fetch('/pay', {method:'POST', body: formData});
    const data = await res.json();
    alert('Payment Status: '+data.status+' | Amount: '+data.amount);
}
</script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def home():
    return frontend_html

# =========================
# Run server
# =========================
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
