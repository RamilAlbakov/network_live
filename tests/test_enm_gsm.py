"""Test enm gsm cells parser."""


from network_live.enm.gsm_parser import parse_gsm_cells
from tests.read_enm_data import read_enm_txt


def test_parse_gsm_cells():
    """Test enm gsm cells parser."""
    enm_gsmcells, enm_bsc, enm_sites, enm_channel_group = read_enm_txt(
        ['gsm_cells', 'bsc_id', 'gsm_sites', 'channel_group']
    )

    cell1, cell2 = parse_gsm_cells(enm_gsmcells, enm_bsc, enm_sites, enm_channel_group)

    assert cell1['bsc_name'] == 'AKTA_B1'
    assert cell1['bsc_id'] == '1'
    assert cell1['cell_name'] == 'RD4H553'
    assert cell1['bcc'] == '5'
    assert cell1['hsn'] == '54'
    assert cell2['bcchNo'] == '59'
    assert cell2['lac'] == '2123'
    assert cell2['cell_id'] == '20791'
    assert cell2['site_name'] == '51029DISTR4H55'
    assert cell2['tch_freqs'] == '[1, 43, 46]'
