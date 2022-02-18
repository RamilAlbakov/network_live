"""Test Tele2 LTE parser."""


from network_live.tele2.parser import parse_lte


def test_parse_lte():
    """Test Tele2 LTE parser."""
    log_path = 'tests/tele2_data/tele2_lte_log.csv'
    cell1, cell2, cell3, cell4 = parse_lte(log_path)

    assert cell1['site_name'] == 'SE5070'
    assert cell1['cell_name'] == 'A-SE5070Z2L-0'
    assert cell2['tac'] == '10024'
    assert cell2['cellId'] == '1'
    assert cell3['physicalLayerCellIdGroup'] == '28'
    assert cell3['longitude'] == None
    assert cell4['eci'] == None
    assert cell4['rachRootSequence'] == 300
