"""Test enm lte cells parser."""


from network_live.enm.lte_parser import parse_lte_cells
from network_live.enm.parser_utils import parse_ips, parse_node_parameter
from tests.read_enm_data import read_enm_txt


def test_parse_lte_cells():
    """Test enm lte cells parser."""
    enm_lte_cells, enm_enodeb_ids, enm_bbu_ips = read_enm_txt(
        ['lte_cells', 'enodeb_id', 'bbu_ip']
    )
    enodeb_ids = parse_node_parameter(enm_enodeb_ids, 'MeContext')
    node_ips = parse_ips(enm_bbu_ips)

    cell1, cell2, cell3 = parse_lte_cells(enm_lte_cells, enodeb_ids, node_ips)

    assert cell1['subnetwork'] == 'LTE_Shymkent'
    assert cell1['site_name'] == 'ERBS_41428_KAINARFARM_K'
    assert cell2['earfcndl'] == '6200'
    assert cell2['qRxLevMin'] == '-124'
    assert cell3['enodeb_id'] == '500074'
    assert cell3['ip_address'] == '10.198.39.201'
