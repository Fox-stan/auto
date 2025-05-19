
import asyncio
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    ChatJoinRequestHandler,
    ContextTypes,
)
from flask import Flask
import threading

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Мини Flask-сервер для поддержки активности (например, от UptimeRobot)
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "✅ Бот працює!"

def run_flask():
    flask_app.run(host="0.0.0.0", port=8080)

# === Telegram логика ===
async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.chat_join_request.from_user
    chat_id = user.id
    username = user.first_name

    context.user_data["chat_id"] = chat_id
    context.user_data["username"] = username

    with open("2.jpeg", "rb") as img:
        message = await context.bot.send_photo(
            chat_id=chat_id,
            photo=img,
            caption=f"{username}, Підтвердіть що ви не робот🤖",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Підтвердити ✅", callback_data="verify")],
            ])
        )
    context.user_data["last_message_id"] = message.message_id

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    chat_id = context.user_data.get("chat_id")
    username = context.user_data.get("username")

    if "last_message_id" in context.user_data:
        await context.bot.delete_message(chat_id=chat_id, message_id=context.user_data["last_message_id"])

    # 2 сообщение
    with open("1.jpeg", "rb") as img:
        message = await context.bot.send_photo(
            chat_id=chat_id,
            photo=img,
            caption=f"{username}, УВАГА❗️
ОБОВʼЯЗКОВА ПЕРЕВІРКА!

👇 Підтвердіть, що вам є 18 років?",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Мені є 18 ✅", url="https://t.me/YOUR_LINK")],
                [InlineKeyboardButton("Мені немає 18 ❌", url="https://t.me/YOUR_LINK")],
                [InlineKeyboardButton("Пропустити", url="https://t.me/YOUR_LINK")],
            ])
        )
    await asyncio.sleep(3)

    # 3 сообщение
    message = await context.bot.send_message(chat_id=chat_id, text="Запит знаходиться в обробці...⌛")
    await asyncio.sleep(3)
    await context.bot.delete_message(chat_id=chat_id, message_id=message.message_id)

    # 4 сообщение
    with open("3.jpeg", "rb") as img:
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=img,
            caption=f"{username}, Просимо вас вказати свою стать!

❗ Оберіть свою стать та натисніть на неї ❗",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Я ЖІНКА 👩", url="https://t.me/YOUR_LINK")],
                [InlineKeyboardButton("Я ЧОЛОВІК 👨", url="https://t.me/YOUR_LINK")],
            ])
        )
    await asyncio.sleep(2)

    # 5 сообщение
    message = await context.bot.send_message(chat_id=chat_id, text="У вас залишилось 10 секунд ☝️")
    await asyncio.sleep(10)
    await context.bot.delete_message(chat_id=chat_id, message_id=message.message_id)

    # 6 сообщение
    with open("4.jpeg", "rb") as img:
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=img,
            caption=f"{username}, Оберіть свою область!",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("СХІДНІ ОБЛАСТІ", url="https://t.me/YOUR_LINK")],
                [InlineKeyboardButton("ЦЕНТРАЛЬНІ ОБЛАСТІ", url="https://t.me/YOUR_LINK")],
                [InlineKeyboardButton("ЗАХІДНІ ОБЛАСТІ", url="https://t.me/YOUR_LINK")],
                [InlineKeyboardButton("• ПІДВЕННІ ОБЛАСТІ", url="https://t.me/YOUR_LINK")],
                [InlineKeyboardButton("• ПІВНІЧНІ ОБЛАСТІ", url="https://t.me/YOUR_LINK")],
            ])
        )

    # 7 сообщение
    with open("5.jpeg", "rb") as img:
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=img,
            caption=f"🔔 {username}, Ваша заявка схвалена,
для отримання доступу натисніть «ПІДТВЕРДИТИ»",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("ПІДТВЕРДИТИ ✅", url="https://t.me/YOUR_LINK")],
            ])
        )

def main():
    threading.Thread(target=run_flask).start()

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(ChatJoinRequestHandler(handle_join_request))
    app.add_handler(CallbackQueryHandler(handle_button))
    app.run_polling()

if __name__ == "__main__":
    main()
