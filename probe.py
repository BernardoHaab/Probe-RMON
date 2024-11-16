import threading
from scapy.all import sniff
import time
import sys
import datetime
import socket
import os
import logging

from entry import set_entry, get_entry, statistics_status, status_valid
from table_operations import inc_stats_pkts

# Configure logging
logging.basicConfig(
    filename='/tmp/log.txt',
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

def is_statistics_valid():
    global table
    is_valid = False
    with table_lock:
        status_oid = statistics_status+'.1'
        status_column = table.get(status_oid)
        is_valid = status_column != None and status_column.get('value') == status_valid
    return is_valid;


def update_stats():
    global table
    if is_statistics_valid():
        inc_stats_pkts(table, 1); #Buscar linha dinamicamente (talvez fazer para cada lina)

# Sniffer thread function
def packet_sniffer(interface):
    logging.info(f"Starting packet sniffer on interface: {interface}")
    try:
        sniff(prn=packet_handler, iface=interface, store=False, promisc=True)
    except Exception as e:
        logging.error(f"Error in packet sniffer: {e}")

def main():
    global table
    logging.info("Program started")
    interface = sys.argv[1]
    logging.info(f"Interface provided: {interface}")


    # Create and start the sniffer thread
    sniffer_thread = threading.Thread(target=packet_sniffer, args=(interface,))
    sniffer_thread.daemon = True  # This makes the thread exit when the main program exits
    sniffer_thread.start()
    logging.info("Sniffer thread started")

    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                raise EOFError()
            line = line.strip()
            logging.info("NOVA LINHA: ---"+line+"---")
            logging.info(f"--->TABELA: {table}")

            if 'PING' in line:
                logging.info("Received PING command")
                print("PONG")

            elif 'get' in line:
                logging.info("Received get command")
                oid = sys.stdin.readline()
                oid = oid.strip()
                logging.info(f"OID received: {oid}")

                res = None
                with table_lock:
                    logging.info("SEARCHING")
                    res = table.get(oid)
                    logging.info(f"Res: {res}")
                
                if res != None and res.get('value') != None:
                    # print(res.get('type'))
                    print(f"{oid}")
                    print(res.get('type'))
                    print(f"{res.get('value')}")

                else:
                    print(f"{oid}")
                    print("string")
                    print("None")

            elif 'set' in line:
                logging.info("Received set command")
                oid = sys.stdin.readline()
                oid = oid.strip()
                logging.info(f"OID received: {oid}")

                data = sys.stdin.readline().strip()
                trash = sys.stdin.readline().strip()

                [type, value] = data.split(" ")
                                
                logging.info(f"data received: {data}")
                logging.info(f"value received: {value}")
                logging.info(f"TRASH received: {trash}")

                has_set = False
                with table_lock:
                    set_entry(table, oid, value)
                if has_set == False:
                    print("None")
            else:
                logging.warning("Unknown command received")
                print("NONE")

            sys.stdout.flush()
        except EOFError:
            logging.info("EOFError encountered, exiting main loop")
            break
        except Exception as e:
            logging.error(f"Error in main loop: {e}")
    print("--ACABOU--")

if __name__ == "__main__":
    main()
