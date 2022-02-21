"""Parse Beeline Huawei xml files for network live."""

import os

from defusedxml import ElementTree
from network_live.date import Date


def make_tag(tag):
    """
    Make tag name with namespace.

    Args:
        tag: string

    Returns:
        string
    """
    namespace = '{http://www.huawei.com/specs/bsc6000_nrm_forSyn_collapse_1.0.0}'
    return '{namespace}{tag}'.format(namespace=namespace, tag=tag)


def parse_tag_text(tag, parent):
    """
    Parse tags text content.

    Args:
        tag: string
        parent: string

    Returns:
        string
    """
    attributes = parent.find(make_tag('attributes'))
    return attributes.find(make_tag(tag)).text


def parse_qrxlevmin(root):
    """
    Parse qrxlevmin for all cells.

    Args:
        root: root object

    Returns:
        dict
    """
    qrxlevmin_data = {}
    for element in root.iter(make_tag('CellSel')):
        cell_id = parse_tag_text('LocalCellId', element)
        qrxlevmin = parse_tag_text('QRxLevMin', element)
        qrxlevmin_data[cell_id] = int(qrxlevmin) * 2
    return qrxlevmin_data


def parse_tac(root):
    """
    Parse Kcell tac.

    Args:
        root: root object

    Returns:
        string
    """
    for element in root.iter(make_tag('CnOperatorTa')):
        tracking_area_id = parse_tag_text('TrackingAreaId', element)
        if tracking_area_id == '1':
            return parse_tag_text('Tac', element)


def parse_ip(root):
    """
    Parse S1 Kcell ip address.

    Args:
        root: root object

    Returns:
        string
    """
    for element in root.iter(make_tag('DEVIP')):
        user_label = parse_tag_text('USERLABEL', element)
        if user_label == 'S1 Kcell':
            return parse_tag_text('IP', element)


def parse_enodeb_id(root):
    """
    Parse enodeb id.

    Args:
        root: root object

    Returns:
        string
    """
    for element in root.iter(make_tag('eNodeBFunction')):
        enodeb_id = parse_tag_text('eNodeBId', element)
    return enodeb_id


def parse_site_name(root):
    """
    Parse site name.

    Args:
        root: root object

    Returns:
        string
    """
    for element in root.iter(make_tag('NE')):
        site_name = parse_tag_text('NENAME', element)
    return site_name


def parse_huawei_xml(xml_path):
    """
    Parse xml file.

    Args:
        xml_path: string

    Returns:
        dict
    """
    eci_factor = 256
    min_kcell_cell_id = 100
    max_kcell_cell_id = 130
    root = ElementTree.parse(xml_path).getroot()

    qrxlevmin_data = parse_qrxlevmin(root)
    enodeb_id = parse_enodeb_id(root)
    eutrancells = []

    for element in root.iter(make_tag('Cell')):
        cell = {
            'subnetwork': 'Beeline',
            'vendor': 'huawei',
            'latitude': None,
            'longitude': None,
            'insert_date': Date.get_date('network_live'),
        }
        cell_id = parse_tag_text('LocalCellId', element)

        if int(cell_id) in list(range(min_kcell_cell_id, max_kcell_cell_id)):
            cell['cell_name'] = parse_tag_text('CellName', element)
            cell['cellId'] = cell_id
            cell['earfcndl'] = parse_tag_text('DlEarfcn', element)
            cell['administrativeState'] = parse_tag_text('CellActiveState', element)
            cell['rachRootSequence'] = parse_tag_text('RootSequenceIdx', element)
            cell['physicalLayerCellIdGroup'] = parse_tag_text('PhyCellId', element)
            cell['qRxLevMin'] = qrxlevmin_data[cell_id]
            cell['tac'] = parse_tac(root)
            cell['ip_address'] = parse_ip(root)
            cell['enodeb_id'] = enodeb_id
            cell['site_name'] = parse_site_name(root)
            cell['eci'] = int(enodeb_id) * eci_factor + int(cell_id)

            eutrancells.append(cell)

    return eutrancells


def parse_lte_huawei(logs_path):
    """
    Parse Beeline Huawei xml logs.

    Args:
        logs_path: string

    Returns:
        list of dicts
    """
    cell_data = []
    for log in os.listdir(logs_path):
        xml_path = '{logs_path}/{log}'.format(logs_path=logs_path, log=log)
        cell_data += parse_huawei_xml(xml_path)

    return cell_data
