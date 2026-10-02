import os
import logging
import random
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

USER_DATABASE = {}

class CustomWebAppHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="static", **kwargs)

    def do_GET(self):
        if self.path == '/' or self.path == '':
            self.path = '/index.html'
        return super().do_GET()

def run_http_server():
    port = int(os.environ.get("PORT", 8000))
    server = HTTPServer(('0.0.0.0', port), CustomWebAppHandler)
    print(f"Serving WebApp on port {port}...")
    server.serve_forever()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name

    if user_id not in USER_DATABASE:
        contact_keyboard = ReplyKeyboardMarkup(
            [[KeyboardButton("📲 ስልክ ቁጥር አጋራ (Share Contact)", request_contact=True)]],
            resize_keyboard=True,
            one_time_keyboard=True
        )
        msg = (
            f"ሰላም {first_name}! 👋\n\n"
            f"እንኳን ወደ **Fast Bingo NextGen Pro** በደህና መጡ! 🎲\n\n"
            f"የራሶትን የሂሳብ መለያ (**Account ID**) ለማግኘትና ጨዋታውን ለመጀመር እባክዎ ከታች ያለውን **'📲 ስልክ ቁጥር አጋራ'** የሚለውን አዝራር ይጫኑ።\n\n"
            f"*(ማሳሰቢያ፦ የቴሌግራም ማስጠንቀቂያ ቢመጣ 'Share contact' የሚለውን በመጫን ይቀጥሉ)*"
        )
        await update.message.reply_text(msg, reply_markup=contact_keyboard, parse_mode="Markdown")
    else:
        await show_main_menu(update, user_id)

async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name
    phone_number = update.message.contact.phone_number

    custom_id = f"FB-{random.randint(1000, 9999)}"
    USER_DATABASE[user_id] = {
        "name": first_name,
        "phone": phone_number,
        "account_id": custom_id,
        "balance": 0.0
    }

    success_msg = f"🎉 **ምዝገባዎ በስኬት ተጠናቋል!**\n\n👤 **ስም:** {first_name}\n🆔 **የመለያ ቁጥር (ID):** `{custom_id}`\n📱 **ስልክ:** {phone_number}"
    await update.message.reply_text(success_msg, parse_mode="Markdown")
    
    await show_main_menu(update, user_id)

