#!/usr/bin/python
from io import Input, Output

def main():
    import sys

    try:
        GPIO.setmode(GPIO.BOARD)

        green_led = Output(7, True)
        red_led = Output(11, False)
        blue_button = Input(12)
        blue_button.callback(red_led.set)

        leds = [green_led, red_led]
        pins = [green_led, red_led, blue_button]
        for p in pins:
            p.start()

        import time
        while True:
            green_led.on()
            time.sleep(1.0)
            green_led.off()
            time.sleep(1.0)

    finally:
        GPIO.cleanup()
    
if __name__ == "__main__":
    main()
