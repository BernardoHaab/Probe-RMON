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
    print("oid", oid)
    line = oid[-1:]
    tableOid = oid[:-4]

    get_Table_oid(oid)
    print("line",line)
    oidColumn = oid[:-2]

    print("oidColumn",oidColumn)

    column = columns.get(oidColumn)

    print(str(column))
    # print("column", column)
    if (column == None or column.get('access') == 'read-only'):
        # ToDo: Verificar como retornar erro (No momento ta tratando no probe e printando mensagem "None")
        return False

    # ToDo: Adicionar coluna key (que é adicionada automaticamente) se ainda nao existir
    

    if (column['isStatus'] and value == statusValid and has_all_required(table, tableOid, line) == False):
        # Se não tiver todos passa pra invalido e da erro (verificar se realmente passa para inválido)
        return False
    
    newEntry = column.copy()

    newEntry['value'] = value
    
    table[oid] = newEntry

# def is_new_row(table, tableOid, line):
#     # T

def get_Table_oid(oid):
    columnsOids = np.array(columns.keys())

    print("--->", columnsOids)
    print("===>", str(columnsOids))

    keys = columnsOids.where(oid.startsWith(columnsOids))
    print(keys)

def has_all_required(table, tableOid, line):

    requiredColumns = {key : val for key, val in columns.items()
                   if val['access'] == READ_CREATE}
    requiredKeys = requiredColumns.keys()

    print("required columns" + str(requiredKeys))

    requiredColumns.keys()

    for columnOid in requiredKeys:
        print("Column+line", columnOid+"."+line)
        tableColumn = table.get(columnOid+"."+line)
        if tableColumn == None or tableColumn['value'] == None:
            print("tableColumn", str(tableColumn))
            print("Não tem todos os campos")
            return False

    
    return True;