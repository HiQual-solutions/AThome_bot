import os

from aiogram import Bot
from dotenv import load_dotenv

load_dotenv(".env")

# print(os.getenv("2TG_TOKEN"))
bot = Bot(token=os.getenv("TEST_TG_TOKEN"))
