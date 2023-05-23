import logging
import os
import asyncio
import aiohttp
import random
from collections import deque
from aiohttp import ClientSession
import openai

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from telegram.constants import ChatAction

from const import TELEGRAM_TOKEN
from auth import oauth_check_user_authentication, login
from commands import passwd, echo, caps


from extentions.openai_talk import call_openai
from extentions.lex_talk import call_lex
from extentions.list_google_calendars import calendar
from extentions.chat_gpt import get_chat_response_async



# Enable logging
LOGLEVEL = os.environ.get("LOGLEVEL", "INFO").upper()
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
logger.setLevel(LOGLEVEL)

async def online(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Test that the bot is online, up and running."""

    # add a typing action to show the bot is doing something
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm online and ready to chat!")

# Define a command handlers.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)

async def ai(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    """Get the user message."""
    message = update.message

    # Get the chat id
    chat_id = update.message.chat_id

    # Get the conversation history for this chat
    conversation_history = context.chat_data.get(chat_id, deque([], maxlen=15))

    # Add the new message to the conversation history
    conversation_history.append(update.message.text)

    # Send the initial "thinking" message immediately

    thinking_emojis = ["🤔", "💭", "🧐"]
    thinking_message = await message.reply_text(text=random.choice(thinking_emojis), reply_to_message_id=message.message_id)
    

    # Call the chat_completion function

    print(conversation_history)

    response = await get_chat_response_async(message.text, conversation_history)
    
    # After a delay of 1-2 seconds, update the "thinking" message with the chatbot's response
    await thinking_message.edit_text(text=response)
    
    # Store the updated conversation history in the context
    context.chat_data[chat_id] = conversation_history 

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Send a "hello" message to the chat when the bot starts up
    # def send_hello(update, context):
    #     update.message.reply_text("Hello! I'm your bot. How can I help you today?")
    # application.add_handler(CommandHandler("start", send_hello))

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))

    # check online status
    application.add_handler(CommandHandler("online", online))

    # define a command handler with multiple aliases
    application.add_handler(CommandHandler(["ai", "sarah", "imagine"], ai))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()

if __name__ == '__main__':

    main()