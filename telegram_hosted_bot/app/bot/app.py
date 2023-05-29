# Standard library imports
import logging
import os
import importlib
import json


# Third party imports
from dotenv import load_dotenv
from telegram import __version__ as TG_VER
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Load environment variables from .env file
load_dotenv()

# Set up TELEGRAM credentials
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

# Version check
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

### Enable logging.
LOGLEVEL = os.environ.get("LOGLEVEL", "INFO").upper()
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
logger.setLevel(LOGLEVEL)


class ApplicationBuilder:
    def __init__(self, token):
        self.token = token
        self.command_handlers = {}
        self.message_handlers = []
        self.error_handler = None
        self._builder = Application.builder().token(self.token)

    def command(self, command):
        """Register a command handler."""
        def decorator(func):
            self.command_handlers[command] = func
            return func
        return decorator

    def message(self, filter):
        """Register a message handler."""
        def decorator(func):
            self.message_handlers.append((filter, func))
            return func
        return decorator

    def error(self, func):
        """Register an error handler."""
        self.error_handler = func
        return func

    def build(self):
        application = self._builder.build()
        for command, handler in self.command_handlers.items():
            application.add_handler(CommandHandler(command, handler))
        for filter, handler in self.message_handlers:
            application.add_handler(MessageHandler(filter, handler))
        if self.error_handler:
            application.add_error_handler(self.error_handler)
        return application

    def load_handlers(self, filename):
        with open(filename) as f:
            data = json.load(f)

        for handler in data["handlers"]:
            module = importlib.import_module(handler["module"])
            function = getattr(module, handler["function"])
            if handler["type"] == "command":
                for command in handler["command"]:
                    self.command(command)(function)
            elif handler["type"] == "message":
                filter = getattr(filters, handler["filter"])
                self.message(filter)(function)



def main() -> None:
    """Start the bot."""
    application_builder = ApplicationBuilder(TELEGRAM_TOKEN)

    # Load handlers from json file
    application_builder.load_handlers('handlers.json')

    # Create the Application and pass it your bot's token.
    application = application_builder.build()

    # print sticker details to the console
    # application.add_handler(MessageHandler(filters.Sticker.ALL, print_sticker_details))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
