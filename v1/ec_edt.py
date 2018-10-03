from __future__ import print_function, absolute_import, division
import subprocess
import urwid
import serial
from subprocess import Popen, PIPE
from time import sleep

# что надо сделать. нужно каждую секунду отсылать команду 
# которая была установлена в интерфейсе. для этого 
# нужно создать ещё один поток, который будет отвечать за отправку / чтение
# и обновление данных в интерфейсе.
# нужно всё взаимодействие с последовательным портом в один файл

def exit_on_q(key):
    global power
    global ser
    global spower
    global p
    global currc

    if key in ('q', 'Q'):
        #if ser != -1:
        #ser.write(b'q')
        #p.stdin.write(b'Q\n')
        #p.stdin.flush()
        raise urwid.ExitMainLoop()

    #if ser == -1:
    #    return

    if key in ('w', 'W'):
    # forward
        #ser.write(b'W')#pw = str(power)
        currc = 'W - Forward'
        #string1 = 'W'
        #string1_encode = string1.encode()
        #ser.write(string1_encode)#pw = str(power)
        p.stdin.write(b'W\n')
        p.stdin.flush()
		
    if key in ('a', 'A'):
    # Left
        #ser.write(b'A')#pw = str(power)
        currc = 'A - Left'
        #pw = str(power)
        #txt_CP.set_text(('banner', u"A"))
        #power = 30
        #spower = 3
        #txt_CP.set_text(('banner', str(power)))
        p.stdin.write(b'A\n')
        p.stdin.flush()

    if key in ('s', 'S'):
    # Backward
        #ser.write(b'S')#pw = str(power)
        currc = 'S - Backward'
        #pw = str(power)
        #txt_CP.set_text(('banner', u"S"))
        p.stdin.write(b'S\n')
        p.stdin.flush()

    if key in ('d', 'D'):
    # Right
        #ser.write(b'D')
        currc = 'D - Right'
        #txt_CP.set_text(('banner', u"D"))
        #power = 30
        #spower = 3
        #txt_CP.set_text(('banner', str(power)))
        p.stdin.write(b'D\n')
        p.stdin.flush()


    if key in (' '):
    # Stop
        #ser.write(b' ');
        currc = 'Space - Stop'
        #power = 0
        #spower = 0
        #txt_CP.set_text(('banner', str(power)))
        #txt_CP.set_text(('banner', u"Space"))
        p.stdin.write(b' \n')
        p.stdin.flush()

    if key in ('+'):
        if (power < 99):
            power = power + 10 
            spower = spower + 1
            txt_CP.set_text(('banner', str(power)))
            #ser.write(bytes([spower+48]))
			
    if key in ('-'):
        if (power > 0):
            power = power - 10
            spower = spower - 1
            txt_CP.set_text(('banner', str(power)))
            #ser.write(bytes([spower+48]))
    
    txt_CCV.set_text(('banner', currc))

def enter_idle():
    loop.remove_watch_file(pipe.stdout)

def update_text(read_data):
    txt_Q.set_text(('banner', read_data))
	
if __name__ == '__main__':

    currc = "No command"
	
    palette = [
        ('banner', 'black', 'light gray'),
        ('streak', 'black', 'dark blue'),
        ('bg', 'black', 'dark blue'),]

    # spower = 0..9 (48 .. 57)
    spower = 4
    power = spower * 10

    txt_F = urwid.Text(('banner', u"W - Forward (\u2191)"), align='center')
    txt_LRS = urwid.Text(('banner', u"\u2190 A - Left | Space - Stop | D - Right \u2192"), align='center')
    txt_B = urwid.Text(('banner', u"S - Backward (\u2193)"), align='center')
    txt_P = urwid.Text(('banner', u"'+' Increase motor power | '-' Decrease motor power"), align='center')
    txt_C = urwid.Text(('banner', u"Current power:"), align='center')

    txt_CP = urwid.Text(('banner', str(power)), align='center')

    # current command
    txt_CC = urwid.Text(('banner', u"Current command: "), align='center')
    txt_CCV = urwid.Text(('banner', u"No command"), align='center')

    txt_Log = urwid.Text(('banner', u"Log: "), align='center')
    txt_LogV = urwid.Text(('banner', u""), align='center')

    txt_Q = urwid.Text(('banner', u"Q - Quit"), align='center')
    #txt_F = urwid.Text(('banner', u"W \u2191"), align='center')
    #txt_LRS = urwid.Text(('banner', u"\u2190 A | Space - Stop | D \u2192"), align='center')
    #txt_B = urwid.Text(('banner', u"S \u2193"), align='center')

    #empty string
    txt_E = urwid.Text(('banner', u""), align='center')

    pile = urwid.Pile([txt_F, txt_LRS, txt_B, txt_E, txt_P, txt_C, txt_CP, txt_E, txt_CC, txt_CCV, txt_E, txt_Log, txt_LogV, txt_E, txt_Q ])
    top = urwid.Filler(pile, top = 5)

    #ser = -1

    #try:
    #    ser = serial.Serial('/dev/ttyACM0', 9600)
    #except serial.serialutil.SerialException:
    #    txt_LogV.set_text(('banner', '[-ERR] Could not connect to Arduino'))

    #if ser != -1:
    #    txt_LogV.set_text(('banner', '[+OK] Connected to Arduino'))

    loop = urwid.MainLoop(top, palette, unhandled_input=exit_on_q, handle_mouse=False)
	
    stdout = loop.watch_pipe(update_text)
    stderr = loop.watch_pipe(update_text)	
    #pipe = subprocess.Popen('for i in $(seq 50); do echo -n "$i "; sleep 0.5; done', shell=True, stdout=stdout, stderr=stderr)	
    p = subprocess.Popen(['python3', 'shell_edt.py'], stdin = PIPE, stdout = stdout, stderr = stdout, shell = False)	
    loop.run()
