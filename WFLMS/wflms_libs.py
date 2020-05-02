# Python 3 WFLMS Implementation V1.0
# Authors: Robert Goldie, Jack Gallegos, Cal Poly San Luis Obispo 2020

# Dependencies: bitstring, time
import binascii
from bitstring import BitArray, BitStream

# Packet encoding function
def encode_lora_packet(packetObject):
	# Input takes in an object of Packet class and outputs a byte literal for sending.

	# Create the output lora packet as a bitarray to be sent
	encoded_lora_packet = BitArray(uintbe = 0, length = 160)

	# Emergency Flag Encoding
	encoded_lora_packet[0] = packetObject.EMERG_FLG	# MSB

	# Fireline Status Encoding
	encoded_lora_packet[1] = packetObject.FLINE_STAT

	# Resource Status Encoding
	encoded_lora_packet[2:4] = packetObject.RSRC_STAT

	# MGRS Location Encoding
	encoded_lora_packet[4:124] = bytes(packetObject.MGRS_LOC, "ascii")

	encoded_lora_packet[124:132] = 0

	# Destination Number Encoding
	encoded_lora_packet[132:140] = packetObject.DEST_NUM

	# Destination Type Encoding
	encoded_lora_packet[140:144] = packetObject.DEST_TYPE

	# Source Number Encoding
	encoded_lora_packet[144:152] = packetObject.SRC_NUM

	# Source Type Encoding
	encoded_lora_packet[152:156] = packetObject.SRC_TYPE
	# Empty Bits Encoding
	encoded_lora_packet[156:160] = 0 # 4 unused bits LSB

	return encoded_lora_packet

# Packet decoding function
def decode_lora_packet(encodedByteLiteral):
	# Input takes in a byte literal and outputs an object of the Packet class

	# Create packet object
	packetObject = Packet()

	# Emergency Flag Decoding
	packetObject.EMERG_FLG = int(encodedByteLiteral[0])	# MSB

	# Fireline Status Decoding
	packetObject.FLINE_STAT = int(encodedByteLiteral[1])

	# Resource Status Decoding
	packetObject.RSRC_STAT = encodedByteLiteral[2:4].uint

	# MGRS Location Decoding
	packetObject.MGRS_LOC = bytes.fromhex(str(encodedByteLiteral[4:124].hex)).decode('ascii')

	# Destination Number Encoding
	packetObject.DEST_NUM = encodedByteLiteral[132:140].uint

	# Destination Type Decoding
	packetObject.DEST_TYPE = encodedByteLiteral[140:144].uint

	# Source Number Deccoding
	packetObject.SRC_NUM = encodedByteLiteral[144:152].uint

	# Source Type Deccoding
	packetObject.SRC_TYPE = encodedByteLiteral[152:156].uint	# LSB (+4 unused bits)

	return packetObject


class Packet:
	def __init__(self):
		# For demo purposes, packets will be from GPS tracker nodes (likely handcrews), so other fields can be set later.
		self.EMERG_FLG = 0
		self.FLINE_STAT = 0
		self.RSRC_STAT = 0
		self.MGRS_LOC = 0
		self.DEST_NUM = 0
		self.DEST_TYPE = 0
		self.SRC_NUM = 0
		self.SRC_TYPE = 0

		# By default, packets target ATGS (repeater station)

	def dump_to_console(self):
		print('EMERG_FLG:	' + str(self.EMERG_FLG))
		print('FLINE_STAT:	' + str(self.FLINE_STAT))
		print('RSRC_STAT:	' + str(self.RSRC_STAT))
		print('MGRS_LOC:	' + str(self.MGRS_LOC))
		print('DEST_NUM:	' + str(self.DEST_NUM))
		print('DEST_TYPE:	' + str(self.DEST_TYPE))
		print('SRC_NUM:	' + str(self.SRC_NUM))
		print('SRC_TYPE:	' + str(self.SRC_TYPE))
