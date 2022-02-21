"""Update network live with cells shared by Beeline."""


from network_live.beeline.huawei_parser import parse_lte_huawei
from network_live.download_logs import download_lte_logs
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
        download_lte_logs('beeline_huawei')
        lte_cells = parse_lte_huawei(logs_path)
        return Sql.insert(lte_cells, 'Beeline Huawei', 'LTE')
