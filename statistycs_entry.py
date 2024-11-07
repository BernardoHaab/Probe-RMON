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


def set_entry(table, oid, value):
    column = columns[oid]

    #Erro se column udefined

    if (column.access == 'read-only'):
        return False
    
    column.value = value
    
    newEntry = column
    
    table[oid] = newEntry

def has_all_required(table, line):
    return True;