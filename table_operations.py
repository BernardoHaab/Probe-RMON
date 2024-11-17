
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
    column_name = 'etherStatsPkts'
    lineOid = get_line_oid(column_name, line)
    oldColumn = get_col_value(table,column_name, line)
    
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
    # print(f'LINE: {line}')
    lineOid = get_line_oid(column_name, line)
    oldColumn = get_col_value(table,column_name, line)

    # print(f"oldcolumn: {oldColumn}")

    oldColumn['value'] += 1
    table[lineOid] = oldColumn

def create_history_sample(table, index, sample_index):
    sample_name = 'etherHistorySampleIndex'
    index_name = 'etherHistoryIndex'

    line = f"{index}.{sample_index}"

    sample_column = get_col_value(table,sample_name, line)
    sample_column['value'] = sample_index

    index_column = get_col_value(table,index_name, line)
    index_column['value'] = index

    sample_oid = get_line_oid(sample_name, line)
    table[sample_oid] = sample_column

    index_oid = get_line_oid(index_name, line)
    table[index_oid] = index_column

def set_interval_start(table, index, sample_index, interval_statr):
    column_name = 'etherHistoryIntervalStart'
   
    line = f"{index}.{sample_index}"

    lineOid = get_line_oid(column_name, line)
    column = get_col_value(table,column_name, line)

    column['value'] = interval_statr
    table[lineOid] = column

def inc_history_pkts(table, index, sample_index):
    column_name = 'etherHistoryPkts'
   
    line = f"{index}.{sample_index}"

    lineOid = get_line_oid(column_name, line)
    column = get_col_value(table,column_name, line)

    column['value'] += 1
    table[lineOid] = column

def acc_history_octs(table, index, sample_index, packet_len):
    column_name = 'etherHistoryOctets'
   
    line = f"{index}.{sample_index}"

    lineOid = get_line_oid(column_name, line)
    column = get_col_value(table,column_name, line)

    column['value'] += packet_len
    table[lineOid] = column

def inc_broadcast(table, line, packet, column_name):
    if(is_broadcast(packet) == False): return
    
    lineOid = get_line_oid(column_name, line)
    oldColumn = get_col_value(table,column_name, line)
    
    oldColumn['value'] += 1
    table[lineOid] = oldColumn

def inc_oversized(table, line, packet, column_name):
    if(len(packet) <= 1518): return
    
    lineOid = get_line_oid(column_name, line)
    oldColumn = get_col_value(table,column_name, line)
    
    oldColumn['value'] += 1
    table[lineOid] = oldColumn


def is_broadcast(packet):
    return packet.dst == 'ff:ff:ff:ff:ff:ff'
