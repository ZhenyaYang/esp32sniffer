#!/usr/bin/env python

import serial
import datetime
import sys

# Integer value 10 and 13, when converted to bytes from python side, one is b'\r' and the other is b'\n'
# and strangely enough, if we write it to the serial, the esp32 side will read both to be 10
# Something must be wrong with this serial write, but I don't have time to investigate into it
# I simply offset it
OFFSET = 50
chan = 1
port = "/dev/ttyS6"
if len(sys.argv) >= 3:
    port = sys.argv[1]
    chan = int(sys.argv[2])
    if len(sys.argv) == 4:
        mac_str = sys.argv[3]
    else:
        mac_str = "000000000000"

print("Port: "+port+" Channel: "+str(chan)+" Mac: "+mac_str)

mac = mac_str.replace(":", "")
mac_bytes = bytearray.fromhex(mac)

ser = serial.Serial(port, 921600)

ser.write(bytes([chan + OFFSET]))
ser.write(mac_bytes)

filename = "capture_%s.pcap" % datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

print("Creating capture file: %s" % filename)
f = open(filename, 'wb')

def write_hex(f, hex_string):
    #print("Writing: "+hex_string)
    f.write(bytes.fromhex(hex_string))
    f.flush()

def write_raw(f, data):
    f.write(data)
    f.flush()

# PCAP file header
header = 'd4c3b2a1' + '0200' + '0400' + '00000000' + '00000000' + 'c4090000' + '69000000'
write_hex(f, header)

print("Waiting for packets...")
try:
    while True:
        line = ser.readline()
        line = line.decode().strip()
        if line.startswith("DATA:"):
            data = line[5:]
            write_hex(f, data)
        else:
            print(line)

except KeyboardInterrupt:
    print("Stopping...")

f.close()
ser.close()
print("Done")
