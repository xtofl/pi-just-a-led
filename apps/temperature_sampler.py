#!/usr/bin/env python
import sys
from time import sleep

def resistorvalue(inputvoltage, voltage, otherresistor):
   return otherresistor * (voltage / (inputvoltage - voltage))


def sample(mcp):
    value = mcp.read(channel=0)
    return value

def publish(what):
    print(what)

def main():
    interval = sys.argv[1]
    from mcp3008 import Mcp3008
    from io import IO
    io = IO()
    mcp = Mcp3008(io, reference_voltage=5.0)
    io.start()
    mcp.start()
    while True:
        publish(sample(mcp))
        sleep(interval)

if __name__ == "__main__":
    main()
