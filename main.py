import asyncio
from aiogram import Bot, Dispatcher
from handlers import registration_handler, order_handler
from config import TOKEN
from database import Database

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # Initialize database connection
    Database.open()
    
    dp.include_router(registration_handler.router)
    dp.include_router(order_handler.router)
    
    try:
        await dp.start_polling(bot)
    finally:
        Database.close()

if __name__ == '__main__':
    asyncio.run(main())