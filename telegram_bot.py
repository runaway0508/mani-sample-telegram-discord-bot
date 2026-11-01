"""Telegram adapter (python-telegram-bot v21). Env: TELEGRAM_TOKEN, ADMIN_IDS=comma-separated user ids."""
import os

from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters

from core import Store, handle

ADMINS = {s.strip() for s in os.getenv("ADMIN_IDS", "").split(",") if s.strip()}
store = Store(os.getenv("BOT_DB", "bot.db"))


async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    u, msg = update.effective_user, update.effective_message
    reply = handle(store, msg.text, str(u.id), u.full_name, str(u.id) in ADMINS)
    if reply:
        await msg.reply_text(reply.text)


def build(token: str) -> Application:
    app = Application.builder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT, on_message))
    return app


if __name__ == "__main__":
    build(os.environ["TELEGRAM_TOKEN"]).run_polling()
