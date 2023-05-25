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
        chat_id=update.effective_chat.id, text="I'm online and ready to chat!"
    )