import os
import requests
import sys
import xml.etree.ElementTree as ET
#ключ к API яндекса
key = "c4cc1e86-0e2b-47f6-b392-8d17bfbbc464"
#базовый текст
text = "Тестовый текст"
#функция синтеза голоса
def TTS (key = key,
         text = text,
         path="speech",
         audio_format = "mp3",
         lang = "ru-RU", speaker = "oksana",
         emotion = "neutral",
         **kwargs):
    #ссылка для запроса
    TTS_URL = "https://tts.voicetech.yandex.net/generate"
    MAX_CHARS = 2000
    #параметны GET запроса
    params = {
            "speaker": speaker,
            "format": audio_format,
            "key": key,
            "lang": lang,
            "emotion":emotion,
            "text":text
        }
    params.update(kwargs)
    #выполнение запроса и создание файла
    data = requests.get(TTS_URL, params=params, stream=False).iter_content()
    extension = "." + params["format"]
    if os.path.splitext(path)[1] != extension:
        path += extension
    #запись в файл
    with open(path, "wb") as f:
        for d in data:
            f.write(d)
#функция распознавания голоса
def STT(key = key,
        path="record.mp3",
        topic = "queries",
        lang = "ru-RU",
        antimat = "true",
        **kwargs):
    #ссылка для запроса
    STT_URL = "https://asr.yandex.net/asr_xml?"
    #параметны POST запроса
    params = {
        "key":key,
        "topic":topic,
        "uuid":"56d9e9b4da2c8e49c1ad1bf6a698d2f1",
        "lang":lang,
        "disableAntimat":antimat,
        }
    #заголовки запроса
    headers = {
        "Content-Type":"audio/x-mpeg-3",
        }
    #данные запроса
    BFile = open(path, "rb")
    BFile = BFile.read()
    #выполнение запроса
    with requests.post(STT_URL, params = params, headers = headers, data=BFile) as r:
        xml = r.iter_content()
        extension = ".asp"
        answer = "answer"
        if os.path.splitext(answer)[1] != extension:
            answer += extension
        #запись в файл
        with open(answer, "wb") as f:
            for d in xml:
                f.write(d)
        for variant in ET.parse(answer).findall('./variant'):
            print(variant.text)
    
    
