"""Update network live with cells shared by Tele2."""

from network_live.download_logs import download_lte_logs
from network_live.sql import Sql
from network_live.tele2.parser import parse_lte


def tele2_main(technology, date):
    """
    Update network live with Tele2 cells.

    Returns:
        string
    """
    if technology == 'LTE':
        download_lte_logs('tele2')
        lte_log_path = 'logs/tele2/tele2_lte_log.csv'
        lte_cells = parse_lte(lte_log_path, date)
        return Sql.insert(lte_cells, 'Tele2', 'LTE')
