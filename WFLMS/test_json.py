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
import sys

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
# Create the empty json File
with open('data.json', 'w') as outfile:
    outfile.truncate(0)

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
        try:
            decoded_pkt = decode_lora_packet(encoded_byteliteral)
        except UnicodeDecodeError:
            pass
        packet_timer = time.time()
        display.fill(0)
        display.text('- PKT received -', 15, 20, 1)
        display.show()

        decoded_pkt.RX_TIME = time.time()   # Unix timestamp for packet received
        decoded_pkt.calc_lat_lon()  # Calculate Long, Lat coordinates from MGRS coordinates
        decoded_pkt.decode_source_unit_id() # Establish unit id numerically

        # go through each element in the "data" dict. start at element 0.
        for i in range(len(data['active_crews'])):
            # If the unit number matches the received packet
            if data['active_crews'][i]['unit_number'] == decoded_pkt.DICT_NUM:
                #update entry for that unit.
                data['active_crews'][i]['emerg_flg'] = decoded_pkt.EMERG_FLG
                data['active_crews'][i]['fline_stat'] = decoded_pkt.FLINE_STAT
                data['active_crews'][i]['rsrc_stat'] = decoded_pkt.RSRC_STAT
                data['active_crews'][i]['lat'] = decoded_pkt.LAT
                data['active_crews'][i]['lon'] = decoded_pkt.LON
                data['active_crews'][i]['rx_time'] = decoded_pkt.RX_TIME
            else:
                # Make a new entry with the data just received, as the unit hasn't been seen before
                data['active_crews'].append({
                'unit_number': decoded_pkt.DICT_NUM,
                'emerg_flg': decoded_pkt.EMERG_FLG,
                'fline_stat': decoded_pkt.FLINE_STAT,
                'rsrc_stat': decoded_pkt.RSRC_STAT,
                'lat': decoded_pkt.LAT,
                'lon': decoded_pkt.LON,
                'rx_time': decoded_pkt.RX_TIME,
                })

        # If there are no received packets
        if (len(data['active_crews']) == 0):
            # Make a new entry with the data just received, as the unit hasn't been seen before
            data['active_crews'].append({
            'unit_number': decoded_pkt.DICT_NUM,
            'emerg_flg': decoded_pkt.EMERG_FLG,
            'fline_stat': decoded_pkt.FLINE_STAT,
            'rsrc_stat': decoded_pkt.RSRC_STAT,
            'lat': decoded_pkt.LAT,
            'lon': decoded_pkt.LON,
            'rx_time': decoded_pkt.RX_TIME,
            })
        # Check for duplicates
        data_without_dupes = []
        for i in range(len(data['active_crews'])):
            if data['active_crews'][i] not in data['active_crews'][i + 1:]:
                data_without_dupes.append(data['active_crews'][i])

        # Send the revised dictionary out as a text file
        with open('data.json', 'w') as outfile:
            json.dump(data_without_dupes, outfile)

        #sys.stderr.write("\x1b[2J\x1b[H")  # clear text line
        print('----------------------------------------------------------------------------------')
        print(json.dumps(data_without_dupes, indent=2))
