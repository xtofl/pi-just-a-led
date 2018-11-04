#!/usr/bin/env python

from justaled.io import IO

pin_names = [
    "ch0", "ch1", "ch2", "ch3", "ch4", "ch5", "ch6", "ch7",
    "vdd", "vref", "agnd", "clk", "dout", "din", "!cs", "dgnd"
        ]


class Mcp3008:
    def __init__(self, spi, reference_voltage=5.0):
        self.spi = spi
        self.vref = reference_voltage

    def read(self, channel): #single-ended
        raw = self.read_raw(channel)[0]
        print("raw: {}".format(raw))
        voltage = int(raw) * self.vref / 1024.0
        return voltage

    def read_raw(self, channel): #single-ended
        if channel < 0 or channel > 7:
            raise RuntimeError("channel must be between 0 and 7")
        self.request_conversion(channel)
        return self.read_result()

    def request_conversion(self, channel):
        print("channel: {}".format(channel))
        command = int('11000', 2) | channel
        bits = command << 3
        print("xfer: {}".format(self.spi.writebytes([bits])))

    def read_result(self):
        return self.spi.readbytes(1)

def main():
    import sys
    import RPi
    gpio = IO(RPi.GPIO)
    mcp = Mcp3008(gpio)
    
    gpio.start()
    mcp.start()

    value = mcp.read(int(sys.argv[1]))
    print("value: {}".format(value))
    gpio.stop()


if __name__ == "__main__":
    main()
