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


while True:
	packet = rfm9x.receive()
	if packet is None:
		display.fill(0)
		display.text('- Waiting for PKT -', 15, 20, 1)
		display.show()
	else:
		display.fill(0)
		display.text('- PKT Received -', 15, 20, 1)
		display.show()
		
		encoded_byteliteral = BitArray(packet)
		decoded_pkt = decode_lora_packet(encoded_byteliteral)
		
		print("\nReceived Packet:\n")
		decoded_pkt.dump_to_console()
		time.sleep(2)
