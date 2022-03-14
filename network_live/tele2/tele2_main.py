"""Update network live with cells shared by Tele2."""

import os

from network_live.download_logs import download_ftp_logs
from network_live.huawei250_parser import parse_huawei_wcdma_cells, parse_gsm_cells
from network_live.sql import Sql
from network_live.tele2.parser import parse_lte


def tele2_main(technology):
    """
    Update network live with Tele2 cells.

    Args:
        technology: string

    Returns:
        string
    """
    logs_path = 'logs/tele2'
    if technology == 'LTE':
        download_ftp_logs('tele2_lte')
        lte_log_path = '{logs_path}/tele2_lte_log.csv'.format(logs_path=logs_path)
        lte_cells = parse_lte(lte_log_path)
        return Sql.insert(lte_cells, 'Tele2', technology)
    elif technology == 'WCDMA':
        download_ftp_logs('tele2_wcdma')
        log_name = os.listdir(logs_path)[0]
        wcdma_log_path = '{logs_path}/{log}'.format(
            logs_path=logs_path,
            log=log_name,
        )
        wcdma_cells = parse_huawei_wcdma_cells(wcdma_log_path, 'Tele2')
        return Sql.insert(wcdma_cells, 'Tele2', technology)
    elif technology == 'GSM':
        download_ftp_logs('tele2_gsm')
        log_name = os.listdir(logs_path)[0]
        gsm_log_path = '{logs_path}/{log}'.format(
            logs_path=logs_path,
            log=log_name,
        )
        gsm_cells = parse_gsm_cells(gsm_log_path, 'Tele2')
        return Sql.insert(gsm_cells, 'Tele2', technology)
