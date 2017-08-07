#!/usr/bin/python

# IMPORTS
import time        # IMPORT TIME FOR THE PAUSES IN OUR CODE
import random
import signal
import sys

#import robotlibcamjam as robot # IMPORT ROBOTMASTER FOR OUR ROBOT CONTROL FUNCTIONS
import robotlibmotozero as robot # IMPORT ROBOTMASTER FOR OUR ROBOT CONTROL FUNCTIONS

def signal_handler(signal, frame):
        print('Caught signal')
        robot.Shutdown()
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def Run():
    try:
        initDutyCycleA = 90
        initDutyCycleB = 100
        robot.SetDutyCycleA(initDutyCycleA) 
        robot.SetDutyCycleB(initDutyCycleB)  

        while (True):
            print("Going forwards")
            robot.Forward(random.random() * 10)
            print("Ramming!")
            robot.Backward(0.3)
            robot.Forward(0.3)
            robot.Backward(0.3)
            robot.Forward(0.3)

            print("Random turn")
            if (random.random() < 0.5):
                robot.Left(random.random() * 5)
            else:
                robot.Right(random.random() * 5)
        
    except KeyboardInterrupt:
        print('Interrupted')
        robot.Shutdown()
        sys.exit(0)            
            
Run()
