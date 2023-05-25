import random
from telegram import Update, Message
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

async def send_thinking_message_async(message) -> Message:
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
    print(type(thinking_message))
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


async def handle_voice_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle a voice message by replying with a voice message."""
    message = update.message
    voice = message.voice

    # Get the voice file ID
    voice_file_id = voice.file_id

    # Reply with a voice message
    #message.reply_voice(voice=voice_file_id)
    print("voice message received")
    print(voice_file_id)