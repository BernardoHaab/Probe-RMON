# entry:
# - valor
# - access
# - type

READ_CREATE='read-create'
READ_ONLY='read-only'

column_oids = {
    'etherStatsIndex': '.1.3.6.1.2.1.16.1.1.1.1',
    'etherStatsDataSource': '.1.3.6.1.2.1.16.1.1.1.2',
    'etherStatsOctets': '.1.3.6.1.2.1.16.1.1.1.4',
    'etherStatsPkts':    '.1.3.6.1.2.1.16.1.1.1.5',
    'etherStatsBroadcastPkts':    '.1.3.6.1.2.1.16.1.1.1.6',
    'etherStatsOversizePkts': '.1.3.6.1.2.1.16.1.1.1.10',
    'etherStatsOwner': '.1.3.6.1.2.1.16.1.1.1.20',
    'etherStatsStatus': '.1.3.6.1.2.1.16.1.1.1.21',

    'etherHistoryOversizePkts':    '.1.3.6.1.2.1.16.2.2.1.11',
    'etherHistoryOctets':    '.1.3.6.1.2.1.16.2.2.1.5',
    'etherHistoryPkts':    '.1.3.6.1.2.1.16.2.2.1.6',
    'etherHistoryBroadcastPkts':    '.1.3.6.1.2.1.16.2.2.1.7',
}

columns = {
    column_oids['etherStatsIndex']: { #Key
        'value': None,
        'access': READ_ONLY,
        'type': 'int',
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
    column_oids['etherStatsOversizePkts']: {
        'value': None,
        'access': READ_ONLY,
        'type': 'string',
        'isKey': False,
        'isStatus': False
    },
    column_oids['etherStatsOctets']: {
        'value': None,
        'access': READ_ONLY,
        'type': 'string',
        'isKey': False,
        'isStatus': False
    },
    column_oids['etherStatsPkts']: {
        'value': None,
        'access': READ_ONLY,
        'type': 'string',
        'isKey': False,
        'isStatus': False
    },
    column_oids['etherStatsBroadcastPkts']: {
        'value': None,
        'access': READ_ONLY,
        'type': 'string',
        'isKey': False,
        'isStatus': False
    },
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
        'type': 'string',
        'isKey': False,
        'isStatus': True
    },
}

status_valid = 1
statistics_status = '.1.3.6.1.2.1.16.1.1.1.21'

def set_entry(table, oid, value):
    oidColumn = get_column_oid(oid)
    column = columns.get(oidColumn)

    if (column == None or column.get('access') == 'read-only'):
        # ToDo: Verificar como retornar erro (No momento ta tratando no probe e printando mensagem "None")
        return False

    line = oid[len(oidColumn)+1:]
    tableOid = oidColumn.split(".")
    tableOid = ".".join(tableOid[:-1])

    if (column['isStatus'] and value == status_valid and has_all_required(table, tableOid, line) == False):
        return False

    if is_new_row(table, tableOid, line):
        create_new_row(table, tableOid, line)

    newEntry = column.copy()
    newEntry['value'] = value
    table[oid] = newEntry

def get_entry(table, oid):
    # column = columns.get(oid)

    column = table.get(oid)
    if column == None:
        return None
    return column.get('value')

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
            print("tableColumn", str(tableColumn))
            print("Não tem todos os campos")
            return False


    return True;