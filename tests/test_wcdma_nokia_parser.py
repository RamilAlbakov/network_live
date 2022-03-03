"""Test Beeline Nokia WCDMA cells parser."""

from network_live.beeline.wcdma_nokia_parser import parse_nokia_wcdma_cells


def test_parse_nokia_wcdma_cells():
    """Test Nokia WCDMA cells parser."""
    logs_path = 'tests/beeline_data/nokia_wcdma'
    wcdma_cells = parse_nokia_wcdma_cells(logs_path)
    cell = list(filter(
        lambda utrancell: utrancell['UtranCellId'] == 'U21_KOK_BD10731_kat-31',
        wcdma_cells,
    ))[0]

    assert cell['rnc_name'] == 'RNC-85'
    assert cell['site_name'] == 'KOK_Kat_U21GL821BK'
    assert cell['rnc_id'] == '85'
    assert cell['LocationArea'] == '164'
