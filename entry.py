# entry:
# - valor
# - access
# - type
import numpy as np

READ_CREATE='read-create'
READ_ONLY='read-only'

columns = {
    '.1.3.6.1.2.1.16.1.1.1.1': { #Key
        'value': None,
        'access': READ_ONLY,
        'type': 'int',
        'isKey': True,
        'isStatus': False
    },
    '.1.3.6.1.2.1.16.1.1.1.2': { # Interfacce
        'value': None,
        'access': READ_CREATE,
        'type': 'string',
        'isKey': False,
        'isStatus': False
    },
    '.1.3.6.1.2.1.16.1.1.1.10': {
        'value': None,
        'access': READ_ONLY,
        'type': 'string',
        'isKey': False,
        'isStatus': False
    },
    '.1.3.6.1.2.1.16.1.1.1.4': {
        'value': None,
        'access': READ_ONLY,
        'type': 'string',
        'isKey': False,
        'isStatus': False
    },
    '.1.3.6.1.2.1.16.1.1.1.5': {
        'value': None,
        'access': READ_ONLY,
        'type': 'string',
        'isKey': False,
        'isStatus': False
    },
    '.1.3.6.1.2.1.16.1.1.1.6': {
        'value': None,
        'access': READ_ONLY,
        'type': 'string',
        'isKey': False,
        'isStatus': False
    },
    '.1.3.6.1.2.1.16.1.1.1.20': { #Owner
        'value': None,
        'access': READ_CREATE,
        'type': 'string',
        'isKey': False,
        'isStatus': False
    },
    '.1.3.6.1.2.1.16.1.1.1.21': { #Status
        'value': None,
        'access': READ_CREATE,
        'type': 'string',
        'isKey': False,
        'isStatus': True
    },
}

statusValid = 1

def set_entry(table, oid, value):
    oidColumn = get_column_oid(oid)
    column = columns.get(oidColumn)

    if (column == None or column.get('access') == 'read-only'):
        # ToDo: Verificar como retornar erro (No momento ta tratando no probe e printando mensagem "None")
        return False

    line = oid[len(oidColumn)+1:]
    tableOid = oidColumn.split(".")
    tableOid = ".".join(tableOid[:-1])

    if (column['isStatus'] and value == statusValid and has_all_required(table, tableOid, line) == False):
        return False

    if is_new_row(table, tableOid, line):
        create_new_row(table, tableOid, line)

    newEntry = column.copy()
    newEntry['value'] = value
    table[oid] = newEntry

def get_entry(table, oid):
    column = columns.get(oid)
    if column == None:
        return None

    return table.get(oid)

def is_new_row(table, tableOid, line):
    for columnOid in table.keys():
        if columnOid.startswith(tableOid) and columnOid[len(tableOid)] == '.':
            return False
    return True

def create_new_row(table, tableOid, line):
    keyColumns = {key : val for key, val in columns.items() if key.startswith(tableOid) and val['isKey'] == True}
    keyColumns = keyColumns.keys()
    sortedKeyColumns = sorted(keyColumns)

    lineIds = line.split('.')

    print("lineIds", lineIds)

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

    requiredColumns.keys()

    for columnOid in requiredKeys:
        tableColumn = table.get(columnOid+"."+line)
        if tableColumn == None or tableColumn['value'] == None:
            print("tableColumn", str(tableColumn))
            print("Não tem todos os campos")
            return False


    return True;