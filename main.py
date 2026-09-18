import os
import asyncio
from datetime import datetime
from fastapi import FastAPI, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import requests

app = FastAPI()

# public ፎልደር ካለክ Static ፋይሎችን ለማስተናገድ
if os.path.exists("public"):
    app.mount("/static", StaticFiles(directory="public"), name="static")

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN")

# የጊዚያዊ ዳታቤዝ መያዣ (የተጫዋቾች መረጃ)
users_db = {}

class PlayRequest(BaseModel):
    user_id: str
    room_price: float
    card_count: int

@app.get("/")
def read_root():
    return FileResponse("index.html")

# 1. የዋሌት መረጃ ማግኛ
@app.get("/api/wallet/{user_id}")
def get_wallet(user_id: str):
    if user_id not in users_db:
        users_db[user_id] = {"balance": 0.0, "weekly_spent": 0.0}
    return {"success": True, "balance": users_db[user_id]["balance"]}

# 2. የጨዋታ ክፍያ መቀነሻ እና የሳምንታዊ ወጪ መመዝገቢያ
@app.post("/api/play-game")
def play_game(data: PlayRequest):
    user_id = data.user_id
    total_cost = data.room_price * data.card_count

    if user_id not in users_db:
        users_db[user_id] = {"balance": 0.0, "weekly_spent": 0.0}

    if users_db[user_id]["balance"] < total_cost:
        return {"success": False, "message": "⚠️ በቂ የብር መጠን የሎትም!"}

    users_db[user_id]["balance"] -= total_cost
    users_db[user_id]["weekly_spent"] += total_cost
    return {"success": True, "new_balance": users_db[user_id]["balance"]}

# 3. በየሳምንቱ እሁድ ማታ 10% Cashback የሚያሰላ ተግባር
def send_telegram_msg(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": chat_id, "text": text})
    except Exception as e:
        print("Error sending msg:", e)

async def weekly_cashback_job():
    while True:
        now = datetime.now()
        # እሁድ ቀን (Weekday 6) እና ማታ 12:00 AM (00:00) መሆኑን ማረጋገጥ
        if now.weekday() == 6 and now.hour == 0 and now.minute == 0:
            for user_id, data in users_db.items():
                if data["weekly_spent"] > 0:
                    cashback = data["weekly_spent"] * 0.10
                    data["balance"] += cashback
                    data["weekly_spent"] = 0.0
                    
                    msg = f"🎉 እንኳን ደስ አለዎት!\n\nየዚህ ሳምንት የ10% Cash Back ቦነስ 🎁 {cashback:.2f} ETB ወደ ዋሌትዎ ገቢ ሆኗል!"
                    send_telegram_msg(user_id, msg)
            await asyncio.sleep(60) # ለአንድ ደቂቃ ማሳረፍ
        await asyncio.sleep(30)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(weekly_cashback_job())
