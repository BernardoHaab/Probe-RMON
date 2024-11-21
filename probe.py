import threading
from scapy.all import sniff
import time
import sys
import datetime
import socket
import os
import logging

from entry import *
from table_operations import *

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

history_lines = {}
history_lines_lock = threading.Lock()

# Function to handle each sniffed packet
def packet_handler(packet):
    update_stats(packet)
    update_history(packet)

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
            inc_broadcast(table, '1', packet, 'etherStatsBroadcastPkts')
            inc_oversized(table, '1', packet, 'etherStatsOversizePkts')


def update_history(packet):
    with history_lines_lock:
        for line in history_lines:
            sample_index = history_lines[line]
            index_line = f"{line}.{sample_index}"
            inc_history_pkts(table, line, sample_index)
            acc_history_octs(table, line, sample_index, len(packet))
            inc_broadcast(table, index_line, packet, 'etherHistoryBroadcastPkts')
            inc_oversized(table, index_line, packet, 'etherHistoryOversizePkts')

# Sniffer thread function
def packet_sniffer(interface):
    logging.info(f"Starting packet sniffer on interface: {interface}")
    try:
        sniff(prn=packet_handler, iface=interface, store=False, promisc=True)
    except Exception as e:
        logging.error(f"Error in packet sniffer: {e}")

def history_control(line_oid):
    reps = None
    requests_oid = column_oids['historyControlBucketsRequested'] + line_oid
    interval_oid = column_oids['historyControlInterval'] + line_oid

    with table_lock:
        reps = table.get(requests_oid)
        interval = table.get(interval_oid)

    logging.info("START --history_control--")
    logging.info(f"reps: {reps}")

    if (reps == None): return;

    reps = reps.get('value')
    interval = interval.get('value')

    logging.info(f"Interval: {interval}")

    [_, index] = line_oid.split('.')
    logging.info(f"index: {index}")
    sample_index = 1
    logging.info(f"sample_index: {history_lines}")

    # with history_lines_lock:
    #     history_lines[index] = sample_index

    for i in range(reps):
        timestamp = time.time()
        with history_lines_lock:
            history_lines[index] = sample_index
            logging.info(f"history_lines: {history_lines}")
        with table_lock:
            inc_buckets_granted(table, index)
            create_history_sample(table, index, sample_index)
            set_interval_start(table, index, sample_index, timestamp)
            # ToDo: add timestamp to table (etherHistoryIntervalStart)
        sample_index += 1
        # reps -= 1
        time.sleep(interval)

    with history_lines_lock:
        history_lines.pop(index)
        logging.info(f"history_lines: {history_lines}")


def hanlde_new_history(oid, value):
    logging.info("value: "+ value)
    logging.info(f"type: {type(value)}")
    logging.info(f"value != '1': {value != '1'}")
    if value != '1': return

    column_oid = get_column_oid(oid)
    logging.info(f"columns[column_oid].get('isStatus'): {columns[column_oid].get('isStatus')}")
    if columns[column_oid].get('isStatus'):
        line = oid.split(column_oid)[1]
        logging.info('Linha: ' + line)
        sniffer_thread = threading.Thread(target=history_control, args=(line,))
        sniffer_thread.daemon = True  # This makes the thread exit when the main program exits
        sniffer_thread.start()

def get_next_line(line:str):
    line_int = int(line)
    return line_int+1

def map_oid(oid):
    column_oid = get_column_oid(oid)
    line = oid[len(column_oid)+1:]

    new_oid = f"{column_oid[:-1]}{line}.{column_oid[-1:]}"
    # new_oid = column_oid[:-1] + line + "." + column_oid[-1:]
    return new_oid

def map_back_oid(oid, table_oid):
    line = oid[len(table_oid): -2]

    new_oid = f"{table_oid}{oid[-2:]}{line}"
    return new_oid

def main():
    global table
    logging.info("Program started")
    interface = sys.argv[1]
    logging.info(f"Interface provided: {interface}")


    set_entry(table, '.1.3.6.1.2.1.16.1.1.1.2.1', "eth0")
    set_entry(table, '.1.3.6.1.2.1.16.1.1.1.20.1', "Bernardo")
    set_entry(table, '.1.3.6.1.2.1.16.1.1.1.21.1', 2)

    set_entry(table, '.1.3.6.1.2.1.16.2.1.1.2.1', "eth0")
    set_entry(table, '.1.3.6.1.2.1.16.2.1.1.3.1', 3)
    set_entry(table, '.1.3.6.1.2.1.16.2.1.1.3.2', 7)
    set_entry(table, '.1.3.6.1.2.1.16.2.1.1.5.1', 10)
    set_entry(table, '.1.3.6.1.2.1.16.2.1.1.6.1', "Eu")
    set_entry(table, '.1.3.6.1.2.1.16.2.1.1.7.1', 2)


    # Create and start the sniffer thread
    sniffer_thread = threading.Thread(target=packet_sniffer, args=(interface,))
    sniffer_thread.daemon = True  # This makes the thread exit when the main program exits
    sniffer_thread.start()
    logging.info("Sniffer thread started")

    set_entry(table, '.1.3.6.1.2.1.16.1.1.1.21.1', 1)
    
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

            elif 'get' == line:
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
            elif 'getnext' == line:
                oid = sys.stdin.readline().strip()
                column = get_column(oid)

                nextOid = None

                if (column != None):
                    # Pega primeira instância pelo oid passa (oid é parte de uma coluna/tabela)
                    filteredKeys = []
                    for tableOid in table.keys():
                        if tableOid.startswith(column) and tableOid[len(column)] == '.':
                            filteredKeys.append(tableOid)
                    filteredKeys.sort()
                    nextOid = filteredKeys[0]
                else :
                    # Oid contém linha

                    # Tenta pegar próxima linha da mesma coluna
                    column_oid = get_column_oid(oid)
                    line = oid[len(column_oid)+1:]
                    next_line = get_next_line(line)

                    nextOid = f"{column_oid}.{next_line}"

                    if (table.get(nextOid) == None):
                        # Se não tem próxima linha, pega proximo valor válido na tabela
                        nextOid = None

                        table_oid = column_oid.split(".")
                        table_oid = ".".join(table_oid[:-1])

                        filteredKeys = []

                        for item in table.keys():
                            if item.startswith(table_oid) and item[len(table_oid)] == ".":
                                filteredKeys.append(item)

                        mapped_oids = []

                        # Mapeia oid:
                        # table.coluna.lina -> tabela.linha.coluna

                        mapped_oids = map(map_oid,filteredKeys)
                        mapped_oids = list(mapped_oids)
                        mapped_oids.sort()
                        curr_id = mapped_oids.index(map_oid(oid))

                        # Se existir proxima posição
                        if (curr_id+1<len(mapped_oids)):
                            nextOid = mapped_oids[curr_id+1]
                            # Pega proximo oid e mapeia de volta
                            # tabela.linha.coluna - > tabela.coluna.linha
                            nextOid = map_back_oid(nextOid, table_oid)


                        logging.info(f"Mapped oid: {mapped_oids}")


                logging.info(f"nextOid: {nextOid}")

                if nextOid:
                    print(f"{nextOid}")
                    print(f"{table.get(nextOid)['type']}")
                    print(f"{table.get(nextOid)['value']}")
                else:
                    print(f"{oid}")
                    print("string")
                    print("End of TABLE")



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
            break

if __name__ == "__main__":
    main()
