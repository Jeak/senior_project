# WFLMS Repeater
# Bobby Goldie and Jack Gallegos, 2020


# The WFLMS Repeater handles all incoming messages and sends it to all receivers

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

# See RFM9x circuitpython library for more documentation.
# Repeater Node ID is 1. This is to prevent multipathed packets from being double-counted in the Incident Command node's FIFO and increases channel capacity.
rfm9x.node = 0x02
rfm9x.tx_power = 23
prev_packet = None
rfm9x.destination = 0x03    # Send to incident command (ID: 2)
last_pkt_tx = 0

while True:
	# Receive a packet
	packet = rfm9x.receive(keep_listening=True,with_header=False,with_ack=True,timeout=None)
	if packet is None:
		if (time.time() - last_pkt_tx > 1):
			display.fill(0)
			display.text('- Waiting for PKT -', 15, 20, 1)
			display.show()
	else:
		# If properly addresses packet received, send it out
		rfm9x.send_with_ack(packet)
		last_pkt_tx = time.time()
		display.fill(0)
		display.text('- Sent PKT -', 15, 20, 1)
		display.show()
		try:
			# Testing for decoded packet to confirm
			encoded_byteliteral = BitArray(packet)
			decoded_pkt = decode_lora_packet(encoded_byteliteral)
		except UnicodeDecodeError:
			print("\nUnicode Decode Error!")
		else:
			# Print to console
			print("\nReceived Packet:\n")
			decoded_pkt.dump_to_console()
