import json
import os
import time
import RPi.GPIO as GPIO
from squid import *


led_first = [7, 11, 13]
led_second = [12, 16, 18]

rgb_first = Squid(4, 17, 21)
rgb_second = Squid(18, 23, 24)

red = [0, 100, 100]
green = [100, 0, 100]
blue = [100, 100, 0]
black = [0, 0, 0]


def setup():
    global pwmRed_first, pwmGreen_first, pwmBlue_first
 #   GPIO.setmode(GPIO.BOARD)  # use PHYSICAL GPIO Numbering
 #   GPIO.setup(led_first, GPIO.OUT)  # set RGBLED pins to OUTPUT mode
 #   GPIO.setup(led_second, GPIO.OUT)  # set RGBLED pins to OUTPUT mode
 #   GPIO.output(led_first, GPIO.HIGH)  # make RGBLED pins output HIGH level
 #   GPIO.output(led_second, GPIO.HIGH)  # make RGBLED pins output HIGH 
 #   pwmRed_first = GPIO.PWM(led_first[0], 2000)  # set PWM Frequence to 2kHz
 #   pwmGreen_first = GPIO.PWM(led_first[1], 2000)  # set PWM Frequence to 2kHz
 #   pwmBlue_first = GPIO.PWM(led_first[2], 2000)  # set PWM Frequence to 2kHz
 #   pwmRed_second = GPIO.PWM(led_first[0], 2000)  # set PWM Frequence to 2kHz
 #   pwmGreen_second = GPIO.PWM(led_first[1], 2000)  # set PWM Frequence to 2kHz
 #   pwmBlue_second = GPIO.PWM(led_first[2], 2000)  # set PWM Frequence to 2kHz
 #   pwmRed_first.start(0)  # set initial Duty Cycle to 0
 #   pwmGreen_first.start(0)
 #   pwmBlue_first.start(0)
 #   pwmRed_second.start(0)  # set initial Duty Cycle to 0
 #   pwmGreen_second.start(0)
 #   pwmBlue_second.start(0)


#def set_colour(rgb_val):  # change duty cycle for three pins to r_val,g_val,b_val
#    pwmRed_first.ChangeDutyCycle(rgb_val[0])  # change pwmRed_first duty cycle to r_val
#    pwmGreen_first.ChangeDutyCycle(rgb_val[1])
#    pwmBlue_first.ChangeDutyCycle(rgb_val[2])
    

#def set_colour_second(rgb_val):  # change duty cycle for three pins to r_val,g_val,b_val
#    pwmRed_second.ChangeDutyCycle(rgb_val[0])  # change pwmRed_first duty cycle to r_val
#    pwmGreen_second.ChangeDutyCycle(rgb_val[1])
#    pwmBlue_second.ChangeDutyCycle(rgb_val[2])


def destroy():
#    pwmRed_first.stop()
#    pwmGreen_first.stop()
#    pwmBlue_first.stop()
#    pwmRed_second.stop()
#    pwmGreen_second.stop()
#    pwmBlue_second.stop()
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
    setup()
    try:
        while True:
            light_up()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()
