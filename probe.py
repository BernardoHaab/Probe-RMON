import datetime
import logging
import os
import pprint
import socket
import sys
import threading
import time

from scapy.all import sniff

from entry import set_entry

# Configure logging
logging.basicConfig(
    filename='./log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Shared variable to store the packet count
packet_count = 0
# Lock for thread-safe access to shared variable
count_lock = threading.Lock()

table = {}
table_lock = threading.Lock()

# Function to handle each sniffed packet
def packet_handler(packet):
    global packet_count
    with count_lock:
        packet_count += 1
        # logging.info(f"Packet received. Total count: {packet_count}")

# Sniffer thread function
def packet_sniffer(interface):
    logging.info(f"Starting packet sniffer on interface: {interface}")
    try:
        sniff(prn=packet_handler, iface=interface, store=False, promisc=True)
    except Exception as e:
        logging.error(f"Error in packet sniffer: {e}")

def main():
    logging.info("Program started")
    interface = sys.argv[1]
    logging.info(f"Interface provided: {interface}")

    set_entry(table, '.1.3.6.1.2.1.16.1.1.1.2.1', interface)
    set_entry(table, '.1.3.6.1.2.1.16.1.1.1.20.1', "Eu")
    set_entry(table, '.1.3.6.1.2.1.16.1.1.1.21.1', 2)
    set_entry(table, '.1.3.6.1.2.1.16.1.1.1.21.1', 1)

    print("---------------------------------------")
    pprint.pprint(table)

    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                raise EOFError()
            line = line.strip()

            if 'PING' in line:
                logging.info("Received PING command")
                print("PONG")

                # Create and start the sniffer thread
                sniffer_thread = threading.Thread(target=packet_sniffer, args=(interface,))
                sniffer_thread.daemon = True  # This makes the thread exit when the main program exits
                sniffer_thread.start()
                logging.info("Sniffer thread started")

            elif 'get' in line:
                logging.info("Received get command")
                oid = sys.stdin.readline()
                oid = oid.strip()
                logging.info(f"OID received: {oid}")

                if oid == ".1.3.6.1.2.1.16.1.1.1.1.1":
                    logging.info("Valid OID received")
                    print(".1.3.6.1.2.1.16.1.1.1.1.1")
                    print("integer")
                    with count_lock:
                        print(f"{packet_count}")
                        logging.info(f"Packet count returned: {packet_count}")
                else:
                    logging.warning("Invalid OID received")
                    print("NONE")
            elif 'set' in line:
                logging.info("Received set command")
                oid = sys.stdin.readline()
                oid = oid.strip()
                logging.info(f"OID received: {oid}")
                has_set = set_entry(table, oid, "Teste")
                if has_set:
                    print("Sucess")
                else:
                    print("None")
            else:
                logging.warning("Unknown command received", line)
                print("NONE")

            sys.stdout.flush()
        except EOFError:
            logging.info("EOFError encountered, exiting main loop")
            break
        except Exception as e:
            logging.error(f"Error in main loop: {e}")

if __name__ == "__main__":
    logging.info("Program started")
    main()