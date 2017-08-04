#! /usr/bin/python

# IMPORTS
import os          # IMPORT OS FOR PYGAME SCREEN FRIG
import pygame      # IMPORT PYGAME FOR 2.4GHZ KEYBOARD CONTROL
import time        # IMPORT TIME FOR THE PAUSES IN OUR CODE
from pygame.locals import *

import robotlib as robot # IMPORT ROBOTLIB FOR OUR ROBOT CONTROL FUNCTIONS


##########################################################################
##       PUT YOUR CODE IN THE TWO 'FUNCTIONS' BELOW THIS POINT          ##
##########################################################################


# I wonder what these do...
robot.SetDutyCycleB(80)
robot.SetDutyCycleA(80)

# go into full screen when running (screen goes black!) if set to 1
fullscrn = 0


def RunChallenge1():
    # this code runs when you press the 1 key
    # write some code go forward for 't' (for time) seconds
    print("running challenge 1")
    t = 1
    robot.Forward(t)



def RunChallenge2():
    # this code runs when you press the 2 key
    print("running challenge 2")
    # navigate around the obstacle course!

 

def RunSelfTest():
    # run a series of simple robot commands to test it 
    print("Self test starting")
    robot.Forward(1) 
    robot.Right(1)
    robot.Left(1)
    robot.Backwards(1)
    print("Self test ended")






##########################################################################
##   DON'T CHANGE THE CODE BELOW HERE UNLESS YOU KNOW WHAT YOU'RE DOING ##
##########################################################################


# initialise everything
print("INITIALISE PYGAME")
time.sleep(3)

# SET UP FAKE VIDEO DRIVER FOR PYGAME
os.environ["SDL_VIDEODRIVER"] = "dummy" 
pygame.init()

width = 300
height = 300

# GO INTO FULL SCREEN MODE, AVOIDS PROBLEMS LOSING FOCUS
if fullscrn == 1:
    print("***************************************************")
    print("* GOING FULL SCREEN - HIT ESC TO EXIT AT ANY TIME *")
    print("***************************************************")
    time.sleep(1)
    print("3...")
    time.sleep(1)
    print("2...")
    time.sleep(1)
    print("1...")
    time.sleep(1)
    display = pygame.display.set_mode((width,height),pygame.FULLSCREEN)
else:
    display = pygame.display.set_mode((width,height))



# MAIN LOOP TO READ KEYPRESSES AND TAKE APPROPRIATE ACTION
try:
    print("READY FOR ROBOT COMMANDS")
    while(True):

        for event in pygame.event.get(): # LOOK FOR A PYGAME EVENT
            
            #########################################
            # IF A KEY IS BEING PRESSED...          #
            #########################################
            
            if event.type == pygame.KEYDOWN: # IF A KEY IS PRESSED DOWN

                #======================================================
                # KEY DEBUG - PRINTS THE KEY DETECTED IN THE TERMINAL (Optional)
                newkey = ""
                newkey = pygame.key.name(event.key)
                print("Pressed: " + newkey)

                # get out if quitting
                if event.key == pygame.K_ESCAPE:
                    print("Escape Pressed - Tidying up and quitting!")
                    robot.StopMotors()
                    pygame.quit()
                    quit()
                    
                #======================================================
                # BASIC MOVEMENT (FWD, REV, RIGHT, LEFT)
            
                if event.key == pygame.K_UP: # UP KEY PRESSED
                    robot.RunForwards()
                    
                if event.key == pygame.K_DOWN: # DOWN KEY PRESSED
                    robot.RunBackwards()

                if event.key == pygame.K_RIGHT: # RIGHT KEY PRESSED
                    robot.TurnRight()

                if event.key == pygame.K_LEFT: # LEFT KEY PRESSED
                    robot.TurnLeft()

                # OTHER FUNCTIONS AND CHALLENGES
                
                if event.key == pygame.K_t: # 't' KEY PRESSED
                    RunSelfTest()
                    
                if event.key == pygame.K_1: # '1' KEY PRESSED
                    RunChallenge1()
                    
                if event.key == pygame.K_2: # '2' KEY PRESSED
                    RunChallenge2()                    
           
            #########################################
            # IF A KEY IS NOT BEING PRESSED...      #
            #########################################

            elif event.type == pygame.KEYUP: # IF A KEY IS RELEASED
            
                # STOP ALL MOVEMENT (WHEN NO KEY PRESSED)

                if event.key == pygame.K_UP: # UP KEY RELEASED
                    robot.StopMotors()
                    
                if event.key == pygame.K_DOWN: # DOWN KEY RELEASED
                    robot.StopMotors()
                    
                if event.key == pygame.K_RIGHT: # RIGHT KEY RELEASED
                    robot.StopMotors()
                    
                if event.key == pygame.K_LEFT: # LEFT KEY RELEASED
                    robot.StopMotors()

        
except KeyboardInterrupt:   
    robot.StopMotors()               
    pygame.quit()
    print("--- EXITING NOW ---")
    quit()
