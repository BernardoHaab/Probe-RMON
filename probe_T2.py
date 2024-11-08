import sys
import time
from threading import Lock, Thread

# from pysnmp.carrier.asynsock.dgram import udp
from pysnmp.carrier.asyncio.dgram import udp
from pysnmp.entity import config, engine
from pysnmp.entity.rfc3413 import cmdrsp
from pysnmp.hlapi import *
from pysnmp.smi import builder, compiler, rfc1902, view
from scapy.all import sniff

# Configurações globais e estatísticas
statistics = {}
history = {}
interval_stats = {}
hosts = {}

stats_lock = Lock()
history_lock = Lock()
interval_lock = Lock()
hosts_lock = Lock()

sampling_interval = 10  # Intervalo de amostragem para o grupo history (em segundos)

oidToName = {
    '.1.3.6.1.2.1.16.1.1.1.10': 'etherStatsOversizePkts',
    '.1.3.6.1.2.1.16.1.1.1.4': 'etherStatsOctets',
    '.1.3.6.1.2.1.16.1.1.1.5': 'etherStatsPkts',
    '.1.3.6.1.2.1.16.1.1.1.6': 'etherStatsBroadcastPkts',

    '.1.3.6.1.2.1.16.2.2.1.11': 'etherHistoryOversizePkts',
    '.1.3.6.1.2.1.16.2.2.1.5': 'etherHistoryOctets',
    '.1.3.6.1.2.1.16.2.2.1.6': 'etherHistoryPkts',
    '.1.3.6.1.2.1.16.2.2.1.7': 'etherHistoryBroadcastPkts',
}

def create_stats_entry(interface):
    if interface not in statistics:
        statistics[interface] = {'etherStatsPkts': 0, 'etherStatsOctets': 0, 'etherStatsOversizePkts': 0, 'etherStatsBroadcastPkts': 0}

def create_interval_entry(interface):
    if interface not in interval_stats:
        clear_interval_stats(interface)

def clear_interval_stats(interface):
    interval_stats[interface] = {'etherHistoryPkts': 0, 'etherHistoryOctets': 0, 'etherHistoryOversizePkts': 0, 'etherHistoryBroadcastPkts': 0}

def create_host_entry(host):
    if host not in hosts:
        hosts[host] = {'hostAddress': host, 'hostInPkts': 0, 'hostOutPkts': 0, 'hostInOctets': 0, 'hostOutOctets': 0, 'hostOutErrors': 0, 'hostOutBroadcastPkts': 0, 'hostOutMulticastPkts': 0}

def is_broadcast(packet):
    return packet.dst == 'ff:ff:ff:ff:ff:ff'

def updateStats(interface, packet):
    with stats_lock, interval_lock:
        create_stats_entry(interface)
        create_interval_entry(interface)
        interval_stats[interface]['etherHistoryPkts'] += 1
        statistics[interface]['etherStatsPkts'] += 1

        interval_stats[interface]['etherHistoryOctets'] += len(packet)
        statistics[interface]['etherStatsOctets'] += len(packet)
        if len(packet) > 1518:
            interval_stats[interface]['etherHistoryOversizePkts'] += 1
            statistics[interface]['etherStatsOversizePkts'] += 1
        if is_broadcast(packet):
            interval_stats[interface]['etherHistoryBroadcastPkts'] += 1
            statistics[interface]['etherStatsBroadcastPkts'] += 1

def update_hosts(packet):
    with hosts_lock:
        src_host = packet.src
        dst_host = packet.dst
        create_host_entry(src_host)
        create_host_entry(dst_host)
        hosts[src_host]['hostOutPkts'] += 1
        hosts[src_host]['hostOutOctets'] += len(packet)
        if is_broadcast(packet):
            hosts[src_host]['hostOutBroadcastPkts'] += 1
        if packet.dst[0] == '01':
            hosts[src_host]['hostOutMulticastPkts'] += 1

        # ToDo: verificar se ocorreu erro no envio (hostOutErrors)

        hosts[dst_host]['hostInPkts'] += 1
        hosts[dst_host]['hostInOctets'] += len(packet)

# Função para capturar pacotes em uma interface e atualizar estatísticas
def capture_packets(interface):
    def process_packet(packet):
        updateStats(interface, packet)
        update_hosts(packet)
    sniff(iface=interface, prn=process_packet)

# Função para monitorar todas as interfaces especificadas
def start_monitoring(interfaces):
    threads = []
    for interface in interfaces:
        thread = Thread(target=capture_packets, args=(interface,))
        thread.daemon = True  # This makes the thread exit when the main program exits
        thread.start()

# Função para capturar dados históricos em intervalos de tempo
def capture_history():
    while True:
        time.sleep(sampling_interval)
        timestamp = time.time()

        with stats_lock, history_lock:
            history[timestamp] = statistics.copy()

def get_value(oid):
    with stats_lock:
        for interface, stats in statistics.items():
            name = oidToName[oid.strip()]
            return stats[name]
    return None, None

# Função para capturar dados históricos em intervalos de tempo
def capture_history():
    while True:
        time.sleep(sampling_interval)
        timestamp = time.time()

        with stats_lock, history_lock:
            history[timestamp] = interval_stats.copy()
            for interface in interval_stats:
                clear_interval_stats(interface)
            print(hosts)

# Função principal
if __name__ == "__main__":
    # Recebe as interfaces da linha de comando
    interfaces = sys.argv[1:]

    # Inicia o monitoramento das interfaces em threads separadas
    print(interfaces)
    start_monitoring(interfaces)


    # monitoring_thread = Thread(target=start_monitoring, args=(interfaces,))
    # monitoring_thread.daemon = True
    # monitoring_thread.start()

    # Inicia a captura de histórico em uma thread separada
    history_thread = Thread(target=capture_history)
    history_thread.daemon = True
    history_thread.start()
    try:
      while True:
        time.sleep
    except KeyboardInterrupt:
      print("Monitoring stopped by user.")
    # print("OID:")
    # oid = sys.stdin.readline()

    # value = get_value(oid)
    # print(value)
    # Inicia o servidor SNMP
    # start_snmp_server()
