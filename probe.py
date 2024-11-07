
import threading
from scapy.all import sniff
import time
import sys
import datetime
import socket
import os

# Shared variable to store the packet count
packet_count = 0
# Lock for thread-safe access to shared variable
count_lock = threading.Lock()

# Function to handle each sniffed packet
def packet_handler(packet):
    global packet_count
    with count_lock:
        packet_count += 1

# Sniffer thread function
def packet_sniffer():
    sniff(prn=packet_handler,iface="eth0", store=False, promisc=True)

def main():

    while True:

        line = sys.stdin.readline()
        if not line:
            raise EOFError()
        line = line.strip()

        if 'PING' in line:
            print("PONG")

            # Create and start the sniffer thread
            sniffer_thread = threading.Thread(target=packet_sniffer)
            sniffer_thread.daemon = True  # This makes the thread exit when the main program exits
            sniffer_thread.start()

        elif 'get' in line:
            oid = sys.stdin.readline()
            oid = oid.strip()
            if oid == ".1.3.6.1.2.1.16.1.1.1.1.1":
                print(".1.3.6.1.2.1.16.1.1.1.1.1")
                print("integer")
                with count_lock:
                    print(f"{packet_count}")
            else:
                print("NONE")
        else:
            print("NONE")

        sys.stdout.flush()

if __name__ == "__main__":
    main()