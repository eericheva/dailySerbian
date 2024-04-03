# dailySerbian

@dailySerbianBot

## Я бот-переводчик с русского языка на сербский язык и с сербского на русский.

Вот что ты должен знать обо мне:

Я могу переводить всякое: текст, документы, войсы. Также я присылаю войс с озвучиванием перевода. Просто пришли мне что
нибудь на русском, а я подумаю, что с этим можно сделать.

Еще я могу создать для тебя отдельный словарь и спамить оттуда словами время от времени, чтобы ты мог тренировать свой
словарь. Я адаптирую словарь под твои знания и чаще присылаю те слова, которые ты переводил недавно, или ошибся во время
тренировки.

### TODO - то что я пока не умею продуктово

- несколько вариантов переводов
- перевод фото и картинок
- тренировка слов (русский->сербский)
- настройка времени тренировки и времени спама слов

### Технически я реализован на открытых библиотеках:

- под капотом у меня pydantic
- в качестве базы данных для словаря пользователя я использую json
- перевод text -> text:
    - deep_translator.GoogleTranslator(source="ru", target="sr")
- recognizer speech -> text:
    - speech_recognition.Recognizer()
- text -> speech_me:
    - gtts.gTTS(text, lang="sr", slow=False)

### У меня настроен некоторый CICD:

- Lint with flake8
- Test with pytest + Generate Coverage Report

### TODO - то, что я не умею пока технически

- размещене на хостинге
    - https://docs.github.com/en/actions/deployment/about-deployments/deploying-with-github-actions#finding-deployment-examples
    - localhost https://djangostars.com/blog/how-to-create-and-deploy-a-telegram-bot/
- localhost
    - self-hosted
      runners https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/about-self-hosted-runners
- база данных на Postgre
- покрытие тестами

### TODO - open ai_tools, которые было бы интересно попробовать

- TEXT 2 SPEECH
    - https://faun.pub/python-text-to-speech-tutorial-b0031f6664a0
    - https://www.codingem.com/best-ai-voice-generators/
- interact with ChatGPT
    - https://medium.com/@andrea.faviait/deploying-a-telegram-bot-using-chatgpt-and-whisper-apis-with-railway-ef79e6cff955
