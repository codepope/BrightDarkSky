# BrightDarkSky

Circuit Python app to read Dark Sky forecast and turn it into LED visualisation

You will need 

* Adafruit Metro M4 Express AirLift (WiFi) - Lite: https://www.adafruit.com/product/4000 (The brains and Wifi)
* Adafruit NeoPixel Shield for Arduino - 40 RGB LED Pixel Matrix:  https://www.adafruit.com/product/1430 (The lights, all of the lights)

Pop CircuitPython on the M4, load up the code, update the secrets/py file with your ssid and password, Dark Sky API key, and your own Lat and Long.

Lights show different colours to reflect probability in columns of different heigts to reflect rain intensity.

If you can work out a way to optimize the ranges for local weather, a PR would be great.

Enjoy...


