
from entry import column_oids, columns

def inc_stats_pkts(table, line):
    lineOid = column_oids['etherStatsPkts'] + '.' + line
    etherStatsPkts = table.get(lineOid)
    if etherStatsPkts == None:
        etherStatsPkts = columns.get(column_oids['etherStatsPkts']).copy()
        etherStatsPkts['value'] = 0
    etherStatsPkts['value'] += 1

def sum_stats_octets(table, line, packetLen):
    lineOid = column_oids['etherStatsOctets'] + '.' + line
    etherStatsOctets = table.get(lineOid)
    if etherStatsOctets == None:
        etherStatsOctets = columns.get(column_oids['etherStatsOctets']).copy()
        etherStatsOctets['value'] = 0
    etherStatsOctets['value'] += packetLen

