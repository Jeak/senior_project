# Python 3 WFLMS Implementation V1.0
# Authors: Robert Goldie, Jack Gallegos, Cal Poly San Luis Obispo 2020


from wflms_libs	import *	# Import everything from wflmslibs file

import busio				# Import Blinka Libraries
from digitalio import DigitalInOut, Direction, Pull
import board
import adafruit_ssd1306		# Import the SSD1306 module
import adafruit_rfm9x		# Import RFM9x

import gpsd					# GPS Stuff
gpsd.connect() 				# connects to local GPSD

import mgrs					# GPS Coordinate Conversion Library
import time					# Import Python System Libraries

# Button Definitions
btnA = DigitalInOut(board.D5)
btnA.direction = Direction.INPUT
btnA.pull = Pull.UP
btnB = DigitalInOut(board.D6)
btnB.direction = Direction.INPUT
btnB.pull = Pull.UP
btnC = DigitalInOut(board.D12)
btnC.direction = Direction.INPUT
btnC.pull = Pull.UP

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
# Set Target node to 1 (Repeater)
rfm9x.node = 0x02
rfm9x.destination = 0x02
prev_packet = None


def init_type():		# returns a string to be assigned to SRC_TYPE
	crew_type = ['Handcrew','Engine Crew','Strike Team','Dozer','Water Tender',
						'Medical Team','SEAT','VLAT','Helicopter','ATGS','IC']
	n = 0
	while btnB.value:
		display.fill(0)
		display.text('Crew Type:' , 0, 0, 1)
		display.text(crew_type[n]+'?' , 0, 16, 1)
		display.show()

		if not btnA.value:
			n += 1
			if n > 10: n = 0
			display.fill(0)
			display.text('Crew Type:' , 0, 0, 1)
			display.text(crew_type[n]+'?' , 0, 16, 1)
			display.show()
			time.sleep(0.200)
	time.sleep(0.200)
	return n


def init_num(crew_type):	# returns an integer to be assigned to SRC_NUM
	if crew_type == 0: crew_abbrev = 'H'
	elif crew_type == 1: crew_abbrev = 'EC'
	elif crew_type == 2: crew_abbrev = 'ST'
	elif crew_type == 3: crew_abbrev = 'D'
	elif crew_type == 4: crew_abbrev = 'WT'
	elif crew_type == 5: crew_abbrev = 'MT'
	elif crew_type == 6: crew_abbrev = 'SEAT'
	elif crew_type == 7: crew_abbrev = 'VLAT'
	elif crew_type == 8: crew_abbrev = 'HELI'
	elif crew_type == 9: crew_abbrev = 'ATGS'
	elif crew_type == 10: crew_abbrev = 'IC'
	else: return 'Error'

	num_list = ['0','1','2','3','4','5','6','7','8','9']
	crew_num = 0
	n = 0
	m = 0

# = Crew 1st Digit Select
	n = 0
	while btnB.value:
		display.fill(0)
		display.text('Crew Number:  ' + crew_abbrev + num_list[n] + '_?' , 0, 0, 1)
		display.show()

		if not btnA.value:
			n += 1
			if n > 9: n = 0
			display.fill(0)
			display.text('Crew Number:  ' + crew_abbrev + num_list[n] + '_?' , 0, 0, 1)
			display.show()
			time.sleep(0.200)
	time.sleep(0.200)

# = Crew 2nd Digit Select
	while btnB.value:
		display.fill(0)
		display.text('Crew Number:  ' + crew_abbrev  + num_list[n] + num_list[m] + '?' , 0, 0, 1)
		display.show()

		if not btnA.value:
			m += 1
			if m > 9: m = 0
			display.fill(0)
			display.text('Crew Number:  ' + crew_abbrev  + num_list[n] + num_list[m] + '?' , 0, 0, 1)
			display.show()
			time.sleep(0.200)

	crew_num = ((int(n) * 10) + int(m))
	time.sleep(0.200)
	return(crew_num)


def main_display(packetObject):
	display.fill(0)	# draw a box to clear the image

	if packetObject.SRC_TYPE == 0: crew_abbrev = 'H'
	elif packetObject.SRC_TYPE == 1: crew_abbrev = 'EC'
	elif packetObject.SRC_TYPE == 2: crew_abbrev = 'ST'
	elif packetObject.SRC_TYPE == 3: crew_abbrev = 'D'
	elif packetObject.SRC_TYPE == 4: crew_abbrev = 'WT'
	elif packetObject.SRC_TYPE == 5: crew_abbrev = 'MT'
	elif packetObject.SRC_TYPE == 6: crew_abbrev = 'SEAT'
	elif packetObject.SRC_TYPE == 7: crew_abbrev = 'VLAT'
	elif packetObject.SRC_TYPE == 8: crew_abbrev = 'HELI'
	elif packetObject.SRC_TYPE == 9: crew_abbrev = 'ATGS'
	elif packetObject.SRC_TYPE == 10: crew_abbrev = 'IC'
	else: crew_abbrev = ('Error')

	if packetObject.RSRC_STAT == 0: resource = 'Active'
	elif packetObject.RSRC_STAT == 1: resource = 'On break'
	elif packetObject.RSRC_STAT == 2: resource = 'In transit'
	elif packetObject.RSRC_STAT == 3: resource = 'Out of service'
	else: resource = 'Error'

	if packetObject.FLINE_STAT == 0: fline = 'No'
	elif packetObject.FLINE_STAT == 1: fline = 'Yes'
	else: fline = 'Error'

	if packetObject.EMERG_FLG == 0: emerg = 'No'
	elif packetObject.EMERG_FLG == 1: emerg = 'Yes'
	else: emerg = 'Error'

	display.text('Crew:      ' + crew_abbrev + str(packetObject.SRC_NUM), 0, 0, 1)
	display.text('Status:    ' + resource, 0, 8, 1)
	display.text('Fireline:  ' + fline, 0, 16, 1)
	display.text('Emergency: ' + emerg, 0, 24, 1)
	display.show()


