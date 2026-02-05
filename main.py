import logging
import asyncio
from configparser import ConfigParser
from datetime import datetime
from telethon import TelegramClient, errors
from telethon.tl.functions.account import UpdateProfileRequest


# Считываем учетные данные
config = ConfigParser()
config.read('config.ini')

api_id = int(config['Telegram']['api_id'])
api_hash = config['Telegram']['api_hash']
phone = config['Telegram']['phone']

logging.debug('Config data read successfully')


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
        client = TelegramClient('liveprofile', api_id, api_hash)
        await client.start(phone=phone)
    except errors.rpcerrorlist.AuthKeyDuplicatedError as e:
        logging.critical(e)

    logging.debug('Connected to Telegram servers successfully')
    
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
            except ConnectionError:
                logging.error('Connection error. Trying to connect again...')
            i += 1


if __name__ == '__main__':
    asyncio.run(main())
