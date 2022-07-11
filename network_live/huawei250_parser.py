"""Parse GSM/UMTS cells data from Huawei xml file shared by Beeline and Tele2."""

from defusedxml import ElementTree
from network_live.date import Date


def make_tag(tag_name):
    """
    Make tag with namespace.

    Args:
        tag_name: string

    Returns:
        string
    """
    namespace = '{http://www.huawei.com/specs/SOM}'
    return '{namespace}{tag_name}'.format(namespace=namespace, tag_name=tag_name)


def get_controller_name(root):
    """
    Get BSC/RNC name.

    Args:
        root: xml root object

    Returns:
        str
    """
    subsession = root.find(make_tag('subsession'))
    node = subsession.find(make_tag('NE'))
    return node.get('neid')


def parse_moi_parameters(root, attribute_type, needed_params):
    """
    Parse necessary parameters of moi tag related to necessary attribute type.

    Args:
        root: xml root object
        attribute_type: str
        needed_params: list of strs

    Returns:
        dict
    """
    moi_parameters = {}
    for moi_tag in root.iter(make_tag('moi')):
        if moi_tag.get('{http://www.w3.org/2001/XMLSchema-instance}type') != attribute_type:
            continue

        attributes = moi_tag.find(make_tag('attributes'))
        cell_id = attributes.find(make_tag('CELLID')).text
        moi_parameters[cell_id] = {}
        for parameter in needed_params:
            moi_parameters[cell_id][parameter] = attributes.find(make_tag(parameter)).text

    return moi_parameters


def parse_huawei_wcdma_cells(xml_path, operator):
    """
    Parse wcdma cells data.

    Args:
        xml_path: string
        operator: string

    Returns:
        list of dicts
    """
    if operator == 'Tele2':
        oss = operator
    elif operator == 'Beeline':
        oss = 'Beeline Huawei'

    root = ElementTree.parse(xml_path).getroot()
    rnc_name = get_controller_name(root)

    ucell_params = [
        'LOGICRNCID',
        'NODEBNAME',
        'CELLNAME',
        'MAXTXPOWER',
        'CELLID',
        'UARFCNDOWNLINK',
        'UARFCNUPLINK',
        'PSCRAMBCODE',
        'LAC',
        'RAC',
        'SAC',
        'ACTSTATUS',
    ]
    ucell_data = parse_moi_parameters(root, 'UCELL', ucell_params)
    cell_ids = ucell_data.keys()

    cpich_params = ['PCPICHPOWER']
    cpich_data = parse_moi_parameters(root, 'UPCPICH', cpich_params)

    wcdma_cells = []

    for cell_id in cell_ids:
        if ucell_data[cell_id]['ACTSTATUS'] == '1':
            cell_state = 'UNLOCKED'
        else:
            cell_state = 'LOCKED'
        cell = {
            'operator': operator,
            'oss': oss,
            'rnc_id': ucell_data[cell_id]['LOGICRNCID'],
            'rnc_name': rnc_name,
            'site_name': ucell_data[cell_id]['NODEBNAME'],
            'UtranCellId': ucell_data[cell_id]['CELLNAME'],
            'cId': cell_id,
            'localCellId': cell_id,
            'uarfcnDl': ucell_data[cell_id]['UARFCNDOWNLINK'],
            'uarfcnUl': ucell_data[cell_id]['UARFCNUPLINK'],
            'primaryScramblingCode': ucell_data[cell_id]['PSCRAMBCODE'],
            'LocationArea': ucell_data[cell_id]['LAC'],
            'RoutingArea': ucell_data[cell_id]['RAC'],
            'ServiceArea': ucell_data[cell_id]['SAC'],
            'Ura': None,
            'primaryCpichPower': cpich_data[cell_id]['PCPICHPOWER'],
            'maximumTransmissionPower': ucell_data[cell_id]['MAXTXPOWER'],
            'IubLink': None,
            'MocnCellProfile': None,
            'administrativeState': cell_state,
            'ip_address': None,
            'vendor': 'Huawei',
            'insert_date': Date.get_date('network_live'),
        }
        wcdma_cells.append(cell)

    return wcdma_cells


