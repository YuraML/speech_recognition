# speech_recognition
 
Два чат-бота, работающих на платформе Google [DialogFlow](https://dialogflow.cloud.google.com/#/login): один для Telegram и другой для VK. Оба бота обрабатывают пользовательские запросы и предоставляют ответы, используя возможности DialogFlow.

![bot](https://dvmn.org/media/filer_public/1e/f6/1ef61183-56ad-4094-b3d0-21800bdb8b09/demo_vk_bot.gif)

### Примеры ботов

Cсылки на примеры работающих ботов:

- [Бот](https://t.me/speechrecon_bot) для Telegram
- [Бот](https://vk.com/public221134484) для VK (в сообщениях группе)


### Что такое DialogFlow?

DialogFlow - это платформа для понимания естественного языка, предоставляемая Google. Она используется для создания разговорных приложений, способных понимать и отвечать на пользовательские запросы естественным, похожим на человеческий, образом.

### Запуск на сервере

Сперва необходимо клонировать репозиторий, выполнив команду:
```shell
$ git clone https://github.com/YuraML/speech_recognition.git
```
После копирования проекта запустите виртуальное окружение:

```shell
$ python3 -m venv env
$ source env/bin/activate
```

Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```

Также для работы программы необходимо создать файл `.env`, заполненный следующим образом:

```
VK_TOKEN={Ваш токен бота VK}
TG_TOKEN={Ваш токен бота Telegram}
TG_LOGS_TOKEN={Ваш токен бота Telegram для логирования}
PROJECT_ID={ID вашего проекта в Google Cloud}
CHAT_ID={ID чата Telegram}
GOOGLE_APPLICATION_CREDENTIALS={путь до файла application_default_credentials.json}
```
Получить ID чата можно [здесь](https://t.me/userinfobot), а получение файла application_default_credentials.json описано [вот тут](https://cloud.google.com/dialogflow/es/docs/quick/setup#sdk).

### Запуск

Для запуска ботов введите в командную строку:

```console
python3 tg_bot.py
```
или
```console
python3 vk_bot.py
```

Скрипт работает непрерывно, 24/7.

### Создание новых интентов с помощью JSON

В проекте представлен скрипт intents.py, который позволяет создавать новые интенты для Dialogflow через JSON файл.

Интент в Dialogflow - это набор тренировочных фраз и ответов, который используется для обучения искусственного интеллекта пониманию и реагированию на определенные запросы пользователя.

- Создайте файл intents.json в корне вашего проекта.

Структура файла должна быть следующей:

```json
{
    "Название вашего интента": {
        "questions": [
            "Вопрос 1",
            "Вопрос 2",
             ...
        ],
        "answer": "Ответ бота на вопросы выше"
    },
    "..."
}
```

- Запустите скрипт intents.py.

```console
python3 intent.py
```

После выполнения этих шагов, новые интенты, которые вы указали в файле intents.json, будут созданы в вашем Dialogflow агенте. Их можно увидеть и редактировать в консоли Dialogflow.

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
