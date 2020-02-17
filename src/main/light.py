import json

try:
    with open('/Users/stuartwilson/.wheelie/schedule.json') as scheduleLocation:
        schedule = json.load(scheduleLocation)
        binsToBeCollected = []

        for collection in schedule:
            if collection["toBeCollected"]:
                binsToBeCollected.append(collection)

        # No schedule - red flashing lights
        if len(binsToBeCollected) == 0:
            print "No bins to be collected"

        # One schedule date - one solid light, turn other one off
        if len(binsToBeCollected) == 1:
            print "Only display one light"

        # Two scheduled dates - two solid lights
        if len(binsToBeCollected) == 2:
            print "Display two lights"

        print binsToBeCollected
except IOError:
    print "File does not exist"



