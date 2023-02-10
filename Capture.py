#!/usr/bin/env python

import serial
import datetime
import sys

chan = 1
port = "/dev/ttyS6"
if len(sys.argv) == 3:
    port = sys.argv[1]
    chan = int(sys.argv[2])

print("Port: "+port+" Channel: "+str(chan))

ser = serial.Serial(port, 921600)

filename = "capture_%s.pcap" % datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

print("Creating capture file: %s" % filename)
f = open(filename, 'wb')

def write_hex(f, hex_string):
    #print("Writing: "+hex_string)
    f.write(bytes.fromhex(hex_string))
    f.flush()

# PCAP file header
header = 'd4c3b2a1' + '0200' + '0400' + '00000000' + '00000000' + 'c4090000' + '69000000'
write_hex(f, header)

ser.write(bytes([chan]))

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
