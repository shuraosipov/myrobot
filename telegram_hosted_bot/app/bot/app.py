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
from telegram import ForceReply, Update, BotCommand
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from telegram.constants import ChatAction, ParseMode

from const import TELEGRAM_TOKEN
from auth import oauth_check_user_authentication, login
from commands import passwd, caps


from extentions.openai_talk import call_openai
from extentions.lex_talk import call_lex
from extentions.list_google_calendars import calendar
from extentions.chat_gpt import get_chat_response_async, get_image_response

### Enable logging.
LOGLEVEL = os.environ.get("LOGLEVEL", "INFO").upper()
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
logger.setLevel(LOGLEVEL)

### Define a command handlers.

async def online(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Test that the bot is online, up and running."""

    # add a typing action to show the bot is doing something
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.TYPING
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm online and ready to chat!"
    )

async def hi(update: Update, context: ContextTypes.DEFAULT_TYPE):
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



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


async def ai(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Call the OpenAI API Completion endpoint to simulate human-like conversation."""

    # [Visual effects] - add a typing action to show the bot is doing something
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.TYPING
    )

    # Get the user message
    message = update.message

    # Get the chat id
    chat_id = update.message.chat_id

    # Send the "thinking" message
    thinking_message = await send_thinking_message_async(message)

    # Get the conversation history for this chat
    conversation_history = context.chat_data.get(chat_id, deque([], maxlen=15))

    # Add the new message to the conversation history
    conversation_history.append(update.message.text)
    # print(conversation_history)

    # Call the chat_completion function
    response = await get_chat_response_async(message.text, conversation_history)

    # Replace the "thinking" message with the chatbot's response
    await thinking_message.edit_text(text=response)

    # Store the updated conversation history in the context
    context.chat_data[chat_id] = conversation_history


async def imagine(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Call the OpenAI API Image endpoint to generate an image from a given prompt."""

    # Get the user message
    message = update.message

    # Send the "thinking" message
    thinking_message = await send_thinking_message_async(message)

    # Get image url from openai
    response = await get_image_response(message.text)

    text = f"<a href=\"{response}\">Open image in Browser</a>"

    # Change the "thinking" message with the chatbot's response
    await thinking_message.edit_text(text=text, parse_mode=ParseMode.HTML)


""" Utility functions for bot responses to make them more human-like """


async def send_thinking_message_async(message):
    """Send a "thinking" message to the chat."""
    # Define a list of thinking emojis
    thinking_emojis = ["🤔", "💭", "😶‍🌫️"]

    # Choose a random thinking emoji
    thinking_emoji = random.choice(thinking_emojis)

    # Prepare the text with HTML formatting
    text = f"<b>On it, one moment...</b> {thinking_emoji}"

    # Send the thinking message to the chat
    thinking_message = await message.reply_text(
        text=text, reply_to_message_id=message.message_id, parse_mode=ParseMode.HTML
    )

    # Return the thinking message object
    return thinking_message



async def print_sticker_details(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Print the details of a sticker pasted to the chat."""
    message = update.message
    sticker = message.sticker

    # Print the sticker details
    print(f"Sticker ID: {sticker.file_id}")
    print(f"Sticker Set Name: {sticker.set_name}")
    print(f"Sticker Emoji: {sticker.emoji}")
    print(f"Sticker File Size: {sticker.file_size} bytes")


    

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

    # say hi
    application.add_handler(CommandHandler("hi", hi))

    # check online status
    application.add_handler(CommandHandler("online", online))

    # define a command handler with multiple aliases
    application.add_handler(CommandHandler(["ai", "sarah"], ai))

    # generate image from text
    application.add_handler(CommandHandler("imagine", imagine))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))


    # print sticker details to the console
    # application.add_handler(MessageHandler(filters.Sticker.ALL, print_sticker_details))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
