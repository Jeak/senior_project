# test

import mgrs
from bitstring import BitArray, BitStream

import json
import time
from wflms_libs import *



# Create fake packet object
currentStatus = Packet()

currentStatus.SRC_TYPE = 0  # hardcode Pi 0 node as Handcrew 2
currentStatus.SRC_NUM = 2   # hardcode for Pi 0
currentStatus.EMERG_FLG = 1
currentStatus.FLINE_STAT = 0
currentStatus.RSRC_STAT = 1
currentStatus.MGRS_LOC = '10SEG6374048456'
currentStatus.DEST_TYPE = 10
currentStatus.DEST_NUM = 1
currentStatus.RX_TIME = time.ctime()
# Established and calculated upon receive

currentStatus.calc_lat_lon()
currentStatus.decode_source_unit_id()

test_dict = {
    "unit_number": currentStatus.DICT_NUM, # Unit Number
    "emerg_flg": currentStatus.EMERG_FLG, # Emergency flag
    "fline_stat": currentStatus.FLINE_STAT, # Fireline Status
    "rsrc_stat": currentStatus.RSRC_STAT, # Resource status"
    "lat": currentStatus.LAT,
    "lon": currentStatus.LON,
    "rx_time": currentStatus.RX_TIME,
}

print('Dump to console:')
currentStatus.dump_to_console()
print('\nOutput of dictionary:\n')
print(test_dict)
