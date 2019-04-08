#импорт внешних библиотек
import requests
import urllib.request
import json
#импорт внутренних скриптов
import path_settings
import yandex_settings
#функция синтеза речи
def text_to_speech(text, name):
    url = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'
    headers = {
        'Authorization': 'Bearer ' + yandex_settings.iam_token,
    }
    data = {
        'text': text,
        'voice': 'oksana',
        'emotion': 'good',
        'folderId': yandex_settings.folder_id,
        'format': 'oggopus',
        'sampleRateHertz': 48000,
    }
    resp = requests.post(url, headers=headers, data=data)
    if resp.status_code != 200:
        return 0
    with open(path_settings.ogg_speech_path + name + path_settings.ogg_format, 'wb') as f:
        f.write(resp.content)
    return 1
#функция распознавания речи
def speech_to_text(name):
    with open(path_settings.ogg_record_path + name +  path_settings.ogg_format, "rb") as f:
        data = f.read()

    params = "&".join([
        "topic=general",
        "folderId=%s" % yandex_settings.folder_id,
        "lang=ru-RU",
        "sampleRateHertz=48000"
    ])
    url = urllib.request.Request("https://stt.api.cloud.yandex.net/speech/v1/stt:recognize/?%s" % params, data = data)
    url.add_header("Authorization", "Bearer %s" % yandex_settings.iam_token)
    url.add_header("Transfer-Encoding", "chunked")

    responseData = urllib.request.urlopen(url)
    responseData = responseData.read().decode('UTF-8')
    decodedData = json.loads(responseData)
        
    if decodedData.get("error_code") is None:
        return decodedData.get("result")