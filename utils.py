from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import os


# Изменение шрифта
def butificate(name):
    table = str.maketrans('0123456789', '𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗')
    return name.translate(table)


# Конвертация даты и времени в строку
def datetime_string(dt: datetime) -> str:

    def hour_to_12_hour_format(h: int) -> int:
        return h % 12 if h % 12 != 0 else 12
    
    # Склонение слова "час"
    def get_hour_form(h: int) -> str:
        if h == 0:
            return "часов"
        last_digit = h % 10
        last_two_digits = h % 100
        if last_digit == 1 and last_two_digits != 11:
            return "час"
        elif last_digit in (2, 3, 4) and last_two_digits not in (12, 13, 14):
            return "часа"
        else:
            return "часов"

    # Часть суток
    def get_time_period(h: int) -> str:
        if 0 <= h <= 4 or h == 23:
            return "ночи"
        elif 5 <= h <= 11:
            return "утра"
        elif 12 <= h <= 17:
            return "дня"
        else:  # 18-22
            return "вечера"

    if not isinstance(dt, datetime):
        raise ValueError("Аргумент должен быть объектом datetime")

    hour = dt.hour
    hour_12 = hour_to_12_hour_format(hour)
    day = dt.day
    month = dt.month
    year = dt.year

    # Месяцы в родительном падеже
    months_genitive = {
        1: "января", 2: "февраля", 3: "марта", 4: "апреля",
        5: "мая", 6: "июня", 7: "июля", 8: "августа",
        9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
    }

    hours_word = get_hour_form(hour_12)
    period = get_time_period(hour)
    month_str = months_genitive[month]

    return (f"Сейчас\n{hour_12} {hours_word}\n{period},\n{day} {month_str}\n{year} года").upper()


# Аватарка из текста
def string_avatar(
    text: str,
    output_file: str = "avatar.png",
    size: int = 512,
    font_path: str = "fonts/Tokeely Brookings.ttf"
):
    # Белый фон
    img = Image.new("RGB", (size, size), "white")
    draw = ImageDraw.Draw(img)

    # Автоподбор размера шрифта
    font_size = 60
    while font_size > 12:
        font = ImageFont.truetype(font_path, font_size)

        bbox = draw.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]

        if w < size * 0.85:
            break

        font_size -= 2

    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    x = (size - w) // 2
    y = (size - h) // 2

    draw.text((x, y - 5), text, font=font, fill="black")

    img.save(output_file)
