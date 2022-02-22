"""Test Beeline Nokia files parser."""

from network_live.beeline.lte_nokia_parser import parse_nokia_xml


def test_nokia_parser():
    """Test Nokia parser."""
    log_path = 'tests/beeline_data/nokia_lte/KAR_Factor_nL818GU21BK.xml'
    cell1, cell2, cell3 = parse_nokia_xml(log_path)

    assert cell1['enodeb_id'] == '30329'
    assert cell1['site_name'] == 'KAR_Factor_nL818GU21BK'
    assert cell2['tac'] == '13214'
    assert cell2['qRxLevMin'] == '-116'
    assert cell3['earfcndl'] == '6200'
