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
stats_lock = Lock()
history_lock = Lock()
interval_lock = Lock()
sampling_interval = 10  # Intervalo de amostragem para o grupo history (em segundos)

oidToName = {
    '.1.3.6.1.2.1.16.1.1.1.10': 'etherStatsOversizePkts',
    '.1.3.6.1.2.1.16.1.1.1.4': 'etherStatsOctets',
    '.1.3.6.1.2.1.16.1.1.1.5': 'etherStatsPkts',
    '.1.3.6.1.2.1.16.1.1.1.6': 'etherStatsBroadcastPkts',
}

def create_stats_entry(interface):
    if interface not in statistics:
        statistics[interface] = {'etherStatsPkts': 0, 'etherStatsOctets': 0, 'etherStatsOversizePkts': 0, 'etherStatsBroadcastPkts': 0}

def create_interval_entry(interface):
        interval_stats[interface] = {'etherStatsPkts': 0, 'etherStatsOctets': 0, 'etherStatsOversizePkts': 0, 'etherStatsBroadcastPkts': 0}

def is_broadcast(packet):
    return packet.dst == 'ff:ff:ff:ff:ff:ff'

# Função para capturar pacotes em uma interface e atualizar estatísticas
def capture_packets(interface):
    def process_packet(packet):
        with stats_lock, interval_lock:
            create_stats_entry(interface)
            create_interval_entry(interface)
            interval_stats[interface]['etherStatsPkts'] += 1
            statistics[interface]['etherStatsPkts'] += 1
            interval_stats[interface]['etherStatsOctets'] += len(packet)
            statistics[interface]['etherStatsOctets'] += len(packet)
            if len(packet) > 1518:
                interval_stats[interface]['etherStatsOversizePkts'] += 1
                statistics[interface]['etherStatsOversizePkts'] += 1
            if is_broadcast(packet):
                interval_stats[interface]['etherStatsBroadcastPkts'] += 1
                statistics[interface]['etherStatsBroadcastPkts'] += 1

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
                create_interval_entry(interface)
            print(f"History: {history}")

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
