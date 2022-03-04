"""Parse GSM/UMTS cells data from Tele2 xml file."""

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
    root = ElementTree.parse(xml_path).getroot()
    rnc_name = get_controller_name(root)

    ucell_params = [
        'LOGICRNCID',
        'NODEBNAME',
        'CELLNAME',
        'MAXTXPOWER',
        'CELLID',
        'UARFCNDOWNLINK',
        'PSCRAMBCODE',
        'LAC',
        'RAC',
        'SAC',
    ]
    ucell_data = parse_moi_parameters(root, 'UCELL', ucell_params)
    cell_ids = ucell_data.keys()

    cpich_params = ['PCPICHPOWER']
    cpich_data = parse_moi_parameters(root, 'UPCPICH', cpich_params)

    wcdma_cells = []

    for cell_id in cell_ids:
        cell = {
            'operator': operator,
            'rnc_id': ucell_data[cell_id]['LOGICRNCID'],
            'rnc_name': rnc_name,
            'site_name': ucell_data[cell_id]['NODEBNAME'],
            'UtranCellId': ucell_data[cell_id]['CELLNAME'],
            'localCellId': cell_id,
            'uarfcnDl': ucell_data[cell_id]['UARFCNDOWNLINK'],
            'primaryScramblingCode': ucell_data[cell_id]['PSCRAMBCODE'],
            'LocationArea': ucell_data[cell_id]['LAC'],
            'RoutingArea': ucell_data[cell_id]['RAC'],
            'ServiceArea': ucell_data[cell_id]['SAC'],
            'Ura': None,
            'primaryCpichPower': cpich_data[cell_id]['PCPICHPOWER'],
            'maximumTransmissionPower': ucell_data[cell_id]['MAXTXPOWER'],
            'IubLink': None,
            'MocnCellProfile': None,
            'ip_address': None,
            'vendor': 'huawei',
            'insert_date': Date.get_date('network_live'),
        }
        wcdma_cells.append(cell)

    return wcdma_cells
