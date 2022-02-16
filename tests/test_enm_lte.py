"""Test enm lte cells parser."""


from datetime import datetime
from network_live.enm.lte_parser import parse_lte_cells
from parser_utils import parse_ips


def test_parse_lte_cells():
    """Test enm lte cells parser."""
    with open('tests/enm_data/lte_cells.txt') as lte_cells_obj:
        enm_lte_cells = lte_cells_obj.read().split('\n')
    with open('tests/enm_data/enodeb_id.txt') as enodeb_id_obj:
        enm_enodeb_ids = enodeb_id_obj.read().split('\n')
    with open('tests/enm_data/bbu_ip.txt') as bbu_ip_obj:
        enm_bbu_ips = bbu_ip_obj.read().split('\n')
        node_ips = parse_ips(enm_bbu_ips)

    date_format = '%{d}%m%y'.format(d='d')
    date = datetime.now().strftime(date_format)

    cell1, cell2, cell3 = parse_lte_cells(enm_lte_cells, enm_enodeb_ids, node_ips, date)

    assert cell1['subnetwork'] == 'LTE_Shymkent'
    assert cell1['site_name'] == 'ERBS_41428_KAINARFARM_K'
    assert cell2['earfcndl'] == '6200'
    assert cell2['qRxLevMin'] == '-124'
    assert cell3['enodeb_id'] == '500074'
    assert cell3['ip_address'] == '10.198.39.201'
