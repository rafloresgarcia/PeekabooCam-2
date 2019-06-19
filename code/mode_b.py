from time import sleep
from picamera import PiCamera
import RPi.GPIO as GPIO
from cameraclick import play_camerasound, stop_camerasound
from peekaboologger import log
import datetime
import time
import logging

# create logger
logger = logging.getLogger('peekaboo')
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = logging.FileHandler('peekaboologger.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


def take_photo():
    sleep(1)
    play_camerasound()
    for i in range(2):
        date = datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
        timeCaptured = '/home/pi/timelapse/TEST_%s.jpg' %date
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

def raise_flag():
    print('flag move')
    for i in range(2):
        p5.ChangeDutyCycle(8)
        time.sleep(1)
        p5.ChangeDutyCycle(6)
        time.sleep(1)
    for i in range(2):
        p5.ChangeDutyCycle(8)
        time.sleep(0.5)
        p5.ChangeDutyCycle(6)
        time.sleep(0.5)
    p5.ChangeDutyCycle(3)
    time.sleep(1)
    p5.ChangeDutyCycle(4)
    time.sleep(1)
    p5.ChangeDutyCycle(5)
    time.sleep(1)
    p5.ChangeDutyCycle(6)
    time.sleep(1)
    p5.ChangeDutyCycle(7)
    time.sleep(1)
    p5.ChangeDutyCycle(8)
    p5.ChangeDutyCycle(0)

def down_flag():
    p5.ChangeDutyCycle(3)
    time.sleep(1)
    p5.ChangeDutyCycle(0)                                                                             
    time.sleep(1)

camera = PiCamera()

GPIO.setmode(GPIO.BOARD)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(3, GPIO.IN)

p15 = GPIO.PWM(15, 50) #P15 is shutter motor
p15.start(0)

p5 = GPIO.PWM(5, 50) #29 is flag motor #remotely control (or detect no human then raise the flag)
p5.start(0)

def callback_function(channel):
    print('callback_interrupt_invoked')
    GPIO.remove_event_detect(3)
    down_flag()
    exit()
    
GPIO.add_event_detect(3, GPIO.FALLING, callback = callback_function)

try:
    raise_flag()
    time.sleep(1)
    open_shutter()
    take_photo()
    print('moveback')
    close_shutter()
    down_flag()
    time.sleep(1)
    exit()

except(KeyboardInterrupt):
    print('An error was raised in sequence')
    close_shutter()
    p15.stop()
    GPIO.cleanup()

