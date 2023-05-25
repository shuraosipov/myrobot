from collections import deque

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatAction

from handlers.utils import send_thinking_message_async

from extentions.chat_gpt import get_chat_response_async


async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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