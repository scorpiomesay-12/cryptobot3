import os
import sqlite3
import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from flask import Flask
from threading import Thread

# ሎጊንግ ማስተካከል
logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN", "7870015707:AAEqqSaPXC-oxofRmMXF7TY6EMA56X61EnE")
ADMIN_ID = 1705750284  # የቦቱ አድሚን (Owner) መታወቂያ

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ----------------- ዳታቤዝ ማዘጋጀት -----------------
def init_db():
    conn = sqlite3.connect("bot_database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            type TEXT,
            amount TEXT,
            payment_method TEXT,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ----------------- የዋናው ሜኑ በተኖች (ለአድሚን እና ለተጠቃሚ የሚለዩበት) -----------------
def get_main_menu(user_id: int):
    if user_id == ADMIN_ID:
        # አድሚን ከሆነ ብቻ የሚታዩ በተኖች (አድሚን ፓነልን ጨምሮ)
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="💸 Buy USDT"), KeyboardButton(text="💵 Sell USDT")],
                [KeyboardButton(text="📊 My Orders"), KeyboardButton(text="🛠 Customer Support")],
                [KeyboardButton(text="👑 Admin Panel")]
            ],
            resize_keyboard=True
        )
    else:
        # መደበኛ ተጠቃሚዎች የሚያዩዋቸው በተኖች (አድሚን ፓነል ከቶውንም አይታይም)
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="💸 Buy USDT"), KeyboardButton(text="💵 Sell USDT")],
                [KeyboardButton(text="📊 My Orders"), KeyboardButton(text="🛠 Customer Support")],
                [KeyboardButton(text="ℹ️ Help & Rates")]
            ],
            resize_keyboard=True
        )
    return keyboard

# ----------------- /start ትእዛዝ -----------------
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_name = message.from_user.first_name
    user_id = message.from_user.id
    
    welcome_text = (
        f"👋 ሰላም <b>{user_name}</b>!\n\n"
        f"ወደ ኦፊሴላዊው የ USDT Crypto Exchange ቦት እንኳን ደህና መጡ።\n"
        f"በቀላል እና ደህንነቱ በተጠበቀ ሁኔታ USDT መግዛት ወይም መሸጥ ይችላሉ።\n\n"
        f"ልዩ የምንዛሬ ዋጋዎች:\n"
        f"• <b>Buy Rate:</b> 185 ETB\n"
        f"• <b>Sell Rate:</b> 170 ETB\n\n"
        f"እባክዎ ከታች ከሚገኙት አማራጮች አንዱን ይምረጡ 👇"
    )
    
    await message.answer(welcome_text, parse_html=True, reply_markup=get_main_menu(user_id))

# ----------------- Customer Support -----------------
@dp.message(F.text == "🛠 Customer Support")
async def customer_support(message: types.Message):
    support_text = (
        "🛠 <b>Customer Support Center</b>\n\n"
        "⏳ <b>Payment delay may fix within 24 hr</b>\n\n"
        "ማንኛውም ጥያቄ ወይም የክፍያ መዘግየት ካጋጠመዎት በቀጥታ አድሚናችንን ማግኘት ይችላሉ፦\n"
        "👤 Admin: @HDIlII"
    )
    await message.answer(support_text, parse_html=True)

# ----------------- Buy USDT -----------------
@dp.message(F.text == "💸 Buy USDT")
async def buy_usdt(message: types.Message):
    text = (
        "📥 <b>USDT ለመግዛት (Buy USDT)</b>\n\n"
        "የምንዛሬ ዋጋ: <b>185 ETB</b>\n"
        "የሚፈልጉትን የክፍያ አማራጭ ይምረጡ እና ከታች የተሰጠውን መለያ በመጠቀም ክፍያውን ፈጽሙ:\n\n"
        "🇪🇹 <b>Telebirr:</b> <code>0966868001</code>\n"
        "🏦 <b>CBE (የንግድ ባንክ):</b> <code>1000650255821</code>\n"
        "🟡 <b>Binance UID:</b> <code>893287919</code>\n"
        "🟣 <b>Bybit UID:</b> <code>359670410</code>\n\n"
        "ክፍያ ከፈጸሙ በኋላ ደረሰኙን (Receipt) ለአድሚን @HDIlII ይላኩ!"
    )
    await message.answer(text, parse_html=True)

# ----------------- Sell USDT -----------------
@dp.message(F.text == "💵 Sell USDT")
async def sell_usdt(message: types.Message):
    text = (
        "📤 <b>USDT ለመሸጥ (Sell USDT)</b>\n\n"
        "የምንዛሬ ዋጋ: <b>170 ETB</b>\n"
        "USDT የሚልኩበትን ትክክለኛ መለያ (UID) ወይም የባንክ/ቴሌብር ቁጥርዎን ከአድሚን ጋር ለመነጋገር እባክዎ በቀጥታ ያነጋግሩን።\n\n"
        "👤 Admin: @HDIlII"
    )
    await message.answer(text, parse_html=True)

# ----------------- Admin Panel -----------------
@dp.message(F.text == "👑 Admin Panel")
async def admin_panel(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("⚠️ ይህ ትእዛዝ ለባለቤቱ (Owner) ብቻ የተፈቀደ ነው!")
        return
    
    text = (
        "👑 <b>Admin Control Panel</b>\n\n"
        "እንኳን ደህና መጡ አድሚን! የቦቱ ባለቤት መሆንዎ ተረጋግጧል።"
    )
    await message.answer(text, parse_html=True)

# ----------------- Flask Web Server -----------------
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running live!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

async def main():
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())