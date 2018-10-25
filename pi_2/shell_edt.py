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

def read():
    global serialport
    global currcomm
	
    threading.Timer(readtimer, read).start()
	
    if (currcomm != -1):
        data = serialport.read(11);
        if (len(data) > 0):
            print(str(data) + " : "  + str(len(data)))
            sys.stdout.flush();
		

### начало главной программы
		
# открытие порта		
#serialport = serial.Serial("/dev/ttyAMA0", 9600, timeout=0.5)

serialport = -1

print('Please wait ...');
sys.stdout.flush();

serialspeed = 38400

# возможный диапазон устройств
ind = range(0,10)
for i in ind:
    devName = '/dev/ttyACM' + str(i)
    try:
        serialport = serial.Serial(devName, serialspeed, timeout = 0.2)
        # без этой задержки ардуино не успевает инициализироваться и не может после нажатия
        # на клавиши обрабатывать команды
        sleep(3);
    except serial.serialutil.SerialException:
        #txt_LogV.set_text(('banner', '[-ERR] Could not connect to Arduino'))
        print('[-ERR] Could not connect to Arduino');
        sys.stdout.flush();
    print('Please wait ...');
    sys.stdout.flush();
    if serialport != -1:
        print('[+OK] Connected to Arduino, dev = ' + devName);
        sys.stdout.flush();	
        break;

# я думаю, там в порте что-то остаётся, из-за этого так и происходит.		
# т.е. без этой команды сначала мусор будет сыпаться
data = serialport.read(100);

# запуск команды на отправку данных на компьютер
currcomm = -1

threading.Timer(readtimer, read).start()
sleep(1)

powerlevels = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
commands    = ['W', 'A', 'S', 'D', ' ']
while True:
    currcomm = input()
	# тут идёт обработка команды

    #print(currcomm) # отправка данных в родительский поток
    #sys.stdout.flush();		
    if (currcomm in powerlevels):
        serialport.write(bytes(currcomm, encoding = 'utf-8'));

    if (currcomm in commands):
        serialport.write(bytes(currcomm, encoding = 'utf-8'));
		
        # команда print пишет в стандартный вывод
    if (currcomm == 'Q'):
        serialport.close() # Only executes once the loop exits
		
   
