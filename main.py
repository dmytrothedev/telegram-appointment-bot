from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from config import (
    ASK_COMMENT,
    ASK_CONTACT,
    ASK_DAY,
    ASK_NAME,
    ASK_PREF_TIME,
    ASK_SERVICE,
    CONFIRM,
    TOKEN,
)
from db import init_db
from handlers.mhandlers import (
    ask_name,
    ask_contact,
    handle_contact_from_button,
    handle_contact_from_text,
    handle_service,
    ask_time,
    ask_comment,
    ask_confirm,
    confirm,
    cancel,
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome! This bot helps you book an appointment. Send /apply to start your request."
    )


async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Admin panel is not available in this demo.")


def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin))

    main_convo_handler = ConversationHandler(
        entry_points=[CommandHandler("apply", ask_name)],
        states={
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_contact)],
            ASK_CONTACT: [
                MessageHandler(filters.CONTACT, handle_contact_from_button),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_contact_from_text),
            ],
            ASK_SERVICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_service)],
            ASK_DAY: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_time)],
            ASK_PREF_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_comment)],
            ASK_COMMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_confirm)],
            CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(main_convo_handler)
    init_db()
    app.run_polling()


if __name__ == "__main__":
    main()
