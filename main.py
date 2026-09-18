import os
import json
import random
import hmac
import hashlib
from urllib.parse import parse_qs
from flask import Flask, jsonify, request, render_template

app = Flask(__name__, template_folder='.')

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "fastbingo123") # አድሚን መግቢያ
COMMISSION_RATE = 0.20  # 20% Platform Commission
REFERRAL_BONUS = 10.0   # 10 ETB Referral Bonus

USER_WALLETS = {}
TOTAL_ADMIN_COMMISSION = 0.0 # የተሰበሰበ አጠቃላይ ኮሚሽን

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

# ADMIN DASHBOARD ENDPOINTS
@app.route('/api/admin/set-rule', methods=['POST'])
def admin_set_rule():
    data = request.json or {}
    password = data.get("password")
    new_rule = data.get("rule") # e.g., "SINGLE LINE", "FULL HOUSE", "CORNERS"
    
    if password != ADMIN_PASSWORD:
        return jsonify({"success": False, "message": "የተሳሳተ የአድሚን ፓስወርድ!"})
    
    current_game["rule"] = new_rule
    return jsonify({"success": True, "message": f"የጨዋታው ህግ ወደ '{new_rule}' ተቀይሯል!", "current_rule": new_rule})

@app.route('/api/admin/stats', methods=['POST'])
def admin_stats():
    data = request.json or {}
    password = data.get("password")
    
    if password != ADMIN_PASSWORD:
        return jsonify({"success": False, "message": "የተሳሳተ የአድሚን ፓስወርድ!"})
    
    return jsonify({
        "success": True,
        "total_users": len(USER_WALLETS),
        "total_commission_earned": TOTAL_ADMIN_COMMISSION,
        "current_game_state": current_game
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
