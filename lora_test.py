from network import LoRa
import time
import ubinascii

lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
print("DevEUI: "+ubinascii.hexlify(lora.mac()).decode('utf-8').upper())

# OTAA authentication parameters
app_eui = ubinascii.unhexlify('70B3D57ED004151E')
app_key = ubinascii.unhexlify('A907E552EE7BE2BB3C8E64BE591F3557')
# join a network using OTAA (Over the Air Activation)
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

# wait until the module has joined the network
while not lora.has_joined():
    time.sleep(2.5)
    print('Not yet joined...')

print('Joined!!')
