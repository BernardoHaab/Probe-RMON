
from entry import column_oids, columns

def get_line_oid(columnName, line):
    return column_oids[columnName] + '.' + line

def get_col_value(table, columnName, line):
    lineOid = get_line_oid(columnName, line)
    column = table.get(lineOid)
    if column == None:
        column = columns.get(column_oids[columnName]).copy()
        if column.get('type') == 'integer':
            column['value'] = 0
        else:
            column['value'] = ""
    return column

def inc_stats_pkts(table, line):
    lineOid = get_line_oid('etherStatsPkts', line)
    oldColumn = get_col_value(table,'etherStatsPkts', line)
    
    oldColumn['value'] += 1
    table[lineOid] = oldColumn

def acc_stats_octets(table, line, packetLen):
    column_name = 'etherStatsOctets'
    lineOid = get_line_oid(column_name, line)
    oldColumn = get_col_value(table,column_name, line)
    
    oldColumn['value'] += packetLen
    table[lineOid] = oldColumn


def inc_buckets_granted(table, line):
    column_name = 'historyControlBucketsGranted'
    lineOid = get_line_oid(column_name, line)
    oldColumn = get_col_value(table,column_name, line)

    oldColumn['value'] += 1
    table[lineOid] = oldColumn

