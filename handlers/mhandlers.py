from datetime import date

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from config import (
    ADMIN_IDS,
    ASK_COMMENT,
    ASK_CONTACT,
    ASK_DAY,
    ASK_NAME,
    ASK_PREF_TIME,
    ASK_SERVICE,
    CONFIRM,
    SERVICES,
)
from db import add_application, get_taken_slots
from keyboards.contact_keyboard import build_contact_keyboard
from keyboards.days_keyboard import build_days_keyboard
from keyboards.pref_time_keyboard import build_time_keyboard
from keyboards.service_keyboard import build_service_keyboard


async def ask_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please enter your name.")
    return ASK_NAME


async def ask_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text(
        "Choose how you'd like to share your contact.",
        reply_markup=build_contact_keyboard(),
    )
    return ASK_CONTACT


async def handle_contact_from_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone = update.message.contact.phone_number
    context.user_data["phone"] = phone
    await update.message.reply_text(
        "Your phone number has been saved.\n\nNow choose a service:",
        reply_markup=build_service_keyboard(),
    )
    return ASK_SERVICE


async def handle_contact_from_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "✏️ Enter contact manually":
        await update.message.reply_text("Please enter your phone number.")
        return ASK_CONTACT

    context.user_data["phone"] = text
    await update.message.reply_text(
        "Contact saved!\n\nChoose a service below:",
        reply_markup=build_service_keyboard(),
    )
    return ASK_SERVICE


async def handle_service(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text not in SERVICES:
        await update.message.reply_text("Please use the buttons below and do not type your own text.")
        return ASK_SERVICE

    context.user_data["service"] = text
    await update.message.reply_text(
        "Service saved. Please choose a day from the list below.",
        reply_markup=build_days_keyboard(),
    )
    return ASK_DAY


async def ask_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    day_text = update.message.text
    today = date.today()
    parts = day_text.split(".")

    try:
        day = int(parts[0])
        month = int(parts[1])
    except Exception:
        await update.message.reply_text("Please choose a date using the buttons below.")
        return ASK_DAY

    selected_date = date(today.year, month, day)
    context.user_data["day"] = day_text

    taken = get_taken_slots(service=context.user_data["service"], day=day_text)

    await update.message.reply_text(
        "Got it. Now choose a time you prefer:",
        reply_markup=build_time_keyboard(selected_date, taken),
    )
    return ASK_PREF_TIME


async def ask_comment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["pref_time"] = update.message.text
    await update.message.reply_text(
        "Got it.\n"
        "If you want, you can add a comment (for example, preferred specialist or extra details).\n"
        "If you don't want to add anything, just write '-'"
    )
    return ASK_COMMENT


async def ask_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["comment"] = update.message.text
    name = context.user_data["name"]
    phone = context.user_data["phone"]
    service = context.user_data["service"]
    day = context.user_data["day"]
    pref_time = context.user_data["pref_time"]
    comment_saved = context.user_data["comment"]
    summary = (
        "Please confirm your application:\n\n"
        f"Name: {name}\n"
        f"Phone: {phone}\n"
        f"Service: {service}\n"
        f"Day: {day}\n"
        f"Time: {pref_time}\n"
        f"Comment: {comment_saved}\n\n"
        "If everything is correct, write 'yes'. To cancel, write 'no'."
    )

    await update.message.reply_text(summary)
    return CONFIRM


async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower().strip()

    if text in ("yes", "y"):
        user_id = update.effective_user.id
        username = update.effective_user.username
        name = context.user_data["name"]
        phone = context.user_data["phone"]
        service = context.user_data["service"]
        day = context.user_data["day"]
        pref_time = context.user_data["pref_time"]
        comment_saved = context.user_data["comment"]
        add_application(user_id, username, name, phone, service, day, pref_time, comment_saved)

        admin_text = (
            "New application received\n\n"
            f"Name: {name}\n"
            f"Phone: {phone}\n"
            f"Service: {service}\n"
            f"Day: {day}\n"
            f"Time: {pref_time}\n"
            f"Comment: {comment_saved}\n"
            f"Username: @{username}\n"
            f"User ID: {user_id}"
        )

        for admin_id in ADMIN_IDS:
            await context.bot.send_message(chat_id=admin_id, text=admin_text)

        await update.message.reply_text("Your application has been saved.")
        return ConversationHandler.END

    if text in ("no", "n"):
        await update.message.reply_text("Application cancelled.")
        return ConversationHandler.END

    await update.message.reply_text("Please write 'yes' or 'no'.")
    return CONFIRM


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Application cancelled.")
    return ConversationHandler.END
