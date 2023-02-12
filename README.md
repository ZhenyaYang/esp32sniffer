# ESP32 Wifi Sniffer for live Wireshark capture

Use ESP32 promiscuous mode to capture frame and send them over serial connection to a Python script that writes a PCAP file and start Wireshark with live capture.

Works on OS X, Linux.

Serial data is human readable, with packet timestamp + size, then packet data as hexstrings:

```
$ make monitor
Packet   1.747875 101 101
DATA:0100000063690b00650000006500000040000000ffffffffffffb8e85617ceceffffffffffff80c100054c45414c59010402040b1632080c1218243048606c0301062d1aad4917ffff0000000000000000000000000000000000000000007f080400000000000040dd0b0017f20a00010400000000
Packet   4.814337 210 210
DATA:04000000016d0c00d2000000d200000040000000ffffffffffffb827eb98c70bffffffffffff80bc0000010402040b1632080c1218243048606c0301062d1a21001fff00000000000000000000000000000000000000000000dd690050f204104a000110103a00010010080002314810470010fb97404916565875a860726c0fe2c424105400080000000000000000103c00010110020002000010090002000010120002000010210001201023000120102400012010110001201049000600372a000120dd11506f9a0902020025000605005858045106dd09001018020000000000
```

`Capture.py` decode this serial stream, saves a PCAP file names `capture_YYYYMMDD_HHMMSS.pcap` and opens Wireshark.

# Configure

# Building

Builds with ESP-IDF v4.x

Build & flash:
`$ idf.py build`
`$ cd build`
`$ make flash`

Or flash the prebuilt binaries directly:
`$ esptool.py --chip esp32 -p /dev/ttyS6 -b 921600 --before=default_reset --after=hard_reset write_flash --flash_mode dio --flash_freq 40m --flash_size 2MB 0x1000 bootloader.bin 0x10000 hello-world.bin 0x8000 partition-table.bin

Start `Capture.py port channel mac`

```
$ ./Capture.py /dev/ttyS6 11 34:94:54:47:f9:f4
Port: /dev/ttyS6 Channel: 11 Mac: 34:94:54:47:f9:f4
Creating capture file: capture_20230212_081757.pcap
Waiting for packets...
Channel set to 11
Packet  23.835624 292 292
Packet  23.938034 292 292
Packet  24.040438 292 292
Packet  24.142832 292 292
Packet  24.245248 292 292
...
```

Enjoy:

![Wireshark screenshot](screenshot.png)

