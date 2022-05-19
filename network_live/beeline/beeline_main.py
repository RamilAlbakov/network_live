"""Update network live with cells shared by Beeline."""

import os

from network_live.beeline.huawei_parser import parse_lte_huawei
from network_live.beeline.lte_nokia_parser import parse_lte_nokia
from network_live.beeline.wcdma_nokia_parser import parse_nokia_wcdma_cells
from network_live.download_logs import download_bee250_huawei_xml, download_ftp_logs
from network_live.huawei250_parser import parse_huawei_wcdma_cells
from network_live.sql import update_network_live
from network_live.beeline.gsm_nokia_parser import parse_nokia_gsm_cells


def beeline_main(technology):
    """
    Update network live with Beeline cells.

    Args:
        technology: string

    Returns:
        string
    """
    logs_path = 'logs/beeline'

    if technology == 'LTE Huawei':
        download_ftp_logs('beeline_huawei')
        lte_cells = parse_lte_huawei(logs_path, 'moran')
        download_ftp_logs('beeline_huawei_mocn')
        lte_cells += parse_lte_huawei(logs_path, 'mocn')
        return update_network_live(lte_cells, 'Beeline Huawei', 'LTE')
    elif technology == 'LTE Nokia':
        download_ftp_logs('beeline_nokia_moran')
        lte_cells = parse_lte_nokia(logs_path)
        download_ftp_logs('beeline_nokia_mocn')
        lte_cells += parse_lte_nokia(logs_path)
        return update_network_live(lte_cells, 'Beeline Nokia', 'LTE')
    elif technology == 'WCDMA Nokia':
        download_ftp_logs('beeline_nokia_250', is_unzip=False)
        nokia_wcdma_cells = parse_nokia_wcdma_cells(logs_path)
        download_ftp_logs('beeline_nokia_wcdma')
        nokia_wcdma_cells += parse_nokia_wcdma_cells(logs_path)
        return update_network_live(nokia_wcdma_cells, 'Beeline Nokia', 'WCDMA')
    elif technology == 'GSM Nokia':
        nokia_gsm_cells = parse_nokia_gsm_cells(logs_path)
        return update_network_live(nokia_gsm_cells, 'Beeline Nokia', 'GSM')
    elif technology == 'WCDMA Huawei':
        download_bee250_huawei_xml(logs_path)
        log_name = os.listdir(logs_path)[0]
        xml_path = '{logs_path}/{log}'.format(logs_path=logs_path, log=log_name)
        huawei_wcdma_cells = parse_huawei_wcdma_cells(xml_path, 'Beeline')
        return update_network_live(huawei_wcdma_cells, 'Beeline Huawei', 'WCDMA')
