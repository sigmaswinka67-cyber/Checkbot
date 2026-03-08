from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from database import get_bots
from datetime import datetime, timedelta

TOKEN = "8682526573:AAGbptMJxR5HtYZoyUTBrfSNvtgS9ppJe8w"

keyboard = [
    ["📊 All bots"],
    ["🟢 Online bots"],
    ["🔴 Offline bots"]
]

markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def format_bots(mode="all"):

    bots = get_bots()

    text = ""

    for bot in bots:

        last = datetime.fromisoformat(bot[2])

        online = datetime.utcnow() - last < timedelta(minutes=10)

        if mode == "online" and not online:
            continue

        if mode == "offline" and online:
            continue

        status = "🟢 ONLINE" if online else "🔴 OFFLINE"

        text += f"""
🤖 {bot[0]}
{status}
status: {bot[1]}
last: {bot[2]}

"""

    if text == "":
        text = "No bots"

    return text


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Bot Monitor",
        reply_markup=markup
    )


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    txt = update.message.text

    if txt == "📊 All bots":
        await update.message.reply_text(format_bots("all"))

    elif txt == "🟢 Online bots":
        await update.message.reply_text(format_bots("online"))

    elif txt == "🔴 Offline bots":
        await update.message.reply_text(format_bots("offline"))

print('bot started')
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, buttons))


app.run_polling()
