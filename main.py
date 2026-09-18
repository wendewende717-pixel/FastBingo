import os
import json
import random
import hmac
import hashlib
from urllib.parse import parse_qs
from flask import Flask, jsonify, request, render_template

app = Flask(__name__, template_folder='.')

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
COMMISSION_RATE = 0.20  # 20% Platform Commission
REFERRAL_BONUS = 10.0   # 10 ETB Referral Bonus for both parties

# IN-MEMORY USER WALLETS DATABASE
USER_WALLETS = {}  # { user_id: {"balance": 0.0, "referred_by": None} }

# 1. GENERATE 600 CARDS
def generate_600_cards():
    cards = {}
    random.seed(42)
    for card_id in range(1, 601):
        b = random.sample(range(1, 16), 5)
        i = random.sample(range(16, 31), 5)
        n = random.sample(range(31, 46), 4)
        g = random.sample(range(46, 61), 5)
        o = random.sample(range(61, 76), 5)
        cards[card_id] = {
            "B": b, "I": i,
            "N": [n[0], n[1], "FREE", n[2], n[3]],
            "G": g, "O": o
        }
    return cards

BINGO_CARDS_DB = generate_600_cards()

current_game = {
    "status": "WAITING",
    "drawn_numbers": [],
    "rule": "FULL HOUSE",
    "room_price": 10,
    "winner": None,
    "neighbor_bonuses": []
}

# WALLET & REFERRAL LOGIC
def get_or_create_wallet(user_id):
    if user_id not in USER_WALLETS:
        USER_WALLETS[user_id] = {"balance": 0.0, "referred_by": None}
    return USER_WALLETS[user_id]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/cards', methods=['GET'])
def get_cards():
    return jsonify({"success": True, "cards": BINGO_CARDS_DB})

@app.route('/api/wallet/<user_id>', methods=['GET'])
def get_wallet(user_id):
    wallet = get_or_create_wallet(str(user_id))
    return jsonify({"success": True, "user_id": user_id, "balance": wallet["balance"]})

# REFERRAL BONUS SYSTEM (10 ETB for both)
@app.route('/api/referral', methods=['POST'])
def process_referral():
    data = request.json or {}
    new_user = str(data.get("new_user_id"))
    referrer = str(data.get("referrer_id"))
    
    if not new_user or not referrer or new_user == referrer:
        return jsonify({"success": False, "message": "Invalid referral request"})
    
    new_wallet = get_or_create_wallet(new_user)
    if new_wallet["referred_by"] is not None:
        return jsonify({"success": False, "message": "User already referred"})
    
    referrer_wallet = get_or_create_wallet(referrer)
    
    new_wallet["referred_by"] = referrer
    new_wallet["balance"] += REFERRAL_BONUS
    referrer_wallet["balance"] += REFERRAL_BONUS
    
    return jsonify({
        "success": True,
        "message": f"🎉 10 ETB ቦነስ ለሁለቱም ወገን ተጨምሯል!",
        "new_user_balance": new_wallet["balance"],
        "referrer_balance": referrer_wallet["balance"]
    })

# DEPOSIT & WITHDRAWAL PLACEHOLDERS (CHAPA / TELEBIRR INTEGRATION)
@app.route('/api/deposit', methods=['POST'])
def deposit():
    data = request.json or {}
    user_id = str(data.get("user_id"))
    amount = float(data.get("amount", 0))
    
    if amount <= 0 or not user_id:
        return jsonify({"success": False, "message": "Invalid amount"})
    
    wallet = get_or_create_wallet(user_id)
    wallet["balance"] += amount
    return jsonify({"success": True, "message": f"{amount} ETB ገቢ ሆኗል!", "new_balance": wallet["balance"]})

@app.route('/api/withdraw', methods=['POST'])
def withdraw():
    data = request.json or {}
    user_id = str(data.get("user_id"))
    amount = float(data.get("amount", 0))
    
    wallet = get_or_create_wallet(user_id)
    if wallet["balance"] < amount or amount <= 0:
        return jsonify({"success": False, "message": "በቂ ቀሪ ሂሳብ የለዎትም!"})
    
    wallet["balance"] -= amount
    return jsonify({"success": True, "message": f"{amount} ETB ወጪ ሆኗል!", "new_balance": wallet["balance"]})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
