#!/usr/bin/env python
#
# Test SDL_Pi_HDC1080
#
# June 2017
#

#imports

import sys          
import time
import datetime
import SDL_Pi_HDC1080



# Main Program
print
print ("")
print ("Test SDL_Pi_HDC1080 Version 1.1 - SwitchDoc Labs")
print ("")
print ("Sample uses 0x40 and SwitchDoc HDC1080 Breakout board ")
print ("Program Started at:"+ time.strftime("%Y-%m-%d %H:%M:%S"))
print ("")

hdc1080 = SDL_Pi_HDC1080.SDL_Pi_HDC1080()

print ("------------")
print ("Manfacturer ID=0x%X"% hdc1080.readManufacturerID())  
print ("Device ID=0x%X"% hdc1080.readDeviceID() ) 
print ("Serial Number ID=0x%X"% hdc1080.readSerialNumber())  
# read configuration register
print ("configure register = 0x%X" % hdc1080.readConfigRegister())
# turn heater on
print ("turning Heater On") 
hdc1080.turnHeaterOn() 
# read configuration register
print ("configure register = 0x%X" % hdc1080.readConfigRegister())
# turn heater off
print ("turning Heater Off")
hdc1080.turnHeaterOff() 
# read configuration register
print ("configure register = 0x%X" % hdc1080.readConfigRegister())

# change temperature resolution
print ("change temperature resolution")
hdc1080.setTemperatureResolution(SDL_Pi_HDC1080.HDC1080_CONFIG_TEMPERATURE_RESOLUTION_11BIT)
# read configuration register
print ("configure register = 0x%X" % hdc1080.readConfigRegister())
# change temperature resolution
print ("change temperature resolution")
hdc1080.setTemperatureResolution(SDL_Pi_HDC1080.HDC1080_CONFIG_TEMPERATURE_RESOLUTION_14BIT)
# read configuration register
print ("configure register = 0x%X" % hdc1080.readConfigRegister())

# change humdity resolution
print ("change humidity resolution")
hdc1080.setHumidityResolution(SDL_Pi_HDC1080.HDC1080_CONFIG_HUMIDITY_RESOLUTION_8BIT)
# read configuration register
print ("configure register = 0x%X" % hdc1080.readConfigRegister())
# change humdity resolution
print ("change humidity resolution")
hdc1080.setHumidityResolution(SDL_Pi_HDC1080.HDC1080_CONFIG_HUMIDITY_RESOLUTION_14BIT)
# read configuration register
print ("configure register = 0x%X" % hdc1080.readConfigRegister())

while True:
        
        print ("-----------------")
        print ("Temperature = %3.1f C" % hdc1080.readTemperature())
        print ("Humidity = %3.1f %%" % hdc1080.readHumidity())
        print ("-----------------")

        time.sleep(3.0)
