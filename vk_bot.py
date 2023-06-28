import os
import random
import vk_api as vk
import logging
import telegram

from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType

from services import create_session, get_response, TelegramLogsHandler

logger = logging.getLogger(__name__)


def reply_to_user(project_id, event, vk_api):
    session, session_client = create_session(project_id, str(event.user_id))
    answer, is_fallback = get_response(session, session_client, event.text, 'ru')
    if not is_fallback and answer:
        vk_api.messages.send(user_id=event.user_id, message=answer, random_id=random.randint(1, 1000))


def main():
    load_dotenv()
    token = os.getenv("VK_TOKEN")
    log_bot_token = os.getenv("TG_LOGS_TOKEN")
    chat_id = os.getenv('CHAT_ID')
    project_id = os.getenv('PROJECT_ID')
    vk_session = vk.VkApi(token=token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    bot = telegram.Bot(token=log_bot_token)

    logger.addHandler(TelegramLogsHandler(bot, chat_id))
    logger.setLevel(logging.INFO)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            try:
                reply_to_user(project_id, event, vk_api)
            except Exception as e:
                logger.exception(f"Ошибка при обработке сообщения: {e}")


if __name__ == "__main__":
    main()
