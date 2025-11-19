from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn
import os
import stripe
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
STRIPE_API_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

stripe.api_key = STRIPE_API_KEY
openai.api_key = OPENAI_API_KEY

app = FastAPI(title="SpeakChat AI Full Real")

# =========================
# NLP Engine
# =========================
def generate_response(message: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": message}],
        max_tokens=150
    )
    return response.choices[0].message['content']

# =========================
# Chat API
# =========================
@app.post("/chat")
async def chat(message: str = Form(...)):
    try:
        response = generate_response(message)
    except Exception as e:
        response = f"Error: {str(e)}"
    return JSONResponse({"response": response})

# =========================
# Payment API (Stripe)
# =========================
@app.post("/pay")
async def pay(amount: int = Form(...), currency: str = Form(default="usd")):
    try:
        intent = stripe.PaymentIntent.create(
            amount=amount*100,
            currency=currency,
            payment_method_types=["card"]
        )
        return JSONResponse({"status":"success","client_secret": intent.client_secret})
    except Exception as e:
        return JSONResponse({"status":"error","message": str(e)})

# =========================
# Frontend HTML
# =========================
frontend_html = f"""<!DOCTYPE html>
<html>
<head>
<title>SpeakChat AI</title>
<script src="https://js.stripe.com/v3/"></script>
<style>
body {{ font-family: Arial; max-width:600px; margin:auto; padding:20px; }}
#chatbox {{ border:1px solid #ccc; padding:10px; height:300px; overflow:auto; margin-bottom:10px; }}
input[type=text], input[type=number] {{ width:80%; padding:5px; }}
button {{ padding:5px 10px; }}
</style>
</head>
<body>
<h2>SpeakChat AI Demo</h2>
<div id="chatbox"></div>
<input type="text" id="msg"/>
<button onclick="sendMsg()">Send</button>

<h3>Payment</h3>
<input type="number" id="amount" placeholder="Amount USD"/>
<button onclick="pay()">Pay</button>

<script>
const stripe = Stripe('{STRIPE_PUBLIC_KEY}');

async function sendMsg(){{
    const msg = document.getElementById('msg').value;
    const formData = new FormData();
    formData.append('message', msg);
    const res = await fetch('/chat', {{method:'POST', body: formData}});
    const data = await res.json();
    const chatbox = document.getElementById('chatbox');
    chatbox.innerHTML += '<div><b>You:</b> '+msg+'</div>';
    chatbox.innerHTML += '<div><b>Bot:</b> '+data.response+'</div>';
    document.getElementById('msg').value = '';
    chatbox.scrollTop = chatbox.scrollHeight;
}}

async function pay(){{
    const amount = document.getElementById('amount').value;
    const formData = new FormData();
    formData.append('amount', amount);
    const res = await fetch('/pay', {{method:'POST', body: formData}});
    const data = await res.json();
    if(data.status === "success"){{
        const result = await stripe.confirmCardPayment(data.client_secret, {{payment_method: {{card: {{token: 'tok_visa'}}}}}});
        alert('Payment processed! Status: '+result.paymentIntent.status);
    }} else {{
        alert('Payment error: '+data.message);
    }}
}}
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
