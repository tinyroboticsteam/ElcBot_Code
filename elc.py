import urwid
import serial

def exit_on_q(key):
    global power
    global ser
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()
    if key in ('w', 'W'):
    # forward
        ser.write(b'W')#pw = str(power)
        #string1 = 'W'
        #string1_encode = string1.encode()
        #ser.write(string1_encode)#pw = str(power)
		
    if key in ('a', 'A'):
    # Left
        pw = str(power)
        txt_CP.set_text(('banner', u"A"))

        power = 30
        spower = 3
        txt_CP.set_text(('banner', str(power)))


    if key in ('s', 'S'):
    # Backward
        ser.write(b'W')#pw = str(power)
        #pw = str(power)
        #txt_CP.set_text(('banner', u"S"))

    if key in ('d', 'D'):
    # Right
        pw = str(power)
        txt_CP.set_text(('banner', u"D"))

        power = 30
        spower = 3
        txt_CP.set_text(('banner', str(power)))


    if key in (' '):
    # Stop
        pw = str(power)
        power = 0
        spower = 0
        txt_CP.set_text(('banner', str(power)))
        txt_CP.set_text(('banner', u"Space"))
    if key in ('+'):
        if (power < 90):
            power = power + 10 
            spower = spower + 1
            txt_CP.set_text(('banner', str(power)))
    if key in ('-'):
        if (power > 0):
            power = power - 10
            spower = spower - 1
            txt_CP.set_text(('banner', str(power)))

palette = [
    ('banner', 'black', 'light gray'),
    ('streak', 'black', 'dark blue'),
    ('bg', 'black', 'dark blue'),]

# spower = 0..9 (48 .. 57)
spower = 4
power = spower * 10

ser = serial.Serial('/dev/ttyUSB0', 9600)


txt_F = urwid.Text(('banner', u"W - Forward (\u2191)"), align='center')
txt_LRS = urwid.Text(('banner', u"\u2190 A - Left | Space - Stop | D - Right \u2192"), align='center')
txt_B = urwid.Text(('banner', u"S - Backward (\u2193)"), align='center')
txt_P = urwid.Text(('banner', u"'+' Increase motor power | '-' Decrease motor power"), align='center')
txt_C = urwid.Text(('banner', u"Current power:"), align='center')
txt_CP = urwid.Text(('banner', str(power)), align='center')

txt_Q = urwid.Text(('banner', u"Q - Quit"), align='center')
#txt_F = urwid.Text(('banner', u"W \u2191"), align='center')
#txt_LRS = urwid.Text(('banner', u"\u2190 A | Space - Stop | D \u2192"), align='center')
#txt_B = urwid.Text(('banner', u"S \u2193"), align='center')

#empty string
txt_E = urwid.Text(('banner', u""), align='center')

pile = urwid.Pile([txt_F,  txt_LRS, txt_B, txt_E, txt_P, txt_C, txt_CP, txt_E, txt_E, txt_Q ])
top = urwid.Filler(pile,  top = 5)

loop = urwid.MainLoop(top, palette, unhandled_input=exit_on_q, handle_mouse=False)
loop.run()