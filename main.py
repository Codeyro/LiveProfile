import os
import asyncio
import logging
from datetime import datetime
from telethon import TelegramClient, errors
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateProfileRequest


# Настройка логирования
logging.basicConfig(level=logging.WARN,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y.%m.%d %H:%M:%S')


# Конфигурация
API_ID = int(os.getenv('API_ID', 0))
API_HASH = os.getenv('API_HASH', '')
SESSION_STRING = os.getenv('SESSION_STRING', '')


# Изменение шрифта
def butificate(name):
    digits = "0123456789"
    bold_digits = "𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗"
    table = str.maketrans(digits, bold_digits)
    return name.translate(table)


async def main():
    # Подключаемся к серверам Telegram
    try:
        client = TelegramClient(
        StringSession(SESSION_STRING),
        API_ID,
        API_HASH
        )
        await client.start()
    except errors.rpcerrorlist.AuthKeyDuplicatedError as e:
        logging.critical(e)
    
    # Основной скрипт
    name = None
    while True:
        try :
            if not client.is_connected():
                await client.connect()

            if datetime.now().strftime('%H:%M') != name:
                name = datetime.now().strftime('%H:%M')
                
            name_b = butificate(name)

            await client(UpdateProfileRequest(first_name=name_b))
            logging.debug(f'Name changed to "{name_b }"')
        except errors.rpcerrorlist.FloodWaitError as e:
            logging.error(f'Flood Wait Error {e.seconds} seconds')
            await asyncio.sleep(e.seconds)
        except (ConnectionError, OSError) as e:
            logging.error(f'Network error: {e}. Retry to connect after 10 seconds...')
            await asyncio.sleep(10)
        except Exception as e:
            logging.exception(f'Unexcepted error: {e}')
            await asyncio.sleep(10)


if __name__ == '__main__':
    asyncio.run(main())
