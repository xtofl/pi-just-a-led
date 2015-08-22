#!/usr/bin/env python
import sys
import os
from time import sleep
import datetime
import httplib

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
    connection =  httplib.HTTPConnection('saraxtofl.be:80')
    body_content = "{}".format(what)
    connection.request('POST', '/pi-just-a-led/index.php', body_content)
    result = connection.getresponse()
    if not result:
        print("putting has failed: {}".format(result))

def main():
    import argparse
    parser = argparse.ArgumentParser(description="temperature sampler & publisher")
    parser.add_argument('--interval-seconds', type=float, dest="interval", help="sampling interval")
    options = parser.parse_args()

    from RPi import GPIO
    from justaled.mcp3008 import Mcp3008
    from justaled.io import IO
    from time import sleep
    io = IO(GPIO)
    mcp = Mcp3008(io, reference_voltage=3.3)
    io.start()
    mcp.start()
    publish(sample(mcp))
    while options.interval:
        sleep(options.interval)
        publish(sample(mcp))

if __name__ == "__main__":
    main()
