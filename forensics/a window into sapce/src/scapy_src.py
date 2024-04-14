from scapy.all import IP, TCP, send


def send_tcp_packet(source_ip, destination_ip, destination_port, message):
    # Craft an IP packet with custom source IP (VMNet8 interface)
    ip_packet = IP(src=source_ip, dst=destination_ip)

    # Craft a TCP packet with destination port and message payload
    tcp_packet = TCP(sport=135,dport=8008, flags="S", window=ord(each))

    # Combine the IP and TCP packets and add the message as payload
    packet = ip_packet / tcp_packet

    # Send the packet
    send(packet)


if __name__ == "__main__":
    # Specify the source and destination IP addresses and port
    source_ip = "172.20.2.136"  # Assuming this is the IP of VMNet8 interface
    destination_ip = "172.20.2.136"  # Destination IP address
    destination_port = 8008  # Destination port

    # Specify the message to be sent in the TCP payload
    message_to_send = "shctf{1_sh0uld_try_h1d1ng_1n_th3_ch3cksum_n3xt_t1me_0817}"

    for each in message_to_send:
        send_tcp_packet(source_ip, destination_ip, destination_port, each)
