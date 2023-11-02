from machine import Pin
import utime

class Ultrasonic:
    def __init__(self):
        self.trigger = Pin(0, Pin.OUT)
        self.echo = Pin(1, Pin.IN)

    def measure(self):
        try:
            self.trigger.low()
            utime.sleep_us(2)
            self.trigger.high()
            utime.sleep_us(5)
            self.trigger.low()
            while self.echo.value() == 0:
               signaloff = utime.ticks_us()
            while self.echo.value() == 1:
               signalon = utime.ticks_us()
            timepassed = signalon - signaloff
            distance = (timepassed * 0.0343) / 2            
            print("Distance: %.1f cm" % distance)
            return distance
        except KeyboardInterrupt:
            self.pinTrigger.value(0)
            
if __name__ == '__main__':
    ultra = Ultrasonic()
    try:
        while True:
            print(ultra.measure())        
    except KeyboardInterrupt:
        exit()            
