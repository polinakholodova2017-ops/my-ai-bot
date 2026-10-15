from flask import Flask
import threading
import telebot
from groq import Groq

app = Flask(__name__)

TELEGRAM_TOKEN = "8938035681:AAE1g9sgbd0H0jPYya7vNNm-p0T_cg9SzF0"
GROQ_API_KEY = "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"

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = Groq(api_key=GROQ_API_KEY)

@app.route('/')
def home():
    return "Bot is running"

@app.route('/health')
def health():
    return "OK"

@bot.message_handler(content_types=['text'])
def handle_message(message):
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": message.text}],
            model="llama-3.1-8b-instant",
        )
        ai_answer = chat_completion.choices[0].message.content
        bot.reply_to(message, ai_answer)
    except Exception as e:
        bot.reply_to(message, "Error")

def run_bot():
    bot.polling(none_stop=True)

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=10000)
