import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
import logging

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if TELEGRAM_BOT_TOKEN is None:
    print("Failed to fetch the telegram token")

# List of daily questions
daily_questions = [
    "What did you do today? 👩‍💻",
    "How long did it took? ⏳",
    "What are you going to do tommorow? 🎯",
    "Do you have any blockers? 😃",
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message when the /start command is issued."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hello! Use /start_daily to receive daily questions.",
    )


async def send_daily_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send daily questions."""
    questions = "\n".join(daily_questions)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=questions)


# async def main():
#     """Main function to start the bot."""
#     app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

#     app.add_handler(CommandHandler("start", start))
#     # app.add_handler(CommandHandler("start_daily", send_daily_question))

#     logger.info("Bot is running...")
#     await app.run_polling()


if __name__ == "__main__":
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    start_handler = CommandHandler("start", start)
    start_daily_handler = CommandHandler("start_daily", send_daily_question)
    application.add_handler(start_handler)
    application.add_handler(start_daily_handler)

    application.run_polling()
