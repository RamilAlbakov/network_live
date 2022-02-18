"""Parse necessary parameters for cells shared by Tele2."""


import csv


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


def parse_lte(log_path, date):
    """
    Parse lte cells shared by Tele2.

    Args:
        log_path: string

    Returns:
        list of dicts
    """
    lte_cells = []
    with open(log_path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if row['Local tracking area ID'] != '2':
                continue

            lte_cell = {
                'subnetwork': 'Tele2',
                'ip_address': None,
                'vendor': 'huawei',
                'insert_date': date,
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
            lte_cell['administrativeState'] = row['Cell admin state']
            lte_cell['rachRootSequence'] = convert_string_to_num(row['Root sequence index'])
            lte_cell['physicalLayerCellIdGroup'] = row['Physical cell ID']

            lte_cells.append(lte_cell)
    return lte_cells
