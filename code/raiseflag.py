#!/usr/bin/python

from time import sleep
import RPi.GPIO as GPIO
from playsound import play_dingdongsound, stop_dingdongsound

import datetime
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(16, GPIO.IN)

p5 = GPIO.PWM(5, 50) #29 is flag motor #remotely control (or detect no human then raise the flag)
p5.start(0)

def raise_flag():
    print('flag move')
    play_dingdongsound()
    for i in range(3):
        p5.ChangeDutyCycle(6)
        time.sleep(0.5)
        p5.ChangeDutyCycle(8.5)
        time.sleep(0.5)
    p5.ChangeDutyCycle(0)
    stop_dingdongsound()

try:
    if GPIO.input(16) == GPIO.HIGH:
        raise_flag()
        exit()
        
    elif GPIO.input(16) == GPIO.LOW:
        exit()

except(KeyboardInterrupt):
    print('An error was raised in sequence')
    p5.stop()
    GPIO.cleanup()