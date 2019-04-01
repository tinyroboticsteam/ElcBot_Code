import requests
# функция получения iam токена
def get():
	try:
		return requests.post('https://iam.api.cloud.yandex.net/iam/v1/tokens','{"yandexPassportOauthToken": %a}' % OAuth).json()['iamToken']
	except Exception:
		print("no iam_token")
#настройки данных API Cloud Yandex
folder_id = 'b1gr0dsacthnti50v9vv' #ссылка на каталок проекта
OAuth = 'AQAAAAAXChLbAATuwTs6m5EmEkNDvEJ_JNQ-r9w' #OAuth код аккаунта
iam_token = get() #получение iam токена
#