from telegram import Update
from telegram.ext import ContextTypes

async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message with the list of available commands."""
    
    # Define the list of available commands
    command_list = [
        "/start - Start the bot",
        "/hi - Say hi to the bot",
        "/online - Check if the bot is online",
        "/ai or /sarah - Talk to the AI",
        "/imagine - Generate a random text",
        "/help - Show this help message",
    ]

    # Join the command list into a single string
    command_text = "\n".join(command_list)

    # Send the command list to the user
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=f"Available commands:\n{command_text}"
    )