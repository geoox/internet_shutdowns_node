import pycom
from network import Bluetooth
from network import LoRa
import socket
import time
import struct
import ubinascii

pycom.heartbeat(False)

# messages will be saved in a list (queue)
messagesQueue = []

lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
app_eui = ubinascii.unhexlify('70B3D57ED004151E')
app_key = ubinascii.unhexlify('A907E552EE7BE2BB3C8E64BE591F3557')

def getDevEUI():
    print("DevEUI: "+ubinascii.hexlify(lora.mac()).decode('utf-8').upper())

def connectToTTNabp():
    lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

    # create an ABP authentication params
    dev_addr = ubinascii.unhexlify('26013105')
    nwk_swkey = ubinascii.unhexlify('B195269DE5ABD1D7AEEB9DC13C07BD72')
    app_swkey = ubinascii.unhexlify('816D055096C27476966FC5E12C193BDB')
    lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))


def connectToTTN():
    lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)
    pycom.rgbled(0xFF0000) # red
    while not lora.has_joined():
        time.sleep(3)
        print('Not yet joined... ')
    pycom.rgbled(0x00FF00) # green
    print('Joined')

def sendTTNMessage(message):
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    # set the LoRaWAN data rate
    s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
    # make the socket blocking
    s.setblocking(True)
    # send message
    s.send(message)
    print('message sent to TTN!')
    # make the socket non-blocking
    s.setblocking(False)

def conn_cb (bt_o):
    events = bt_o.events()
    if  events & Bluetooth.CLIENT_CONNECTED:
        print("Client connected")
    elif events & Bluetooth.CLIENT_DISCONNECTED:
        print("Client disconnected")

def bt_write_handler(data):
    events = data.events()
    value = data.value() #value received from client
    if events & Bluetooth.CHAR_WRITE_EVENT:
        print("New write request with value = {}".format(value))
        messagesQueue.append(value)
        print(messagesQueue)

def lora_cb(lora):
    events = lora.events()
    if events & LoRa.RX_PACKET_EVENT:
        print('Lora packet received')
    if events & LoRa.TX_PACKET_EVENT:
        print('Lora packet sent')
    if events & LoRa.TX_FAILED_EVENT:
        print('Lora packet failed event')

# main

bluetooth = Bluetooth()
bluetooth.set_advertisement(name='LoPy', service_uuid=b'1234567890123456')
bluetooth.callback(trigger=Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED, handler=conn_cb)
bluetooth.advertise(True)
arg=None

srv1 = bluetooth.service(uuid=b'1234567890123456', isprimary=True)
chr1 = srv1.characteristic(uuid=b'ab34567890123456', value=5)
<<<<<<< HEAD
char1_cb = chr1.callback(trigger=Bluetooth.CHAR_WRITE_EVENT, handler=bt_write_handler, arg=arg)

lora.callback(trigger=(LoRa.RX_PACKET_EVENT | LoRa.TX_PACKET_EVENT | LoRa.TX_FAILED_EVENT), handler=lora_cb)

while(True):
    time.sleep(5)
    if(len(messagesQueue)!=0):
        if not lora.has_joined():
            print('attempting to connect to TTN...')
            connectToTTN()

        print('sending messages to TTN...')
        for message in messagesQueue:
            sendTTNMessage(message)
            messagesQueue.remove(message) # message is sent, delete from queue



=======
char1_cb = chr1.callback(trigger=Bluetooth.CHAR_WRITE_EVENT, handler=message_characteristic_handler, arg=arg)
>>>>>>> 39a7d4202f88af3c737440dd5adc0809e6868cbd
