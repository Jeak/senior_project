# Python 3 WFLMS Implementation V1.0
# Authors: Robert Goldie, Jack Gallegos, Cal Poly San Luis Obispo 2020
# add comment
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

#Receive only packets from the Repeater (Node id of 2)
rfm9x.node = 0x03
rfm9x.destination = 0x04
prev_packet = None
last_pkt_rx = 0

while True:
	packet = rfm9x.receive(keep_listening=True,with_header=False,with_ack=True,timeout=None)
	if packet is None:
		if (time.time() - last_pkt_rx > 1):
			display.fill(0)
			display.text('- Waiting for PKT -', 15, 20, 1)
			display.show()
	else:
		try:
			encoded_byteliteral = BitArray(packet)
			decoded_pkt = decode_lora_packet(encoded_byteliteral)
			last_pkt_rx = time.time()
			display.fill(0)
			display.text('- PKT received -', 15, 20, 1)
			display.show()		
		except UnicodeDecodeError:
			print("\nUnicode Decode Error!\n")
		else:
			print("\nReceived Packet:\n")
			decoded_pkt.dump_to_console()
