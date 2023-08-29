
from mfrc522 import MFRC522  #495155827, 3588359545
import utime
from machine import I2C,UART, Pin

import utime
import time

reader = MFRC522(spi_id=0,sck=6,miso=4,mosi=7,cs=5,rst=3)
 
gpsModule = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
loraModule = UART(1, baudrate=115200, tx=Pin(8), rx=Pin(9))
print(gpsModule)

buff = bytearray(255)

TIMEOUT = False
FIX_STATUS = False

latitude = ""
longitude = ""
satellites = ""
GPStime = ""

def getGPS(gpsModule):
    global FIX_STATUS, TIMEOUT, latitude, longitude, satellites, GPStime
    
    timeout = time.time() + 2
    while True:
        #gpsModule.readline()
        buff = str(gpsModule.readline())
        parts = buff.split(',')
    
        if (parts[0] == "b'$GPGGA" and len(parts) == 15):
            if(parts[1] and parts[2] and parts[3] and parts[4] and parts[5] and parts[6] and parts[7]):
                print(buff)
                
                latitude = convertToDegree(parts[2])
                if (parts[3] == 'S'):
                    latitude = -latitude
                longitude = convertToDegree(parts[4])
                if (parts[5] == 'W'):
                    longitude = -longitude
                satellites = parts[7]
                GPStime = parts[1][0:2] + ":" + parts[1][2:4] + ":" + parts[1][4:6]
                FIX_STATUS = True
                break
                
        if (time.time() > timeout):
            TIMEOUT = True
            break
        utime.sleep_ms(500)
        
def convertToDegree(RawDegrees):

    RawAsFloat = float(RawDegrees)
    firstdigits = int(RawAsFloat/100) 
    nexttwodigits = RawAsFloat - float(firstdigits*100) 
    
    Converted = float(firstdigits + nexttwodigits/60.0)
    Converted = '{0:.6f}'.format(Converted) 
    return str(Converted)
     
 
 
lora_band = "865000000"
lora_networkid = "5"
lora_address = "2"
lora_RX_address = "1"
 
 
 
print("Bring TAG closer...")
print("")
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
        getGPS(gpsModule)

        if(FIX_STATUS == True):
          
            print("Latitude: "+latitude)
            print("Longitude: "+longitude)
           
            
        
        if(TIMEOUT == True):
            print("No GPS data is found.")
            TIMEOUT = False
            latitude=0
            longitude=0
            
      
        reader.init()
        (stat, tag_type) = reader.request(reader.REQIDL)
        if stat == reader.OK:
            (stat, uid) = reader.SelectTagSN()
            if stat == reader.OK:
                card = int.from_bytes(bytes(uid),"little",False)
                
                msg=str(card) + "_"+str(latitude)+ "_"+str(longitude)
                print("MSG: "+msg)
                loraModule.write("AT+SEND="+ lora_RX_address +",2,hi\r\n");
                print(loraModule.readline())
                time.sleep(0.3)
     
        utime.sleep_ms(2500)
        loraModule.write("AT+SEND="+ lora_RX_address +",2,hi\r\n");
        print(loraModule.readline())
        
    except:
        time.sleep(0.2)
