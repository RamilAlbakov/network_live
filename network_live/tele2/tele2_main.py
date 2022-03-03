"""Update network live with cells shared by Tele2."""

from network_live.download_logs import download_ftp_logs
from network_live.sql import Sql
from network_live.tele2.gu_parser import parse_wcdma_cells
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
        wcdma_log_path = '{logs_path}/UNBI_Conf_Export_XML_RT_20220301.xml'.format(
            logs_path=logs_path,
        )
        wcdma_cells = parse_wcdma_cells(wcdma_log_path)
        return Sql.insert(wcdma_cells, 'Tele2', technology)
