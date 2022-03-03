"""Test Tele2 GSM/UMTS parser."""

from network_live.tele2.gu_parser import parse_wcdma_cells


def test_parse_wcdma_cells():
    """Test Tele2 WCDMA cells parser."""
    xml_path = 'tests/tele2_data/UNBI_Conf_Export_XML_RT_20220301.xml'
    wcdma_cells = parse_wcdma_cells(xml_path)

    cell = list(filter(
        lambda utrancell: utrancell['localCellId'] == '20095',
        wcdma_cells,
    ))[0]

    assert cell['rnc_name'] == 'RALMA06'
    assert cell['UtranCellId'] == 'UK7381B0U-0'
    assert cell['primaryCpichPower'] == '330'
    assert cell['LocationArea'] == '32326'
