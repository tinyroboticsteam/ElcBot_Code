import sys
import threading
import serial
from time import sleep

global currcomm

writetimer = 1 # запуск команды на отправку данных на ардуино каждую секунду
# слишком часто отправлять нельзя, т.к. пропускной способности порта может не хватить
# т.е. её и не хватает.
# проблема ещё в ардуино программе она не должна всегда отправлять скорость
# наверное, раз в 2 секунды

readtimer = 0.5 # запуск команды на чтение данных из порта

# rwflag, 0 - can read, 1 - can write
# получается переключение между чтением / записью как раз только
# между writesensor и readsensor выполняется

# функция для отправки команды ардуино
def writesensor():
    global rwflag
    global currcomm
    global serialport
	
    threading.Timer(writetimer, writesensor).start()

    #p = rwflag
    #print('1. writesensor' + ' ' +str(p) + str(currcomm)) # отправка данных в родительский поток
    #sys.stdout.flush();		
	
    if (rwflag == 1) and (currcomm != -1):
        # тут код, который команду ардуино отправляет: currcomm
        serialport.write(bytes(currcomm, encoding = 'utf-8'));
        #print('2. writesensor' + ' ' +str(p) + str(currcomm)) # отправка данных в родительский поток
        #sys.stdout.flush();		
        rwflag = 0 # установка разрешения на чтение данных с сенсора
		

# функция для получения данных от ардуино
def readsensor():	
    global rwflag
    global serialport
	
    #while True:
    threading.Timer(readtimer, readsensor).start()

    #p = rwflag
    #print('1. readsensor' + ' ' + str(p)) # отправка данных в родительский поток
    #sys.stdout.flush();		
	
    if (rwflag == 0):
        #print('readsensor' + ' ' +str(rwflag)) # отправка данных в родительский поток
        #sys.stdout.flush();				
        sensor_data = serialport.readline();
        print(sensor_data) # отправка данных в родительский поток
        sys.stdout.flush();
        #print('2. readsensor' + ' ' +str(rwflag)) # отправка данных в родительский поток
        #sys.stdout.flush();				
        #sleep(0.5); # ???
        rwflag = 1; # установка разрешения на отправку команд
		
	
### начало главной программы
		
# открытие порта		
#serialport = serial.Serial("/dev/ttyAMA0", 9600, timeout=0.5)
serialport = serial.Serial("/dev/ttyACM0", 19200)

# запуск команды на отправку данных на компьютер
rwflag   =  1
currcomm = -1

writesensor()
readsensor()

#t1 = threading.Thread(target=readsensor, args=())
#t1.start()

while True:
    currcomm_ = input()
	# тут идёт обработка команды
	
    if (currcomm_ == 'S') or (currcomm_ == 'D') or (currcomm_ == 'W') or (currcomm_ == 'A') or (currcomm_ == ' '):
        currcomm = currcomm_
        rwflag = 1		
        #serialport.write(bytes(currcomm, encoding = 'utf-8'));
		
        #print(currcomm) # от	правка данных в родительский поток
        #sys.stdout.flush();		
		# команда print пишет в стандартный вывод

	
serialport.close() # Only executes once the loop exits
		
    
# ардуино программа всегда должна что-от отправлять, хотя бы -1, иначе питон программа может заблокироваться.	