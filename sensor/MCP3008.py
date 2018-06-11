# !/usr/bin/python
# coding = utf-8

import spidev

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000


# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 4) << 8) + adc[2]
    return data


def ConvertVolts(data, places):
    volts = (data * 5.5) / float(1023)
    volts = round(volts, places)
    return volts


def readVolts(channel):
    adc = ReadChannel(channel)
    volts = ConvertVolts(adc,2)
    return volts

# # Define sensor channels
# light_channel = 7
#
# # Define delay between readings
# delay = 5
#
# while True:
#     # Read the light sensor data
#     level = ReadChannel(light_channel)
#     volts = ConvertVolts(level, 2)
#     real_data = convertVoltsToHumi(volts)
#     # Print out results
#     print "--------------------------------------------"
#     print("humidity: {} ({}ADC,{}V)".format(real_data,level, volts))
#
#     # Wait before repeating loop
#     time.sleep(delay)