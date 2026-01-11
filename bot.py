import asyncio
import sqlite3 
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from database import init_db, update_price
from main import get_dns_prices_stealth
from apscheduler.schedulers.asyncio import AsyncIOScheduler

API_TOKEN = '8069282045:AAF57Bmau-bZzib_doEVHXWkHzZZ6dnnQMY'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

async def check_prices():
    print("--- Запускаю плановую проверку цен по расписанию ---")
    conn = sqlite3.connect('prices.db')
    cursor = conn.cursor()
    cursor.execute('SELECT url, last_price FROM products')
    items = cursor.fetchall()
    conn.close()

    for url, old_price in items:
        prices = get_dns_prices_stealth(url)
        if prices:
            new_price = max(prices)
            if new_price < old_price:
                message_text = f"📢 ЦЕНА УПАЛА!\nТовар: {url}\nСтарая цена: {old_price}\nНовая цена: {new_price}"
                print(message_text)
                update_price(url, new_price)
            else:
                print(f"Цена для {url} не изменилась или выросла.")
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_name = message.from_user.full_name if message.from_user else "Пользователь"
    print(f"Получена команда /start от {user_name}") 
    await message.answer(f"Привет, {user_name}! Пришли мне ссылку на товар DNS, и я запомню его цену.")

@dp.message()
async def handle_message(message: types.Message):
    if message.text and "dns-shop.ru" in message.text:
        url = message.text
        print(f"Получена ссылка: {url}")
        await message.answer("Смотрю цену... Это займет около 15 секунд.")
        
        prices = get_dns_prices_stealth(url)
        
        if prices:
            current_price = max(prices) 
            update_price(url, current_price)
            await message.answer(f"✅ Товар добавлен!\nТекущая цена: {current_price} руб.\nЯ сообщу, если она изменится.")
        else:
            await message.answer("❌ Не удалось достать цену. Возможно, сайт заблокировал запрос.")
    elif message.text:
        await message.answer("Пожалуйста, пришли корректную ссылку на сайт dns-shop.ru.")

async def start_bot():
    print("--- Инициализация системы ---")
    try:
        init_db()
        print("✅ 1. База данных готова")
        
        scheduler = AsyncIOScheduler()
        scheduler.add_job(check_prices, "interval", minutes=60)
        scheduler.start()
        print("✅ 2. Планировщик проверок запущен")
        
        print("✅ 3. Бот запущен и готов к работе в Telegram!")
        await dp.start_polling(bot)
    except Exception as e:
        print(f"❌ Критическая ошибка при запуске: {e}")

if __name__ == '__main__':
    asyncio.run(start_bot())