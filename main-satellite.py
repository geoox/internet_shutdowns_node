import pycom
from network import Bluetooth
from network import LoRa
import socket
import time
import struct
import ubinascii

messagesQueue = ['1','2','3']

# LoRa mode instead of LoRaWAN
lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868, frequency=868000000, sf=7, bandwidth=LoRa.BW_125KHZ, public=False, coding_rate=LoRa.CODING_4_5)

def sendLoraMessage(message):
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

    s.setblocking(True)
    s.send(message)

    print('message sent via LoRa!')
    # unblock socket
    s.setblocking(False)

# main

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

bluetooth = Bluetooth()
bluetooth.set_advertisement(name='LoPy', service_uuid=b'1234567890123456')
bluetooth.callback(trigger=Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED, handler=conn_cb)
bluetooth.advertise(True)
arg=None

srv1 = bluetooth.service(uuid=b'1234567890123456', isprimary=True)
chr1 = srv1.characteristic(uuid=b'ab34567890123456', value=5)
char1_cb = chr1.callback(trigger=Bluetooth.CHAR_WRITE_EVENT, handler=bt_write_handler, arg=arg)

lora.callback(trigger=(LoRa.RX_PACKET_EVENT | LoRa.TX_PACKET_EVENT | LoRa.TX_FAILED_EVENT), handler=lora_cb)

while(True):
    time.sleep(20)
    # sendLoraMessage('Test!')
    if(len(messagesQueue)!=0):
        print('sending messages to satellite compatbile node...')
        for message in messagesQueue:
            sendLoraMessage(message)
            messagesQueue.remove(message) # message is sent, delete from queue
            time.sleep(5)