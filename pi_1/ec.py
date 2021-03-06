import urwid
import serial

def exit_on_q(key):
    global power
    global ser
    global spower

    currc = "No command"

    if key in ('q', 'Q'):
        if ser != -1:
            ser.write(b'q')
        raise urwid.ExitMainLoop()

    if ser == -1:
        return

    if key in ('w', 'W'):
    # forward
        ser.write(b'W')#pw = str(power)
        currc = 'W - Forward'
        #string1 = 'W'
        #string1_encode = string1.encode()
        #ser.write(string1_encode)#pw = str(power)
		
    if key in ('a', 'A'):
    # Left
        ser.write(b'A')#pw = str(power)
        currc = 'A - Left'
        #pw = str(power)
        #txt_CP.set_text(('banner', u"A"))
        #power = 30
        #spower = 3
        #txt_CP.set_text(('banner', str(power)))

    if key in ('s', 'S'):
    # Backward
        ser.write(b'S')#pw = str(power)
        currc = 'S - Backward'
        #pw = str(power)
        #txt_CP.set_text(('banner', u"S"))

    if key in ('d', 'D'):
    # Right
        ser.write(b'D')
        currc = 'D - Right'
        #txt_CP.set_text(('banner', u"D"))
        #power = 30
        #spower = 3
        #txt_CP.set_text(('banner', str(power)))

    if key in (' '):
    # Stop
        ser.write(b' ');
        currc = 'Space - Stop'
        #power = 0
        #spower = 0
        #txt_CP.set_text(('banner', str(power)))
        #txt_CP.set_text(('banner', u"Space"))
		
    if key in ('+'):
        if (power < 99):
            power = power + 10 
            spower = spower + 1
            txt_CP.set_text(('banner', str(power)))
            ser.write(bytes([spower+48]))
			
    if key in ('-'):
        if (power > 0):
            power = power - 10
            spower = spower - 1
            txt_CP.set_text(('banner', str(power)))
            ser.write(bytes([spower+48]))
    
    txt_CCV.set_text(('banner', currc))

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

pile = urwid.Pile([txt_F,  txt_LRS, txt_B, txt_E, txt_P, txt_C, txt_CP, txt_E,  txt_CC, txt_CCV, txt_E, txt_Log, txt_LogV, txt_E, txt_Q ])
top = urwid.Filler(pile,  top = 5)

ser = -1

try:
    ser = serial.Serial('/dev/ttyACM0', 9600)
except serial.serialutil.SerialException:
    txt_LogV.set_text(('banner', '[-ERR] Could not connect to Arduino'))

if ser != -1:
    txt_LogV.set_text(('banner', '[+OK] Connected to Arduino'))


loop = urwid.MainLoop(top, palette, unhandled_input=exit_on_q, handle_mouse=False)
loop.run()
