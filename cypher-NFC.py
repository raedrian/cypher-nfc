from time import sleep_ms, sleep
from machine import Pin, SPI, I2C
from mfrc522 import MFRC522
import ssd1306
from LDR import LDR
#-----------------LED ASSIGNMENT-----------------
rled=Pin(4,Pin.OUT)
gled=Pin(16,Pin.OUT)
wled=Pin(25,Pin.OUT)

#-----------------OLED ASSIGNMENT-----------------

i2c = I2C(-1, scl=Pin(22), sda=Pin(21))
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)


#-----------------RFID ASSIGNMENT-----------------
sck = Pin(18, Pin.OUT)
mosi = Pin(23, Pin.OUT)
miso = Pin(19, Pin.OUT)
spi = SPI(baudrate=100000, polarity=0, phase=0, sck=sck, mosi=mosi, miso=miso)

sda = Pin(5, Pin.OUT)

#-----------------GET DATA FROM RFID SCANNER-----------------
def do_read():
    try:
            rdr = MFRC522(spi, sda)
            uid = ""
            (stat, tag_type) = rdr.request(rdr.REQIDL)
            if stat == rdr.OK:
                (stat, raw_uid) = rdr.anticoll()

                if stat == rdr.OK:
                    uid = ("0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
                    sleep_ms(100)
                    return uid
            else:
                uid = '0'
                return uid;
    except KeyboardInterrupt:
        print("Bye")
        
        
#-----------------AUTHORIZATION-----------------
while True:
    keycard = do_read()
    oled.text('[CYPHER]', 0, 0)
    ldr = LDR(34)
    wled.value(1)
    
    value = ldr.value()
    
    if value < 50:
        wled.value(0)
        print('INTRUDER DETECTED!')
        oled.text('INTRUDER', 0, 40)
        oled.text('DETECTED!', 0, 50)
        oled.show()
        
        
        t = 1
        while t < 10:
            gled.value(1)
            sleep(0.1)
            gled.value(0)
            rled.value(1)
            sleep(0.1)
            rled.value(0)
            t+=1
            
        oled.fill(0)
    
    elif keycard == '0x175fea4d':
        print('KEYCARD NO: ',keycard,'[Access Granted]')
        oled.text('KEYCARD NO: ', 0, 20)
        oled.text(str(keycard), 0, 30)
        oled.text('[Access Granted] ', 0, 40)
        oled.show()
        gled.value(1)
        wled.value(0)
        sleep(3)
        gled.value(0)
        oled.fill(0)
        
    elif keycard == '0':
        
        oled.text('READY TO SCAN', 0, 40)
        oled.show()
        oled.fill(0)
    else:
        print('KEYCARD NO: ',keycard,'[Access Denied]')
        oled.text('KEYCARD NO: ', 0, 20)
        oled.text(str(keycard), 0, 30)
        oled.text('[Access Denied] ', 0, 40)
        oled.show()
        rled.value(1)
        sleep(3)
        rled.value(0)
        oled.fill(0)

  
