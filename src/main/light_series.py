import json
import os
import time
import RPi.GPIO as GPIO

pins = [22, 32, 38, 37]

def setup():
    GPIO.setmode(GPIO.BOARD)  # use PHYSICAL GPIO Numbering
    GPIO.setup(pins, GPIO.OUT)  # set RGBLED pins to OUTPUT mode
    GPIO.output(pins, GPIO.LOW)  # make RGBLED pins output HIGH level


def destroy():
    GPIO.cleanup()


def set_bin_colour(bins):
    print("Bin colour " + bins['colour'])
    if bins['colour'] == 'Brown':
        GPIO.output(pins[0], GPIO.HIGH)
    elif bins['colour'] == 'Green':
        GPIO.output(pins[1], GPIO.HIGH)
    elif bins['colour'] == 'Blue':
        GPIO.output(pins[2], GPIO.HIGH)
    elif bins['colour'] == 'Grey':
        GPIO.output(pins[3], GPIO.HIGH)
    elif bins['colour'] == 'Glass':
        flash_green()      

def flash_green():
    for i in range(1, 30):
        for p in range(0, 3):
            GPIO.output(pins[3], GPIO.HIGH)
        time.sleep(1)
        for p in range(0, 3):
            GPIO.output(pins[3], GPIO.LOW)
        time.sleep(1)   

def flash_all():
    for i in range(1, 30):
        for p in range(0, 3):
            GPIO.output(pins, GPIO.HIGH)
        time.sleep(1)
        for p in range(0, 3):
            GPIO.output(pins, GPIO.LOW)
        time.sleep(1)


def light_up():

    try:
        with open(os.environ['HOME'] + '/.wheelie/schedule.json') as scheduleLocation:
            schedule = json.load(scheduleLocation)
            bins_to_be_collected = []

            for collection in schedule:
                if collection["toBeCollected"]:
                    bins_to_be_collected.append(collection)

            GPIO.output(pins, GPIO.LOW)

            # No schedule - red flashing lights
            if len(bins_to_be_collected) == 0:
                print("No scheduled bins found")
                flash_all()

            # One schedule date - one solid light, turn other one off
            if len(bins_to_be_collected) == 1:
                print("One scheduled bins found")
                for bins in bins_to_be_collected:
                    set_bin_colour(bins)
                time.sleep(60)

            # Two scheduled dates - two solid lights
            if len(bins_to_be_collected) == 2:
                print("Two scheduled bins found")
                for bins in bins_to_be_collected:
                    set_bin_colour(bins)
                time.sleep(60)

    except IOError:
        print("File does not exist")
        flash_all()

    except ValueError:
        print("Could not read schedule")
        flash_all()


if __name__ == '__main__':  # Program entrance
    print ('Program is starting ... ')
    setup()
    try:
        while True:
            light_up()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()
