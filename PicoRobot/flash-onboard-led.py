from machine import Pin
import time
onboardLED = Pin(25, Pin.OUT)
while (True):
    onboardLED.value(1)
    time.sleep(1)
    onboardLED.value(0)
    time.sleep(1)