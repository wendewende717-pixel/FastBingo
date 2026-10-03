elif data == "inst":
        await query.message.reply_text("📖 የጨዋታ መመሪያ (Instruction)\n\n1. 'ቢንጎ ተጫወት' የሚለውን በመጫን ቦርዱን ይክፈቱ።\n2. ከ 1-600 ካርቴላዎች ውስጥ የሚፈልጉትን ይምረጡ።\n3. ቁጥሮች ሲጠሩ በራሱ ወይም በእጅዎ ይመልከቱ።\n4. ቀድመው ቢንጎ ሲሰሩ ያሸንፋሉ!", parse_mode="Markdown")
    elif data == "reg":
        await query.message.reply_text(f"📝 የምዝገባ መረጃ\n\nተመዝግበዋል! የቋሚ መለያ ቁጥርዎ: {user_data['account_id']} ነው::", parse_mode="Markdown")
    elif data == "trans":
        await query.message.reply_text("🎁 ብር ማስተላለፊያ (Transfer)\n\nለሌላ ተጫዋች ብር ለማስተላለፍ የያዙትን ID ያስገቡ፦", parse_mode="Markdown")
    elif data == "inv":
        await query.message.reply_text(f"🔗 ጓደኛ ይጋብዙ\n\nይህንን የጋበዛ ሊንክ ለጓደኞችዎ በመላክ ቦነስ ያግኙ፦\nhttps://t.me/FastBingoBot?start={user_data['account_id']}", parse_mode="Markdown")
    elif data == "bon":
        await query.message.reply_text("🔄 ቦነስ መመንዘሪያ\n\nያለዎት የቦነስ ነጥብ: 0 Points (100 Points = 10 ብር)", parse_mode="Markdown")

def main():
    threading.Thread(target=run_http_server, daemon=True).start()

    TOKEN = os.environ.get("BOT_TOKEN")
    if not TOKEN or TOKEN == "YOUR_BOT_TOKEN_HERE":
        TOKEN = "8234368672:AAHaTtqt08OpQQmrDDjknqtdhH66FeF5Oss" # <--- የቦትህ Token

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.CONTACT, contact_handler))
    app.add_handler(CallbackQueryHandler(button_callback))

    print("Fast Bingo Bot running with Banner Header & Database...")
    app.run_polling()

if name == "main":
    main()
