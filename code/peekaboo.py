#!/usr/bin/python
from time import sleep
import RPi.GPIO as GPIO
import datetime
import time
import os
from playsound import play_dingdongsound, stop_dingdongsound

GPIO.setmode(GPIO.BOARD)
GPIO.setup(16, GPIO.IN)
time.sleep(2)

try:
    if GPIO.input(16) == GPIO.HIGH:
        print('switch to mode 01')
        exec(open('/home/pi/timelapse/mode_a.py').read())
        
    elif GPIO.input(16) == GPIO.LOW:
        print('switch to mode 02')
        time.sleep(2)
        play_dingdongsound()
        time.sleep(2)
        stop_dingdongsound()
        exec(open('/home/pi/timelapse/mode_b.py').read())
        
except(KeyboardInterrupt):
    print('An error was raised in sequence')
    GPIO.cleanup()
    
