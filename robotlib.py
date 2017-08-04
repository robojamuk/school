
import RPi.GPIO as GPIO # Import the GPIO Library
import time # Import the Time library

# Set the GPIO modes
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set variables for the GPIO motor pins
pinMotorAForwards = 10
pinMotorABackwards = 9
pinMotorBForwards = 8
pinMotorBBackwards = 7

# Define GPIO pins to use on the Pi for the ultrasonic distance measurer
pinTrigger = 17
pinEcho = 18

# Defin pins on the GPIO for the line sensor
pinLineFollower = 25

# How many times to turn the pin on and off each second
Frequency = 20
# How long the pin stays on each cycle, as a percent
DutyCycleA = 70
DutyCycleB = 70
# Settng the duty cycle to 0 means the motors will not turn
Stop = 0

# Set the GPIO Pin mode to be Output
GPIO.setup(pinMotorAForwards, GPIO.OUT)
GPIO.setup(pinMotorABackwards, GPIO.OUT)
GPIO.setup(pinMotorBForwards, GPIO.OUT)
GPIO.setup(pinMotorBBackwards, GPIO.OUT)
# Set pins as output and input
GPIO.setup(pinTrigger, GPIO.OUT)  # Trigger
GPIO.setup(pinEcho, GPIO.IN)      # Echo
# Set pin 25 as an input so we can read its value
GPIO.setup(pinLineFollower, GPIO.IN)


# Distance Variables
HowNear = 15.0
ReverseTime = 0.5
TurnTime = 0.75

# Set the GPIO to software PWM at 'Frequency' Hertz
pwmMotorAForwards = GPIO.PWM(pinMotorAForwards, Frequency)
pwmMotorABackwards = GPIO.PWM(pinMotorABackwards, Frequency)
pwmMotorBForwards = GPIO.PWM(pinMotorBForwards, Frequency)
pwmMotorBBackwards = GPIO.PWM(pinMotorBBackwards, Frequency)

# Start the software PWM with a duty cycle of 0 (i.e. not moving)
pwmMotorAForwards.start(Stop)
pwmMotorABackwards.start(Stop)
pwmMotorBForwards.start(Stop)
pwmMotorBBackwards.start(Stop)

# Turn all motors off
def StopMotors():
    pwmMotorAForwards.ChangeDutyCycle(Stop)
    pwmMotorABackwards.ChangeDutyCycle(Stop)
    pwmMotorBForwards.ChangeDutyCycle(Stop)
    pwmMotorBBackwards.ChangeDutyCycle(Stop)

# Turn both motors forwards
def RunForwards():
    pwmMotorAForwards.ChangeDutyCycle(DutyCycleA)
    pwmMotorABackwards.ChangeDutyCycle(Stop)
    pwmMotorBForwards.ChangeDutyCycle(DutyCycleB)
    pwmMotorBBackwards.ChangeDutyCycle(Stop)

# Turn both motors backwards
def RunBackwards():
    pwmMotorAForwards.ChangeDutyCycle(Stop)
    pwmMotorABackwards.ChangeDutyCycle(DutyCycleA)
    pwmMotorBForwards.ChangeDutyCycle(Stop)
    pwmMotorBBackwards.ChangeDutyCycle(DutyCycleB)

# Turn left
def TurnLeft():
    pwmMotorAForwards.ChangeDutyCycle(DutyCycleA)
    pwmMotorABackwards.ChangeDutyCycle(Stop)
    pwmMotorBForwards.ChangeDutyCycle(Stop)
    pwmMotorBBackwards.ChangeDutyCycle(DutyCycleB)

# Turn Right
def TurnRight():
    pwmMotorAForwards.ChangeDutyCycle(Stop)
    pwmMotorABackwards.ChangeDutyCycle(DutyCycleA)
    pwmMotorBForwards.ChangeDutyCycle(DutyCycleB)
    pwmMotorBBackwards.ChangeDutyCycle(Stop)

# See if the line sensor sees black or white
def SenseWhite():
    # returns 0 for black; 1 for white
    # if sensor returns 0, it's over black, else white
    if GPIO.input(pinLineFollower)==0:
        return 0
    else:
        return 1


# Take a distance measurement, returns in CM
# calculation = signal time * speed of sound / 2
def Measure():
    GPIO.output(pinTrigger, False)
    time.sleep(0.03)
    GPIO.output(pinTrigger, True)
    time.sleep(0.00001)
    GPIO.output(pinTrigger, False)
    StartTime = time.time()
    StopTime = StartTime

    while GPIO.input(pinEcho)==0:
        print("in loop A")
        StartTime = time.time()
        StopTime = StartTime

    while GPIO.input(pinEcho)==1:
        print("in loop B")
        StopTime = time.time()
        # If the sensor is too close to an object, the Pi cannot
        # see the echo quickly enough, so we have to detect that
        # problem and say what has happened.
        if StopTime-StartTime >= 0.04:
            print("Hold on there!  You're too close for me to see.")
            StopTime = StartTime
            break

    ElapsedTime = StopTime - StartTime
    Distance = (ElapsedTime * 34300)/2

    return Distance

# Return True if the ultrasonic sensor sees an obstacle
def IsNearObstacle(localHowNear):
    Distance = Measure()

    print("IsNearObstacle: "+str(Distance))
    if Distance < localHowNear:
        return True
    else:
        return False

# Move back a little, then turn right
def AvoidObstacle():
    # Back off a little
    print("Backwards")
    RunBackwards()
    time.sleep(ReverseTime)
    StopMotors()

    # Turn right
    print("Right")
    TurnRight()
    time.sleep(TurnTime)
    StopMotors()


# Go forwards for i secs, then stop
def Forward(i):
    RunForwards()
    time.sleep(i)
    StopMotors()

def Right(i):
    TurnRight()
    time.sleep(i)
    StopMotors()

def Left(i):
    TurnLeft()
    time.sleep(i)
    StopMotors()

def Backwards(i):
    RunBackwards()
    time.sleep(i)
    StopMotors()

def Calibrate():
    Forward(1)
    Right(1)
    Left(1)
    Backward(1)

def SetDutyCycleA(i):
    global DutyCycleA
    DutyCycleA = i
    
def SetDutyCycleB(i):
    global DutyCycleB
    DutyCycleB = i

def ForwardAvoiding():
    # Your code to control the robot goes below this line
    try:
        # Set trigger to False (Low)
        GPIO.output(pinTrigger, False)

        # Allow module to settle
        time.sleep(0.1)

        #repeat the next indented block forever
        while True:
            RunForwards()
            time.sleep(0.1)
            if IsNearObstacle(HowNear):
                StopMotors()
                AvoidObstacle()

    # If you press CTRL+C, cleanup and stop
    except KeyboardInterrupt:
        GPIO.cleanup()
