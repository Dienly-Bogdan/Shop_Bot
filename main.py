import asyncio

from aiogram import Bot, Dispatcher
from handlers import registration_handler, order_handler

from config import TOKEN

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    dp.include_routers(registration_handler.router)
    dp.include_routers(order_handler.router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
