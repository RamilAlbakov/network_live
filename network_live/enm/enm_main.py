"""Update network live with ENM cells."""


from network_live.enm.enm import Enm
from network_live.enm.lte_parser import parse_lte_cells
from network_live.enm.parser_utils import parse_ips, parse_node_parameter
from network_live.enm.wcdma_parser import parse_wcdma_cells
from network_live.sql import Sql


def enm_main(technology, truncate=False):
    """
    Update network live with ENM cells.

    Args:
        technology: string
        truncate: bool

    Returns:
        list of dicts
    """
    enm_lte_cells = Enm.execute_enm_command('lte_cells')

    enm_enodeb_ids = Enm.execute_enm_command('enodeb_id')
    enodeb_ids = parse_node_parameter(enm_enodeb_ids, 'MeContext')

    enm_node_ips = Enm.execute_enm_command('dus_ip') + Enm.execute_enm_command('bbu_ip')
    node_ips = parse_ips(enm_node_ips)

    enm_wcdma_cells = Enm.execute_enm_command('wcdma_cells')
    enm_rnc_ids = Enm.execute_enm_command('rnc_ids')
    enm_site_names = Enm.execute_enm_command('site_names')
    enm_iublink_data = Enm.execute_enm_command('iublink')

    if technology == 'LTE':
        lte_cells = parse_lte_cells(enm_lte_cells, enodeb_ids, node_ips)
        return Sql.insert(lte_cells, 'ENM', technology, truncate)
    elif technology == 'WCDMA':
        wcdma_cells = parse_wcdma_cells(
            enm_wcdma_cells,
            enm_rnc_ids,
            enm_iublink_data,
            enm_site_names,
            node_ips,
        )
        return Sql.insert(wcdma_cells, 'ENM', technology, truncate)
