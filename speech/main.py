import speech
import system

import RPi.GPIO as GPIO

KEY = 4
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(KEY, GPIO.IN)
flag = True

print ('Полное функционирование запущено')

try:
    while True:
        if ((GPIO.input(KEY) == False)&(flag == True)):
        	flag = False
        	print("Кнопка нажата")
        	try:
                speech.run()
            except Exception:
                system.play("error")
        	flag = True
except Exception:
    GPIO.cleanup()
    system.play("error")
    