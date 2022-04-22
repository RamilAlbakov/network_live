"""Update network live with ENM cells."""

from network_live.enm.enm import Enm
from network_live.enm.gsm_parser import parse_gsm_cells
from network_live.enm.lte_parser import parse_lte_cells
from network_live.enm.nr_parser import parse_nr_cells
from network_live.enm.parser_utils import parse_ips, parse_node_parameter
from network_live.enm.wcdma_parser import parse_wcdma_cells
from network_live.sql import update_network_live


def enm_main(technology):
    """
    Update network live with ENM cells.

    Args:
        technology: string

    Returns:
        string
    """
    oss = 'ENM'
    if technology in {'LTE', 'WCDMA', 'NR'}:
        enm_node_ips = Enm.execute_enm_command('dus_ip') + Enm.execute_enm_command('bbu_ip')
        node_ips = parse_ips(enm_node_ips)

    if technology == 'LTE':
        enm_lte_cells = Enm.execute_enm_command('lte_cells')
        enm_enodeb_ids = Enm.execute_enm_command('enodeb_id')
        enodeb_ids = parse_node_parameter(enm_enodeb_ids, 'MeContext')
        lte_cells = parse_lte_cells(enm_lte_cells, enodeb_ids, node_ips)
        if lte_cells:
            return update_network_live(lte_cells, oss, technology)
    elif technology == 'WCDMA':
        enm_wcdma_cells = Enm.execute_enm_command('wcdma_cells')
        enm_rnc_ids = Enm.execute_enm_command('rnc_ids')
        enm_site_names = Enm.execute_enm_command('site_names')
        enm_iublink_data = Enm.execute_enm_command('iublink')
        wcdma_cells = parse_wcdma_cells(
            enm_wcdma_cells,
            enm_rnc_ids,
            enm_iublink_data,
            enm_site_names,
            node_ips,
        )
        if wcdma_cells:
            return update_network_live(wcdma_cells, oss, technology)
    elif technology == 'GSM':
        enm_bsc = Enm.execute_enm_command('bsc_id')
        enm_sites = Enm.execute_enm_command('gsm_sites')
        enm_gsmcells = Enm.execute_enm_command('gsm_cells')
        enm_channel_group = Enm.execute_enm_command('channel_group')
        gsm_cells = parse_gsm_cells(enm_gsmcells, enm_bsc, enm_sites, enm_channel_group)
        if gsm_cells:
            return update_network_live(gsm_cells, oss, technology)
    elif technology == 'NR':
        enm_nr_cells = Enm.execute_enm_command('nrcells')
        enm_nr_sectors = Enm.execute_enm_command('nr_sector_carrier')
        enm_nr_ids = Enm.execute_enm_command('gnbid')
        nr_ids = parse_node_parameter(enm_nr_ids, 'MeContext')
        nr_cells = parse_nr_cells(enm_nr_cells, enm_nr_sectors, nr_ids, node_ips)
        if nr_cells:
            return update_network_live(nr_cells, oss, technology)
    return '{tech} {oss} Fail'.format(tech=technology, oss=oss)
