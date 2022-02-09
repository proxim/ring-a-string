import os
import time
from pydub import AudioSegment
from pydub.playback import play

def play_mp3(file_name):
    sound = AudioSegment.from_mp3(file_name)
    play(sound)
    
if __name__ == '__main__':
    file_name = 'super-mario-bros-coin.mp3'
    sound = AudioSegment.from_mp3(file_name)
    for _ in range(5):
        play(sound)
        time.sleep(.5)

