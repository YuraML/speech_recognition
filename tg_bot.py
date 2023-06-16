import logging
import os
import telegram

from dotenv import load_dotenv
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from services import create_session, get_response, TelegramLogsHandler

load_dotenv()

logger = logging.getLogger(__name__)


def start_command(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Привет {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Help!')


def reply_to_user(update: Update, context: CallbackContext) -> None:
    project_id = os.getenv('PROJECT_ID')
    session_id = os.getenv('CHAT_ID')
    text = update.message.text
    language_code = 'ru'

    try:
        session, session_client = create_session(project_id, session_id)
        response, is_fallback = get_response(session, session_client, text, language_code)
        if not response:
            response = "Не совсем понимаю, о чем вы. Можете уточнить?"

        update.message.reply_text(response)

    except Exception as e:
        logger.exception(f"Ошибка при обработке сообщения: {e}")


def main() -> None:
    token = os.getenv("TG_TOKEN")
    log_bot_token = os.getenv("TG_LOGS_TOKEN")
    chat_id = os.getenv('CHAT_ID')

    updater = Updater(token)
    dispatcher = updater.dispatcher

    bot = telegram.Bot(token=log_bot_token)

    logger.addHandler(TelegramLogsHandler(bot, chat_id))
    logger.setLevel(logging.INFO)

    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CommandHandler("help", help_command))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reply_to_user))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
