"""Parse all necessary wcdma cell data from enm data for network live db."""

from network_live.date import Date
from network_live.enm.parser_utils import parse_mo_value, parse_node_parameter
from network_live.physical_data import add_physical_params


def parse_site_names(enm_site_names, enm_iublink_data):
    """
    Parse umts site names using iublink and rbs_ids from ENM.

    Args:
        enm_site_names: enmscripting ElementGroup
        enm_iublink_data: enmscripting ElementGroup

    Returns:
        dict
    """
    rbs_ids = parse_node_parameter(enm_site_names, 'MeContext')
    reversed_rbs_ids = {rbsid: site_name for site_name, rbsid in rbs_ids.items()}
    iublink_data = parse_node_parameter(enm_iublink_data, 'IubLink')

    site_names = {}
    for iublink, rbsid in iublink_data.items():
        try:
            site_names[iublink] = reversed_rbs_ids[rbsid]
        except KeyError:
            site_names[iublink] = rbsid
    return site_names


def parse_parameter(parameter_string):
    """
    Parse parameter_name and parameter_value from string.

    Args:
        parameter_string: string

    Returns:
        tuple
    """
    attr_name, attr_value = parameter_string.split(' : ')
    if attr_name.endswith('Ref'):
        name_and_value = attr_value.split(',')[-1]
        try:
            parameter_name, parameter_value = name_and_value.split('=')
        except ValueError:
            parameter_name = attr_name[:-3]
            parameter_value = None
        if parameter_name == 'Ura':
            return (parameter_name, parameter_value[:-1])
        return (parameter_name, parameter_value)

    return (attr_name, attr_value)


def parse_wcdma_cells(enm_wcdma_cells, enm_rnc_ids, enm_iublink_data, enm_site_names, node_ips, atoll_data):
    """
    Parse utrancell parameters from enm data.

    Args:
        enm_wcdma_cells: enmscripting ElementGroup
        enm_rnc_ids: enmscripting ElementGroup
        enm_iublink_data: enmscripting ElementGroup
        enm_site_names: enmscripting ElementGroup
        node_ips: dict
        atoll_data: dict

    Returns:
        list of dicts
    """
    site_names = parse_site_names(enm_site_names, enm_iublink_data)
    rnc_ids = parse_node_parameter(enm_rnc_ids, 'MeContext')

    attr_delimeter = ' : '
    wcdma_cells = []
    for element in enm_wcdma_cells:
        element_val = element.value()
        if 'error' in element_val.lower():
            return []
        elif 'FDN' in element_val:
            cell = {
                'operator': 'Kcell',
                'oss': 'ENM',
                'rnc_name': parse_mo_value(element_val, 'MeContext'),
                'cell_name': parse_mo_value(element_val, 'UtranCell'),
                'vendor': 'Ericsson',
                'insert_date': Date.get_date('network_live'),
            }
        elif attr_delimeter in element_val:
            parameter_name, parameter_value = parse_parameter(element_val)
            cell[parameter_name] = parameter_value
            if parameter_name == 'Ura':
                cell['site_name'] = site_names[cell['IubLink']]
                cell['rnc_id'] = rnc_ids[cell['rnc_name']]
                try:
                    cell['ip_address'] = node_ips[cell['site_name']]
                except KeyError:
                    cell['ip_address'] = None
                wcdma_cells.append(
                    add_physical_params(atoll_data, cell),
                )
    return wcdma_cells
