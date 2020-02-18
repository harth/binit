import json
import os
import time
import RPi.GPIO as GPIO

pins = [35, 37, 40]
red = [0, 100, 100]
green = [100, 0, 100]
blue = [100, 100, 0]
black = [0, 0, 0]


def setup():
    global pwmRed, pwmGreen, pwmBlue
    GPIO.setmode(GPIO.BOARD)  # use PHYSICAL GPIO Numbering
    GPIO.setup(pins, GPIO.OUT)  # set RGBLED pins to OUTPUT mode
    GPIO.output(pins, GPIO.HIGH)  # make RGBLED pins output HIGH level
    pwmRed = GPIO.PWM(pins[0], 2000)  # set PWM Frequence to 2kHz
    pwmGreen = GPIO.PWM(pins[1], 2000)  # set PWM Frequence to 2kHz
    pwmBlue = GPIO.PWM(pins[2], 2000)  # set PWM Frequence to 2kHz
    pwmRed.start(0)  # set initial Duty Cycle to 0
    pwmGreen.start(0)
    pwmBlue.start(0)


def set_colour(rgb_val):  # change duty cycle for three pins to r_val,g_val,b_val
    pwmRed.ChangeDutyCycle(rgb_val[0])  # change pwmRed duty cycle to r_val
    pwmGreen.ChangeDutyCycle(rgb_val[1])
    pwmBlue.ChangeDutyCycle(rgb_val[2])


def destroy():
    pwmRed.stop()
    pwmGreen.stop()
    pwmBlue.stop()
    GPIO.cleanup()


def set_bin_colour(bins):
    print("Bin colour " + bins['colour'])
    if bins['colour'] == 'Brown':
        set_colour(red)
    elif bins['colour'] == 'Green':
        set_colour(green)
    elif bins['colour'] == 'Blue':
        set_colour(blue)
    elif bins['colour'] == 'Grey':
        set_colour(blue)
    elif bins['colour'] == 'Glass':
        set_colour(green)


def flash_red():
    for i in range(1, 30):
        set_colour(red)
        time.sleep(1)
        set_colour(black)
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


if __name__ == '__main__':  # Program entrance
    print ('Program is starting ... ')
    setup()
    try:
        while True:
            light_up()
            time.sleep()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()
