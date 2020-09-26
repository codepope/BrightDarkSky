# Metro M4 AirLift BrightDarkSkies

import time
import board
from digitalio import DigitalInOut
import busio

# ESP32 SPI lib
from adafruit_esp32spi import adafruit_esp32spi, adafruit_esp32spi_wifimanager


# Import NeoPixel Library
import neopixel


# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise


# ESP32 Setup
try:
    esp32_cs = DigitalInOut(board.ESP_CS)
    esp32_ready = DigitalInOut(board.ESP_BUSY)
    esp32_reset = DigitalInOut(board.ESP_RESET)
except AttributeError:
    esp32_cs = DigitalInOut(board.D9)
    esp32_ready = DigitalInOut(board.D10)
    esp32_reset = DigitalInOut(board.D5)

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

for ap in esp.scan_networks():
    print("\t%s\t\tRSSI: %d" % (str(ap['ssid'], 'utf-8'), ap['rssi']))
 
print("Connecting to AP...")
while not esp.is_connected:
    try:
        esp.connect_AP(secrets['ssid'], secrets['password'])
    except RuntimeError as e:
        print("could not connect to AP, retrying: ",e)
        continue

status_light = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.2)
wifi = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(
    esp, secrets, status_light)

# NeoPixel strip (of 16 LEDs) connected on D6
NUMPIXELS = 40
neopixels = neopixel.NeoPixel(
    board.D6, NUMPIXELS, brightness=0.2, auto_write=False)
pixlayout = [[32, 24, 16, 8, 0],
             [33, 25, 17, 9, 1],
             [34, 26, 18, 10, 2],
             [35, 27, 19, 11, 3],
             [36, 28, 20, 12, 4],
             [37, 29, 21, 13, 5],
             [38, 30, 22, 14, 6],
             [39, 31, 23, 15, 7]]

APIURL = "https://api.darksky.net/forecast/" + \
    secrets['darksky_key']+"/"+secrets['lat']+"," + \
    secrets['long']+'?exclude=hourly,daily,alerts,flags&units=si'

while True:
    try:
        print("Fetching JSON from DarkSky")
        response = wifi.get(APIURL)
        data=response.json()
        value=data
        for X in [ 'minutely', 'data']:
            value=value[X]
        minutedata=value
        neopixels.fill((0,0,0))
        for n in range(0,8):
            val=minutedata[n*8]
            print(val)
            prob=val['precipProbability']
            intense=val['precipIntensity']
            color=(0,0,0)
            bar=0
            if prob<0.25:
                color=(0,0,64)
            elif prob<0.5:
                color=(0,128,0)
            elif prob<0.75:
                color=(192,192,0)
            else:
                color=(255,0,0)
            if intense==0.0:
                bar=0
            elif intense<0.5:
                bar=1
            elif intense<1.00:
                bar=2
            elif intense<2.00:
                bar=3
            elif intense<7.5:
                bar=4
            else:
                bar=5
            if bar!=0:
                for m in range(0,bar):
                    neopixels[pixlayout[n][m]]=color
        neopixels.show()
        time.sleep(120)
    except (ValueError, RuntimeError) as e:
        print("Failed to get data, retrying\n", e)
        wifi.reset()
        continue
