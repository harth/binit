@Grab(group = 'com.pi4j', module = 'pi4j-core', version = '1.2')

import com.pi4j.io.gpio.*

import java.awt.*
import com.pi4j.wiringpi.SoftPwm;

def led = new RGBLed(pinLayout: new PinLayout(redPin: RaspiPin.GPIO_11, bluePin: RaspiPin.GPIO_12, greenPin: RaspiPin.GPIO_13))
led.displayColor(Color.BLUE)




class RGBLed {

    private final PinLayout pinLayout;
    private Color color = Color.BLACK;

    /**
     * constructs a new RGBLed using the given pinLayout to control the
     * LED
     *
     * @param pinLayout a GPIO pinLayout
     */
    public RGBLed(PinLayout pinLayout) {
        this.pinLayout = pinLayout;

        final GpioController gpio = GpioFactory.getInstance();

        final GpioPinDigitalOutput ledRed = gpio.provisionDigitalOutputPin(pinLayout.getRedPin());
        final GpioPinDigitalOutput ledGreen = gpio.provisionDigitalOutputPin(pinLayout.getGreenPin());
        final GpioPinDigitalOutput ledBlue = gpio.provisionDigitalOutputPin(pinLayout.getBluePin());

        ledRed.setShutdownOptions(true, PinState.LOW, PinPullResistance.OFF);
        ledGreen.setShutdownOptions(true, PinState.LOW, PinPullResistance.OFF);
        ledBlue.setShutdownOptions(true, PinState.LOW, PinPullResistance.OFF);

        SoftPwm.softPwmCreate(pinLayout.getRedPin().getAddress(), 0, 50);
        SoftPwm.softPwmCreate(pinLayout.getGreenPin().getAddress(), 0, 50);
        SoftPwm.softPwmCreate(pinLayout.getBluePin().getAddress(), 0, 50);

        off();
    }

    void displayColor(Color color) {
        final float[] colors = color.getRGBColorComponents(null);
        SoftPwm.softPwmWrite(pinLayout.getRedPin().getAddress(), (int) (colors[0] * 50f));
        SoftPwm.softPwmWrite(pinLayout.getGreenPin().getAddress(), (int) (colors[1] * 50f));
        SoftPwm.softPwmWrite(pinLayout.getBluePin().getAddress(), (int) (colors[2] * 50f));
        this.color = color;
    }

    final void off() {
        displayColor(Color.RED);
    }

    Color getDisplayedColor() {
        return color;
    }

}

class PinLayout {
    Pin redPin
    Pin greenPin
    Pin bluePin
}