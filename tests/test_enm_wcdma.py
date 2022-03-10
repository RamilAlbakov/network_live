"""Test enm wcdma cells parser."""


from network_live.enm.wcdma_parser import parse_wcdma_cells
from network_live.enm.parser_utils import parse_ips, parse_node_parameter
from tests.read_enm_data import read_enm_txt


def test_parse_wcdma_cells():
    """Test enm wcdma cells parser."""
    enm_wcdma_cells, enm_rnc_ids, enm_site_names, enm_iublink_data, enm_bbu_ips = read_enm_txt(
        ['wcdma_cells', 'rnc_id', 'site_names', 'iublink', 'bbu_ip']
    )
    node_ips = parse_ips(enm_bbu_ips)

    cell1, cell2 = parse_wcdma_cells(
        enm_wcdma_cells,
        enm_rnc_ids,
        enm_iublink_data,
        enm_site_names,
        node_ips
    )

    assert cell1['rnc_name'] == 'ASTA_RNC_4'
    assert cell1['UtranCellId'] == 'UKOBAT6'
    assert cell1['IubLink'] == 'Iub_11707KOKBATYGAY'
    assert cell2['rnc_id'] == '2123'
    assert cell2['ip_address'] == '10.207.64.52'
    assert cell2['Ura'] == '21230'
