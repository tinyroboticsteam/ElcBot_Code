#импорт внешних библиотек
import RPi.GPIO as GPIO
#иморт внутренних скриптов
import speech
import system
import chat
#инициализация переменных GPIO
KEY = 4
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(KEY, GPIO.IN)
flag = True
#функция выполняемая по нажатию кнопки
def run():
    try:
        system.play("listen") #воспроизведение предупреждения о начале записи
        system.record("record") #запись голосовой команды
        text = speech.speech_to_text("record") #преобразование голосовой записи в текстовую строку
        answer = chat.get_answer(text) #получение ответа из преобразованной фразы
        if answer != "":
            speech.text_to_speech(answer, "temp") #синтез ответа в голосовую запись
            system.convert("temp") #конвертация ответа в необходимый формат
            system.play("temp") #воспроизведение ответа через динамики
    except Exception:
        system.play("error") #обработка ошибки и воспроизведение сообщения об ошибке
#основной цикл, который обрабатывает нажатия кнопки
try:
    while True:
        if ((GPIO.input(KEY) == False)&(flag == True)):
        	flag = False
        	try:
                run() #выполнение функции
            except Exception:
                system.play("error") #обработка ошибок
        	flag = True
except Exception:
    GPIO.cleanup() #дополнительная обработка ошибок
    system.play("error")
#