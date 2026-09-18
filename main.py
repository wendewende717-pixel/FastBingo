
import os
import json
import random
import hmac
import hashlib
from urllib.parse import parse_qs
from flask import Flask, jsonify, request, render_template

app = Flask(__name__, template_folder='.')

# 1. TELEGRAM BOT SECURITY & CONFIG
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
COMMISSION_RATE = 0.20  # 20% Platform Commission

ROOM_PRICES = [5, 10, 15, 20, 25, 50, 100]  # Game rooms in ETB

# 2. GENERATE 600 UNIQUE BINGO CARDS (Non-Repeating Matrix)
def generate_600_cards():
    cards = {}
    random.seed(42)  # Fixed seed to preserve card IDs consistency
    for card_id in range(1, 601):
        b = random.sample(range(1, 16), 5)
        i = random.sample(range(16, 31), 5)
        n = random.sample(range(31, 46), 4)  # 4 numbers + FREE space
        g = random.sample(range(46, 61), 5)
        o = random.sample(range(61, 76), 5)
        
        cards[card_id] = {
            "B": b,
            "I": i,
            "N": [n[0], n[1], "FREE", n[2], n[3]],
            "G": g,
            "O": o
        }
    return cards

BINGO_CARDS_DB = generate_600_cards()

# 3. TELEGRAM DATA VERIFICATION (Anti-Hack Mechanism)
def verify_telegram_data(init_data_str):
    if not init_data_str or BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        return True  # Dev bypass if token not set
    try:
        parsed_data = parse_qs(init_data_str)
        hash_from_tg = parsed_data.get('hash', [''])[0]
        data_check_arr = [f"{k}={v[0]}" for k, v in parsed_data.items() if k != 'hash']
        data_check_arr.sort()
        data_check_string = "\n".join(data_check_arr)

        secret_key = hmac.new(b"WebAppData", BOT_TOKEN.encode(), hashlib.sha256).digest()
        calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
        return calculated_hash == hash_from_tg
    except Exception:
        return False

# 4. SERVER ROUTES
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/cards', methods=['GET'])
def get_cards():
    return jsonify({"success": True, "cards_count": len(BINGO_CARDS_DB), "cards": BINGO_CARDS_DB})

@app.route('/api/calculate-prize', methods=['POST'])
def calculate_prize():
    data = request.json or {}
    entry_fee = data.get('entry_fee', 10)
    total_players = data.get('total_players', 1)
    
    total_pool = entry_fee * total_players
    admin_commission = total_pool * COMMISSION_RATE
    winner_prize = total_pool - admin_commission
    
    return jsonify({
        "success": True,
        "total_pool": total_pool,
        "admin_commission": admin_commission,
        "winner_prize": winner_prize
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