def parse_trx(root):
    """
    Parse TRx parameters for GSM cells.

    Args:
        root: xml root obj

    Returns:
        dict
    """
    trx_parameters = {}
    for trx_tag in root.iter(make_tag('moi')):
        if trx_tag.get('{http://www.w3.org/2001/XMLSchema-instance}type') != 'GTRX':
            continue

        attributes = trx_tag.find(make_tag('attributes'))
        cell_id = attributes.find(make_tag('CELLID')).text
        if cell_id not in trx_parameters:
            trx_parameters[cell_id] = {'tch_freqs': []}
        is_main_bcch = attributes.find(make_tag('ISMAINBCCH')).text
        freq = attributes.find(make_tag('FREQ')).text
        if is_main_bcch == '1':
            trx_parameters[cell_id]['bcchNo'] = freq
        else:
            trx_parameters[cell_id]['tch_freqs'].append(freq)
    return trx_parameters


def parse_site_names(root):
    """
    Parse GSM site names from Huawei xml file.

    Args:
        root: xml root object

    Returns:
        dict
    """
    bts_ids = parse_moi_parameters(root, 'CELLBIND2BTS', ['BTSID'])

    bts_data = {}
    for moi_tag in root.iter(make_tag('moi')):
        if moi_tag.get('{http://www.w3.org/2001/XMLSchema-instance}type') != 'BTS':
            continue
        attributes = moi_tag.find(make_tag('attributes'))
        bts_id = attributes.find(make_tag('BTSID')).text
        bts_name = attributes.find(make_tag('BTSNAME')).text
        bts_data[bts_id] = bts_name

    site_names = {}
    for cell_id in bts_ids.keys():
        bts_id = bts_ids[cell_id]['BTSID']
        site_names[cell_id] = bts_data[bts_id]

    return site_names


def parse_gsm_cells(xml_path, operator):
    """
    Parse GSM xml data from Huawei xml files.

    Args:
        xml_path: string
        operator: string

    Returns:
        list of dicts
    """
    root = ElementTree.parse(xml_path).getroot()
    bsc_name = get_controller_name(root)

    gcell_attrs = [
        'CELLNAME',
        'BCC',
        'NCC',
        'LAC',
        'CI',
        'ACTSTATUS',
    ]
    cell_attrs = parse_moi_parameters(root, 'GCELL', gcell_attrs)

    magrp_attrs = [
        'HSN',
    ]
    all_magrp_attrs = parse_moi_parameters(root, 'GCELLMAGRP', magrp_attrs)

    trx_parameters = parse_trx(root)
    site_names = parse_site_names(root)

    gsm_cells = []
    for cell_id in cell_attrs.keys():
        try:
            hsn = all_magrp_attrs[cell_id]['HSN']
        except KeyError:
            hsn = None
        if cell_attrs[cell_id]['ACTSTATUS'] == '1':
            cell_state = 'ACTIVE'
        else:
            cell_state = 'HALTED'
        cell = {
            'operator': operator,
            'oss': 'Tele2',
            'bsc_id': None,
            'bsc_name': bsc_name,
            'site_name': site_names[cell_id],
            'cell_name': cell_attrs[cell_id]['CELLNAME'],
            'bcc': cell_attrs[cell_id]['BCC'],
            'ncc': cell_attrs[cell_id]['NCC'],
            'lac': cell_attrs[cell_id]['LAC'],
            'cell_id': cell_attrs[cell_id]['CI'],
            'bcchNo': trx_parameters[cell_id]['bcchNo'],
            'hsn': hsn,
            'maio': None,
            'tch_freqs': ', '.join(trx_parameters[cell_id]['tch_freqs']),
            'state': cell_state,
            'vendor': 'Huawei',
            'insert_date': Date.get_date('network_live'),
        }
        gsm_cells.append(cell)
    return gsm_cells
