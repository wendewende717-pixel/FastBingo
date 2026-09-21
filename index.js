const { Telegraf, Markup } = require('telegraf');
const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// የ ቦት ቶከን (Bot Token)
const BOT_TOKEN = process.env.BOT_TOKEN || 'YOUR_TELEGRAM_BOT_TOKEN';
const bot = new Telegraf(BOT_TOKEN);

// Web App URL (Render URL)
const WEB_APP_URL = 'https://fastbingo.onrender.com';

// Static ፋይሎችን ማስተናገድ
app.use(express.static(path.join(__dirname, 'public')));

// ዋናው ገጽ ሲጠየቅ ወደ rooms.html መምራት
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'rooms.html'));
});

// Telegram Bot Command (/start)
bot.start((ctx) => {
    ctx.reply(
        'እንኳን ወደ Fast Bingo በሰላም መጡ! 🎲\n\nጨዋታውን ለመጀመር ከታች ያለውን አዝራር ይጫኑ።',
        Markup.inlineKeyboard([
            [Markup.button.webApp('🎮 ጨዋታውን ጀምር', `${WEB_APP_URL}/rooms.html`)]
        ])
    );
});

// Express Server ማስነሳት
app.listen(PORT, () => {
    console.log(`Bingo Server is running on port ${PORT}`);
});

// Bot ማስነሳት
bot.launch().then(() => {
    console.log('Bingo Server & Bot በመስራት ላይ ይገኛል...');
}).catch((err) => {
    console.error('Bot Launch Error:', err);
});

// process termination handling
process.once('SIGINT', () => bot.stop('SIGINT'));
process.once('SIGTERM', () => bot.stop('SIGTERM'));
