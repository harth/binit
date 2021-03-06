import json
import os
import time
import RPi.GPIO as GPIO
from squid import *

rgb_first = Squid(4, 17, 21)
rgb_second = Squid(18, 23, 24)


def destroy():
    GPIO.cleanup()


def set_bin_colour(bin, bins):
    print("Bin colour " + bins['colour'])
    if bins['colour'] == 'Brown':
        bin.set_color(PURPLE, 100)
    elif bins['colour'] == 'Green':
        bin.set_color(GREEN)
    elif bins['colour'] == 'Blue':
        bin.set_color(BLUE)
    elif bins['colour'] == 'Grey':
        bin.set_color(CYAN)
    elif bins['colour'] == 'Glass':
        bin.set_color(YELLOW)


def flash_red():
    for i in range(1, 30):
        rgb_first.set_color(RED)
        rgb_second.set_color(RED)
        time.sleep(1)
        rgb_first.set_color([0, 0, 0])
        rgb_second.set_color([0, 0, 0])
        time.sleep(1)


def light_up():

    try:
        with open(os.environ['HOME'] + '/.wheelie/schedule.json') as scheduleLocation:
            schedule = json.load(scheduleLocation)
            bins_to_be_collected = []

            for collection in schedule:
                if collection["toBeCollected"]:
                    bins_to_be_collected.append(collection)

            # No schedule - red flashing lights
            if len(bins_to_be_collected) == 0:
                print("No scheduled bins found")
                flash_red()

            # One schedule date - one solid light, turn other one off
            if len(bins_to_be_collected) == 1:
                print("One scheduled bins found")
                set_bin_colour(rgb_first, bins_to_be_collected[0])
                rgb_second.set_color(BLACK)
                time.sleep(60)

            # Two scheduled dates - two solid lights
            if len(bins_to_be_collected) == 2:
                print("Two scheduled bins found")
                set_bin_colour(rgb_first, bins_to_be_collected[0])
                set_bin_colour(rgb_second, bins_to_be_collected[1])
                time.sleep(60)

    except IOError:
        print("File does not exist")
        flash_red()

    except ValueError:
        print("Could not read schedule")
        flash_red()


if __name__ == '__main__':  # Program entrance
    print ('Program is starting ... ')
    try:
        while True:
            light_up()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()
