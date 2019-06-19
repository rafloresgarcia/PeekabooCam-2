
import pygame
from pygame.locals import *

import math
import numpy

size = (1366, 720)
bits = 16
#the number of channels specified here is NOT 
#the channels talked about here http://www.pygame.org/docs/ref/mixer.html#pygame.mixer.get_num_channels
pygame.mixer.pre_init(44100, -bits, 2)
pygame.init()
pygame.mixer.music.load('/home/pi/timelapse/sounds/camera.mp3')

def play_camerasound():
    #play once, then loop forever
    #sound.play(loops = -1)
    pygame.mixer.music.play(0)
    
def stop_camerasound():
    pygame.mixer.music.stop()
    





