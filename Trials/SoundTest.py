import time

from pygame import mixer
from time import sleep
mixer.init()
tempo = 84
mixer.music.load('ode to joy 84 bpm.mp3')
while True:
    mixer.music.play()
    time.sleep(10.5)
    mixer.music.pause()
    while True:
        x = input("Press Enter")
        mixer.music.unpause()
        time.sleep(60 / tempo)
        mixer.music.pause()
        if mixer.music.get_busy() == False:
            break
    print("Playing")

