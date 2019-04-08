#импорт внешних библиотек
import os
#импорт внутренних скриптов
import path_settings
#функция записи голоса
def record(filename):
	#--quiet - тихий режим
	#-d - блительность записи
	#-D - выбор девайса
    os.system("arecord --quiet -d 5 -f dat -t raw -c 1 -D hw:1,0 | opusenc --quiet --raw-chan 1 -  " + path_settings.ogg_record_path + filename + path_settings.ogg_format)
#функция конвертации из ogg в wav
def convert(filename):
    os.system('opusdec --quiet ' + path_settings.ogg_speech_path + filename + path_settings.ogg_format + ' ' + path_settings.wav_speech_path + filename + path_settings.wav_format)
#функция воспроизведения записи
def play(filename):
	#--quiet - тихий режим
	#-D - выбор девайса
    os.system('aplay --quiet -f dat -D hw:1,0 ' + path_settings.wav_speech_path + filename + path_settings.wav_format)