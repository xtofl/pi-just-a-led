#!/usr/bin/env python
import sys
import os
from time import sleep
import datetime
import httplib

#FIXME: add 'justaled' to the PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(sys.argv[0])))
from justaled import epoxy_thermistor

def resistorvalue(inputvoltage, voltage, otherresistor):
   return otherresistor * (voltage / (inputvoltage - voltage))


def sample(mcp):
    voltage = mcp.read(channel=0)
    resistance = 10.0 / ( 1.0 - voltage / mcp.vref )
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
    interval = None
    if len(sys.argv) > 1:
        interval = float(sys.argv[1])
    from RPi import GPIO
    from justaled.mcp3008 import Mcp3008
    from justaled.io import IO
    from time import sleep
    io = IO(GPIO)
    mcp = Mcp3008(io, reference_voltage=3.3)
    io.start()
    mcp.start()
    publish(sample(mcp))
    while interval:
        publish(sample(mcp))
        sleep(interval)

if __name__ == "__main__":
    main()
