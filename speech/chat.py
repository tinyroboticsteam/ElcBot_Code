#
import random
#
greeting_recognition_wordbook = ["привет","здравствуй","здравствуйте","приветствую"]
howareyou_recognition_wordbook = ["дела", "как"]
myself_recognition_wordbook = ["ты", "себе", "расскажи", "кто", "себя"]
farewell_recognition_wordbook = ["пока", "свидания", "увидимся", "прощай"]
#
greeting_answer_wordbook = ["Здравствуйте, ", "Приветствую, ", "Рада Вас видеть, ", "Какие люди в Голливуде! "]
myself_answer_wordbook = ["меня зовут Елка, ", "я робот телеприсутствия Елка, ", "EXTERMINATE! EXTERMINATE! EXTERMINATE! ", "очень оригинальный способ клеить телочек, "]
farewell_answer_wordbook = ["досвидания!", "всего Вам доброго!", "всегда рада помочь!", "пошел ты нахер, козел!"]
howareyou_answer_wordbook = ["все хорошо, ","все охуенно, все идеально, все так пиздато, но так банально, ","Пока не родила! ","дел+а?!ты спросил дел+а?! Хуево все нахуй! "]
#
def get_answer(text):
	#
    words = text.split()
    #
    greeting_counter = 0
    farewell_counter = 0
    myself_counter = 0
    howareyou_counter =0
    #
    for word in words:
        if word in greeting_recognition_wordbook:
            greeting_counter += 1
        if word in farewell_recognition_wordbook:
            farewell_counter += 1
        if word in myself_recognition_wordbook:
            myself_counter += 1
        if word in howareyou_recognition_wordbook:
            howareyou_counter += 1
    #
    print(words)
    answer = ""
    if greeting_counter > 0:
        answer += greeting_answer_wordbook[random.randint(0,3)]
    if howareyou_counter > 0:
        answer += howareyou_answer_wordbook[random.randint(0,3)]
    if myself_counter > 0:
        answer += myself_answer_wordbook[random.randint(0,3)]
    if farewell_counter > 0:
        answer += farewell_answer_wordbook[random.randint(0,3)]
    #
    print(answer)
    return answer