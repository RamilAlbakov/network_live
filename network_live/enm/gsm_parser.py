"""Parse all necessary gsm cell data from enm data for network live db."""

from network_live.date import Date
from network_live.enm.parser_utils import parse_mo_value, parse_node_parameter


def parse_sites(enm_sites):
    """
    Parse site names for bsc and cell name.

    Args:
        enm_sites: list of dicts

    Returns:
        dict
    """
    sites = {}
    previous_bsc_name = ''
    for element in enm_sites:
        element_val = element.value()
        if 'FDN' in element_val:
            bsc_name = parse_mo_value(element_val, 'MeContext')
            if previous_bsc_name != bsc_name:
                sites[bsc_name] = {}
                previous_bsc_name = bsc_name
        elif 'rSite' in element_val:
            site_name = element_val.split(' : ')[-1]
        elif 'sector' in element_val:
            cell_name = element_val.split(' : ')[-1]
            sites[bsc_name][cell_name[:-1]] = site_name
    return sites


def parse_channel_group(enm_channel_group):
    """
    Parse hsn, maio, tch_freqs parameters from ChannelGroup mo.

    Args:
        enm_channel_group: list of strings

    Returns:
        dict
    """
    channel_data = {}
    previous_bsc_name = ''
    for element in enm_channel_group:
        element_val = element.value()
        if 'FDN' in element_val:
            bsc_name = parse_mo_value(element_val, 'MeContext')
            if previous_bsc_name != bsc_name:
                channel_data[bsc_name] = {}
                previous_bsc_name = bsc_name
            cell_name = parse_mo_value(element_val, 'ChannelGroupCell')
            channel_data[bsc_name][cell_name] = {}
        elif ' : ' in element_val:
            parameter_name, parameter_value = element_val.split(' : ')
            channel_data[bsc_name][cell_name][parameter_name] = parameter_value
    return channel_data


def parse_gsm_cells(enm_gsmcells, enm_bsc, enm_sites, enm_channel_group):
    """
    Parse gsm cell data for network live from enm data.

    Args:
        enm_gsmcells: list of strings
        enm_bsc: list of strings
        enm_sites: list of strings
        enm_channel_group: list of strings

    Returns:
        list of dicts
    """
    bsc_ids = parse_node_parameter(enm_bsc, 'MeContext')
    sites = parse_sites(enm_sites)
    channel_data = parse_channel_group(enm_channel_group)
    gsm_cells = []
    for element in enm_gsmcells:
        element_val = element.value()
        if 'error' in element_val.lower():
            return []
        elif 'FDN' in element_val:
            bsc_name = parse_mo_value(element_val, 'MeContext')
            cell_name = parse_mo_value(element_val, 'GeranCell')
            short_cell_name = cell_name[:-1]
            try:
                site_name = sites[bsc_name][short_cell_name]
            except KeyError:
                site_name = None
            cell = {
                'operator': 'Kcell',
                'oss': 'ENM',
                'bsc_id': bsc_ids[bsc_name],
                'bsc_name': bsc_name,
                'site_name': site_name,
                'cell_name': cell_name,
                'tch_freqs': channel_data[bsc_name][cell_name]['dchNo'],
                'hsn': channel_data[bsc_name][cell_name]['hsn'],
                'maio': channel_data[bsc_name][cell_name]['maio'],
                'vendor': 'Ericsson',
                'insert_date': Date.get_date('network_live'),
            }
        elif ' : ' in element_val:
            parameter_name, parameter_value = element_val.split(' : ')
            if parameter_name == 'cgi':
                cell['lac'] = parameter_value.split('-')[-2]
                cell['cell_id'] = parameter_value.split('-')[-1]
            else:
                cell[parameter_name] = parameter_value
                if parameter_name == 'state':
                    gsm_cells.append(cell)
    return gsm_cells
