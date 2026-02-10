import os
import asyncio
import logging
from datetime import datetime
from telethon import TelegramClient, errors
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateProfileRequest


# Настройка логирования
logging.basicConfig(level=logging.INFO,
                    filename="liveprofile.log",
                    filemode="w",
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y.%m.%d %H:%M:%S')


# Чтение учетных данных
try:
    api_id = int(os.getenv('API_ID', 0))
    api_hash = os.getenv('API_HASH', '')
    session_string = StringSession(os.getenv('SESSION_STRING', ''))
except Exception as e:
    logging.critical(f'Config data read error: {e}')


# Изменение шрифта
def butificate(name):
    name = name.replace('0', '𝟎')
    name = name.replace('1', '𝟏')
    name = name.replace('2', '𝟐')
    name = name.replace('3', '𝟑')
    name = name.replace('4', '𝟒')
    name = name.replace('5', '𝟓')
    name = name.replace('6', '𝟔')
    name = name.replace('7', '𝟕')
    name = name.replace('8', '𝟖')
    name = name.replace('9', '𝟗')
    name = name.replace(':', ':')
    return name


async def main():
    # Подключаемся к серверам Telegram
    try:
        client = TelegramClient(
        session_string,
        api_id,
        api_hash
        )
        await client.start()
    except errors.rpcerrorlist.AuthKeyDuplicatedError as e:
        logging.critical(e)
    
    # Основной скрипт
    i = 1
    name = None
    while True:
        if datetime.now().strftime('%H:%M') != name:
            try :
                name = datetime.now().strftime('%H:%M')
                name_b = butificate(name)
                await client(UpdateProfileRequest(first_name=name_b))
                logging.debug(f'Name changed to "{name_b }"')
            except errors.rpcerrorlist.FloodWaitError as e:
                logging.error(f'Flood Wait Error {e.seconds} seconds')
            except ConnectionError as e:
                logging.error(e)
            i += 1


if __name__ == '__main__':
    asyncio.run(main())
