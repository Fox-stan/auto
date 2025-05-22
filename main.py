import asyncio
import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ChatJoinRequestHandler,
    ContextTypes,
)
from flask import Flask
import threading

BOT_TOKEN = os.getenv("BOT_TOKEN")

# === Словарь для хранения временных данных пользователей ===
user_contexts = {}

# Flask-сервер для UptimeRobot
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "✅ Бот працює!"

def run_flask():
    flask_app.run(host="0.0.0.0", port=8080)

# Когда пользователь отправил запрос на вступление
async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.chat_join_request.from_user
    chat_id = user.id
    username = user.first_name

    user_contexts[chat_id] = {
        "username": username
    }

    # Заменить YourBotUsername на юзернейм вашего бота!
    start_link = "https://t.me/Nst_auto_bot?start=ok"
    caption = (
        f"{username}, Підтвердіть що ви не робот🤖"
        f"<a href='{start_link}'>/start</a>. "
        f"Після чого ваша заявка буде вам повторно надіслано."
    )

    with open("2.jpeg", "rb") as img:
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=img,
            caption=caption,
            parse_mode="HTML"
        )

def main():
    threading.Thread(target=run_flask).start()
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(ChatJoinRequestHandler(handle_join_request))
    app.run_polling()

if __name__ == "__main__":
    main()
