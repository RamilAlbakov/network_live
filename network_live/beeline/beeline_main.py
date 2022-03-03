"""Update network live with cells shared by Beeline."""


from network_live.beeline.huawei_parser import parse_lte_huawei
from network_live.beeline.lte_nokia_parser import parse_lte_nokia
from network_live.download_logs import download_ftp_logs
from network_live.sql import Sql


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
        lte_cells = parse_lte_huawei(logs_path)
        return Sql.insert(lte_cells, 'Beeline Huawei', 'LTE')
    elif technology == 'LTE Nokia':
        download_ftp_logs('beeline_nokia_moran')
        lte_cells = parse_lte_nokia(logs_path)
        download_ftp_logs('beeline_nokia_mocn')
        lte_cells += parse_lte_nokia(logs_path)
        return Sql.insert(lte_cells, 'Beeline Nokia', 'LTE')
