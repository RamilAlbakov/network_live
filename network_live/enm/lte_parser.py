"""Parse all necessary lte cell data from enm data for network live db."""

from network_live.date import Date
from network_live.enm.parser_utils import parse_mo_value
from network_live.physical_data import add_physical_params


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


def parse_lte_cells(enm_lte_cells, enodeb_ids, ip_data, atoll_data):
    """
    Parse lte cells parameters from ENM data.

    Args:
        enm_lte_cells: enmscripting ElementGroup
        enodeb_ids: dict
        ip_data: dict
        atoll_data: dict

    Returns:
        list of dicts
    """
    lte_cells = []
    for element in enm_lte_cells:
        element_val = element.value()
        if 'error' in element_val.lower():
            return []
        elif 'FDN' in element_val:
            cell = {
                'oss': 'ENM',
                'vendor': 'Ericsson',
                'insert_date': Date.get_date('network_live'),
            }
            cell['subnetwork'] = parse_mo_value(element_val, 'SubNetwork')
            cell['site_name'] = parse_mo_value(element_val, 'MeContext')
            cell['cell_name'] = parse_mo_value(element_val, 'EUtranCellFDD')
        elif ' : ' in element_val:
            attr_name, attr_value = element_val.split(' : ')
            if attr_name == 'physicalLayerCellIdGroup':
                pci_group = int(attr_value)
            elif attr_name == 'physicalLayerSubCellId':
                cell['physicalLayerCellId'] = pci_group * 3 + int(attr_value)
            elif attr_name == 'tac':
                cell['tac'] = attr_value
                cell['enodeb_id'] = enodeb_ids[cell['site_name']]
                cell['eci'] = calculate_eci(cell['enodeb_id'], cell['cellId'])
                cell['ip_address'] = ip_data[cell['site_name']]
                lte_cells.append(
                    add_physical_params(atoll_data, cell),
                )
            else:
                cell[attr_name] = attr_value

    return lte_cells
