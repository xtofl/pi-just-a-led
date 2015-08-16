#!/usr/bin/env python

from io import Input, Output

pin_names = [
    "ch0", "ch1", "ch2", "ch3", "ch4", "ch5", "ch6", "ch7",
    "vdd", "vref", "agnd", "clk", "dout", "din", "!cs", "dgnd"
        ]


class Pin:
    def __init__(self, name, gpiopin):
        self.name = name
        self.pin = gpiopin


class Mcp3008:
    def __init__(self):
        self.clk = Pin("clk", Input(24))
        self.dout = Pin("dout", Output(30))
        self.din = Pin("din", Input(32))
        self.not_cs = Pin("!cs", Input(34))

    def read(self, channel): #single-ended
        self.request_conversion(channel)
        result = self.read_result()
        return result

    def request_conversion(self, channel):
        pass

    def read_result(self):
        pass

def main():
    mcp = Mcp3008()
    value = mcp.read(sys.argv[1])
    print("value: {}".format(value))


if __name__ == "__main__":
    main()
