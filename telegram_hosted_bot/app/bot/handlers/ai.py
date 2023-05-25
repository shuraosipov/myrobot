from collections import deque

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatAction

from handlers.utils import send_thinking_message_async

from extentions.chat_gpt import get_chat_response_async


async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the '/ai' command by simulating a human-like conversation using OpenAI's GPT-X model.
    """

    # Inform the user that the bot is processing their message
    await context.bot.send_chat_action(chat_id=update.effective_chat.id,action=ChatAction.TYPING)
    thinking_message = await send_thinking_message_async(update.message)

    # Get the conversation history for this chat
    conversation_history = context.chat_data.get(update.message.chat_id, deque([], maxlen=15))
    
    # Add the new message to the conversation history
    conversation_history.append(update.message.text)

    # Generate a thoughtful response using the conversation history
    response = await get_chat_response_async(update.message.text, conversation_history)

    # Respond to the user by editing the thinking message
    await thinking_message.edit_text(text=response)

    # Store the updated conversation history
    context.chat_data[update.message.chat_id] = conversation_history