import pycom
import time

pycom.heartbeat(False)

while True:
    #colors in hexadecimal (0xRRGGBB)
    pycom.rgbled(0xFF0000)  # Red
    print('red')
    time.sleep(1)
    pycom.rgbled(0x00FF00)
    print('green')  # Green
    time.sleep(1)
    pycom.rgbled(0x0000FF)  # Blue
    time.sleep(1)