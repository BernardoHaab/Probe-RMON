
import logging

READ_CREATE='read-create'
READ_ONLY='read-only'

logging.basicConfig(
    filename='/tmp/log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

column_oids = {
    'etherStatsIndex': '.1.3.6.1.2.1.16.1.1.1.1',
    'etherStatsDataSource': '.1.3.6.1.2.1.16.1.1.1.2',
    'etherStatsOctets': '.1.3.6.1.2.1.16.1.1.1.4',
    'etherStatsPkts':    '.1.3.6.1.2.1.16.1.1.1.5',
    'etherStatsBroadcastPkts':    '.1.3.6.1.2.1.16.1.1.1.6',
    'etherStatsMulticastPkts':    '.1.3.6.1.2.1.16.1.1.1.7',
    'etherStatsOversizePkts': '.1.3.6.1.2.1.16.1.1.1.10',
    'etherStatsPkts64Octets': '.1.3.6.1.2.1.16.1.1.1.14',
    'etherStatsPkts65to127Octets': '.1.3.6.1.2.1.16.1.1.1.15',
    'etherStatsPkts128to255Octets': '.1.3.6.1.2.1.16.1.1.1.16',
    'etherStatsPkts256to511Octets': '.1.3.6.1.2.1.16.1.1.1.17',
    'etherStatsPkts512to1023Octets': '.1.3.6.1.2.1.16.1.1.1.18',
    'etherStatsPkts1024to1518Octets': '.1.3.6.1.2.1.16.1.1.1.19',
    'etherStatsOwner': '.1.3.6.1.2.1.16.1.1.1.20',
    'etherStatsStatus': '.1.3.6.1.2.1.16.1.1.1.21',

    'historyControlIndex':  '.1.3.6.1.2.1.16.2.1.1.1',
    'historyControlDataSource':  '.1.3.6.1.2.1.16.2.1.1.2',
    'historyControlBucketsRequested':  '.1.3.6.1.2.1.16.2.1.1.3',
    'historyControlBucketsGranted':  '.1.3.6.1.2.1.16.2.1.1.4',
    'historyControlInterval':  '.1.3.6.1.2.1.16.2.1.1.5',
    'historyControlOwner':  '.1.3.6.1.2.1.16.2.1.1.6',
    'historyControlStatus':  '.1.3.6.1.2.1.16.2.1.1.7',

    'etherHistoryIndex':    '.1.3.6.1.2.1.16.2.2.1.1',
    'etherHistorySampleIndex':    '.1.3.6.1.2.1.16.2.2.1.2',
    'etherHistoryIntervalStart':    '.1.3.6.1.2.1.16.2.2.1.3',
    'etherHistoryOctets':    '.1.3.6.1.2.1.16.2.2.1.5',
    'etherHistoryPkts':    '.1.3.6.1.2.1.16.2.2.1.6',
    'etherHistoryBroadcastPkts':    '.1.3.6.1.2.1.16.2.2.1.7',
    'etherHistoryMulticastPkts':    '.1.3.6.1.2.1.16.2.2.1.8',
    'etherHistoryOversizePkts':    '.1.3.6.1.2.1.16.2.2.1.11',
}

column_integer_read_only = {
    'value': None,
    'access': READ_ONLY,
    'type': 'integer',
    'isKey': False,
    'isStatus': False
}

columns = {
    column_oids['etherStatsIndex']: { #Key
        'value': None,
        'access': READ_ONLY,
        'type': 'integer',
        'isKey': True,
        'isStatus': False
    },
    column_oids['etherStatsDataSource']: { # Interfacce
        'value': None,
        'access': READ_CREATE,
        'type': 'string',
        'isKey': False,
        'isStatus': False
    },
    column_oids['etherStatsOversizePkts']: column_integer_read_only.copy(),
    column_oids['etherStatsOctets']: column_integer_read_only.copy(),
    column_oids['etherStatsPkts']: column_integer_read_only.copy(),
    column_oids['etherStatsBroadcastPkts']: column_integer_read_only.copy(),
    column_oids['etherStatsMulticastPkts']: column_integer_read_only.copy(),
    column_oids['etherStatsPkts64Octets']: column_integer_read_only.copy(),
    column_oids['etherStatsPkts65to127Octets']: column_integer_read_only.copy(),
    column_oids['etherStatsPkts128to255Octets']: column_integer_read_only.copy(),
    column_oids['etherStatsPkts256to511Octets']: column_integer_read_only.copy(),
    column_oids['etherStatsPkts512to1023Octets']: column_integer_read_only.copy(),
    column_oids['etherStatsPkts1024to1518Octets']: column_integer_read_only.copy(),
    column_oids['etherStatsOwner']: { #Owner
        'value': None,
        'access': READ_CREATE,
        'type': 'string',
        'isKey': False,
        'isStatus': False
    },
    column_oids['etherStatsStatus']: { #Status
        'value': None,
        'access': READ_CREATE,
        'type': 'integer',
        'isKey': False,
        'isStatus': True
    },

    # --------------------------------------------------------------------------------------------------

    column_oids['historyControlIndex']: { #Key
        'value': None,
        'access': READ_ONLY,
        'type': 'integer',
        'isKey': True,
        'isStatus': False
    },
    column_oids['historyControlDataSource']: { # Interfacce
        'value': None,
        'access': READ_CREATE,
        'type': 'string',
        'isKey': False,
        'isStatus': False
    },
    column_oids['historyControlBucketsRequested']: { # Qnt de leituras
        'value': None,
        'access': READ_CREATE,
        'type': 'integer',
        'isKey': False,
        'isStatus': False
    },
    column_oids['historyControlBucketsGranted']: { # Qnt de leituras realizadas
        'value': None,
        'access': READ_ONLY,
        'type': 'integer',
        'isKey': False,
        'isStatus': False
    },
    column_oids['historyControlInterval']: { # Intervalo em segundos
        'value': None,
        'access': READ_CREATE,
        'type': 'integer',
        'isKey': False,
        'isStatus': False
    },
    column_oids['historyControlOwner']: { #Owner
        'value': None,
        'access': READ_CREATE,
        'type': 'string',
        'isKey': False,
        'isStatus': False
    },
    column_oids['historyControlStatus']: { #Status
        'value': None,
        'access': READ_CREATE,
        'type': 'integer',
        'isKey': False,
        'isStatus': True
    },

    # --------------------------------------------------------------------------------------------------

    column_oids['etherHistoryIndex']: { # Key de control
        'value': None,
        'access': READ_ONLY,
        'type': 'integer',
        'isKey': True,
        'isStatus': False
    },
    column_oids['etherHistorySampleIndex']: { # Key
        'value': None,
        'access': READ_CREATE,
        'type': 'string',
        'isKey': True,
        'isStatus': False
    },
    column_oids['etherHistoryIntervalStart']: column_integer_read_only.copy(),
    column_oids['etherHistoryOctets']: column_integer_read_only.copy(),
    column_oids['etherHistoryPkts']: column_integer_read_only.copy(),
    column_oids['etherHistoryBroadcastPkts']: column_integer_read_only.copy(),
    column_oids['etherHistoryMulticastPkts']: column_integer_read_only.copy(),
    column_oids['etherHistoryOversizePkts']: column_integer_read_only.copy(),

}

status_valid = 1
status_create_req = 2
status_creating = 3
status_invalid = 4
statistics_status = '.1.3.6.1.2.1.16.1.1.1.21'

def set_entry(table, oid, value):
    logging.info(f"SET-ENTRY_OID: {oid}")
    oidColumn = get_column_oid(oid)
    column = columns.get(oidColumn)

    if (column == None or column.get('access') == 'read-only'):
        # ToDo: Verificar como retornar erro (No momento ta tratando no probe e printando mensagem "None")
        return False

    line = oid[len(oidColumn)+1:]
    tableOid = oidColumn.split(".")
    tableOid = ".".join(tableOid[:-1])

    if (column['isStatus']):
        if (value == status_create_req):
            value = status_creating
        elif (value == status_creating):
            return False
        elif (value == status_valid):
            if (has_all_required(table, tableOid, line) == False):
                value = status_invalid
            else:
                create_default_line(table, tableOid, line)
            # return False

    if is_new_row(table, tableOid, line):
        create_new_row(table, tableOid, line)

    newEntry = column.copy()

    if (newEntry.get('type') == 'integer'):
        newEntry['value'] = int(value)
    else:
        newEntry['value'] = value

    table[oid] = newEntry

def get_entry(table, oid):
    # column = columns.get(oid)

    column = table.get(oid)
    if column == None:
        return None
    return column.get('value')


def create_default_line(table, table_oid, line):
    table_columns = {key : val for key, val in columns.items() if key.startswith(table_oid) and val['access'] == READ_ONLY and val['isKey'] == False}
    logging.info(f"Table_columns: {table_columns}")
    for col in table_columns:
        complete_oid = f"{col}.{line}"

        logging.info(f"-->complete_oid: {complete_oid}")
        new_entry = columns.get(col).copy()
        new_entry['value'] = 0
        table[complete_oid] = new_entry


def is_new_row(table, tableOid, line):
    for columnOid in table.keys():
        if columnOid.startswith(tableOid) and columnOid[len(tableOid)] == '.' and table.get(columnOid+"."+line):
            return False
    return True

def create_new_row(table, tableOid, line):
    keyColumns = {key : val for key, val in columns.items() if key.startswith(tableOid) and val['isKey'] == True}
    keyColumns = keyColumns.keys()
    sortedKeyColumns = sorted(keyColumns)

    lineIds = line.split('.')

    # print("lineIds", lineIds)

    for keyColumn in sortedKeyColumns:
        newEntry = columns[keyColumn].copy()
        newEntry['value'] = lineIds.pop(0)
        table[keyColumn + '.' + line] = newEntry

def get_column_oid(oid):
    for columnOid in columns.keys():
      if oid.startswith(columnOid) and oid[len(columnOid)] == '.':
        return columnOid
    return None

def has_all_required(table, tableOid, line):

    requiredColumns = {key : val for key, val in columns.items()
                   if key.startswith(tableOid) and val['access'] == READ_CREATE}
    requiredKeys = requiredColumns.keys()

    for columnOid in requiredKeys:
        tableColumn = table.get(columnOid+"."+line)
        if tableColumn == None or tableColumn['value'] == None:
            # print("tableColumn", str(tableColumn))
            # print("Não tem todos os campos")
            return False


    return True

def get_column(oid):
    for column in column_oids.values():
        if column.startswith(oid):
            return oid
    return None
    