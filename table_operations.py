
import ipaddress
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

def inc_pkts_64_octets(table, line, packet_len):
    if not is_len_in_interval(packet_len, 64, 64):
      return
    column_name = 'etherStatsPkts64Octets'
    lineOid = get_line_oid(column_name, line)
    oldColumn = get_col_value(table, column_name, line)
    oldColumn['value'] += 1
    table[lineOid] = oldColumn

def inc_pkts_65_to_127_octets(table, line, packet_len):
    if not is_len_in_interval(packet_len, 65, 127):
      return
    column_name = 'etherStatsPkts65to127Octets'
    lineOid = get_line_oid(column_name, line)
    oldColumn = get_col_value(table, column_name, line)
    oldColumn['value'] += 1
    table[lineOid] = oldColumn

def inc_pkts_128_to_255_octets(table, line, packet_len):
    if not is_len_in_interval(packet_len, 128, 255):
      return
    column_name = 'etherStatsPkts128to255Octets'
    lineOid = get_line_oid(column_name, line)
    oldColumn = get_col_value(table, column_name, line)
    oldColumn['value'] += 1
    table[lineOid] = oldColumn

def inc_pkts_256_to_511_octets(table, line, packet_len):
    if not is_len_in_interval(packet_len, 256, 511):
      return
    column_name = 'etherStatsPkts256to511Octets'
    lineOid = get_line_oid(column_name, line)
    oldColumn = get_col_value(table, column_name, line)
    oldColumn['value'] += 1
    table[lineOid] = oldColumn

def inc_pkts_512_to_1023_octets(table, line, packet_len):
    if not is_len_in_interval(packet_len, 512, 1023):
      return
    column_name = 'etherStatsPkts512to1023Octets'
    lineOid = get_line_oid(column_name, line)
    oldColumn = get_col_value(table, column_name, line)
    oldColumn['value'] += 1
    table[lineOid] = oldColumn

def inc_pkts_1024_to_1518_octets(table, line, packet_len):
    if not is_len_in_interval(packet_len, 1024, 1518):
      return
    column_name = 'etherStatsPkts1024to1518Octets'
    lineOid = get_line_oid(column_name, line)
    oldColumn = get_col_value(table, column_name, line)
    oldColumn['value'] += 1
    table[lineOid] = oldColumn

def inc_buckets_granted(table, line):
    column_name = 'historyControlBucketsGranted'
    lineOid = get_line_oid(column_name, line)
    oldColumn = get_col_value(table,column_name, line)

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

def inc_multicast(table, line, packet, column_name):
    if(is_multicast(packet) == False): return

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

def is_len_in_interval(packet_len, lower, upper):
    return lower <= packet_len <= upper

def is_broadcast(packet):
    return packet.dst == 'ff:ff:ff:ff:ff:ff'

def is_multicast(packet):
  try:
      # Parse the IP address
      ip_obj = ipaddress.ip_address(ip)

      # Check if it is multicast
      return ip_obj.is_multicast
  except ValueError:
      # Invalid IP address
      return False
