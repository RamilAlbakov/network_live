"""Test OSS WCDMA parser."""


from network_live.oss.wcdma_parser import parse_rbs_data, parse_iublink_data, parse_wcdma_cells
from defusedxml import ElementTree


xml_path = 'tests/oss_data/oss_utrancells.xml'
root = ElementTree.parse(xml_path).getroot()


def test_parse_rbs_data():
    """Test oss parse_wcdma_sites function."""
    sites = parse_rbs_data(root)

    assert sites['41001']['site_name'] == '41001BCUKGU'
    assert sites['42523']['ip_address'] == '10.13.203.173/27'
    assert sites['41005']['ip_address'] == '10.206.98.15'
    assert sites['41006']['site_name'] == '41006USHYMADAL'


def test_parse_iublink_data():
    """Test oss parse_rbs_ids function."""
    rbs_ids = parse_iublink_data(root)

    assert rbs_ids['Iub_41001'] == '41001'
    assert rbs_ids['Iub_41014SHDOSTYK_EB014'] == '41014'
    assert rbs_ids['Iub_41006USHYMADAL_EB006'] == '41006'

def test_parse_wcdma_cells():
    """Test oss parse_wcdma_cells function."""
    wcdma_cells = parse_wcdma_cells(xml_path)

    cell = list(filter(
        lambda utrancell: utrancell['UtranCellId'] == '2UKGU2',
        wcdma_cells,
    ))[0]

    assert cell['rnc_id'] == '1401'
    assert cell['site_name'] == '41001BCUKGU'
    assert cell['uarfcnDl'] == '10562'
    assert cell['LocationArea'] == '13251'
    assert cell['MocnCellProfile'] == None
