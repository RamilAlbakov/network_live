"""Parse all necessary lte cell data from enm data for network live db."""

from parser_utils import parse_mo_value, parse_node_parameter


def calculate_eci(enodeb_id, cell_id):
    """
    Calculate ECI for cell.

    Args:
        enodeb_id: string
        cell_id: string

    Returns:
        int
    """
    eci_factor = 256
    int_enodeb_id = int(enodeb_id)
    int_cell_id = int(cell_id)
    return int_enodeb_id * eci_factor + int_cell_id


def parse_lte_cells(enm_lte_cells, enm_enodeb_ids, ip_data, date):
    """
    Parse lte cells parameters from ENM data.

    Args:
        enm_lte_cells: list of strings
        enm_enodeb_ids: list of strings
        ip_data: dict
        date: string

    Returns:
        list of dicts
    """
    enodeb_ids = parse_node_parameter(enm_enodeb_ids, 'MeContext')
    lte_cells = []
    for element in enm_lte_cells:
        if 'FDN' in element:
            cell = {
                'vendor': 'ericsson',
                'insert_date': date,
            }
            cell['subnetwork'] = parse_mo_value(element, 'SubNetwork')
            cell['site_name'] = parse_mo_value(element, 'MeContext')
            cell['cell_name'] = parse_mo_value(element, 'EUtranCellFDD')
        elif ' : ' in element:
            attr_name, attr_value = element.split(' : ')
            cell[attr_name] = attr_value
        elif element == '' and cell:
            cell['enodeb_id'] = enodeb_ids[cell['site_name']]
            cell['eci'] = calculate_eci(cell['enodeb_id'], cell['cellId'])
            cell['ip_address'] = ip_data[cell['site_name']]
            lte_cells.append(cell)
            cell = {}
    return lte_cells
