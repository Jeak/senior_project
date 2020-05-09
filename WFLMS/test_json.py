# test

import mgrs
from bitstring import BitArray, BitStream

import json
import time
from wflms_libs import *

# Create MGRS object
m = mgrs.MGRS()

# Create fake packet object
currentStatus = Packet()

currentStatus.SRC_TYPE = 0  # hardcode Pi 0 node as Handcrew 2
currentStatus.SRC_NUM = 2   # hardcode for Pi 0
currentStatus.EMERG_FLG = 1
currentStatus.FLINE_STAT = 0
currentStatus.RSRC_STAT = 1
currentStatus.MGRS_LOC = bytes('10SEG6374048456','utf-8')
currentStatus.DEST_TYPE = 10
currentStatus.DEST_NUM = 1
currentStatus.RX_TIME = time.ctime()
# Established and calculated upon receive
# Convert MGRS to lat and lon
try:
    lat_lon = m.toLatLon(currentStatus.MGRS_LOC)
except mgrs.core.RTreeError:
    print('RTree Error')

print(lat_lon)
print(type(lat_lon))
currentStatus.LAT = lat_lon[0]
currentStatus.LON = lat_lon[1]

print('Dump to console:')
currentStatus.dump_to_console()
