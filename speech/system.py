import os
#
import path_settings
#
def record(filename):
    os.system("arecord --quiet -d 5 -f dat -t raw -c 1 -D hw:1,0 | opusenc --quiet --raw-chan 1 -  " + path_settings.ogg_record_path + filename + path_settings.ogg_format)
#
def convert(filename):
    os.system('opusdec --quiet ' + path_settings.ogg_speech_path + filename + path_settings.ogg_format + ' ' + path_settings.wav_speech_path + filename + path_settings.wav_format)
#
def play(filename):
    os.system('aplay --quiet -f dat ' + path_settings.wav_speech_path + filename + path_settings.wav_format)