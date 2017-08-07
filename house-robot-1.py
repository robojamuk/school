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
    initDutyCycleA = 90
    initDutyCycleB = 100
    goDistance = 20
    stopDistance = 10   
    distances = InitDistances()
 
    robot.SetDutyCycleA(initDutyCycleA) 
    robot.SetDutyCycleB(initDutyCycleB)  

    while (True):
        print("Going forwards")
        distance = CorrectedDistance(distances, robot.Measure())
        print("Distance", distance)
        robot.RunForwards()
        while (distance > stopDistance):
            distance = CorrectedDistance(distances, robot.Measure())
        print("Distance", distance)
        robot.StopMotors()
        print("Ramming!")
        robot.Backward(0.3)
        robot.Forward(0.3)
        robot.Backward(0.3)
        robot.Forward(0.3)

        while(distance < goDistance):
            print("Distance", distance)
            print("Random turn")
            if (random.random() < 0.5):
                robot.Left(random.random() * 5)
            else:
                robot.Right(random.random() * 5)
            distances = InitDistances()
            distance = CorrectedDistance(distances, robot.Measure())

def CorrectedDistance(distances, reading):
    del distances[0]
    distances.append(reading)
    (min,max) = MinMax(distances)
    if (max == min):
        return max

    total = 0.0
    count = 0
    for n in distances:
        if (n>min) and (n<max):
            total = total + n
            count = count + 1
    if (count > 0):
        return total / count
    return distances[0]

def InitDistances():
    return [robot.Measure(), robot.Measure(), robot.Measure(), robot.Measure(), robot.Measure()]

def MinMax(distances):
    max = distances[0]
    min = distances[0]
    for n in distances:
        if (n<min):
            min=n
        if (n>max):
            max=n
    return (min,max)

Run()
