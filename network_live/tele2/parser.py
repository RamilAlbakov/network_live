"""Parse necessary parameters for cells shared by Tele2."""


import csv

from network_live.date import Date
from network_live.physical_data import add_physical_params


def convert_string_to_num(string_value):
    """
    Convert string value to number.

    Args:
        string_value: string

    Returns:
        number
    """
    try:
        num_value = round(float(string_value))
    except ValueError:
        num_value = None

    return num_value


def parse_lte(log_path, atoll_data):
    """
    Parse lte cells shared by Tele2.

    Args:
        log_path: string
        atoll_data: dict

    Returns:
        list of dicts
    """
    lte_cells = []
    with open(log_path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if row['Local tracking area ID'] != '2':
                continue

            if row['Cell admin state'] == 'CELL_UNBLOCK':
                cell_state = 'UNLOCKED'
            else:
                cell_state = 'LOCKED'

            lte_cell = {
                'oss': 'Tele2',
                'subnetwork': 'Tele2',
                'ip_address': None,
                'vendor': 'Huawei',
                'insert_date': Date.get_date('network_live'),
            }
            lte_cell['enodeb_id'] = convert_string_to_num(row['eNodeB Id'])
            lte_cell['site_name'] = row['NENAME']
            lte_cell['cell_name'] = row['Cell Name']
            lte_cell['tac'] = row['Tracking area code']
            lte_cell['cellId'] = row['Cell ID']
            lte_cell['eci'] = convert_string_to_num(row['eCI'])
            lte_cell['earfcndl'] = convert_string_to_num(row['Downlink EARFCN'])
            lte_cell['qRxLevMin'] = int(row['CELLSEL Minimum required RX level(2dBm)']) * 2
            lte_cell['latitude'] = None
            lte_cell['longitude'] = None
            lte_cell['administrativeState'] = cell_state
            lte_cell['rachRootSequence'] = convert_string_to_num(row['Root sequence index'])
            lte_cell['physicalLayerCellId'] = row['Physical cell ID']

            lte_cells.append(
                add_physical_params(atoll_data, lte_cell),
            )
    return lte_cells
