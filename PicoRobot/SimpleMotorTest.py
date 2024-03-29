import PicoMotorDriver
import utime

board = PicoMotorDriver.KitronikPicoMotor()
directions = ["f","r"]

while True:
    for motor in range(2):
        for direction in directions:
            for speed in range(100):
                board.motorOn(motor+1, direction, speed)
                utime.sleep_ms(10) #ramp speed over 10x100ms => approx 1 second.
            utime.sleep_ms(1000)
            for speed in range(100):
                board.motorOn(motor+1, direction, 100-speed) #ramp down
                utime.sleep_ms(10) #ramp speed over 10x100ms => approx 1 second.
            utime.sleep_ms(1000)
        utime.sleep_ms(500)#pause between motors 
    