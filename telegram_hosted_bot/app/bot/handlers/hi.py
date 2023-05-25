import random
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatAction

async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Test that the bot is online, up and running."""

    # add a typing action to show the bot is doing something
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.TYPING
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Hey! I'm online and ready to chat!"
    )

    # jinxpowder stickers ;)
    stickers = [
        "CAACAgIAAxkBAAIKLGRuiw0frKVyGY47-NPoNh_7xWzLAAKTGwACVoFBSYxpB21uy7wjLwQ", 
        "CAACAgIAAxkBAAEhkVdkbN9OBb4Bz1jHo7LncM4gAzuYHwACkhgAAmi5OUnF93JLwz5cVC8E",
        "CAACAgIAAxkBAAIKMGRui4GNZn3S5Fb4sAkhx3pLN90wAAI4GQACe19ASY731Aqr2LJMLwQ"
    ]

    await context.bot.send_sticker(
        chat_id=update.effective_chat.id, sticker=random.choice(stickers),
    )