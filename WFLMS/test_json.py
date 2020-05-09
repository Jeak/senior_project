# Python 3 WFLMS Implementation V1.0
# Authors: Robert Goldie, Jack Gallegos, Cal Poly San Luis Obispo 2020
# add comment
# Dependencies: mgrs, bitstring, time

from bitstring import BitArray, BitStream
from wflms_libs import *
from digitalio import DigitalInOut, Direction, Pull
import busio				# Import Blinka Libraries
import board
import adafruit_ssd1306		# Import the SSD1306 module.
import adafruit_rfm9x		# Import RFM9x
import time
import mgrs
import json
import os

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
packet_timer = 0

# Create the JSON Object
data = {}
# Create the active_crews dictionary
data['active_crews'] = []

while True:
    # Keep listening for and processing packets
    packet = rfm9x.receive(keep_listening=True,with_header=False,with_ack=True,timeout=None)
    if packet is None:
        if (time.time() - packet_timer > 1):    # timing for display message
            display.fill(0)
            display.text('- Waiting for PKT -', 15, 20, 1)
            display.show()
    else:
        encoded_byteliteral = BitArray(packet)
        decoded_pkt = decode_lora_packet(encoded_byteliteral)
        packet_timer = time.time()
        display.fill(0)
        display.text('- PKT received -', 15, 20, 1)
        display.show()

        decoded_pkt.RX_TIME = time.time()   # Unix timestamp for packet received
        decoded_pkt.calc_lat_lon()  # Calculate Long, Lat coordinates from MGRS coordinates
        decoded_pkt.decode_source_unit_id() # Establish unit id numerically

        # Check if unit id is same as any others in the dict
        try:
            # go through each element in the "data" dict. start at element 0
            for i in range(len(data['active_crews'])):
                if data['active_crews'][i]['unit_number'] == decoded_pkt.DICT_NUM:
                    #update entry for that unit.
                    data['active_crews'][i]['emerg_flg'] == decoded_pkt.EMERG_FLG
                    data['active_crews'][i]['fline_stat'] == decoded_pkt.FLINE_STAT
                    data['active_crews'][i]['rsrc_stat'] == decoded_pkt.RSRC_STAT
                    data['active_crews'][i]['lat'] == decoded_pkt.LAT
                    data['active_crews'][i]['lon'] == decoded_pkt.LON
                    data['active_crews'][i]['rx_time'] == decoded_pkt.RX_TIME

                else:
                    # Else, make a new entry, as the unit hasn't been seen before
                    data['active_crews'].append({
                    'unit_number': decoded_pkt.DICT_NUM,
                    'emerg_flg': decoded_pkt.EMERG_FLG,
                    'fline_stat': decoded_pkt.FLINE_STAT,
                    'rsrc_stat': decoded_pkt.RSRC_STAT,
                    'lat': decoded_pkt.LAT,
                    'lon': decoded_pkt.LON,
                    'rx_time': decoded_pkt.RX_TIME,
                    })

        except IndexError:
            # List is empty on first entry
            # Append the entry
            data['active_crews'].append({
            'unit_number': decoded_pkt.DICT_NUM,
            'emerg_flg': decoded_pkt.EMERG_FLG,
            'fline_stat': decoded_pkt.FLINE_STAT,
            'rsrc_stat': decoded_pkt.RSRC_STAT,
            'lat': decoded_pkt.LAT,
            'lon': decoded_pkt.LON,
            'rx_time': decoded_pkt.RX_TIME,
            })

        # Send the revised dictionary out as a text file
        #with open('data.txt', 'w') as outfile:
        #json.dump(data, outfile)

        print("\nReceived Packet:\n")
        decoded_pkt.dump_to_console()
        print(json.dumps(data['active_crews'], indent=2))
