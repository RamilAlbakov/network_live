"""Update network live with ZTE cells."""

from network_live.sql import Sql
from network_live.zte.parser import parse_wcdma_cells
from network_live.zte.select_data import select_zte_data


def zte_main(technology):
    """
    Update network live with ZTE cells.

    Args:
        technology: string

    Returns:
        string
    """
    if technology == 'WCDMA':
        zte_rnc_data = select_zte_data('rnc')
        zte_wcdma_cell_data = select_zte_data('wcdma_cell')
        wcdma_cells = parse_wcdma_cells(zte_wcdma_cell_data, zte_rnc_data)
        return Sql.insert(wcdma_cells, 'ZTE', technology)
