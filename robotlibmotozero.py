import RPi.GPIO as GPIO # Import the GPIO Library
import time # Import the Time library

# Set the GPIO modes
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


Motor1Enable = 5 
Motor1A = 24 
Motor1B = 27 

Motor2Enable = 17 
Motor2A = 6 
Motor2B = 22 

Motor3Enable = 12 
Motor3A = 23
Motor3B = 16 

Motor4Enable = 25 
Motor4A = 18 
Motor4B = 13 

# Define GPIO pins to use on the Pi for the ultrasonic distance measurer
pinTrigger = 21
pinEcho = 20

# How many times to turn the pin on and off each second
Frequency = 20
# How long the pin stays on each cycle, as a percent
DutyCycleA = 70
DutyCycleB = 70

# Settng the duty cycle to 0 means the motors will not turn
Stop = 0

# Set the GPIO Pin mode to be Output
GPIO.setup(Motor1Enable, GPIO.OUT)
GPIO.setup(Motor1A, GPIO.OUT)
GPIO.setup(Motor1B, GPIO.OUT)
GPIO.setup(Motor2Enable, GPIO.OUT)
GPIO.setup(Motor2A, GPIO.OUT)
GPIO.setup(Motor2B, GPIO.OUT)
GPIO.setup(Motor3Enable, GPIO.OUT)
GPIO.setup(Motor3A, GPIO.OUT)
GPIO.setup(Motor3B, GPIO.OUT)
GPIO.setup(Motor4Enable, GPIO.OUT)
GPIO.setup(Motor4A, GPIO.OUT)
GPIO.setup(Motor4B, GPIO.OUT)

# Set pins as output and input
GPIO.setup(pinTrigger, GPIO.OUT)  # Trigger
GPIO.setup(pinEcho, GPIO.IN)      # Echo

# Set the GPIO to software PWM at 'Frequency' Hertz
pwmMotor1 = GPIO.PWM(Motor1Enable, Frequency)
pwmMotor2 = GPIO.PWM(Motor2Enable, Frequency)
pwmMotor3 = GPIO.PWM(Motor3Enable, Frequency)
pwmMotor4 = GPIO.PWM(Motor4Enable, Frequency)

# Start the software PWM with a duty cycle of 0 (i.e. not moving)
pwmMotor1.start(Stop)
pwmMotor2.start(Stop)
pwmMotor3.start(Stop)
pwmMotor4.start(Stop)

# Turn all motors off
def StopMotors():
    pwmMotor1.ChangeDutyCycle(Stop)
    pwmMotor2.ChangeDutyCycle(Stop)


# Turn both motors forwards
def RunForwards():
    GPIO.output(Motor1A,GPIO.HIGH) # GPIO high to send power to the + terminal
    GPIO.output(Motor1B,GPIO.LOW)  # GPIO low to ground the - terminal 
    GPIO.output(Motor2A,GPIO.HIGH) # GPIO high to send power to the + terminal
    GPIO.output(Motor2B,GPIO.LOW)  # GPIO low to ground the - terminal 
    pwmMotor1.ChangeDutyCycle(DutyCycleA)
    pwmMotor2.ChangeDutyCycle(DutyCycleB)

# Turn both motors backwards
def RunBackwards():
    GPIO.output(Motor1A,GPIO.LOW) 
    GPIO.output(Motor1B,GPIO.HIGH)  
    GPIO.output(Motor2A,GPIO.LOW) 
    GPIO.output(Motor2B,GPIO.HIGH)  
    pwmMotor1.ChangeDutyCycle(DutyCycleA)
    pwmMotor2.ChangeDutyCycle(DutyCycleB)

# Turn left
def TurnLeft():
    GPIO.output(Motor1A,GPIO.LOW) 
    GPIO.output(Motor1B,GPIO.HIGH)  
    GPIO.output(Motor2A,GPIO.HIGH)
    GPIO.output(Motor2B,GPIO.LOW)  
    pwmMotor1.ChangeDutyCycle(DutyCycleA)
    pwmMotor2.ChangeDutyCycle(DutyCycleB)

# Turn Right
def TurnRight():
    GPIO.output(Motor1A,GPIO.HIGH) 
    GPIO.output(Motor1B,GPIO.LOW)  
    GPIO.output(Motor2A,GPIO.LOW) 
    GPIO.output(Motor2B,GPIO.HIGH)  
    pwmMotor1.ChangeDutyCycle(DutyCycleA)
    pwmMotor2.ChangeDutyCycle(DutyCycleB)


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
        StartTime = time.time()
        StopTime = StartTime

    while GPIO.input(pinEcho)==1:
        StopTime = time.time()
        # If the sensor is too close to an object, the Pi cannot
        # see the echo quickly enough, so we have to detect that
        # problem and say what has happened.
        if StopTime-StartTime >= 0.04:
            print("Hold on there!  You're too close for me to see.")
            StopTime = StartTime
            return 0

    ElapsedTime = StopTime - StartTime
    Distance = (ElapsedTime * 34300)/2

    return Distance

def TestGpio():
    GPIO.output(pinTrigger, False)
    time.sleep(0.03)
    state = GPIO.input(pinEcho)
    if (state):
        print("Bad state " + str(pinEcho) + " should be low")
    else:
        print("Good low state")
        
    GPIO.output(pinTrigger, True)
    time.sleep(0.03)
    state = GPIO.input(pinEcho)
    if (state):
        print("Good high state")
    else:
        print("Bad state " + str(pinEcho) + " should be high")
                
    GPIO.output(pinTrigger, False)


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

def Backward(i):
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

def Shutdown():
    StopMotors()
    GPIO.cleanup()
    