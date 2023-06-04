import random
from telegram import Update, Message
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from datetime import datetime
import uuid
from langdetect import detect

def detect_language(message: str) -> str:
    """
    Detect the language of a message using the langdetect library.
    """
    try:
        return detect(message)
    except Exception as e:
        return "Error: " + str(e)

async def send_thinking_message_async(message) -> Message:
    """Send a "thinking" message to the chat."""
    
    # Define a list of thinking emojis
    thinking_emojis = ["🤔", "💭", "😶‍🌫️"]

    # Choose a random thinking emoji
    thinking_emoji = random.choice(thinking_emojis)

    # reply to the chat on the same language as user prompt
    if message.text is not None:
        language = detect_language(message.text.replace("/sarah ", ""))
        print("language: ", language)
    else:
        language = "en"

    # Prepare the text with HTML formatting
    if language == "en":
        text = f"<b>On it, one moment...</b> {thinking_emoji}"
    elif language == "ru":
        text = f"<b>Думаю...</b> {thinking_emoji}"
    else:
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





    
    
    