def main_menu(packetObject):
	options = ['Change status','Change fireline','Activate emergency','Exit']
	status_options = ['Active','On break','In transit','Out of service']
	N_Y_options = ['No','Yes']
	n = 0
	time.sleep(0.200)

	while btnB.value:
		display.fill(0)
		display.text(options[n]+'?' , 0, 0, 1)
		display.show()

		if not btnA.value:
			n += 1
			if n > 3: n = 0
			display.fill(0)
			display.text(options[n]+'?' , 0, 0, 1)
			display.show()
			time.sleep(0.200)
	time.sleep(0.200)

	if n == 0:	# Status change
		m = 0
		while btnB.value:
			display.fill(0)
			display.text(status_options[m]+'?' , 0, 0, 1)
			display.show()

			if not btnA.value:
				m += 1
				if m > 3: m = 0
				display.fill(0)
				display.text(status_options[m]+'?' , 0, 0, 1)
				display.show()
				time.sleep(0.200)
		time.sleep(0.200)

		packetObject.RSRC_STAT = m
		if packetObject.RSRC_STAT == 1: packetObject.FLINE_STAT = 0	# if on break, also deactivate fireline construction
		return packetObject

	elif n == 1:	# Fireline change
		i = 1
		while btnB.value:
			display.fill(0)
			display.text(N_Y_options[i]+'?' , 0, 0, 1)
			display.show()

			if not btnA.value:
				i += 1
				if i > 1: i = 0
				display.fill(0)
				display.text(N_Y_options[i]+'?' , 0, 0, 1)
				display.show()
				time.sleep(0.200)
		time.sleep(0.200)

		packetObject.FLINE_STAT = i
		return packetObject

	elif n == 2:	# Emergency change
		j = 1
		while btnB.value:
			display.fill(0)
			display.text(N_Y_options[j]+'?' , 0, 0, 1)
			display.show()

			if not btnA.value:
				j += 1
				if j > 1: j = 0
				display.fill(0)
				display.text(N_Y_options[j]+'?' , 0, 0, 1)
				display.show()
				time.sleep(0.200)
		time.sleep(0.200)

		packetObject.EMERG_FLG = j
		return packetObject

	elif n == 3:	# Exit menu
		display.fill(0)
		time.sleep(0.200)
		return packetObject

def get_MGRS():
	location = gpsd.get_current()
	m = mgrs.MGRS()
	while location.mode <= 1:
		location = gpsd.get_current()
		display.fill(0)
		display.text('- Waiting for GPS -', 15, 20, 1)
		display.show()
	coords_MGRS = m.toMGRS(location.lat, location.lon)
	coords_MGRS = str(coords_MGRS.decode("ascii"))
	return coords_MGRS

#-----------------------------------------------------------------------
currentStatus = Packet()

currentStatus.SRC_TYPE = init_type()
currentStatus.SRC_NUM = init_num(currentStatus.SRC_TYPE)

currentStatus.EMERG_FLG = 1
currentStatus.FLINE_STAT = 0
currentStatus.RSRC_STAT = 1
currentStatus.MGRS_LOC = get_MGRS()
currentStatus.DEST_TYPE = 10
currentStatus.DEST_NUM = 1

last_pkt_tx = 0

time_a = 0 	# test
time_b = 0 	# test

while True:
	while (time.time() - last_pkt_tx <= 1):
			if ((not btnA.value) or (not btnB.value)):
				currentStatus = main_menu(currentStatus)

	main_display(currentStatus)
	if ((not btnA.value) or (not btnB.value)):
		currentStatus = main_menu(currentStatus)
	if (time.time() - last_pkt_tx > 10):
		print("\nPacket before Encoding\n")
		currentStatus.dump_to_console()

		encoded_byteliteral = encode_lora_packet(currentStatus)

		time_a = time.time()  	# test
		rfm9x.send_with_ack(encoded_byteliteral.bytes)
		time_b = time.time() 	# test
		print('TX Duration: '+str()(time_a - time_b)) 	# test

		last_pkt_tx = time.time()
		display.fill(0)
		display.text('- Sent PKT -', 15, 20, 1)
		display.show()
