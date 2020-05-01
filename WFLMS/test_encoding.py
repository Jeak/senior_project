# Python 3 WFLMS Implementation V1.0
# Authors: Robert Goldie, Jack Gallegos, Cal Poly San Luis Obispo 2020

# Dependencies: mgrs, bitstring, time
#import mgrs
from bitstring import BitArray, BitStream
from wflms_libs import *
from digitalio import DigitalInOut, Direction, Pull
import busio				# Import Blinka Libraries
import board
import adafruit_ssd1306		# Import the SSD1306 module.
import adafruit_rfm9x		# Import RFM9x
import time

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# 128x32 OLED Display
reset_pin = DigitalInOut(board.D4)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, reset=reset_pin)
# Clear the display.
display.fill(0)
display.show()
width = display.width
height = display.height

# Configure LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
rfm9x.tx_power = 23
prev_packet = None


currentStatus = Packet() 	# Create currentStatus as PAcket class
currentStatus.EMERG_FLG = 1
currentStatus.MGRS_LOC = get_MGRS()
	
while True:
	print("\nPacket before Encoding\n")
	encoded_byteliteral = encode_lora_packet(currentStatus)
	currentStatus.dump_to_console()
	
	decoded_pkt = decode_lora_packet(encoded_byteliteral)
	print("\nPacket after Decoding\n")
	decoded_pkt.dump_to_console()

	time.sleep(100)
