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

    def set(self, value):
        GPIO.output(self.pin, value)

class Input:
    def __init__(self, pin):
        self.pin = pin
        self.mode = GPIO.IN
        self.callbacks = []

    def start(self):
        GPIO.setup(self.pin, GPIO.IN)
        GPIO.add_event_detect(self.pin, GPIO.BOTH, callback=self.__event_detect)

    def on(self):
        return GPIO.input(self.pin)

    def callback(self, what):
        self.callbacks.append(what)

    def __event_detect(self, channel):
        print("event detected for channel {}".format(channel))
        if channel != self.pin:
            print("!!!! event detected for wrong channel {}".format(channel))
        state = self.on()
        for c in self.callbacks:
            c(state)


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
