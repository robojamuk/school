from PCA9685 import MotorDriver
from Ultrasonic import Ultrasonic
from machine import Pin
import utime
from random import random

motorDriver = MotorDriver()
ultra = Ultrasonic()
directions = ["f","r"]
smallest = 5

onboardLED = Pin(25, Pin.OUT)

def forward(t):
    print("Forward %.1fs" % t)
    motorDriver.MotorStart('MA', 'forward', 100)
    motorDriver.MotorStart('MB', 'forward', 100)
    motorDriver.MotorStart('MC', 'forward', 100)
    motorDriver.MotorStart('MD', 'forward', 100)
    utime.sleep(t)
    motorDriver.MotorStop('MA')
    motorDriver.MotorStop('MB')
    motorDriver.MotorStop('MC')
    motorDriver.MotorStop('MD')

    
def forwardAndMeasure(t):
    print("Forward and measure %.1fs" % t)
    motorDriver.MotorStart('MA', 'forward', 100)
    motorDriver.MotorStart('MB', 'forward', 100)
    motorDriver.MotorStart('MC', 'forward', 100)
    motorDriver.MotorStart('MD', 'forward', 100)
    count = 0
    distance = ultra.measure()
    hit = False
    while (count < (t*10) and distance > smallest):
        count = count + 1
        print("->", end="")
        utime.sleep_ms(100)
        distance = ultra.measure()
    print("")   
    if distance <= smallest:
        print("Hit!", distance)
        hit = True
    motorDriver.MotorStop('MA')
    motorDriver.MotorStop('MB')
    motorDriver.MotorStop('MC')
    motorDriver.MotorStop('MD')
    return hit
    
def backward(t):
    print("Backward %.1fs" % t)
    motorDriver.MotorStart('MA', 'backward', 100)
    motorDriver.MotorStart('MB', 'backward', 100)
    motorDriver.MotorStart('MC', 'backward', 100)
    motorDriver.MotorStart('MD', 'backward', 100)
    utime.sleep(t)
    motorDriver.MotorStop('MA')
    motorDriver.MotorStop('MB')
    motorDriver.MotorStop('MC')
    motorDriver.MotorStop('MD')

def turn_left(t):
    print("Turn Left %.1fs" % t)
    motorDriver.MotorStart('MA', 'backward', 100)
    motorDriver.MotorStart('MB', 'backward', 100)
    motorDriver.MotorStart('MC', 'forward', 100)
    motorDriver.MotorStart('MD', 'forward', 100)
    utime.sleep(t)
    motorDriver.MotorStop('MA')
    motorDriver.MotorStop('MB')
    motorDriver.MotorStop('MC')
    motorDriver.MotorStop('MD')
    
def turn_right(t):
    print("Turn Right %.1fs" % t)
    motorDriver.MotorStart('MA', 'forward', 100)
    motorDriver.MotorStart('MB', 'forward', 100)
    motorDriver.MotorStart('MC', 'backward', 100)
    motorDriver.MotorStart('MD', 'backward', 100)
    utime.sleep(t)
    motorDriver.MotorStop('MA')
    motorDriver.MotorStop('MB')
    motorDriver.MotorStop('MC')
    motorDriver.MotorStop('MD')

def shift_left(t):
    print("Shift Left %.1fs" % t)
    motorDriver.MotorStart('MA', 'forward', 100)
    motorDriver.MotorStart('MB', 'backward', 100)
    motorDriver.MotorStart('MC', 'backward', 100)
    motorDriver.MotorStart('MD', 'forward', 100)
    utime.sleep(t)
    motorDriver.MotorStop('MA')
    motorDriver.MotorStop('MB')
    motorDriver.MotorStop('MC')
    motorDriver.MotorStop('MD')
    
def shift_right(t):
    print("Shift Right %.1fs" % t)
    motorDriver.MotorStart('MA', 'backward', 100)
    motorDriver.MotorStart('MB', 'forward', 100)
    motorDriver.MotorStart('MC', 'forward', 100)
    motorDriver.MotorStart('MD', 'backward', 100)
    utime.sleep(t)
    motorDriver.MotorStop('MA')
    motorDriver.MotorStop('MB')
    motorDriver.MotorStop('MC')
    motorDriver.MotorStop('MD')


def ram(c):
    print("Ram!")
    for i in range(c):
        onboardLED.value(1)
        forward(0.2)
        onboardLED.value(0)
        backward(0.2)

def flash_led(c):
    for i in range(c):
        onboardLED.value(1)
        utime.sleep(0.1)
        onboardLED.value(0)
        utime.sleep(0.1)

def rand(s):
    return random() * s

def fiftyFifty():
    return random() < 0.5

def run():
    flash_led(10)
    while True:
        onboardLED.value(1)
        if forwardAndMeasure(rand(5)):
            ram(4)
        if (fiftyFifty()):
            if (fiftyFifty()):
                turn_left(rand(3))
            else:
                shift_left(rand(3))
        else:
            if (fiftyFifty()):
                turn_right(rand(3))
            else:
                shift_right(rand(3))

try:
    run()
except KeyboardInterrupt:
    motorDriver.MotorStop('MA')
    motorDriver.MotorStop('MB')
    motorDriver.MotorStop('MC')
    motorDriver.MotorStop('MD')
    print("Stopped")

