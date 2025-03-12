import telebot
import google.generativeai as genai
import schedule
import time
import threading
import os

# Load environment variables (you can use dotenv for better security)
TELEGRAM_BOT_TOKEN = "your-telegram-bot-token"
GEMINI_API_KEY = "your-gemini-api-key"

# Initialize bot
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Configure Gemini AI
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# Dictionary to store users
subscribed_users = set()


# Function to generate a daily question
def get_daily_question():
    prompt = "Generate a unique and engaging question for daily discussion."
    response = model.generate_content(prompt)
    return response.text if response else "What's your favorite memory?"


# Function to send daily questions to all users
def send_daily_question():
    question = get_daily_question()
    for chat_id in subscribed_users:
        bot.send_message(chat_id, f"🌟 Daily Question: {question}")


# Schedule the daily question (you can adjust the time)
schedule.every().day.at("10:00").do(send_daily_question)


# Run the scheduler in a separate thread
def schedule_runner():
    while True:
        schedule.run_pending()
        time.sleep(60)


threading.Thread(target=schedule_runner, daemon=True).start()


# Command to start the bot and subscribe users
@bot.message_handler(commands=["start"])
def start(message):
    chat_id = message.chat.id

    if message.chat.type in ["group", "supergroup"]:
        subscribed_users.add(chat_id)
        bot.reply_to(message, "✅ This group is now subscribed to daily questions!")
    else:
        subscribed_users.add(chat_id)
        bot.reply_to(message, "✅ You have subscribed to daily questions!")


# Start polling
bot.polling()
