from telegram import Update
from telegram.ext import ContextTypes

async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)