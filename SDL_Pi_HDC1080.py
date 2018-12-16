
#
# SDL_Pi_HDC1080
# Python 3
# Raspberry Pi Driver for the SwitchDoc Labs HDC1080 Breakout Board
#
# SwitchDoc Labs
# December 2018
#
# Version 1.1

#constants

# I2C Address
HDC1080_ADDRESS =                       (0x40)    # 1000000 
# Registers
HDC1080_TEMPERATURE_REGISTER =          (0x00)
HDC1080_HUMIDITY_REGISTER =             (0x01)
HDC1080_CONFIGURATION_REGISTER =        (0x02)
HDC1080_MANUFACTURERID_REGISTER =       (0xFE)
HDC1080_DEVICEID_REGISTER =         (0xFF)
HDC1080_SERIALIDHIGH_REGISTER =         (0xFB)
HDC1080_SERIALIDMID_REGISTER =          (0xFC)
HDC1080_SERIALIDBOTTOM_REGISTER =       (0xFD)



#Configuration Register Bits

HDC1080_CONFIG_RESET_BIT =              (0x8000)
HDC1080_CONFIG_HEATER_ENABLE =          (0x2000)
HDC1080_CONFIG_ACQUISITION_MODE =       (0x1000)
HDC1080_CONFIG_BATTERY_STATUS =         (0x0800)
HDC1080_CONFIG_TEMPERATURE_RESOLUTION = (0x0400)
HDC1080_CONFIG_HUMIDITY_RESOLUTION_HBIT =    (0x0200)
HDC1080_CONFIG_HUMIDITY_RESOLUTION_LBIT =    (0x0100)

HDC1080_CONFIG_TEMPERATURE_RESOLUTION_14BIT = (0x0000)
HDC1080_CONFIG_TEMPERATURE_RESOLUTION_11BIT = (0x0400)

HDC1080_CONFIG_HUMIDITY_RESOLUTION_14BIT = (0x0000)
HDC1080_CONFIG_HUMIDITY_RESOLUTION_11BIT = (0x0100)
HDC1080_CONFIG_HUMIDITY_RESOLUTION_8BIT = (0x0200)

I2C_SLAVE=0x0703

import struct, array, time, io, fcntl

HDC1080_fw= 0
HDC1080_fr= 0

