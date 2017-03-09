import time
import pigpio

def mycb(x, y, z):
    print(time.time())

pin = pigpio.pi()
cb = pin.callback(23, pigpio.FALLING_EDGE, mycb)
