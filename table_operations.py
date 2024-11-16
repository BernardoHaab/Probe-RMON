
from entry import column_oids, columns

def inc_stats_pkts(table, line):
    lineOid = column_oids['etherStatsPkts'] + '.' + line
    # print(f"lineOid: {lineOid}")
    etherStatsPkts = table.get(lineOid)
    # print(f"etherStatsPkts: {etherStatsPkts}")
    if etherStatsPkts == None:
        etherStatsPkts = columns.get(column_oids['etherStatsPkts']).copy()
        etherStatsPkts['value'] = 0
    etherStatsPkts['value'] += 1
    table[lineOid] = etherStatsPkts

def acc_stats_octets(table, line, packetLen):
    lineOid = column_oids['etherStatsOctets'] + '.' + line
    etherStatsOctets = table.get(lineOid)
    if etherStatsOctets == None:
        etherStatsOctets = columns.get(column_oids['etherStatsOctets']).copy()
        etherStatsOctets['value'] = 0
    etherStatsOctets['value'] += packetLen
    table[lineOid] = etherStatsOctets

