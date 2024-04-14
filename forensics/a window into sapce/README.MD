# A window into space


This is a pcap analysis challenge where I sent each character of the flag through the Window header of a TCP packet. 

# To Solve

Use scapy to read each TCP packet either from port 8008 or with the syn flag set (either will do) and then read the window and chr() it back to ascii. See solve script