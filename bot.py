import os
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")


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
            "❌ Invalid UID. Numbers lamang ang ilagay."
        )
        return

    await update.message.reply_text(
        f"🔎 Checking UID: {uid}\n\n"
        "✅ UID format is valid.\n"
        "ℹ️ Kailangan pa ng legitimate CODM data API "
        "para makuha ang tunay na player information."
    )


def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is not configured")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
