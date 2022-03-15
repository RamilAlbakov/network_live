"""Parse ZTE cell data."""

from network_live.date import Date


def parse_wcdma_cells(zte_cell_data, zte_rnc_data):
    """
    Parse ZTE cell data.

    Args:
        zte_cell_data: list of tuples
        zte_rnc_data: list of tuples

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
            uarfcndl,
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
            'rnc_id': rnc_id,
            'rnc_name': rnc_names[rnc_id],
            'site_name': nodeb_name.split(' ')[0],
            'UtranCellId': cell_name,
            'localCellId': cell_id,
            'uarfcndl': uarfcndl,
            'primaryScramblingCode': psc,
            'LocationArea': lac,
            'RoutingArea': rac,
            'ServiceArea': sac,
            'Ura': uralist,
            'primaryCpichPower': primary_cpich_power,
            'maximumTransmissionPower': max_tx_power,
            'IubLink': iublinkref.split('=')[-1],
            'MocnCellProfile': None,
            'ip_address': None,
            'vendor': 'zte',
            'insert_date': Date.get_date('network_live'),
        }
        wcdma_cells.append(cell)
    return wcdma_cells