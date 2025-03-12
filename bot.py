import os
import telebot
import google.generativeai as genai
import schedule
import time
import threading
from dotenv import load_dotenv
import logging

# Enable logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# List of daily questions
daily_questions = [
    "What’s one thing you learned today? 📚",
    "How do you feel right now? 😊",
    "What’s your biggest goal this week? 🎯",
    "What’s something that made you smile today? 😃",
    "What would you do differently if you could restart today? 🔄",
]

# Load environment variables
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not TELEGRAM_BOT_TOKEN:
    logger.error("TELEGRAM_BOT_TOKEN environment variable is missing.")
    exit(1)

# Initialize bot
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

logger.info("Bot is starting...")

# Configure Gemini AI
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# Store subscribed users/groups
subscribed_chats = set()


# Function to generate a daily question
def get_daily_question():
    prompt = "Generate a unique and engaging question for daily discussion."
    response = model.generate_content(prompt)
    return response.text if response else "What's your favorite memory?"


# Function to send daily questions
def send_daily_question():
    question = get_daily_question()
    for chat_id in subscribed_chats:
        bot.send_message(chat_id, f"🌟 Daily Question: {question}")


# Schedule daily question (10:00 AM)
schedule.every().day.at("16:59").do(send_daily_question)


# Run scheduled tasks in a separate thread
def schedule_runner():
    while True:
        schedule.run_pending()
        time.sleep(60)


threading.Thread(target=schedule_runner, daemon=True).start()


# Handle /start command (for users & groups)
@bot.message_handler(commands=["start"])
def start(message):
    logger.debug(f"Received /start command from {message.chat.id}")
    chat_id = message.chat.id
    subscribed_chats.add(chat_id)

    if message.chat.type in ["group", "supergroup"]:
        bot.reply_to(message, "✅ This group is now subscribed to daily questions!")
    else:
        bot.reply_to(message, "✅ You have subscribed to daily questions!")


# Handle /start command (for users & groups)
@bot.message_handler(commands=["start_daily", "start_daily@daily_jim_bot"])
def start_daily(message):
    logger.debug(f"Received /start_daily command from {message.chat.id}")

    if message.chat.type in ["group", "supergroup"]:
        bot.reply_to(message, "Starting the daily questions! 📢")
        send_daily_question()
    else:
        bot.reply_to(message, "This command only works in a group chat. 😊")


# Start the bot
bot.polling()
