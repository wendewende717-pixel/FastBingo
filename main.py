import logging
import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = os.getenv("BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN_HERE")

ENTRY_FEE = 10
PRIZE_AMOUNT = 8
COMMISSION_AMOUNT = 2
TOTAL_CARDS = 600

user_wallets = {}
game_state = {
    "is_active": False,
    "players": {},
    "drawn_numbers": [],
    "total_pot": 0,
    "admin_commission": 0
}

def generate_deterministic_card(card_id: int):
    rng = random.Random(card_id * 777 + 12345)
    
    b_col = rng.sample(range(1, 16), 5)
    i_col = rng.sample(range(16, 31), 5)
    n_col = rng.sample(range(31, 46), 4)
    g_col = rng.sample(range(46, 61), 5)
    o_col = rng.sample(range(61, 76), 5)
    
    card = []
    for row in range(5):
        r_data = []
        r_data.append(b_col[row])
        r_data.append(i_col[row])
        if row < 2:
            r_data.append(n_col[row])
        elif row == 2:
            r_data.append("FREE")
        else:
            r_data.append(n_col[row - 1])
        r_data.append(g_col[row])
        r_data.append(o_col[row])
        card.append(r_data)
    return card

def format_card_display(card, card_id):
    header = f"📋 **Bingo Card #{card_id}**\n"
    header += "` B   I   N   G   O `\n"
    header += "`---------------------`\n"
    
    rows_str = []
    for row in card:
        formatted_row = []
        for val in row:
            if val == "FREE":
                formatted_row.append("★ ")
            else:
                formatted_row.append(f"{val:02d}")
        rows_str.append(" ".join(formatted_row))
    
    return header + "`" + "\n".join(rows_str) + "`"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_wallets:
        user_wallets[user_id] = 100  # Welcome Bonus
        
    welcome_msg = (
        f"🎯 **እንኳን ወደ Fast Bingo Bot በደህና መጡ!**\n\n"
        f"💰 የሒሳብ መጠንዎ: {user_wallets[user_id]} ETB\n"
        f"🎟 የመግቢያ ዋጋ: {ENTRY_FEE} ETB\n"
        f"🏆 የአሸናፊ ሽልማት: {PRIZE_AMOUNT} ETB\n\n"
        f"ለመጫወት ከታች ያሉትን አማራጮች ይጠቀሙ።"
    )
    
    keyboard = [
        [InlineKeyboardButton("🎮 ጨዋታ ጀምር / ተቀላቀል", callback_data="join_game")],
        [InlineKeyboardButton("💰 Wallet (ሒሳብ)", callback_data="view_wallet")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_msg, parse_mode="Markdown", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data

    if user_id not in user_wallets:
        user_wallets[user_id] = 100

    if data == "view_wallet":
        await query.message.reply_text(f"💳 የአሁኑ ሒሳብዎ: {user_wallets[user_id]} ETB ነው::")

    elif data == "join_game":
        if user_wallets[user_id] < ENTRY_FEE:
            await query.message.reply_text("❌ በቂ ሒሳብ የሎትም። እባክዎን ሒሳብዎን ይሙሉ::")
            return
            
        if user_id in game_state["players"]:
            card_id = game_state["players"][user_id]
            card = generate_deterministic_card(card_id)
            await query.message.reply_text(f"ተመዝግበዋል!\n\n" + format_card_display(card, card_id), parse_mode="Markdown")
            return

        used_cards = set(game_state["players"].values())
        available_cards = [c for c in range(1, TOTAL_CARDS + 1) if c not in used_cards]
        
        if not available_cards:
            await query.message.reply_text("❌ ሁሉም ካርዶች ተይዘዋል። እባክዎን ቀጣዩን ጨዋታ ይጠብቁ::")
            return

        assigned_card_id = random.choice(available_cards)
        user_wallets[user_id] -= ENTRY_FEE
        game_state["players"][user_id] = assigned_card_id
        game_state["total_pot"] += PRIZE_AMOUNT
        game_state["admin_commission"] += COMMISSION_AMOUNT

        card = generate_deterministic_card(assigned_card_id)
        msg = f"✅ በትክክል ተመዝግበዋል! {ENTRY_FEE} ETB ተቀናንሷል።\n\n" + format_card_display(card, assigned_card_id)
        await query.message.reply_text(msg, parse_mode="Markdown")

def main():
    if TOKEN == "YOUR_TELEGRAM_BOT_TOKEN_HERE":
        print("ERROR: Please insert your actual Telegram Bot Token in the code or environment variable.")
        return

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("Fast Bingo Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
