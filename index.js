const { Telegraf, Markup } = require('telegraf');
const express = require('express');
const app = express();

app.use(express.static('public'));

const bot = new Telegraf('8234368672:AAEWNj58YASdxqbQmvRmeeINLlMpNfDoz10');

bot.start((ctx) => ctx.reply('እንኳን ወደ Fast Bingo በደህና መጡ! 🎲', Markup.inlineKeyboard([
  [Markup.button.webApp('🎮 ጨዋታውን ክፈት (Mini App)', 'https://fastbingo-bot.onrender.com')]
])));

bot.launch();
app.listen(3000, () => console.log('Bingo Server & Bot በመስራት ላይ ይገኛሉ...'));
