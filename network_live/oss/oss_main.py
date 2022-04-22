"""Update network live with OSS cells."""


from network_live.download_logs import download_oss_logs
from network_live.enm.enm import Enm
from network_live.enm.parser_utils import parse_ips, parse_node_parameter
from network_live.oss.gsm_parser import parse_gsm_cells
from network_live.oss.oss_ssh import collect_oss_logs
from network_live.oss.wcdma_parser import parse_wcdma_cells
from network_live.sql import update_network_live


def oss_main(technology):
    """
    Update network live with OSS cells.

    Args:
        technology: string

    Returns:
        string
    """
    oss = 'OSS'
    if technology == 'WCDMA':
        enm_sites_data = Enm.execute_enm_command('site_names')
        enm_sites = parse_node_parameter(enm_sites_data, 'MeContext')

        enm_node_ips = Enm.execute_enm_command('dus_ip') + Enm.execute_enm_command('bbu_ip')
        enm_ips = parse_ips(enm_node_ips)

        bcg_result = collect_oss_logs('WCDMA')
        if 'Export has succeeded' in bcg_result:
            download_oss_logs(technology)
            logs_path = 'logs/oss/oss_utrancells.xml'
            wcdma_cells = parse_wcdma_cells(logs_path, enm_sites, enm_ips)
            return update_network_live(wcdma_cells, oss, technology)
    elif technology == 'GSM':
        cna_result = collect_oss_logs(technology)
        if '100%' in cna_result:
            download_oss_logs(technology)
            logs_path = 'logs/oss/network_live_gsm_export.txt'
            gsm_cells = parse_gsm_cells(logs_path)
            return update_network_live(gsm_cells, oss, technology)

    return '{technology} {oss} Fail'.format(technology=technology, oss=oss)
