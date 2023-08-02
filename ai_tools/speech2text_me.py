import io
import pydub
import speech_recognition


def speech2text_me(file_path):
    f = pydub.AudioSegment.from_file(io.BytesIO(file_path)).export(format='wav')
    recognator = speech_recognition.Recognizer()
    with speech_recognition.AudioFile(f) as source:
        audio_data = recognator.record(source)
    out = recognator.recognize_google(audio_data, language="ru")
    return out