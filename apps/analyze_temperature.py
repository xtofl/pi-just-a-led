#!/usr/bin/env python
import sys
import os
import datetime
import httplib
import json
import urlparse
import numpy as np
import smtplib
from email.mime.text import MIMEText

#FIXME: add 'justaled' to the PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(sys.argv[0])))

def sendmail(status, options):
    message = MIMEText(status)
    message['Subject'] = status
    message['From'] = 'your raspberry pi'
    message['To'] = options.mailto
    smtp = smtplib.SMTP('localhost')
    smtp.sendmail('your pi', options.mailto.split(";"), message.as_string())

def analyze_sample_file(options):
    with open(options.samplefile, 'r') as f:
        lines = [line for line in f]
    last_lines = lines[-options.window:]
    samples = [json.loads(line) for line in last_lines]

    times = np.array([s['time'] for s in samples])
    temperatures = np.array([s['temperature']['value'] for s in samples])

    result = analyze(times, temperatures)
    if result:
        sendmail(result, options)


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
    parser.add_argument('--mailto')
    options = parser.parse_args()

    analyze_sample_file(options)

if __name__ == "__main__":
    main()
