from RPi import GPIO

def init_gpio():
    GPIO.setmode(GPIO.BOARD)
    return GPIO

class IO:
    def __init__(self, gpio):
        self.gpio = gpio

    def start(self):
        self.gpio.setmode(self.gpio.BOARD)

    def inpin(self, pin):
        return Input(pin)

    def outpin(self, pin, initial=False):
        return Output(pin, initial)

    def stop(self):
        return self.gpio.cleanup()

class Output:
    def __init__(self, pin, initial=False, io=GPIO):
        self.io = io
        self.pin = pin
        self.initial = initial

    def start(self):
        self.io.setup(self.pin, self.io.OUT)
        self.io.output(self.pin, self.initial)

    def on(self):
        self.io.output(self.pin, True)

    def off(self):
        self.io.output(self.pin, False)

    def set(self, value):
        self.io.output(self.pin, value)

class Input:
    def __init__(self, pin, io=GPIO):
        self.io = io
        self.pin = pin
        self.mode = self.io.IN
        self.callbacks = []

    def start(self):
        self.io.setup(self.pin, self.io.IN)
        self.io.add_event_detect(self.pin, self.io.BOTH, callback=self.__event_detect)

    def on(self):
        return self.io.input(self.pin)

    def callback(self, what):
        self.callbacks.append(what)

    def __event_detect(self, channel):
        if channel != self.pin:
            print("!!!! event detected for wrong channel {}".format(channel))
        state = self.on()
        for c in self.callbacks:
            c(state)


