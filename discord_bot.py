"""Discord adapter (discord.py 2.x). Env: DISCORD_TOKEN, ADMIN_IDS. Enable the Message Content intent for the bot."""
import os

import discord

from core import Store, handle

ADMINS = {s.strip() for s in os.getenv("ADMIN_IDS", "").split(",") if s.strip()}
store = Store(os.getenv("BOT_DB", "bot.db"))


def build() -> discord.Client:
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_message(message: discord.Message):
        if message.author.bot:
            return
        a = message.author
        reply = handle(store, message.content, str(a.id), a.display_name, str(a.id) in ADMINS)
        if reply:
            await message.reply(reply.text)

    return client


if __name__ == "__main__":
    build().run(os.environ["DISCORD_TOKEN"])
