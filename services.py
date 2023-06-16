import logging

from google.cloud import dialogflow


class TelegramLogsHandler(logging.Handler):
    def __init__(self, bot, chat_id):
        super().__init__()
        self.bot = bot
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)


def create_session(project_id, session_id):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    return session, session_client


def get_response(session, session_client, text, language_code):
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(request={"session": session, "query_input": query_input})
    return response.query_result.fulfillment_text, response.query_result.intent.is_fallback
