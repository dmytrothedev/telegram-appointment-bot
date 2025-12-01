from datetime import date, datetime

from telegram import KeyboardButton, ReplyKeyboardMarkup


def get_time_slot() -> list[str]:
    return [f"{hour:02d}:00" for hour in range(10, 22)]


def build_time_keyboard(selected_date: date, taken_slots: list[str]):
    slots = get_time_slot()
    now = datetime.now()
    today = now.date()
    current_hour = now.hour

    keyboard = []
    row = []

    for slot in slots:
        if slot in taken_slots:
            continue

        hour = int(slot.split(":")[0])
        if selected_date == today and hour <= current_hour:
            continue

        row.append(KeyboardButton(slot))

        if len(row) == 3:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    if not keyboard:
        keyboard = [[KeyboardButton("No available time slots")]]

    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
