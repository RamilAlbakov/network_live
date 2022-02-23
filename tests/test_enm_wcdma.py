"""Test enm wcdma cells parser."""


from network_live.enm.wcdma_parser import parse_wcdma_cells
from network_live.enm.parser_utils import parse_ips, parse_node_parameter


def test_parse_wcdma_cells():
    """Test enm wcdma cells parser."""
    with open('tests/enm_data/wcdma_cells.txt') as wcdma_cells_obj:
        enm_wcdma_cells = wcdma_cells_obj.read().split('\n')
    with open('tests/enm_data/rnc_id.txt') as rnc_id_obj:
        enm_rnc_ids = rnc_id_obj.read().split('\n')
    with open('tests/enm_data/site_names.txt') as site_names_obj:
        enm_site_names = site_names_obj.read().split('\n')
    with open('tests/enm_data/iublink.txt') as iublink_obj:
        enm_iublink_data = iublink_obj.read().split('\n')
    with open('tests/enm_data/bbu_ip.txt') as bbu_ip_obj:
        enm_bbu_ips = bbu_ip_obj.read().split('\n')
        node_ips = parse_ips(enm_bbu_ips)

    cell1, cell2 = parse_wcdma_cells(enm_wcdma_cells, enm_rnc_ids, enm_iublink_data, enm_site_names, node_ips)

    assert cell1['rnc_name'] == 'ASTA_RNC_4'
    assert cell1['UtranCellId'] == 'UKOBAT6'
    assert cell1['IubLink'] == 'Iub_11707KOKBATYGAY'
    assert cell2['rnc_id'] == '2123'
    assert cell2['ip_address'] == '10.207.64.52'
    assert cell2['Ura'] == '21230'
