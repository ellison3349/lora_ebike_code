import os as MOD_OS
import network as MOD_NETWORK
import time as MOD_TIME
import time
#Connect to Wifi
GLOB_WLAN=MOD_NETWORK.WLAN(MOD_NETWORK.STA_IF)
GLOB_WLAN.active(True)
GLOB_WLAN.connect("SRC 24", "src@internet")
print("Connecting..")
while not GLOB_WLAN.isconnected():
  print(".")
  time.sleep(2)
  
print("Connected")
#firebase example
import ufirebase as firebase
firebase.setURL("https://milk-d6036-default-rtdb.firebaseio.com/")
i=0
while(1):
    time.sleep(1)
    #Put Tag1
    i=i+1
    firebase.put("pico", str(i), bg=0)

    firebase.get("pico", "var1", bg=0)
    print("testtag: "+str(firebase.var1))
