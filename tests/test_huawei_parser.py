"""Test Beeline Huawei LTE xml parser."""


from network_live.beeline.huawei_parser import parse_huawei_xml


def test_parse_huawei_xml():
    """Test Huawei LTE xml file parser."""
    xml_path = 'tests/beeline_data/huawei/16012022_OSK_Tekstil_U21L81821BK.XML'
    cell1, cell2, cell3 = parse_huawei_xml(xml_path, 'moran')

    cell_names = (cell1['cell_name'], cell2['cell_name'], cell3['cell_name'])

    assert cell1['site_name'] == 'OSK_Tekstil_U21L81821BK'
    assert cell2['enodeb_id'] == '20259'
    assert '3520259-104' in cell_names
    assert cell3['tac'] == '243'
    assert len(cell1.keys()) == 17
