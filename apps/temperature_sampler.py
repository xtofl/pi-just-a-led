#!/usr/bin/env python
import sys
import os
from time import sleep
import datetime
import httplib
import json
import urlparse

#FIXME: add 'justaled' to the PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(sys.argv[0])))
from justaled import epoxy_thermistor

def voltage_divider_R2(inputvoltage, voltage, R1):
   return R1 * (voltage / (inputvoltage - voltage))


class Sample:
    def __init__(self, source, mcp, channel=0):
        self.source = source
        self.mcp = mcp
        self.value = None
        self.voltage = mcp.read(channel=channel)
        self.resistance = voltage_divider_R2(mcp.vref, self.voltage, R1=10000.0)
        self.temperature = epoxy_thermistor.temperature(self.resistance)
        self.now = datetime.datetime.now()

    def value(self):
        return (self.now, self.voltage, self.resistance, self.temperature)

    def as_csv(self):
        return "{}, {}V, {} kOhm, {} C".format(self.now, self.voltage, self.resistance, self.temperature)

    def as_json(self):
        return json.dumps({
            'source': self.source,
            'time': self.now.isoformat(),
            'voltage': self.voltage,
            'thermistor': {'value': self.resistance, 'unit': 'Ohm'},
            'temperature': {'value': self.temperature, 'unit': 'C'}
        })

def publish(what, where, samplefile):
    print(what.as_csv())
    if samplefile:
        with open(samplefile, 'a') as f:
            f.write(what.as_json() + "\n")
    connection =  httplib.HTTPConnection('{}:{}'.format(where.hostname, where.port))
    body_content = what.as_json()
    connection.request('POST', where.path, body_content)
    result = connection.getresponse()
    if not result:
        print("putting has failed: {}".format(result))

def main():
    import argparse
    parser = argparse.ArgumentParser(description="temperature sampler & publisher")
    parser.add_argument('--format', help="output format [json|csv]")
    parser.add_argument('--target-url', dest="target", help="url to publish to")
    parser.add_argument('--interval-seconds', type=float, dest="interval", help="sampling interval")
    parser.add_argument('--samplefile', type=str, help="file to contain samples")
    options = parser.parse_args()

    from RPi import GPIO
    from justaled.mcp3008 import Mcp3008
    from justaled.io import IO
    from time import sleep
    io = IO(GPIO)
    mcp = Mcp3008(io, reference_voltage=3.3)
    io.start()
    mcp.start()
    target = urlparse.urlparse(options.target)
    publish(Sample('pi-01', mcp), target, options.samplefile)
    while options.interval:
        sleep(options.interval)
        publish(Sample('pi-01', mcp), target, options.samplefile)

if __name__ == "__main__":
    main()
