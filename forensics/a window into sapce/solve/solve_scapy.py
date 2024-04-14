from scapy.all import *

def convert_window_to_char(pcap_file):
    # Open the PCAP file for reading
    flag = ""
    packets = rdpcap(pcap_file)

    # Iterate over each packet in the PCAP file
    for packet in packets:
        # Check if the packet is a TCP packet
        if TCP in packet and packet[TCP].flags & 0x02:
            # Extract the TCP Window field value
            tcp_window = packet[TCP].window

            # Convert the window value to a character (using ASCII encoding)
            try:
                char_value = chr(tcp_window)
                flag += char_value
            except ValueError:
                # Handle any value error (e.g., non-printable characters)
                char_value = '?'  # Replace with a placeholder for non-printable characters

            # Print the TCP window value and its corresponding character
            print(f"TCP Window: {tcp_window} => Character: {char_value}")

            print(flag)

if __name__ == "__main__":
    # Specify the path to the PCAP file
    pcap_file_path = "space.pcapng"

    # Call the function to convert TCP Window values to characters
    convert_window_to_char(pcap_file_path)
