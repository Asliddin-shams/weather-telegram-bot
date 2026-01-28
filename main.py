from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import requests
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEATHER_API = os.getenv("WEATHER_API")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌦 Ob-havo botiga xush kelibsiz!\n"
        "Shahar nomini yozing:\nMasalan: Toshkent"
    )

async def get_weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = update.message.text
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API}&units=metric&lang=uz"

    data = requests.get(url).json()

    if data.get("cod") != 200:
        await update.message.reply_text("❌ Shahar topilmadi")
        return

    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]
    wind = data["wind"]["speed"]

    await update.message.reply_text(
        f"📍 {city}\n"
        f"🌡 Harorat: {temp}°C\n"
        f"☁️ Holati: {desc}\n"
        f"💨 Shamol: {wind} m/s"
    )

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_weather))
app.run_polling()
