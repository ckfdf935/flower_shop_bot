from aiogram import Bot, Dispatcher, types
from os import getenv
from dotenv import load_dotenv
from handlers import router
from SQL import Database
import asyncio


load_dotenv()

async def main():
    bot = Bot(getenv("TOKEN"))
    dp = Dispatcher()
    flowers_db = Database('flowers_data.db')
    dp.include_router(router)
    print("Starting bot...")
    await dp.start_polling(bot,  flowers_db=flowers_db)


if __name__ == "__main__":
    asyncio.run(main())
