from time import sleep
from picamera import PiCamera
import RPi.GPIO as GPIO
import pigpio
from cameraclick import play_camerasound, stop_camerasound
from peekaboologger import log
import datetime
import time
import logging

# create logger
logger = logging.getLogger('peekaboo')
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
date = datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
logname = 'peekaboologger_%s.log' %date
fh = logging.FileHandler(logname)

fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(16, GPIO.IN)

p15 = GPIO.PWM(15, 50) #P15 is shutter motor
p15.start(0)

p5 = GPIO.PWM(5, 50) #29 is flag motor #remotely control (or detect no human then raise the flag)
p5.start(0)

camera = PiCamera()
time.sleep(2)

pi = pigpio.pi()
if not pi.connected:
    exit()
    
pi.set_mode(2, pigpio.INPUT)
pi.set_pull_up_down(2, pigpio.PUD_DOWN)
pi.set_glitch_filter(2, 100)

def waitButton():
    while not pi.wait_for_edge(2):
        time.sleep(1)
    print('Button is pressed')
    
def take_photo():
    sleep(1)
    play_camerasound()
    for i in range(2):
        date = datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
        timeCaptured = '/home/pi/timelapse/photos/photos/TEST_%s.jpg' %date
        camera.capture(timeCaptured)
        log(timeCaptured)
        time.sleep(1)
        stop_camerasound()

def open_shutter():
    print('move')
    p15.ChangeDutyCycle(3)
    time.sleep(1)
    p15.ChangeDutyCycle(0)
    time.sleep(0.5)                                                                                 
    
def close_shutter():
    p15.ChangeDutyCycle(6)
    time.sleep(1)
    p15.ChangeDutyCycle(0)
    time.sleep(1)
    
def down_flag():
    p5.ChangeDutyCycle(3)
    time.sleep(1)
    p5.ChangeDutyCycle(0)                                                                             
    time.sleep(1)

def callback_function_a(channel):
    print('mode_a_callback_interrupt_invoked')
    GPIO.remove_event_detect(16)
    exit()
    
GPIO.add_event_detect(16, GPIO.FALLING, callback_function_a)

while True:
    try:
        if GPIO.input(16) == GPIO.HIGH:
            print('in the mode 01')
            waitButton()
            down_flag()
            open_shutter()
            take_photo()
            print('moveback')
            close_shutter()
            
        elif GPIO.input(16) == GPIO.LOW:
            log('Node 2 Detected, Esiting Mode 1')
            exit()
            
    except(KeyboardInterrupt):
        print('An error was raised in sequence')
        close_shutter()
        p15.stop()
        p5.stop()
        GPIO.cleanup()
