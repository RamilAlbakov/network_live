"""Parse ZTE cell data."""

from network_live.date import Date
from network_live.physical_data import add_physical_params


def parse_wcdma_cells(zte_cell_data, zte_rnc_data, atoll_data):
    """
    Parse ZTE cell data.

    Args:
        zte_cell_data: list of tuples
        zte_rnc_data: list of tuples
        atoll_data: dict

    Returns:
        list of dicts
    """
    rnc_names = {rnc_id: rnc_name for rnc_name, rnc_id in zte_rnc_data}

    wcdma_cells = []

    for cell_params in zte_cell_data:
        (
            rnc_id,
            nodeb_name,
            cell_name,
            cell_id,
            local_cell_id,
            uarfcndl,
            uarfcnul,
            psc,
            lac,
            rac,
            sac,
            uralist,
            primary_cpich_power,
            max_tx_power,
            iublinkref,
        ) = cell_params

        cell = {
            'operator': 'Kcell',
            'oss': 'ZTE',
            'rnc_id': rnc_id,
            'rnc_name': rnc_names[rnc_id],
            'site_name': nodeb_name.split(' ')[0],
            'cell_name': cell_name,
            'cId': cell_id,
            'localCellId': local_cell_id,
            'uarfcnDl': uarfcndl,
            'uarfcnUl': uarfcnul,
            'primaryScramblingCode': psc,
            'LocationArea': lac,
            'RoutingArea': rac,
            'ServiceArea': sac,
            'Ura': uralist,
            'primaryCpichPower': primary_cpich_power,
            'maximumTransmissionPower': max_tx_power,
            'IubLink': iublinkref.split('=')[-1],
            'MocnCellProfile': None,
            'administrativeState': 'UNLOCKED',
            'ip_address': None,
            'vendor': 'ZTE',
            'insert_date': Date.get_date('network_live'),
        }
        wcdma_cells.append(
            add_physical_params(atoll_data, cell),
        )
    return wcdma_cells


def parse_gsm_cells(zte_gsm_data, atoll_data):
    """
    Parse ZTE GSM cell data.

    Args:
        zte_gsm_data: list of tuples
        atoll_data: dict

    Returns:
        list of dicts
    """
    gsm_cells = []
    bcch_trx_cells = []
    for gcell in set(zte_gsm_data):
        (
            bsc_id,
            bsc_name,
            site_name,
            cell_name,
            bcc,
            ncc,
            lac,
            cell_id,
            bcch,
            tch_freqs,
        ) = gcell
        cell = {
            'operator': 'Kcell',
            'oss': 'ZTE',
            'bsc_id': bsc_id,
            'bsc_name': bsc_name,
            'site_name': site_name,
            'cell_name': cell_name,
            'bcc': bcc,
            'ncc': ncc,
            'lac': lac,
            'cell_id': cell_id,
            'bcchNo': bcch,
            'hsn': None,
            'maio': None,
            'tch_freqs': tch_freqs,
            'state': 'Active',
            'vendor': 'ZTE',
            'insert_date': Date.get_date('network_live'),
        }
        if tch_freqs:
            gsm_cells.append(
                add_physical_params(atoll_data, cell),
            )
        else:
            bcch_trx_cells.append(cell)

    for bcch_cell in bcch_trx_cells:
        one_trx_cells = list(filter(
            lambda cell: cell['cell_name'] == bcch_cell['cell_name'] and cell['bsc_name'] == bcch_cell['bsc_name'],
            gsm_cells,
        ))
        if not one_trx_cells:
            gsm_cells.append(
                add_physical_params(atoll_data, bcch_cell),
            )

    return gsm_cells
