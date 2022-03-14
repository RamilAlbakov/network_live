"""Test GSM parser of huawei 250+ cells."""

from network_live.huawei250_parser import parse_gsm_cells


def test_parse_gsm_cells():
    """Test GSM parser."""
    xml_path = 'tests/tele2_data/GNBI_Conf_Export_XML_RT_20220308.xml'
    gsm_cells = parse_gsm_cells(xml_path, 'Tele2')

    cell = list(filter(
        lambda gcell: gcell['cell_id'] == '962',
        gsm_cells,
    ))[0]

    assert cell['site_name'] == 'PE7237_F'
    assert cell['lac'] == '174'
    assert cell['cell_name'] == 'PKARAG2'
    assert cell['bcchNo'] == '56'
    assert cell['tch_freqs'] == '4'
    assert cell['hsn'] == '9'

