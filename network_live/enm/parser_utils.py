"""Present utilities for parsing necessary parameters from ENM data."""

import re


def parse_mo_value(fdn, mo_type):
    """
    Get MO value from FDN for related MO type.

    Args:
        fdn: string
        mo_type: string

    Returns:
        strings
    """
    mo_re_patterns = {
        'MeContext': 'MeContext=[^,]*',
        'SubNetwork': ',SubNetwork=[^,]*',
        'EUtranCellFDD': 'EUtranCellFDD=.*',
        'UtranCell': 'UtranCell=.*',
        'IubLink': 'IubLink=.*',
        'GeranCell': 'GeranCell=.*',
        'ChannelGroupCell': 'GeranCell=[^,]*',
        'NRSectorCarrier': 'NRSectorCarrier=.*',
        'NRCellDU': 'NRCellDU=.*',
    }
    mo_value_index = -1

    mo = re.search(mo_re_patterns[mo_type], fdn).group()
    return mo.split('=')[mo_value_index]


def get_ip(ip_string):
    """
    Isolate ip address from string.

    Args:
        ip_string: string

    Returns:
        string
    """
    ip_re_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    try:
        ip_address = re.search(ip_re_pattern, ip_string).group()
    except AttributeError:
        ip_address = None
    return ip_address


def parse_ips(enm_ip_data):
    """
    Parse ip addresses for nodes in enm data.

    Args:
        enm_ip_data: enmscripting ElementGroup

    Returns:
        dict
    """
    node_ips = {}
    for element in enm_ip_data:
        element_val = element.value()
        if 'FDN' in element_val and 'oam' in element_val.lower():
            name = parse_mo_value(element_val, 'MeContext')
            oam = True
        elif ' : ' in element_val and oam:
            node_ips[name] = get_ip(element_val)
            oam = False
    return node_ips


def parse_node_parameter(enm_node_data, node_type):
    """
    Parse parameter if in enm data for one node present one parameter.

    Args:
        enm_node_data: enmscripting ElementGroup
        node_type: string

    Returns:
        dict
    """
    attr_delimeter = ' : '
    attr_value_index = -1
    node_parameter = {}
    for element in enm_node_data:
        element_val = element.value()
        if 'FDN' in element_val:
            node_name = parse_mo_value(element_val, node_type)
        elif attr_delimeter in element_val:
            node_parameter[node_name] = element_val.split(attr_delimeter)[attr_value_index]

    return node_parameter
