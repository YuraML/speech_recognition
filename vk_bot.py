import os
import random
import vk_api as vk

from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType

from services import create_session, get_response

load_dotenv()


def reply_to_user(event, vk_api):
    project_id = os.getenv('PROJECT_ID')
    session, session_client = create_session(project_id, str(event.user_id))
    response = get_response(session, session_client, event.text, 'ru')
    if not response:
        response = "Не совсем понимаю, о чем вы. Можете уточнить?"
    vk_api.messages.send(user_id=event.user_id, message=response, random_id=random.randint(1, 1000))


if __name__ == "__main__":
    token = os.getenv("VK_TOKEN")
    vk_session = vk.VkApi(token=token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            reply_to_user(event, vk_api)
