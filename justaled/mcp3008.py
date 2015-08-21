#!/usr/bin/env python

from justaled.io import IO

pin_names = [
    "ch0", "ch1", "ch2", "ch3", "ch4", "ch5", "ch6", "ch7",
    "vdd", "vref", "agnd", "clk", "dout", "din", "!cs", "dgnd"
        ]


class Mcp3008:
    def __init__(self, io, reference_voltage=5.0):
        self.clk = io.outpin(23)
        self.dout = io.inpin(29)
        self.din = io.outpin(31)
        self.not_cs = io.outpin(33)
        self.vref = reference_voltage

    def start(self):
        self.clk.start()
        self.dout.start()
        self.din.start()
        self.not_cs.start()

    def read(self, channel): #single-ended
        raw = self.read_raw(channel)
        voltage = raw * self.vref / 1024.0
        return voltage

    def read_raw(self, channel): #single-ended
        if channel < 0 or channel > 7:
            raise RuntimeError("channel must be between 0 and 7")
        self.not_cs.on()
        self.clk.off()
        self.not_cs.off()
        self.request_conversion(channel)
        result = self.read_result()
        self.not_cs.off()
        return result

    def request_conversion(self, channel):
        command = int('11000', 2) | channel
        bits = command << 3
        for _ in range(5):
           self.din.set(bits & 0x80)
           self.clk.on()
           self.clk.off()
           bits <<= 1

    def read_result(self):
        adcout = 0
        for _ in range(12):
           self.clk.on()
           self.clk.off()
           adcout <<= 1
           bit = self.dout.on()
           adcout |= bit

        adcout >>= 1
        return adcout

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
