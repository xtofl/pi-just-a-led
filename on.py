#!/usr/bin/python


def main():
    import sys
    pin = int(sys.argv[1])
    print("light on for pin {}".format(pin))

    from RPi import GPIO
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, True)
    
if __name__ == "__main__":
    main()
