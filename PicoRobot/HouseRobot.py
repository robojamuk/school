from KitronikPicoMotor import KitronikPicoMotor
from Ultrasonic import Ultrasonic
from machine import Pin
import utime
from random import random

board = KitronikPicoMotor()
ultra = Ultrasonic()
directions = ["f","r"]
smallest = 50

onboardLED = Pin(25, Pin.OUT)

def forward(t):
    board.motorOn(1, "f", 100)    
    board.motorOn(2, "f", 100)
    utime.sleep(t)
    
def forwardAndMeasure(t):
    print("Forward %.1fs" % t)
    count = 0
    distance = 1000
    while (count < t and distance > smallest):
        count = count + 1
        print("->", end="")
        forward(1)
        distance = ultra.measure()
    print("")    
    
def backward(t):
    board.motorOn(1, "r", 100)    
    board.motorOn(2, "r", 100)
    utime.sleep(t)

def left(t):
    print("Left %.1fs" % t)
    board.motorOn(1, "f", 100)    
    board.motorOn(2, "r", 100)
    utime.sleep(t)
    
def right(t):
    print("Right %.1fs" % t)
    board.motorOn(1, "r", 100)    
    board.motorOn(2, "f", 100)
    utime.sleep(t)

def ram(c):
    print("Ram!")
    for i in range(c):
        onboardLED.value(1)
        forward(0.2)
        onboardLED.value(0)
        backward(0.2)

def rand(s):
    return random() * s

def fiftyFifty():
    return random() < 0.5

def run():
    while True:
        onboardLED.value(1)
        forwardAndMeasure(rand(5))
        ram(4)
        if (fiftyFifty()):
            left(rand(3))
        else:
            right(rand(3))

try:
    run()
except KeyboardInterrupt:
    board.motorOff(1)    
    board.motorOff(2)
    print("Stopped")
    
