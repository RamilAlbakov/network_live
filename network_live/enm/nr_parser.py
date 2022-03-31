"""Parses nrcell parameters for network live."""

from network_live.date import Date
from network_live.enm.parser_utils import parse_mo_value


def parse_nr_sectors(enm_nr_sectors):
    """
    Parse nr sectors parameters from ENM data.

    Args:
        enm_nr_sectors: list of strings

    Returns:
        dict
    """
    nr_sectors = {}
    for element in enm_nr_sectors:
        if 'FDN' in element:
            sector = parse_mo_value(element, 'NRSectorCarrier')
            sector_params = {}
        elif ' : ' in element:
            attr_name, attr_value = element.split(' : ')
            sector_params[attr_name] = attr_value
        elif element == '' and sector_params:
            nr_sectors[sector] = sector_params
    return nr_sectors


def parse_nr_cells(enm_nr_cells, enm_nr_sectors, nr_ids, ip_data):
    """
    Parse nr cells parameters from ENM data.

    Args:
        enm_nr_cells: list of strings
        enm_nr_sectors: list of strings
        nr_ids: dict
        ip_data: dict

    Returns:
        list of dicts
    """
    nr_sectors = parse_nr_sectors(enm_nr_sectors)
    nr_cells = []
    for element in enm_nr_cells:
        if 'FDN' in element:
            cell = {
                'vendor': 'ericsson',
                'insert_date': Date.get_date('network_live'),
            }
            cell['subnetwork'] = parse_mo_value(element, 'SubNetwork')
            cell['site_name'] = parse_mo_value(element, 'MeContext')
            cell_name = parse_mo_value(element, 'NRCellDU')
            cell['cell_name'] = cell_name
        elif ' : ' in element:
            attr_name, attr_value = element.split(' : ')
            cell[attr_name] = attr_value
        elif element == '' and cell:
            cell['gNBId'] = nr_ids[cell['site_name']]
            cell['arfcnDL'] = nr_sectors[cell_name]['arfcnDL']
            cell['bSChannelBwDL'] = nr_sectors[cell_name]['bSChannelBwDL']
            cell['configuredMaxTxPower'] = nr_sectors[cell_name]['configuredMaxTxPower']
            cell['ip_address'] = ip_data[cell['site_name']]
            if not cell['nCI'].isnumeric():
                cell['nCI'] = None
            nr_cells.append(cell)
            cell = {}
    return nr_cells
