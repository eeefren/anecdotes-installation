#!/usr/bin/python
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|R|a|s|p|b|e|r|r|y|P|i|-|S|p|y|.|c|o|.|u|k|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# ultrasonic_1.py
# Measure distance using an ultrasonic module
#
# Author : Matt Hawkins
# Date   : 09/01/2013

# Import required Python libraries
import time
import RPi.GPIO as GPIO

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

# Define GPIO to use on Pi
GPIO_TRIGGER = 23
GPIO_ECHO = 24

print "Ultrasonic Measurement"

# Set pins as output and input
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  # Trigger
GPIO.setup(GPIO_ECHO,GPIO.IN)      # Echo

# Set trigger to False (Low)
GPIO.output(GPIO_TRIGGER, False)

# Allow module to settle
time.sleep(0.5)

def measure_distance():
    time.sleep(0.5)
    reset = time.time()
    # Send 10us pulse to trigger
    print "Send 10us pulse to trigger"
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    #time.sleep(0.0001)
    GPIO.output(GPIO_TRIGGER, False)
    start = time.time()
    print "waiting for GPIO_ECHO to become 1"
    while GPIO.input(GPIO_ECHO)==0:
        if start > reset + 1.0:
            return
        start = time.time()

    stop = time.time()
    print "waiting for GPIO_ECHO to become 0"
    while GPIO.input(GPIO_ECHO)==1:
        if stop > reset + 3.0:
            return
        stop = time.time()

    # Calculate pulse length
    elapsed = stop-start

    # Distance pulse travelled in that time is time
    # multiplied by the speed of sound (cm/s)
    distance = elapsed * 34000

    # That was the distance there and back so halve the value
    distance = distance / 2

    print "Distance : %.1f" % distance

try:
    while True:
        measure_distance()
except KeyboardInterrupt:
    # Reset GPIO settings
    GPIO.cleanup()
