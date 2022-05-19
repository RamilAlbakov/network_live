"""Parse Beeline Nokia WCDMA xml file for network live."""

from defusedxml import ElementTree
from network_live.date import Date
from network_live.beeline.nokia_utils import make_tag, parse_sites, parse_nodes, parse_cell_parameter, get_xml_path


def parse_nokia_wcdma_cells(logs_path):
    """
    Parse WCDMA cells from Nokia xml file.

    Args:
        logs_path: string

    Returns:
        list of dicts
    """
    uarfcnul = {
        '2965': 2740,
        '2999': 2774,
        '10562': 9612,
        '10587': 9637,
        '10662': 9712,
        '10687': 9737,
        '10712': 9762,
        '10737': 9787,
    }
    root = ElementTree.parse(get_xml_path(logs_path, 'UMTS')).getroot()
    sites = parse_sites(root, 'WCDMA')

    wcdma_cells = []
    for cell_tag in root.iter(make_tag('managedObject')):
        if cell_tag.get('class') != 'WCEL':
            continue
        site_id, rnc_name, rnc_id = parse_nodes(cell_tag)
        if parse_cell_parameter(cell_tag, 'AdminCellState') == '1':
            cell_state = 'UNLOCKED'
        else:
            cell_state = 'LOCKED'
        uarfcndl = parse_cell_parameter(cell_tag, 'UARFCN')
        cell = {
            'operator': 'Beeline',
            'oss': 'Beeline Nokia',
            'rnc_id': rnc_id,
            'rnc_name': rnc_name,
            'site_name': sites[site_id],
            'UtranCellId': parse_cell_parameter(cell_tag, 'name'),
            'localCellId': parse_cell_parameter(cell_tag, 'CId'),
            'uarfcnDl': uarfcndl,
            'uarfcnUl': uarfcnul[uarfcndl],
            'primaryScramblingCode': parse_cell_parameter(cell_tag, 'PriScrCode'),
            'LocationArea': parse_cell_parameter(cell_tag, 'LAC'),
            'RoutingArea': parse_cell_parameter(cell_tag, 'RAC'),
            'ServiceArea': parse_cell_parameter(cell_tag, 'SAC'),
            'Ura': None,
            'primaryCpichPower': parse_cell_parameter(cell_tag, 'PtxPrimaryCPICH'),
            'maximumTransmissionPower': parse_cell_parameter(cell_tag, 'PtxCellMax'),
            'IubLink': None,
            'MocnCellProfile': None,
            'administrativeState': cell_state,
            'ip_address': None,
            'vendor': 'Nokia',
            'insert_date': Date.get_date('network_live'),
        }
        wcdma_cells.append(cell)
    return wcdma_cells
