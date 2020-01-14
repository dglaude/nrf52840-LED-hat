# This example adapted from ble_detailed_scan.py
# If the correct peripherial is found, it writes a couple predefined characteristic values

import time
import board
from digitalio import DigitalInOut, Direction, Pull

led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

from adafruit_ble import BLERadio
from adafruit_ble.advertising import Advertisement
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement

###
import _bleio
###

ble = BLERadio()

from adafruit_ble.services import Service
from adafruit_ble.uuid import VendorUUID
from adafruit_ble.characteristics import Characteristic

class MyService(Service):
  uuid = VendorUUID("0000fee9-0000-1000-8000-00805f9b34fb")
  my_characteristic1 = Characteristic(uuid=VendorUUID("d44bc439-abfd-45a2-b575-925416129600")) #
  my_characteristic2 = Characteristic(uuid=VendorUUID("d44bc439-abfd-45a2-b575-92541612960A")) #

ble_connection = None

#daysLeft = 2
currentTime = 1234

digit_characteristic = [ \
    b'\x28\x33\x1e\xf1\x5f\x7d\x34\x47\xd9\x28\x77\x0c\x6d\xd9\x87\xcb' , \
    b'\x4d\x3a\xc3\x7c\x3b\x44\x1c\x13\xdb\x3e\x24\x91\x33\xbb\x29\x7f' , \
    b'\x50\x37\x9d\x46\x47\xab\x31\xc4\x1f\x4a\x58\x50\x49\xb3\x36\x40' , \
    b'\x1b\x67\xd7\x1e\x60\xd2\xb8\xc4\xc1\x6d\x52\x23\xa4\xd3\xe6\x59' , \
    b'\xff\x01\xb0\x49\x71\x11\xd5\x84\xb5\x4f\xed\x67\x78\xba\x09\xf2' , \
    b'\x39\x4c\x83\xde\xd8\x57\xac\x8d\xbf\xb3\x97\x84\x07\x7f\x0f\x9a' , \
    b'\xab\x06\xcd\x98\x6d\xea\x65\x82\x97\xe5\x60\x9d\x3a\x7a\x10\x73' , \
    b'\x4e\xa0\x29\x9a\xe3\x84\x98\x4b\x73\xb9\x00\x66\x03\x11\x14\xe7' , \
    b'\x08\x8b\x1b\x4b\xd1\xc4\x3b\x32\x83\xd6\x70\x24\xb2\xed\x0c\x3d' , \
    b'\x1b\x41\xe2\xa7\x82\x0b\x9d\x01\x9d\xbe\xba\x10\xaf\x36\x09\xa9'
]

lastBits_characteristic = [ \
    b'\x8a\xc8\x6a\xe0\x7a\x14\x36\x22\x44\x37\xd4\xd2\xc1\xcf\x45\x03' , \
    b'\xeb\xd3\x72\xed\x98\x85\x73\x17\xf2\xf5\x4c\xd2\x13\x0f\xdc\x9c' , \
    b'\xc5\x25\xa8\xe8\x25\xa9\xf1\x3b\x6c\x5e\xe0\x0b\x48\xfa\x1d\x52' , \
    b'\x12\xbe\x7e\x04\x40\x87\x14\x92\x79\x94\x40\x78\x89\x0f\x45\x7a' , \
 # set to move Left
    b'\x0a\xdb\xfd\xd9\xe8\x56\xe5\x4e\x61\xf3\xc9\xd3\x54\x52\xd5\xd0' , \
    b'\xeb\xd3\x72\xed\x98\x85\x73\x17\xf2\xf5\x4c\xd2\x13\x0f\xdc\x9c' , \
# max brightness
    b'\x1a\x7a\x2a\x59\x17\xb4\x93\x48\x34\xe5\xde\x2e\xd2\x7c\x6d\x6b' , \
# high speed
    b'\xb5\x60\xce\x6b\xe6\xe4\xc7\x72\xe6\x51\x7f\x59\x84\x94\xf1\x1f'
]


startBits_characteristic = [ \
    b'\x8a\xc8\x6a\xe0\x7a\x14\x36\x22\x44\x37\xd4\xd2\xc1\xcf\x45\x03' , \
    b'\xc5\x25\xa8\xe8\x25\xa9\xf1\x3b\x6c\x5e\xe0\x0b\x48\xfa\x1d\x52'
]

