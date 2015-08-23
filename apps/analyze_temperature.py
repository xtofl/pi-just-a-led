#!/usr/bin/env python
import sys
import os
import datetime
import httplib
import json
import urlparse
import numpy as np

#FIXME: add 'justaled' to the PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(sys.argv[0])))


def analyze_sample_file(filename, window):
    with open(filename, 'r') as f:
        lines = [line for line in f]
    last_lines = lines[-window:]
    samples = [json.loads(line) for line in last_lines]

    times = np.array([s['time'] for s in samples])
    temperatures = np.array([s['temperature']['value'] for s in samples])

    result = analyze(times, temperatures)
    if result:
        print(result)


def analyze(times, temperatures):
    """
    >>> import numpy as np
    >>> analyze(np.array([1,2,3]), np.array([1, 1, 1]))
    >>> analyze(np.array([1,2,3]), np.array([1, 1, -1]))
    >>> analyze(np.array([1,2,3]), np.array([1, 2, 3]))
    'temperature rises'
    """
    temperature_differences = np.diff(temperatures)
    if np.all(temperature_differences > 0):
        return 'temperature rises'
    return None


def main():
    import argparse
    parser = argparse.ArgumentParser(description="temperature trend analysis")
    parser.add_argument('--sample-file', dest="samplefile", help="file containing json samples")
    parser.add_argument('--window', help="size of time window to analyze", type=int, default=3)
    options = parser.parse_args()

    analyze_sample_file(options.samplefile, options.window)

if __name__ == "__main__":
    main()
