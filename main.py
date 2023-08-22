import utime
from machine import I2C,UART, Pin

import time

import os as MOD_OS
import network as MOD_NETWORK
import time as MOD_TIME
import time
#Connect to Wifi
GLOB_WLAN=MOD_NETWORK.WLAN(MOD_NETWORK.STA_IF)
GLOB_WLAN.active(True)
GLOB_WLAN.connect("SRC 24G", "src@internet")
print("Connecting..")
while not GLOB_WLAN.isconnected():
  print(".")
  time.sleep(2)
  
print("Connected")
#firebase example
import ufirebase as firebase
firebase.setURL("https://milk-d6036-default-rtdb.firebaseio.com/")

loraModule = UART(1, baudrate=115200, tx=Pin(8), rx=Pin(9))
buff = bytearray(255)

TIMEOUT = False
FIX_STATUS = False

 
 
lora_band = "915000000"
lora_networkid = "5"
lora_address = "1"
lora_RX_address = "2"
 
 
loraModule.write("AT+BAND=" + lora_band +"\r\n")
time.sleep(0.5)
print(loraModule.readline())
 
 
loraModule.write("AT+NETWORKID=" + lora_networkid+"\r\n")
time.sleep(0.5)
print(loraModule.readline())
loraModule.write("AT+ADDRESS=" + lora_address+"\r\n");
time.sleep(1)
print(loraModule.readline())
while True:
    try:
        time.sleep(0.2)
        rcv=loraModule.readline()
        #print(rcv)
        if(rcv is not None):
            #print(rcv)
            info=str(rcv).split("_")
            print('USER:'+ str(info[1]))
            print('LOC :'+ str(info[2])+","+str(info[3]))
            firebase.put("ASHOK_USER", str(info[1]), bg=0)
            firebase.put("ASHOK_LOC", str(info[2])+","+str(info[3]), bg=0)

            #firebase.get("pico", "var1", bg=0)
            #print("testtag: "+str(firebase.var1)
        
    except:
        time.sleep(0.2)
