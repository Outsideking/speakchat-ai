# SpeakChat AI Full Real (Single File)

## Features
- GPT-4 Chat (AI Chat จริง)
- Stripe Payment Integration (รับเงินจริง)
- Frontend + Backend ในไฟล์เดียว
- พร้อม deploy ขายออนไลน์หรือทำเว็บหลังบ้าน

## Setup
1. ติดตั้ง dependencies:
```
pip install fastapi uvicorn openai stripe python-dotenv
```

2. ตั้งค่า `.env` ตาม `.env.example`

3. รัน server:
```
python speakchat_full_real.py
```

4. เปิดเว็บ browser:
```
http://localhost:8000/
```

## Notes
- เปลี่ยน API keys ของคุณให้ถูกต้อง
- สามารถต่อยอด STT/TTS, SC Wallet หรือระบบหลังบ้านได้ทันที
