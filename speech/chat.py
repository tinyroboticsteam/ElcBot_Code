#импорт внешних бибилиотек
import random
#словарь распознавания приветствия
greeting_rw = [
 "привет",
 "здравствуй",
 "здравствуйте",
 "приветствую",
 "приветик"
 ]
#словарь распознавания как дела
howareyou_rw = [
 "дела",
 "как"
 ]
#словарь распознавания рассказа о себе
myself_rw = [
 "себе",
 "расскажи",
 "кто",
 "себя"
 ]
#словарь распознавания прощания
farewell_rw = [
"пока",
"свидания",
"увидимся",
"прощай"
]
#словарь генерации приветствия
greeting_aw =[
 "Здравствуйте! ",
 "Приветствую! ",
 "Рада Вас видеть! ",
 "Какие люди в Голливуде! "
 ]
#словарь генерации рассказа о себе
myself_aw = [
 "Меня зовут Елка. ",
 "Я робот телеприсутствия Елка. ",
 "EXTERMINATE! EXTERMINATE! EXTERMINATE! ",
 "Очень оригинальный способ клеить телочек. "
 ]
#словарь генерации прощания
farewell_aw = [
 "Досвидания! ",
 "Всего Вам доброго! ",
 "Всегда рада помочь! ",
 "Пошел ты нахер, козел! "
 ]
#словарь генерации как дела
howareyou_aw = [
 "Все хорошо. ",
 "Все охуенно, все идеально, все так пиздато, но так банально. ",
 "Пока не родила! ",
 "Дел+а?!ты спросил дел+а?! Хуево все нахуй! "
 ]
#функция получения ответа из выражения
def get_answer(text):
	#разбиваем строку на отдельные слова
    words = text.split()
    #инициализация счетчиков 
    greeting_counter = 0
    farewell_counter = 0
    myself_counter = 0
    howareyou_counter =0
    #проход по всем словам выражения и проверка их наличия в словарях
    for word in words:
        if word in greeting_rw:
            greeting_counter += 1
        if word in farewell_rw:
            farewell_counter += 1
        if word in myself_rw:
            myself_counter += 1
        if word in howareyou_rw:
            howareyou_counter += 1
    #генерация ответа
    answer = ""
    #добавление приветствия
    if greeting_counter > 0:
        #рандомный выбор фразы приветствия из словаря
        answer += greeting_aw[random.randint(0, len(greeting_aw) - 1)]
    #добавление как дела
    if howareyou_counter > 0:
        #рандомный выбор фразу как дела из словаря
        answer += howareyou_aw[random.randint(0, len(howareyou_aw) - 1)]
    #добавление о себе
    if myself_counter > 0:
        #рандомный выбор фразы о себе из словаря
        answer += myself_aw[random.randint(0, len(myself_aw) - 1)]
    #добавлеие прощания
    if farewell_counter > 0:
        #рандомный выбор фразы прощания из словаря
        answer += farewell_aw[random.randint(0, len(farewell_aw) - 1)]
    #возврат ответа
    return answer
print(get_answer("привет , как дела, пока"))