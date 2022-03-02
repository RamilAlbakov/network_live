"""Update network live with OSS cells."""


from network_live.download_logs import download_oss_logs
from network_live.oss.oss_ssh import run_bcgtool
from network_live.oss.wcdma_parser import parse_wcdma_cells
from network_live.sql import Sql


def oss_main(technology):
    """
    Update network live with OSS cells.

    Args:
        technology: string

    Returns:
        string
    """
    if technology == 'WCDMA':
        bcg_result = run_bcgtool()
        if 'Export has succeeded' in bcg_result:
            download_oss_logs(technology)
            logs_path = 'logs/oss/oss_utrancells.xml'
            wcdma_cells = parse_wcdma_cells(logs_path)
            return Sql.insert(wcdma_cells, 'OSS', technology)

    return '{technology} OSS Fail'.format(technology=technology)
