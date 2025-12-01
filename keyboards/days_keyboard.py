from datetime import date, timedelta

from telegram import KeyboardButton, ReplyKeyboardMarkup


def get_next_seven_days() -> list[str]:
    today = date.today()
    return [(today + timedelta(days=i)).strftime("%d.%m") for i in range(7)]


def build_days_keyboard():
    dates = get_next_seven_days()
    keyboard = []
    row = []
    for day in dates:
        row.append(KeyboardButton(day))
        if len(row) == 3:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
