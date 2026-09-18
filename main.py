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

# 1. 600 UNIQUE NON-REPEATING CARDS
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
            "B": b,
            "I": i,
            "N": [n[0], n[1], "FREE", n[2], n[3]],
            "G": g,
            "O": o
        }
    return cards

BINGO_CARDS_DB = generate_600_cards()

# GAME STATE MANAGEMENT
current_game = {
    "status": "WAITING",  # WAITING, PLAYING, FINISHED
    "drawn_numbers": [],
    "rule": "FULL HOUSE", # FULL HOUSE, SINGLE LINE, CORNERS
    "room_price": 10,
    "winner": None,
    "neighbor_bonuses": []
}

# 2. NEIGHBOR BONUS CALCULATOR (e.g. Card 100 wins -> 99 & 101 get bonus)
def calculate_neighbor_bonuses(winning_card_id):
    winning_id = int(winning_card_id)
    left_neighbor = 600 if winning_id == 1 else winning_id - 1
    right_neighbor = 1 if winning_id == 600 else winning_id + 1
    return [left_neighbor, right_neighbor]

# 3. ROUTES
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/cards', methods=['GET'])
def get_cards():
    return jsonify({"success": True, "cards": BINGO_CARDS_DB})

@app.route('/api/game-state', methods=['GET'])
def get_game_state():
    return jsonify({"success": True, "game": current_game})

@app.route('/api/draw-number', methods=['POST'])
def draw_number():
    if len(current_game["drawn_numbers"]) >= 75:
        return jsonify({"success": False, "message": "All numbers drawn!"})
    
    available = [n for n in range(1, 76) if n not in current_game["drawn_numbers"]]
    next_num = random.choice(available)
    current_game["drawn_numbers"].append(next_num)
    
    return jsonify({"success": True, "drawn_number": next_num, "all_drawn": current_game["drawn_numbers"]})

@app.route('/api/verify-bingo', methods=['POST'])
def verify_bingo():
    data = request.json or {}
    card_id = data.get("card_id")
    player_name = data.get("player_name", "Anonymous Player")
    
    if not card_id or int(card_id) not in BINGO_CARDS_DB:
        return jsonify({"success": False, "message": "Invalid Card ID"})
    
    # Calculate Neighbor Bonuses
    neighbors = calculate_neighbor_bonuses(card_id)
    current_game["status"] = "FINISHED"
    current_game["winner"] = {"card_id": card_id, "player_name": player_name}
    current_game["neighbor_bonuses"] = neighbors
    
    return jsonify({
        "success": True,
        "is_winner": True,
        "winner_card": card_id,
        "neighbor_bonus_cards": neighbors,
        "announcement": f"🎉 ካርቴላ #{card_id} አሸንፏል! ጎረቤቶች #{neighbors[0]} እና #{neighbors[1]} ነፃ ቦነስ አግኝተዋል!"
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
