#!/usr/bin/python


def main():
    import sys
    pin = int(sys.argv[1])
    print("light on for pin {}".format(pin))

    try:
        from RPi import GPIO
        GPIO.setmode(GPIO.BOARD)
        try:
            GPIO.setup(pin, GPIO.OUT)
        except RuntimeError as e:
            print("error setting pin {} to OUT: {}".format(pin, e))
        GPIO.output(pin, True)
    finally:
        GPIO.cleanup()
    
if __name__ == "__main__":
    main()
