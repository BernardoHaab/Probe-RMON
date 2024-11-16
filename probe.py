import threading
from scapy.all import sniff
import time
import sys
import datetime
import socket
import os
import logging

from entry import set_entry, statistics_status, status_valid, get_column_oid, columns
from table_operations import *

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

history_lines = {}
history_lines_lock = threading.Lock()

# Function to handle each sniffed packet
def packet_handler(packet):
    update_stats(packet)

def is_statistics_valid():
    global table
    is_valid = False
    with table_lock:
        status_oid = statistics_status+'.1'
        status_column = table.get(status_oid)
        is_valid = status_column != None and status_column.get('value') == status_valid
    return is_valid;

def update_stats(packet):
    global table
    if is_statistics_valid():
       with table_lock:
            # logging.info("É valido!!!")
            inc_stats_pkts(table, '1'); #Buscar linha dinamicamente (talvez fazer para cada lina)
            acc_stats_octets(table, '1', len(packet))

def update_history(packet):
    with history_lines_lock:
        for line in history_lines:
            print("--> line" + line)

# Sniffer thread function
def packet_sniffer(interface):
    logging.info(f"Starting packet sniffer on interface: {interface}")
    try:
        sniff(prn=packet_handler, iface=interface, store=False, promisc=True)
    except Exception as e:
        logging.error(f"Error in packet sniffer: {e}")

def history_control(line_oid):
    reps = table.get('historyControlBucketsRequested')
    if (reps == None): return;
    reps = reps.get('value')
    interval = table.get('historyControlInterval').get('value')
    [_, index] = line_oid.spli('.')
    print('index'+ index)
    sample_index = 1
    print('sample_index'+ sample_index)

    with history_lines_lock:
        history_lines[index] = sample_index

    for i in range(reps):
        time.sleep(interval)
        reps -= 1
        with history_lines_lock:
            sample_index += 1
            history_lines[index] = sample_index
        with table:
            inc_buckets_granted(table, index)

    with history_lines_lock:
        history_lines.pop(index)


def hanlde_new_history(oid, value):
    if value != 1: return

    column_oid = get_column_oid(oid)
    if columns[column_oid].get('isStatus'):
        line = oid.split(column_oid)[1]
        print('Linha: ' + line)
        sniffer_thread = threading.Thread(target=history_control, args=(line,))
        sniffer_thread.daemon = True  # This makes the thread exit when the main program exits
        sniffer_thread.start()


def main():
    global table
    logging.info("Program started")
    interface = sys.argv[1]
    logging.info(f"Interface provided: {interface}")


    set_entry(table, '.1.3.6.1.2.1.16.1.1.1.2.1', "eth0")
    set_entry(table, '.1.3.6.1.2.1.16.1.1.1.20.1', "Eu")
    set_entry(table, '.1.3.6.1.2.1.16.1.1.1.21.1', 2)
    set_entry(table, '.1.3.6.1.2.1.16.1.1.1.21.1', '1')


    # Create and start the sniffer thread
    sniffer_thread = threading.Thread(target=packet_sniffer, args=(interface,))
    sniffer_thread.daemon = True  # This makes the thread exit when the main program exits
    sniffer_thread.start()
    logging.info("Sniffer thread started")

    stop = False

    while stop == False:
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
                oid = sys.stdin.readline().strip()
                logging.info(f"OID received: {oid}")

                data = sys.stdin.readline().strip()
                trash = sys.stdin.readline().strip()

                [type, value] = data.split(" ")
                                
                logging.info(f"data received: {data}")
                logging.info(f"value received: {value}")

                has_set = False
                with table_lock:
                    set_entry(table, oid, value)
                hanlde_new_history(oid, value)
                print("None")
                # if has_set == False:
            elif line == "":
                logging.info("--Program end--")
                stop = True
            else:
                logging.warning("Unknown command received")
                print("NONE")

            sys.stdout.flush()
        except EOFError:
            logging.info("EOFError encountered, exiting main loop")
            break
        except Exception as e:
            logging.error(f"Error in main loop: {e}")

if __name__ == "__main__":
    main()
