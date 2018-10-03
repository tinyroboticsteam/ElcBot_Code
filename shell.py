import sys
import threading

def printit():
    threading.Timer(5.0, printit).start()
    print("Hello, World!")

while True:
    s = input()
    if s == 'd':
	    print('1 m/s')
    if s == 's':
	    print('2 m/s')
    
    printit()		
	
    sys.stdout.flush()