async def show_main_menu(update: Update, user_id: int):
    user_data = USER_DATABASE.get(user_id, {"account_id": f"FB-{user_id}", "balance": 0.0})
    web_app_url = "https://my-fastbingo-app.onrender.com"

    # የቦቱ ባነር/ሎጎ ምስል URL
    logo_url = "https://raw.githubusercontent.com/wendewende717-pixel/FastBingo/main/static/logo.jpg"

    keyboard = [
        [InlineKeyboardButton("🎮 ቢንጎ ተጫወት (Play)", web_app=WebAppInfo(url=web_app_url)), InlineKeyboardButton("📝 ምዝገባ", callback_data="reg")],
        [InlineKeyboardButton("💵 ቀሪ ሂሳብ (Balance)", callback_data="bal"), InlineKeyboardButton("💳 ብር መሙያ (Deposit)", callback_data="dep")],
        [InlineKeyboardButton("☎️ እገዛ (Support)", callback_data="sup"), InlineKeyboardButton("📖 መመሪያ (Instruction)", callback_data="inst")],
        [InlineKeyboardButton("🎁 ብር ማስተላለፊያ", callback_data="trans"), InlineKeyboardButton("🤑 ብር ማውጫ (Withdraw)", callback_data="with")],
        [InlineKeyboardButton("🔗 ጓደኛ ጋብዝ (Invite)", callback_data="inv"), InlineKeyboardButton("🔄 ቦነስ ቀይር", callback_data="bon")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_txt = (
        f"👋 👋 እንኳን ወደ **Fast Bingo NextGen Pro** በደህና መጡ!\n\n"
        f"🆔 **የእርስዎ ID:** `{user_data['account_id']}`\n"
        f"💰 **የአካውንትዎ ቀሪ ሂሳብ:** {user_data['balance']} ብር\n\n"
        f"ከታች ካሉት አማራጮች አንዱን ይምረጡ፦"
    )

    try:
        # ምስል ካለ በምስል ያወጣል፤ ካልሆነ ቀጥታ ፅሁፉን ይልካል
        await update.message.reply_photo(photo=logo_url, caption=welcome_txt, reply_markup=reply_markup, parse_mode="Markdown")
    except Exception:
        await update.message.reply_text(welcome_txt, reply_markup=reply_markup, parse_mode="Markdown")

# አዝራሮቹ ሲነኩ የሚሰጡት ምላሽ (Button Callbacks)
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    user_data = USER_DATABASE.get(user_id, {"account_id": f"FB-{user_id}", "balance": 0.0})

    data = query.data

    if data == "bal":
        await query.message.reply_text(f"💵 **የቀሪ ሂሳብ መረጃ**\n\n🆔 ID: `{user_data['account_id']}`\n💰 ቀሪ ሂሳብ: **{user_data['balance']} ብር**", parse_mode="Markdown")
    elif data == "dep":
        await query.message.reply_text("💳 **ብር መሙያ (Deposit)**\n\nበቴሌብር (Telebirr) ወይም ቻፓ (Chapa) ሂሳብዎን መሙላት ይችላሉ።\nለማስገባት የሚፈልጉትን የብር መጠን ይጻፉ፦", parse_mode="Markdown")
    elif data == "with":
        await query.message.reply_text("🤑 **ብር ማውጫ (Withdraw)**\n\nዝቅተኛ የማውጫ መጠን: **50 ብር**\nለማውጣት የሚፈልጉትን የብር መጠን ይጻፉ፦", parse_mode="Markdown")
    elif data == "sup":
        await query.message.reply_text("☎️️ **የደንበኞች እገዛ (Support)**\n\nለማንኛውም ጥያቄ ወይም አቤቱታ በቴሌግራም ያውሩን፦ @wende4366", parse_mode="Markdown")
    elif data == "inst":
        await query.message.reply_text("📖 **የጨዋታ መመሪያ (Instruction)**\n\n1. 'ቢንጎ ተጫወት' የሚለውን በመጫን ቦርዱን ይክፈቱ።\n2. ከ 1-600 ካርቴላዎች ውስጥ የሚፈልጉትን ይምረጡ።\n3. ቁጥሮች ሲጠሩ በራሱ ወይም በእጅዎ ይመልከቱ።\n4. ቀድመው ቢንጎ ሲሰሩ ያሸንፋሉ!", parse_mode="Markdown")
    elif data == "reg":
        await query.message.reply_text(f"📝 **የምዝገባ መረጃ**\n\nተመዝግበዋል! የሂሳብ መለያ ቁጥርዎ: `{user_data['account_id']}` ነው::", parse_mode="Markdown")
    elif data == "trans":
        await query.message.reply_text("🎁 **ብር ማስተላለፊያ (Transfer)**\n\nለሌላ ተጫዋች ብር ለማስተላለፍ የያዙትን ID ያስገቡ፦", parse_mode="Markdown")
    elif data == "inv":
        await query.message.reply_text(f"🔗 **ጓደኛ ይጋብዙ**\n\nይህንን የጋበዛ ሊንክ ለጓደኞችዎ በመላክ ቦነስ ያግኙ፦\nhttps://t.me/FastBingoBot?start={user_data['account_id']}", parse_mode="Markdown")
    elif data == "bon":
        await query.message.reply_text("🔄 **ቦነስ መመንዘሪያ**\n\nያለዎት የቦነስ ነጥብ: **0 Points** (100 Points = 10 ብር)", parse_mode="Markdown")

def main():
    threading.Thread(target=run_http_server, daemon=True).start()

    TOKEN = os.environ.get("BOT_TOKEN")
    if not TOKEN or TOKEN == "YOUR_BOT_TOKEN_HERE":
        TOKEN = "8156382103:AAH..." # <--- የቦትህ Token እዚህ ይግባ

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.CONTACT, contact_handler))
    app.add_handler(CallbackQueryHandler(button_callback))

    print("Fast Bingo Bot with Interactive Buttons is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
