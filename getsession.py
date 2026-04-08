import os
import logging
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession


# Настройка логирования
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y.%m.%d %H:%M:%S')


# Конфигурация
API_ID = int(os.getenv('API_ID', 0))
API_HASH = os.getenv('API_HASH', '')
SESSION_STRING = os.getenv('SESSION_STRING', '')


async def main():
    async with TelegramClient(StringSession(), API_ID, API_HASH) as client:
        print("Session string:", client.session.save())

if __name__ == '__main__':
    asyncio.run(main())
