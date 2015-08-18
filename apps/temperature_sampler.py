#!/usr/bin/env python
import sys
import os
from time import sleep

#FIXME: add 'justaled' to the PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(sys.argv[0])))

def resistorvalue(inputvoltage, voltage, otherresistor):
   return otherresistor * (voltage / (inputvoltage - voltage))


def sample(mcp):
    value = mcp.read(channel=0)
    return value

def publish(what):
    print(what)

def main():
    interval = float(sys.argv[1])
    from RPi import GPIO
    from justaled.mcp3008 import Mcp3008
    from justaled.io import IO
    from time import sleep
    io = IO(GPIO)
    mcp = Mcp3008(io, reference_voltage=5.0)
    io.start()
    mcp.start()
    while True:
        publish(sample(mcp))
        sleep(interval)

if __name__ == "__main__":
    main()
