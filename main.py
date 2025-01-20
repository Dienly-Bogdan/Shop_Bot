import asyncio

from aiogram import Bot, Dispatcher
import handlers.handler

from config import TOKEN

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    dp.include_routers(handlers.handler.router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
