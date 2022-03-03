"""Parse Beeline Nokia WCDMA xml file for network live."""

import os

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
    namespace = '{raml20.xsd}'
    return '{namespace}{tag}'.format(namespace=namespace, tag=tag_name)


def parse_sites(root):
    """
    Parse site names from root tag object of Nokia xml file.

    Args:
        root: xml root object

    Returns:
        dict
    """
    sites = {}
    for site_tag in root.iter(make_tag('managedObject')):
        if site_tag.get('class') != 'WBTS':
            continue
        site_id = site_tag.get('distName').split('/')[-1]
        for site_parameter_tag in site_tag.iter(make_tag('p')):
            if site_parameter_tag.get('name') == 'name':
                site_name = site_parameter_tag.text
                sites[site_id] = site_name
                break
    return sites


def parse_cell_parameter(cell_tag, parameter_name):
    """
    Parse cell parameter value.

    Args:
        cell_tag: xml tag object
        parameter_name: strng

    Returns:
        string
    """
    for parameter_tag in cell_tag.iter(make_tag('p')):
        if parameter_tag.get('name') != parameter_name:
            continue
        return parameter_tag.text


def get_xml_path(logs_path):
    """
    Get WCDMA Nokia xml path.

    Args:
        logs_path: string

    Returns:
        string
    """
    for log in os.listdir(logs_path):
        if 'UMTS' in log:
            return '{logs_path}/{log}'.format(logs_path=logs_path, log=log)


def parse_nokia_wcdma_cells(logs_path):
    """
    Parse WCDMA cells from Nokia xml file.

    Args:
        logs_path: string

    Returns:
        list of dicts
    """
    root = ElementTree.parse(get_xml_path(logs_path)).getroot()
    sites = parse_sites(root)

    wcdma_cells = []
    for cell_tag in root.iter(make_tag('managedObject')):
        if cell_tag.get('class') != 'WCEL':
            continue
        nodes = cell_tag.get('distName').split('/')
        site_id = nodes[-2]
        rnc_name = nodes[-3]
        rnc_id = rnc_name.split('-')[-1]
        cell = {
            'operator': 'Beeline',
            'rnc_id': rnc_id,
            'rnc_name': rnc_name,
            'site_name': sites[site_id],
            'UtranCellId': parse_cell_parameter(cell_tag, 'name'),
            'localCellId': parse_cell_parameter(cell_tag, 'CId'),
            'uarfcnDl': parse_cell_parameter(cell_tag, 'UARFCN'),
            'primaryScramblingCode': parse_cell_parameter(cell_tag, 'PriScrCode'),
            'LocationArea': parse_cell_parameter(cell_tag, 'LAC'),
            'RoutingArea': parse_cell_parameter(cell_tag, 'RAC'),
            'ServiceArea': parse_cell_parameter(cell_tag, 'SAC'),
            'Ura': None,
            'primaryCpichPower': parse_cell_parameter(cell_tag, 'PtxPrimaryCPICH'),
            'maximumTransmissionPower': parse_cell_parameter(cell_tag, 'PtxCellMax'),
            'IubLink': None,
            'MocnCellProfile': None,
            'ip_address': None,
            'vendor': 'nokia',
            'insert_date': Date.get_date('network_live'),
        }
        wcdma_cells.append(cell)
    return wcdma_cells
