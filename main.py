import os
import threading
import time
from datetime import datetime
from flask import Flask, jsonify, request, send_from_directory
import requests

app = Flask(__name__, static_folder='.')

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID", "YOUR_TELEGRAM_ADMIN_CHAT_ID")

# የጊዚያዊ ዳታቤዝ መያዣ
users_db = {}

def send_telegram_msg(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"})
    except Exception as e:
        print("Error sending msg:", e)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# 1. የዋሌት መረጃ ማግኛ
@app.route('/api/wallet/<user_id>', methods=['GET'])
def get_wallet(user_id):
    if user_id not in users_db:
        users_db[user_id] = {"balance": 0.0, "weekly_spent": 0.0}
    return jsonify({"success": True, "balance": users_db[user_id]["balance"]})

# 2. የጨዋታ ክፍያ መቀነሻ እና የሳምንታዊ ወጪ መመዝገቢያ
@app.route('/api/play-game', methods=['POST'])
def play_game():
    data = request.get_json() or {}
    user_id = str(data.get("user_id"))
    room_price = float(data.get("room_price", 0))
    card_count = int(data.get("card_count", 0))
    
    total_cost = room_price * card_count

    if user_id not in users_db:
        users_db[user_id] = {"balance": 0.0, "weekly_spent": 0.0}

    if users_db[user_id]["balance"] < total_cost:
        return jsonify({"success": False, "message": "⚠️ በቂ የብር መጠን የሎትም!"})

    users_db[user_id]["balance"] -= total_cost
    users_db[user_id]["weekly_spent"] += total_cost
    return jsonify({"success": True, "new_balance": users_db[user_id]["balance"]})

# 3. የብር ማስገቢያ ጥያቄ መቀበያ
@app.route('/api/deposit-request', methods=['POST'])
def deposit_request():
    data = request.get_json() or {}
    user_id = str(data.get("user_id"))
    user_name = data.get("user_name", "User")
    amount = data.get("amount")
    txn_id = data.get("txn_id")

    msg = f"📥 *አዲስ የብር ማስገቢያ ጥያቄ!*\n\n👤 ተጫዋች: {user_name} (ID: `{user_id}`)\n💰 መጠን: {amount} ETB\n🧾 Txn No: `{txn_id}`"
    send_telegram_msg(ADMIN_CHAT_ID, msg)

    return jsonify({"success": True, "message": "የብር ማስገቢያ ጥያቄዎ ተልኳል! በቅርቡ ተመርምሮ ዋሌትዎ ላይ ይጨመራል።"})

# 4. የብር ማውጫ ጥያቄ መቀበያ
@app.route('/api/withdraw-request', methods=['POST'])
def withdraw_request():
    data = request.get_json() or {}
    user_id = str(data.get("user_id"))
    user_name = data.get("user_name", "User")
    amount = float(data.get("amount", 0))
    method = data.get("method")
    account = data.get("account")

    if user_id in users_db and users_db[user_id]["balance"] >= amount:
        msg = f"📤 *አዲስ የብር ማውጫ ጥያቄ!*\n\n👤 ተጫዋች: {user_name} (ID: `{user_id}`)\n💰 መጠን: {amount} ETB\n🏦 መንገድ: {method}\nቁጥር: `{account}`"
        send_telegram_msg(ADMIN_CHAT_ID, msg)
        return jsonify({"success": True, "message": "የብር ማውጣት ጥያቄዎ ተልኳል! በቅርቡ ገቢ ይደረግልዎታል።"})
    else:
        return jsonify({"success": False, "message": "⚠️ ማውጣት የሚፈልጉት የብር መጠን ከዋሌትዎ ሚዛን ይበልጣል!"})

# 5. በየሳምንቱ እሁድ ማታ 10% Cashback የሚያሰላ Background Worker
def weekly_cashback_worker():
    while True:
        now = datetime.now()
        if now.weekday() == 6 and now.hour == 0 and now.minute == 0:
            for user_id, data in users_db.items():
                if data["weekly_spent"] > 0:
                    cashback = data["weekly_spent"] * 0.10
                    data["balance"] += cashback
                    data["weekly_spent"] = 0.0
                    
                    msg = f"🎉 እንኳን ደስ አለዎት!\n\nየዚህ ሳምንት የ10% Cash Back ቦነስ 🎁 {cashback:.2f} ETB ወደ ዋሌትዎ ገቢ ሆኗል!"
                    send_telegram_msg(user_id, msg)
            time.sleep(60)
        time.sleep(30)

threading.Thread(target=weekly_cashback_worker, daemon=True).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
