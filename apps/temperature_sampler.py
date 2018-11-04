#!/usr/bin/env python
import sys
import os
from time import sleep
import datetime

#FIXME: add 'justaled' to the PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(sys.argv[0])))
from justaled import epoxy_thermistor

def voltage_divider_R2(inputvoltage, voltage, R1):
   return R1 * (voltage / (inputvoltage - voltage))

def sample(mcp):
    voltage = mcp.read(channel=0)
    resistance = voltage_divider_R2(mcp.vref, voltage, R1=10000.0)
    temperature = epoxy_thermistor.temperature(resistance)
    now = datetime.datetime.now()
    return (now, voltage, resistance, temperature)

def publish(what):
    now, voltage, resistance, temperature = what
    print( "{}, {}V, {} kOhm, {} C".format(now, voltage, resistance, temperature))

def main():
    interval = None
    if len(sys.argv) > 1:
        interval = float(sys.argv[1])
    from RPi import GPIO
    from justaled.mcp3008 import Mcp3008
    from justaled.io import IO
    import spidev
    spi = spidev.SpiDev()
    spi.open(0, 1)
    spi.max_speed_hz = 10000
    mcp = Mcp3008(spi, reference_voltage=3.3)
    publish(sample(mcp))

if __name__ == "__main__":
    main()
