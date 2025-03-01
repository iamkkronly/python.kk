import telebot
import requests
import json

# Bot Configurations
TELEGRAM_BOT_TOKEN = "7798993298:AAH8bXJWWmz4nL9JzpgGN0GIyBJ_UWdHY3c"
GEMINI_API_KEY = "AIzaSyDJc-B4LNpfT0ArVLnZTZd0hkSb5rG-jkU"

# Bot Personalization
BOT_NAME = "iamkkronly"  # Change this to your bot's name
WELCOME_MESSAGE = f"Hello! I'm {BOT_NAME}, your AI assistant. Ask me anything!"
BOT_PERSONALITY = "You are a friendly and helpful AI, always providing clear and concise answers.Movies channel:https://t.me/freemovieslight Anime channel: https://t.me/freeanimelight Chat Support(movies):https://t.me/chgtmovie"

# Initialize Telegram Bot
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Google Gemini API URL
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

# Function to get AI response from Gemini
def get_gemini_response(user_input):
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{
            "parts": [{"text": f"{BOT_PERSONALITY}\n\nUser: {user_input}\n\nAI:"}]
        }]
    }

    response = requests.post(GEMINI_API_URL, headers=headers, json=data)

    if response.status_code == 200:
        try:
            result = response.json()
            print("API Response:", json.dumps(result, indent=2))  # Debugging

            # Extract response text
            return result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No response found.")
        except Exception as e:
            print("Parsing Error:", str(e))
            return "Sorry, I couldn't process the response correctly."
    else:
        print("API Error:", response.status_code, response.text)  # Debugging
        return f"API Error: {response.status_code} - {response.text}"

# Start Command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, WELCOME_MESSAGE)

# AI Response Handler
@bot.message_handler(func=lambda message: True)
def chat_with_gemini(message):
    try:
        response = get_gemini_response(message.text)
        bot.reply_to(message, response)
    except Exception as e:
        print("Bot Error:", str(e))  # Debugging
        bot.reply_to(message, "Sorry, I encountered an error. Please try again later.")

# Run the bot
print(f"{BOT_NAME} is running...")
bot.infinity_polling()