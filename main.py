import os
import asyncio
import logging
from datetime import datetime
from telethon import TelegramClient, errors
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateProfileRequest


# Настройка логирования
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y.%m.%d %H:%M:%S')


# Конфигурация
API_ID = int(os.getenv('API_ID', 0))
API_HASH = os.getenv('API_HASH', '')
SESSION_STRING = os.getenv('SESSION_STRING', '')


# Изменение шрифта
def butificate(name):
    table = str.maketrans('0123456789', '𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗')
    return name.translate(table)


# Основной скрипт
async def main():
    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH, connection_retries=None, retry_delay=10)

    try:
        await client.start()
        logging.info('Successfully connected to Telegram.')
    
        while True:
            try :
                now = datetime.now()
                name = butificate(now.strftime('%H:%M'))

                await client(UpdateProfileRequest(first_name=name))
                logging.info(f'Name changed to "{name}"')

                sleep_time = 60 - now.second - (now.microsecond / 1000000) + 0.1
                await asyncio.sleep(max(sleep_time, 1))

            except errors.rpcerrorlist.FloodWaitError as e:
                logging.error(f'Flood Wait Error: Please, wait {e.seconds} seconds')
                await asyncio.sleep(e.seconds)
            except Exception as e:
                logging.exception(f'Unexcepted error: {e}')
                await asyncio.sleep(10)

    except Exception as e:
        logging.critical(f'Critical error: {e}')
    finally:
        await client.disconnect()
        logging.info("LiveProfile successfully stopped.")


if __name__ == '__main__':
    asyncio.run(main())
