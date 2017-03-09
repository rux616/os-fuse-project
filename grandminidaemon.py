import time
import pigpio
import sys

def mycb(x, y, z):
    print(time.time())

def main():
    pin = pigpio.pi()
    cb = pin.callback(23, pigpio.FALLING_EDGE, mycb)
    while(True):
        time.sleep(10)
