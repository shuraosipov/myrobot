from telegram import Update
from telegram.ext import ContextTypes

async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message with the list of available commands."""
    
    # Define the list of available commands
    command_list = [
        "/hi - Проверить, в сети ли бот",
        "/sarah - Поговорить с ИИ",
        "/imagine - Создание изображений из текста",
        "/help - Показать это сообщение",
    ]


    # Join the command list into a single string
    command_text = "\n".join(command_list)

    # Send the command list to the user
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=f"Список команд:\n\n{command_text}"
    )