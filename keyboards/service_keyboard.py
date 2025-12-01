from telegram import KeyboardButton, ReplyKeyboardMarkup

from config import SERVICES


def build_service_keyboard():
    keyboard = []
    for service in SERVICES:
        keyboard.append([KeyboardButton(service)])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
