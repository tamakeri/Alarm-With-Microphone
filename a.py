import audioop
import os
import time
from math import log10
from threading import *
import keyboard
import pyaudio
import pygetwindow
from playsound import playsound
global clearthis
global ılk_pencere
win = pygetwindow.getActiveWindow()
win = str(win)
x = str(win).index("title=")+6
a=str(win).index(">")
ılk_pencere=win[x:a]
average = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
average_sum = 0
i = 0
clearthis=0
p = pyaudio.PyAudio()
WIDTH = 2
RATE = int(p.get_default_input_device_info()['defaultSampleRate'])
DEVICE = p.get_default_input_device_info()['index']
rms = 0
db = 0
print("hold + or - to incrase/decrease thres hold")
time.sleep(2)
file1 = open("oku.txt","r+") 
def callback(in_data, frame_count, time_info, status):
    global rms
    rms = audioop.rms(in_data, WIDTH) / 32767
    return in_data, pyaudio.paContinue
def progress_bar(current_value, total):
    increments = 100
    percentual = ((current_value / total) * 100)
    i = int(percentual // (100 / increments))
    text = "\r[{0: <{1}}] {2}%    ".format('=' * i, increments, int(percentual))
    print(text, end="\t" if percentual == 100 else "")
stream = p.open(format=p.get_format_from_width(WIDTH),
                input_device_index=DEVICE,
                channels=1,
                rate=RATE,
                input=True,
                output=False,
                stream_callback=callback)
stream.start_stream()
seviye = 80
def threading():
    try:
        win = pygetwindow.getActiveWindow()
        x = str(win).index("title=")+6
        a=str(win).index(">")
        win = str(win)
        son=win[x:a]
        if(ılk_pencere!=son):
            return
        tuş = keyboard.read_key()
        if tuş == "+":
            setak(getak()+1)
        if tuş == "-":
            setak(getak()-1)
    except:
        pass
def getak():
    return seviye
def setak(ol):
    global seviye
    time.sleep(0.1)
    if (ol >= 100 or ol <= 0):
        return
    seviye = ol
setak(int(file1.read()))
file1.close()
while stream.is_active():
    if rms != 0.0:
        db = 30 * log10(rms)
        #print(f"RMS: {rms} DB: {db}") 
        average[i] = db
        i = i+1
        clearthis=clearthis+1
        if clearthis > 300:
            file1 = open("oku.txt","w")#write mode
            L=getak()
            L=str(L)
            file1.writelines(L)
            file1.close()
            clearthis = 0
            os.system('cls')
        if i == 17:i = 0
        for x in range(0, 17):
            average_sum = average_sum+average[x]
        average_sum = average_sum/10
        ak = 100-average_sum*(-1)
        t2 = Thread(target=threading).start()
        off = getak()
        progress_bar(ak, 100)
        print(seviye)
        if off < ak:
            playsound('a.wav')
            time.sleep(0.1)
            # Beep at 1000 Hz for 100 ms
    time.sleep(0.01)
