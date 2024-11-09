# entry:
# - valor
# - access
# - type

columns = {
    '.1.3.6.1.2.1.16.1.1.1.1': { #Key
        'value': None,
        'access': 'read-only',
        'type': 'int',
        'isKey': True,
        'isStatus': False
    },
    '.1.3.6.1.2.1.16.1.1.1.2': { # Interfacce
        'value': None,
        'access': 'read-create',
        'type': 'string',
        'isKey': False,
        'isStatus': False
    },
    '.1.3.6.1.2.1.16.1.1.1.10': {
        'value': None,
        'access': 'read-only',
        'type': 'string',
        'isKey': False,
        'isStatus': False
    },
    '.1.3.6.1.2.1.16.1.1.1.4': {
        'value': None,
        'access': 'read-only',
        'type': 'string',
        'isKey': False,
        'isStatus': False
    },
    '.1.3.6.1.2.1.16.1.1.1.5': {
        'value': None,
        'access': 'read-only',
        'type': 'string',
        'isKey': False,
        'isStatus': False
    },
    '.1.3.6.1.2.1.16.1.1.1.6': {
        'value': None,
        'access': 'read-only',
        'type': 'string',
        'isKey': False,
        'isStatus': False
    },
    '.1.3.6.1.2.1.16.1.1.1.20': { #Owner
        'value': None,
        'access': 'read-create',
        'type': 'string',
        'isKey': False,
        'isStatus': False
    },
    '.1.3.6.1.2.1.16.1.1.1.21': { #Status
        'value': None,
        'access': 'read-create',
        'type': 'string',
        'isKey': False,
        'isStatus': True
    },
}

statusValid = 1

def set_entry(table, oid, value):
    # print("oid", oid)
    line = oid[-1:]
    # print("line",line)
    oidColumn = oid[:-2]

    # print("oidColumn",oidColumn)

    column = columns.get(oidColumn)

    # print("column", column)

    #Erro se column udefined

    if (column == None or column.access == 'read-only'):
        return False

    if (column.isStatus and value == statusValid):
        has_all_required(table, line)
        # Se não tiver todos passa pra invalido e da erro (verificar se realmente passa para inválido)
    
    newEntry = column.copy()
    
    newEntry.value = value
    
    table[oid] = newEntry

def has_all_required(table, line):
    return True;