#!/usr/bin/python

# IMPORTS
import time        # IMPORT TIME FOR THE PAUSES IN OUR CODE
import random
import signal
import sys
import os 
import curses


import robotlibcamjam as robot # IMPORT ROBOTMASTER FOR OUR ROBOT CONTROL FUNCTIONS
#import robotlibmotozero as robot # IMPORT ROBOTMASTER FOR OUR ROBOT CONTROL FUNCTIONS

def signal_handler(signal, frame):
        print('Caught signal')
        robot.Shutdown()
        curses.endwin()
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def Run():
    initDutyCycleA = 100
    initDutyCycleB = 100
 
    robot.SetDutyCycleA(initDutyCycleA) 
    robot.SetDutyCycleB(initDutyCycleB)  

    stdscr = curses.initscr()
    curses.cbreak()
    stdscr.keypad(1)
    
    stdscr.addstr(0,10,"Hit 'q' to quit")
    stdscr.nodelay(1)  #nodelay(1) give us a -1 back when nothing is pressed

    action = "unknown"
    startTime = time.time()
    dir = ' '
    while dir != ord('q'):
        stdscr.refresh()
        last_dir = dir
        dir = stdscr.getch() 
        stdscr.addch(20,25,dir)
        
        if dir == ord('e'):
            stdscr.addstr(1,10,"Stop      ")
            robot.StopMotors()
        if  dir == ord('a') or dir == 260:
            stdscr.addstr(1,10,"Left      ")
            action = "robot.Left"
            startTime = time.time()
            robot.TurnLeft()
        if dir == ord('s') or dir == 258:
            stdscr.addstr(1,10,"Backwards ")
            action = "robot.Backward"
            startTime = time.time()
            robot.RunBackwards()
        if dir == ord('d') or dir == 261:
            stdscr.addstr(1,10,"Right     ")
            action = "robot.Right"
            startTime = time.time()
            robot.TurnRight()
        if dir == ord('w') or dir == 259:
            stdscr.addstr(1,10,"Forwards  ")
            action = "robot.Forward"
            startTime = time.time()
            robot.RunForwards()
        if dir == int('-1'):
            stdscr.addstr(1,10,"Stop      ")
            robot.StopMotors()
            interval = time.time() - startTime
#            print(action + "(" + str(interval) + ")")
        if (dir != last_dir) and (dir != int('-1')):
            time.sleep(0.25)
        else:
            time.sleep(0.03)
        
    curses.nocbreak()
    stdscr.keypad(0)
    curses.endwin()
    robot.Shutdown()

Run()
