# servo touch hat
# https://www.explainingcomputers.com/pi_servos_video.html
# https://github.com/adafruit/Adafruit_CircuitPython_MPR121

# sudo apt update
# sudo apt install RPi.GPIO
# sudo apt install board
# sudo apt install busio
# sudo api install adafruit_mpr121

# Import libraries
import RPi.GPIO as GPIO
import time
import board
import busio

# Set GPIO numbering mode
GPIO.setmode(GPIO.BOARD)

# Set pin 11 as an output, and define as servo1 as PWM pin
GPIO.setup(11,GPIO.OUT)
servo1 = GPIO.PWM(11,50) # pin 11 for servo1, pulse 50Hz

# Start PWM running, with value of 0 (pulse off)
servo1.start(0)

# Loop to allow user to set servo angle. Try/finally allows exit
# with execution of servo.stop and GPIO cleanup :)

def dispenseTreat(angle=90,delayTime=0.3):
    servo1.ChangeDutyCycle(2+(angle/18))
    time.sleep(delayTime)
    servo1.ChangeDutyCycle(0)
    #Clean things up at the end
    servo1.stop()
    GPIO.cleanup()



# Simple test of the MPR121 capacitive touch sensor library.
# Will print out a message when any of the 12 capacitive touch inputs of the
# board are touched.  Open the serial REPL after running to see the output.
# Author: Tony DiCola

def testTouched():
    # Create I2C bus.
    i2c = busio.I2C(board.SCL, board.SDA)

    # Create MPR121 object.
    mpr121 = adafruit_mpr121.MPR121(i2c)

    # Note you can optionally change the address of the device:
    # mpr121 = adafruit_mpr121.MPR121(i2c, address=0x91)

    # Loop forever testing each input and printing when they're touched.
    while True:
        # Loop through all 12 inputs (0-11).
        for i in range(12):
            # Call is_touched and pass it then number of the input.  If it's touched
            # it will return True, otherwise it will return False.
            if mpr121[i].value:
                print("Input {} touched!".format(i))
        time.sleep(0.25)  # Small delay to keep from spamming output messages.


def ifTouchedThenDispenseTreat():
    i2c = busio.I2C(board.SCL, board.SDA)
    mpr121 = adafruit_mpr121.MPR121(i2c)

    while True:
        # Loop through all 12 inputs (0-11).
        for i in range(12):
            # Call is_touched and pass it then number of the input.  If it's touched
            # it will return True, otherwise it will return False.
            if mpr121[i].value:
                dispenseTreat()
        time.sleep(0.25)  # Small delay to keep from spamming output messages.

def ifTouchedInOrderDispenseTreat(numNeededToTouch=3):
    i2c = busio.I2C(board.SCL, board.SDA)
    mpr121 = adafruit_mpr121.MPR121(i2c)
    lastTouched = -1
    while True:
        # Loop through all 12 inputs (0-11).
        for i in range(numNeededToTouch):
            
            if mpr121[i].value and (int(i)==int(lastTouched+1)):
                lastTouched += 1
                if int(lastTouched-1) == numNeededToTouch:
                    dispenseTreat()
                    lastTouched = -1
        time.sleep(0.25)  # Small delay to keep from spamming output messages.