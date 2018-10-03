import sys
import threading
import serial
from time import sleep

global currcomm

#writetimer = 1 # запуск команды на отправку данных на ардуино каждую секунду
# слишком часто отправлять нельзя, т.к. пропускной способности порта может не хватить
# т.е. её и не хватает.
# проблема ещё в ардуино программе она не должна всегда отправлять скорость
# наверное, раз в 2 секунды

readtimer = 0.25 # запуск команды на чтение данных из порта

# rwflag, 0 - can read, 1 - can write
# получается переключение между чтением / записью как раз только
# между writesensor и readsensor выполняется

# функция для отправки команды ардуино
'''def writesensor():
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
'''		
'''
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
'''
'''
def read():
    global serialport
    while True:
        data = serialport.readline();
        print(data)
        #sleep(0.5)		'''

def read():
    global serialport
    global currcomm
	
    threading.Timer(readtimer, read).start()
	
    if (currcomm != -1):
        data = serialport.read(10);
        print(str(data) + " : "  + str(len(data)))
        sys.stdout.flush();
        #sleep(0.5)		'''		
		

# я думаю, там в порте что-то остаётся, из-за этого так и происходит.		
	
### начало главной программы
		
# открытие порта		
#serialport = serial.Serial("/dev/ttyAMA0", 9600, timeout=0.5)

serialport = -1

print('Please wait ...');
sys.stdout.flush();

serialspeed = 38400

try:
    serialport = serial.Serial('/dev/ttyACM0', serialspeed, timeout = 0.2)
    # без этой задержки ардуино не успевает инициализироваться и не может после нажатия
    # на клавиши обрабатывать команды
    sleep(3);
except serial.serialutil.SerialException:
    #txt_LogV.set_text(('banner', '[-ERR] Could not connect to Arduino'))
    print('[-ERR] Could not connect to Arduino');
    sys.stdout.flush();


print('Please wait ...');
sys.stdout.flush();


try:
    serialport = serial.Serial('/dev/ttyACM1', serialspeed, timeout = 0.2)
    # без этой задержки ардуино не успевает инициализироваться и не может после нажатия
    # на клавиши обрабатывать команды
    sleep(3);
except serial.serialutil.SerialException:
    #txt_LogV.set_text(('banner', '[-ERR] Could not connect to Arduino'))
    print('[-ERR] Could not connect to Arduino');
    sys.stdout.flush();


if serialport != -1:
    #txt_LogV.set_text(('banner', '[+OK] Connected to Arduino'))
    print('[+OK] Connected to Arduino');
    sys.stdout.flush();


#serialport = serial.Serial("/dev/ttyACM0", 19200, timeout=0.2)
data = serialport.read(100);

#t1 = threading.Thread(target=read, args=())
#t1.start()

# запуск команды на отправку данных на компьютер
currcomm = -1

threading.Timer(readtimer, read).start()
sleep(1)

while True:
    currcomm = input()
	# тут идёт обработка команды
	
    if (currcomm == 'S') or (currcomm == 'D') or (currcomm == 'W') or (currcomm == 'A') or (currcomm == ' '):
        #currcomm = currcomm_
        #rwflag = 1		
        serialport.write(bytes(currcomm, encoding = 'utf-8'));
        #print(currcomm) # от	правка данных в родительский поток
        #sys.stdout.flush();		
        # команда print пишет в стандартный вывод
    if (currcomm == 'Q'):
        serialport.close() # Only executes once the loop exits
		
   