class SDL_Pi_HDC1080:
        def __init__(self, twi=1, addr=HDC1080_ADDRESS ):
                global HDC1080_fr, HDC1080_fw
                
                HDC1080_fr= io.open("/dev/i2c-"+str(twi), "rb", buffering=0)
                HDC1080_fw= io.open("/dev/i2c-"+str(twi), "wb", buffering=0)

                # set device address
                fcntl.ioctl(HDC1080_fr, I2C_SLAVE, HDC1080_ADDRESS)
                fcntl.ioctl(HDC1080_fw, I2C_SLAVE, HDC1080_ADDRESS)
                time.sleep(0.015) #15ms startup time

                config = HDC1080_CONFIG_ACQUISITION_MODE 

                s = [HDC1080_CONFIGURATION_REGISTER,config>>8,0x00]
                s2 = bytearray( s )
                HDC1080_fw.write( s2 ) #sending config register bytes
                time.sleep(0.015)               # From the data sheet
                
                #       0x10(48)    Temperature, Humidity enabled, Resolultion = 14-bits, Heater off
                #config = HDC1080_CONFIG_ACQUISITION_MODE 
                #self._bus.write_byte_data(HDC1080_ADDRESS,HDC1080_CONFIGURATION_REGISTER, config>>8)


        # public functions

        def readTemperature(self):
               

                s = [HDC1080_TEMPERATURE_REGISTER] # temp
                s2 = bytearray( s )
                HDC1080_fw.write( s2 )
                time.sleep(0.0625)              # From the data sheet

                data = HDC1080_fr.read(2) #read 2 byte temperature data
                buf = array.array('B', data)
                #print ( "Temp: %f 0x%X %X" % (  ((((buf[0]<<8) + (buf[1]))/65536.0)*165.0 ) - 40.0   ,buf[0],buf[1] )  )

                
                # Convert the data
                temp = (buf[0] * 256) + buf[1]
                cTemp = (temp / 65536.0) * 165.0 - 40
                return cTemp


        def readHumidity(self):
                # Send humidity measurement command, 0x01(01)
                time.sleep(0.015)               # From the data sheet

                s = [HDC1080_HUMIDITY_REGISTER] # hum
                s2 = bytearray( s )
                HDC1080_fw.write( s2 )
                time.sleep(0.0625)              # From the data sheet

                data = HDC1080_fr.read(2) #read 2 byte humidity data
                buf = array.array('B', data)
                #print ( "Humidity: %f 0x%X %X " % (  ((((buf[0]<<8) + (buf[1]))/65536.0)*100.0 ),  buf[0], buf[1] ) )
                humidity = (buf[0] * 256) + buf[1]
                humidity = (humidity / 65536.0) * 100.0
                return humidity
        
        def readConfigRegister(self):
                # Read config register


                s = [HDC1080_CONFIGURATION_REGISTER] # temp
                s2 = bytearray( s )
                HDC1080_fw.write( s2 )
                time.sleep(0.0625)              # From the data sheet

                data = HDC1080_fr.read(2) #read 2 byte config data

                buf = array.array('B', data)


                #print "register=%X %X"% (buf[0], buf[1])
                return buf[0]*256+buf[1]

       
        def turnHeaterOn(self):
                # Read config register
                config = self.readConfigRegister()
                config = config | HDC1080_CONFIG_HEATER_ENABLE 
                s = [HDC1080_CONFIGURATION_REGISTER,config>>8,0x00]
                s2 = bytearray( s )
                HDC1080_fw.write( s2 ) #sending config register bytes
                time.sleep(0.015)               # From the data sheet

                return

        def turnHeaterOff(self):
                # Read config register
                config = self.readConfigRegister()
                config = config & ~HDC1080_CONFIG_HEATER_ENABLE 
                s = [HDC1080_CONFIGURATION_REGISTER,config>>8,0x00]
                s2 = bytearray( s )
                HDC1080_fw.write( s2 ) #sending config register bytes
                time.sleep(0.015)               # From the data sheet

                return

        

        def setHumidityResolution(self,resolution):
                # Read config register
                config = self.readConfigRegister()
                config = (config & ~0x0300) | resolution 
                s = [HDC1080_CONFIGURATION_REGISTER,config>>8,0x00]
                s2 = bytearray( s )
                HDC1080_fw.write( s2 ) #sending config register bytes
                time.sleep(0.015)               # From the data sheet
                return

        def setTemperatureResolution(self,resolution):
                # Read config register
                config = self.readConfigRegister()
                config = (config & ~0x0400) | resolution 
               
                s = [HDC1080_CONFIGURATION_REGISTER,config>>8,0x00]
                s2 = bytearray( s )
                HDC1080_fw.write( s2 ) #sending config register bytes
                time.sleep(0.015)               # From the data sheet
                
                
                return

        def readBatteryStatus(self):
                
                # Read config register
                config = self.readConfigRegister()
                config = config & ~ HDC1080_CONFIG_HEATER_ENABLE

                if (config == 0):
                    return True
                else:
                    return False

                return 0


        def readManufacturerID(self):

            s = [HDC1080_MANUFACTURERID_REGISTER] # temp
            s2 = bytearray( s )
            HDC1080_fw.write( s2 )
            time.sleep(0.0625)              # From the data sheet
    
            data = HDC1080_fr.read(2) #read 2 byte config data
    
            buf = array.array('B', data)
            return buf[0] * 256 + buf[1]

        def readDeviceID(self):
    
            s = [HDC1080_DEVICEID_REGISTER] # temp
            s2 = bytearray( s )
            HDC1080_fw.write( s2 )
            time.sleep(0.0625)              # From the data sheet
    
            data = HDC1080_fr.read(2) #read 2 byte config data
    
            buf = array.array('B', data)
            return buf[0] * 256 + buf[1]

        def readSerialNumber(self):

            serialNumber = 0
    
            s = [HDC1080_SERIALIDHIGH_REGISTER] # temp
            s2 = bytearray( s )
            HDC1080_fw.write( s2 )
            time.sleep(0.0625)              # From the data sheet
            data = HDC1080_fr.read(2) #read 2 byte config data
            buf = array.array('B', data)
            serialNumber = buf[0]*256+ buf[1] 
    
            s = [HDC1080_SERIALIDMID_REGISTER] # temp
            s2 = bytearray( s )
            HDC1080_fw.write( s2 )
            time.sleep(0.0625)              # From the data sheet
            data = HDC1080_fr.read(2) #read 2 byte config data
            buf = array.array('B', data)
            serialNumber = serialNumber*256 + buf[0]*256 + buf[1] 
    
            s = [HDC1080_SERIALIDBOTTOM_REGISTER] # temp
            s2 = bytearray( s )
            HDC1080_fw.write( s2 )
            time.sleep(0.0625)              # From the data sheet
            data = HDC1080_fr.read(2) #read 2 byte config data
            buf = array.array('B', data)
            serialNumber = serialNumber*256 + buf[0]*256 + buf[1] 
    
            return serialNumber
