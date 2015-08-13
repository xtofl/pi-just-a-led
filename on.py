#!/usr/bin/python
from RPi import GPIO

class Output:
    def __init__(self, pin, initial=False):
        self.pin = pin
        self.initial = initial

    def start(self):
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, self.initial)

    def on(self):
        GPIO.output(self.pin, True)

    def off(self):
        GPIO.output(self.pin, False)

class Input:
    def __init__(self, pin):
        self.pin = pin
        self.mode = GPIO.IN

    def start(self):
        GPIO.setup(self.pin, GPIO.IN)

    def on(self):
        return GPIO.input(self.pin)


def main():
    import sys

    try:
        GPIO.setmode(GPIO.BOARD)

        green_led = Output(7, True)
        red_led = Output(11, False)
        blue_button = Input(12)

        leds = [green_led, red_led]
        pins = [green_led, red_led, blue_button]
        for p in pins:
            p.start()


        import time
        while True:
            [l.on() for l in leds]
            time.sleep(1.0)
            [l.off() for l in leds]
            time.sleep(1.0)

        
    except RuntimeError as e:
        print("error setting pin {} to OUT: {}".format(pin, e))
    finally:
        GPIO.cleanup()
    
if __name__ == "__main__":
    main()
