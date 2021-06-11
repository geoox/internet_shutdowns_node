from network import Bluetooth
from network import LoRa
import socket
import time
import ubinascii

def getDevEUI():
    print("DevEUI: "+ubinascii.hexlify(lora.mac()).decode('utf-8').upper())

def connectToTTN():
    lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
    app_eui = ubinascii.unhexlify('70B3D57ED004151E')
    app_key = ubinascii.unhexlify('13ADF6C2995E0E3E815B68DDFB95B64C')
    lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)
    while not lora.has_joined():
        time.sleep(2.5)
        print('Not yet joined...')
    print('Joined TTN')

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

def bluetooth_connection_handler (bt_o):
    events = bt_o.events()
    if  events & Bluetooth.CLIENT_CONNECTED:
        print("Client connected")
    elif events & Bluetooth.CLIENT_DISCONNECTED:
        print("Client disconnected")

def message_characteristic_handler(data):
    events = data.events()
    value = data.value() # value received from client
    if  events & Bluetooth.CHAR_WRITE_EVENT:
        print("Received value = {}".format(value))
        # add new message to queu
        messagesQueue.append(value)
        print(messagesQueue)
        # attempt to send all queued messages
        for message in messagesQueue:
            sendTTNMessage(message)
            # if message is sent, delete from queue
            messagesQueue.remove(message) 


# messages will be saved in a list (queue)
messagesQueue = []

bluetooth = Bluetooth()
bluetooth.set_advertisement(name='LoPy', service_uuid=b'1234567890123456')

bluetooth.callback(trigger=Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED, handler=bluetooth_connection_handler)
bluetooth.advertise(True)
arg=None

connectToTTN()

srv1 = bluetooth.service(uuid=b'1234567890123456', isprimary=True)
chr1 = srv1.characteristic(uuid=b'ab34567890123456', value=5)
char1_cb = chr1.callback(trigger=Bluetooth.CHAR_WRITE_EVENT, handler=message_characteristic_handler, arg=arg)