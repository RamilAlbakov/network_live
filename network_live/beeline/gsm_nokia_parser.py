"""Parse Beeline Nokia GSM xml file for network live."""

from defusedxml import ElementTree
from network_live.date import Date
from network_live.beeline.nokia_utils import make_tag, parse_sites, parse_nodes, get_xml_path, parse_cell_parameter


def parse_trx_params(root):
    """
    Parse bcch and tch frequencies.

    Args:
        root: xml root tag object
    
    Returns:
        dict
    """
    trxs = {}
    for trx_tag in root.iter(make_tag('managedObject')):
        if trx_tag.get('class') != 'TRX':
            continue
        cell_id = trx_tag.get('distName').split('/')[-2]

        for default_tag in trx_tag.iter(make_tag('defaults')):
            trx_type = default_tag.get('name')
            frequency = parse_cell_parameter(trx_tag, 'initialFrequency')
            if 'BCCH' in trx_type or 'System' in trx_type:
                trxs[cell_id] = {
                    'bcch': frequency,
                    'tch': [],
                }
            elif 'TCH' in trx_type:
                trxs[cell_id]['tch'].append(frequency)
    return trxs


def parse_nokia_gsm_cells(logs_path):
    """
    Parse GSM cells from Nokia xml file

    Args:
        logs_path: string
    
    Returns:
        list of dicts
    """
    root = ElementTree.parse(get_xml_path(logs_path, 'GSM')).getroot()
    sites = parse_sites(root, 'GSM')
    trxs = parse_trx_params(root)

    gsm_cells = []
    for cell_tag in root.iter(make_tag('managedObject')):
        if cell_tag.get('class') != 'BTS':
            continue
        site_id, bsc_name, bsc_id = parse_nodes(cell_tag)
        cell_id = cell_tag.get('distName').split('/')[-1]
        if parse_cell_parameter(cell_tag, 'adminState') == '1':
            cell_state = 'ACTIVE'
        else:
            cell_state = 'HALTED'
        cell = {
            'operator': 'Beeline',
            'bsc_id': bsc_id,
            'bsc_name': bsc_name,
            'site_name': sites[site_id],
            'cell_name': parse_cell_parameter(cell_tag, 'name'),
            'bcc': parse_cell_parameter(cell_tag, 'bsIdentityCodeBCC'),
            'ncc': parse_cell_parameter(cell_tag, 'bsIdentityCodeNCC'),
            'lac': parse_cell_parameter(cell_tag, 'locationAreaIdLAC'),
            'cell_id': parse_cell_parameter(cell_tag, 'cellId'),
            'bcchNo': trxs[cell_id]['bcch'],
            'hsn': None,
            'maio': 0,
            'tch_freqs': ', '.join(trxs[cell_id]['tch']),
            'state': cell_state,
            'vendor': 'Nokia',
            'insert_date': Date.get_date('network_live'),
            'oss': 'Beeline Nokia',
        }
        gsm_cells.append(cell)
    return gsm_cells