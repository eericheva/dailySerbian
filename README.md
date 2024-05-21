## dailySerbian

@dailySerbianBot

## I am a bot-translator from Russian to Serbian and from Serbian to Russian.

Here's what you should know about me:

I can translate all sorts of things: text, documents, voice messages. I also send voice messages with the translation.

Just send me something in Russian or in Serbian, and I'll figure out what to do with it.

I can also create a separate dictionary for you and occasionally spam words from there so you can practice your vocabulary. I adapt the dictionary to your knowledge and often send words that you have translated recently or made mistakes with during training.

### ML part is implemented using open libraries:

- I have some pydantic and json-schema inplementation

[comment]: <> (- For the user dictionary database, I use json)
- Translation text -> text:
    - ``` deep_translator.GoogleTranslator(source="ru", target="sr") ```
- Recognizer speech -> text:
    - ``` speech_recognition.Recognizer() ```
- Text -> speech:
    - ``` gtts.gTTS(text, lang="sr", slow=False) ```
- Image -> text:
  - ```easyocr.Reader(lang_list=["en", "ru"])```
- Sourse language detection:
  - ```deep_translator.single_detection()```

### I have some CI/CD configured:

- Lint with pre-commit-hooks, flake8, blake
- Test with pytest + Generate Coverage Report
- Build, Test and Deploy to Heroku hosting with Github Actions
- Deploy with Docker Compose

### TODO - what I'm not yet capable of product-wise

- Word self-training (Russian->Serbian) --> in progress
- Setting self-training time and word spam time

### TODO - what I'm not yet capable of technically

- Postgre database
- Test coverage

### TODO - open ai_tools, it would be interesting to try

- Multiple translation options as output
- TEXT 2 SPEECH
    - https://faun.pub/python-text-to-speech-tutorial-b0031f6664a0
    - https://www.codingem.com/best-ai-voice-generators/
- Interact with ChatGPT
    - https://medium.com/@andrea.faviait/deploying-a-telegram-bot-using-chatgpt-and-whisper-apis-with-railway-ef79e6cff955
