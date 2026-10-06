import os
import re
import asyncio
from threading import Thread

from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", "10000"))

web_app = Flask(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎮 VOK CODM CHECKER\n\n"
        "Gamitin:\n"
        "/check <UID>\n\n"
        "Halimbawa:\n"
        "/check 123456789"
    )


async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "❌ Ilagay ang UID.\n\n"
            "Halimbawa: /check 123456789"
        )
        return

    uid = context.args[0]

    if not re.fullmatch(r"\d{5,20}", uid):
        await update.message.reply_text(
            "❌ Invalid UID.\n"
            "Numbers lamang ang ilagay."
        )
        return

    await update.message.reply_text(
        f"🔎 Checking UID: {uid}\n\n"
        "✅ UID format is valid.\n"
        "ℹ️ Account lookup API is not connected yet."
    )


def run_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("check", check))

    application.run_polling(
        drop_pending_updates=True,
        stop_signals=None
    )


@web_app.route("/")
def home():
    return "VOK CODM CHECKER is running!"


if __name__ == "__main__":
    bot_thread = Thread(target=run_bot, daemon=True)
    bot_thread.start()

    web_app.run(
        host="0.0.0.0",
        port=PORT
    )
