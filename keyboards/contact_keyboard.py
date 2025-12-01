from telegram import KeyboardButton, ReplyKeyboardMarkup


def build_contact_keyboard():
    keyboard = [
        [KeyboardButton("📱 Share your contact", request_contact=True)],
        [KeyboardButton("✏️ Enter contact manually")],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
