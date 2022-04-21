import time

from pygame import mixer
from time import sleep
mixer.init()
mixer.music.load('BASS DRUM Lvl 6.mp3')
mixer.music.play()
time.sleep(1)
mixer.music.load('SNARE DRUM 5B.mp3')
mixer.music.play()
mixer.music.set_volume(1)
while mixer.music.get_busy():
    continue
