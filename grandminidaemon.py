import sys
import time
import pigpio

def pigpio_callback(x, y, z):
    print(time.time())

def signal_handler(signal, frame):


def main(output_file):
    # open file
    try:
        file_handle = open(output_file, "a")
    except expression as identifier:
        sys.exit()

    # set up signal handler

    # set up pigpio
    pigpio_connection = pigpio.pi()
    cb = pigpio_connection.callback(23, pigpio.FALLING_EDGE, pigpio_callback)

    # loop forever
    while(True):
        time.sleep(30)

if __name__ == '__main__':
    main(sys.argv[1])