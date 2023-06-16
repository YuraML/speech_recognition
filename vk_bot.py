import os
import random
import vk_api as vk
import logging
import telegram

from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType, TelegramLogsHandler

from services import create_session, get_response

load_dotenv()

logger = logging.getLogger(__name__)


def reply_to_user(event, vk_api):
    project_id = os.getenv('PROJECT_ID')
    try:
        session, session_client = create_session(project_id, str(event.user_id))
        answer, is_fallback = get_response(session, session_client, event.text, 'ru')
        if not is_fallback and answer:
            vk_api.messages.send(user_id=event.user_id, message=answer, random_id=random.randint(1, 1000))
    except Exception as e:
        logger.exception(f"Ошибка при обработке сообщения: {e}")


if __name__ == "__main__":
    token = os.getenv("VK_TOKEN")
    log_bot_token = os.getenv("TG_LOGS_TOKEN")
    chat_id = os.getenv('CHAT_ID')

    vk_session = vk.VkApi(token=token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    bot = telegram.Bot(token=log_bot_token)

    logger.addHandler(TelegramLogsHandler(bot, chat_id))
    logger.setLevel(logging.INFO)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            reply_to_user(event, vk_api)
