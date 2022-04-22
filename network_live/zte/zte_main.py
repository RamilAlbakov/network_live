"""Update network live with ZTE cells."""

from network_live.sql import Sql, update_network_live
from network_live.zte.parser import parse_gsm_cells, parse_wcdma_cells
from network_live.zte.select_data import select_zte_data


def zte_main(technology):
    """
    Update network live with ZTE cells.

    Args:
        technology: string

    Returns:
        string
    """
    oss = 'ZTE'
    if technology == 'WCDMA':
        zte_rnc_data = select_zte_data('rnc')
        zte_wcdma_cell_data = select_zte_data('wcdma_cell')
        wcdma_cells = parse_wcdma_cells(zte_wcdma_cell_data, zte_rnc_data)
        return update_network_live(wcdma_cells, oss, technology)
    elif technology == 'GSM':
        zte_gsm_data = select_zte_data('gsm_cell')
        gsm_cells = parse_gsm_cells(zte_gsm_data)
        return update_network_live(gsm_cells, oss, technology)
    return '{tech} {oss} Fail'.format(tech=technology, oss=oss)