import logging
import asyncio
from configparser import ConfigParser
from telethon import TelegramClient
from telethon.sessions import StringSession


# Настройка логирования
logging.basicConfig(level=logging.INFO,
                    filename="liveprofile.log",
                    filemode="w",
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y.%m.%d %H:%M:%S')

# Чтение учетныех данных
try:
    config = ConfigParser()
    config.read('config.ini')

    api_id = int(config['Telegram']['api_id'])
    api_hash = config['Telegram']['api_hash']
    phone = config['Telegram']['phone']
except Exception as e:
    logging.critical(f'Config data read error: {e}')

async def main():
    async with TelegramClient(StringSession(), api_id, api_hash) as client:
        print("Session string:", client.session.save())

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())