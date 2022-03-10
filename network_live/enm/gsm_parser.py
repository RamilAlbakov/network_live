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
        if 'FDN' in element:
            bsc_name = parse_mo_value(element, 'MeContext')
            if previous_bsc_name != bsc_name:
                sites[bsc_name] = {}
                previous_bsc_name = bsc_name
        elif 'rSite' in element:
            site_name = element.split(' : ')[-1]
        elif 'sector' in element:
            cell_name = element.split(' : ')[-1]
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
        if 'FDN' in element:
            bsc_name = parse_mo_value(element, 'MeContext')
            if previous_bsc_name != bsc_name:
                channel_data[bsc_name] = {}
                previous_bsc_name = bsc_name
            cell_name = parse_mo_value(element, 'ChannelGroupCell')
            channel_data[bsc_name][cell_name] = {}
        elif ' : ' in element:
            parameter_name, parameter_value = element.split(' : ')
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
        if 'FDN' in element:
            bsc_name = parse_mo_value(element, 'MeContext')
            cell_name = parse_mo_value(element, 'GeranCell')
            short_cell_name = cell_name[:-1]
            cell = {
                'operator': 'Kcell',
                'bsc_id': bsc_ids[bsc_name],
                'bsc_name': bsc_name,
                'site_name': sites[bsc_name][short_cell_name],
                'cell_name': cell_name,
                'tch_freqs': channel_data[bsc_name][cell_name]['dchNo'],
                'hsn': channel_data[bsc_name][cell_name]['hsn'],
                'maio': channel_data[bsc_name][cell_name]['maio'],
                'vendor': 'ericsson',
                'insert_date': Date.get_date('network_live'),
            }
        elif ' : ' in element:
            parameter_name, parameter_value = element.split(' : ')
            if parameter_name == 'cgi':
                cell['lac'] = parameter_value.split('-')[-2]
                cell['cell_id'] = parameter_value.split('-')[-1]
            else:
                cell[parameter_name] = parameter_value
        elif element == '' and cell:
            gsm_cells.append(cell)
            cell = {}
    return gsm_cells
