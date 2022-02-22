"""Update network live with ENM cells."""


from network_live.enm.enm import Enm
from network_live.enm.lte_parser import parse_lte_cells
from network_live.enm.parser_utils import parse_ips, parse_node_parameter
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

    if technology == 'LTE':
        lte_cells = parse_lte_cells(enm_lte_cells, enodeb_ids, node_ips)
        return Sql.insert(lte_cells, 'ENM', technology, truncate)
