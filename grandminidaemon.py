import sys
import time
import pigpio

def pigpio_callback(x, y, z):
    time_triggered = time.time()
    print(time_triggered)
    file_handle.write(str(time_triggered))
    file_handle.flush()

# open file
output_file = sys.argv[1]
try:
    file_handle = open(output_file, "a")
except IOError:
    print("Error opening file ", output_file)
    sys.exit()

# set up pigpio
pigpio_connection = pigpio.pi()
cb = pigpio_connection.callback(23, pigpio.FALLING_EDGE, pigpio_callback)

# loop forever
while(True):
    time.sleep(30)