connectBits_characteristic = [ \
    b'\x3b\x3e\xb0\xf5\x95\x4b\xda\xbd\xe6\x10\x17\x4b\x52\xbf\xce\xcb' , \
    b'\xe5\x62\x66\xe2\x55\x5b\xa2\xab\x92\xe7\x3f\x27\x0b\x27\x74\xb5' , \
    b'\xeb\xd3\x72\xed\x98\x85\x73\x17\xf2\xf5\x4c\xd2\x13\x0f\xdc\x9c'
]





def sendNumberToHat(numberToSend, startBits, lastBits):
    if numberToSend >= 0 and numberToSend <= 9:
        my_service.my_characteristic2 = digit_characteristic[numberToSend]
        time.sleep(.2)

    #these bytes erase the screen
    if startBits == 1: #only have to write these values once at the beginning
        for i in startBits_characteristic:
            my_service.my_characteristic1 = i
            time.sleep(.2)

    #these bytes scroll the message, turn the brightness to max, and turn up the speed
    if lastBits == 1: #write these values at the end
        for i in lastBits_characteristic:
            my_service.my_characteristic1 = i
            time.sleep(.2)

def turnOff(): #tested, works, but not used
    my_service.my_characteristic1 = b'\xcb\xb1\xfd\xbf\xc5\x60\xd5\xe4\x53\xc2\xcb\xd9\x28\xb5\x3f\xab'
    time.sleep(.2)

def turnOn(): #tested, works, but not used
    my_service.my_characteristic1 = b'\xb8\xec\x4a\x55\xcc\x32\xfa\xe6\x70\x57\xc2\x6c\x65\x4a\x4f\x53'
    time.sleep(.2)


def FourDigit(theTime):
    firstDigit = theTime / 1000
    firstDigit = int(firstDigit)

    secondDigit = int(theTime/100)
    secondDigit2 = secondDigit - (firstDigit * 10)

    thirdDigit = theTime / 10
    thirdDigit = int(thirdDigit)
    thirdDigit2 = thirdDigit - (secondDigit * 10)

    forthDigit = int(theTime)
    forthDigit = forthDigit - (thirdDigit * 10)

    print(int(firstDigit), secondDigit2, thirdDigit2, forthDigit)

    return ( (firstDigit, secondDigit2, thirdDigit2, forthDigit) )
	
def blinkForMinute():
###    for x in range(120):
    for x in range(1):
        #print(x)
        led.value = True
        time.sleep(0.2)
        led.value = False
        time.sleep(0.2)

led.value = True
time.sleep(1)
led.value = False

# Unlike most circuitpython code, this runs in two loops
# one outer loop manages reconnecting bluetooth if we lose connection
# then one inner loop for doing what we want when connected!
while True:
    # Initialize the module
    try:        # Wireless connections can have corrupt data or other runtime failures
                # This try block will reset the module if that happens
				
        if not ble_connection:
            print("scanning")
            found = set()
            scan_responses = set()
            # By providing Advertisement as well we include everything, not just specific advertisements.
            for advertisement in ble.start_scan(ProvideServicesAdvertisement, Advertisement):
                addr = advertisement.address
                if advertisement.scan_response and addr not in scan_responses:
                    scan_responses.add(addr)
                elif not advertisement.scan_response and addr not in found:
                    found.add(addr)
                else:
                    continue
                print(addr, advertisement)
                print("\t" + repr(advertisement))
                print()
                if advertisement.short_name == "DSD-00A705":
                    print("Yes, found our peripherial, let's connect")
                    ble_connection = ble.connect(advertisement)
                    time.sleep(2)
                    break
            print("scan done")
            ble.stop_scan()

		# Once connected, check for incoming BLE UART data
        while ble_connection:  # Check our connection status every 3 seconds
            print("while ble_connection")
            my_service = ble_connection[MyService]
            print("my_service = ble_connection[MyService]")
            for i in connectBits_characteristic:
                my_service.my_characteristic1 = i
                time.sleep(.2)
            currentTime = currentTime - 1

            (firstDigit, secondDigit2, thirdDigit2, forthDigit) = FourDigit(currentTime)

            sendNumberToHat(firstDigit, 1, 0)
            sendNumberToHat(secondDigit2, 0, 0)
            sendNumberToHat(thirdDigit2, 0, 0)
            sendNumberToHat(forthDigit, 0, 1)
			
            blinkForMinute()                  # Not a minute anymore... fast count down.
            print("After blinkForMinute")

    except _bleio.ConnectionError:
        print("disconnected")
        ble_connection.disconnect()
        ble_connection = None
        continue
    except RuntimeError as e:
        print(e)                           # Print what happened
        continue


# Removed

#turnOff()
#turnOn()
#myService = None
#ble.stop_scan()
#break
