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
            'UtranCellId': cell_name,
            'localCellId': cell_id,
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
        wcdma_cells.append(cell)
    return wcdma_cells


def get_gsm_cell(cell_name, bsc_name, gsm_cells):
    """
    Get gsm cell by cell name and bsc name from gsm_cells.

    Args:
        cell_name: string
        bsc_name: string
        gsm_cells: list of dicts
    
    Returns:
        gsm cell dict or None
    """


def parse_gsm_cells(zte_gsm_data):
    """
    Parse ZTE GSM cell data.

    Args:
        zte_gsm_data: list of tuples

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
            gsm_cells.append(cell)
        else:
            bcch_trx_cells.append(cell)
    
    for bcch_cell in bcch_trx_cells:
        one_trx_cells = list(filter(
            lambda cell: cell['cell_name'] == bcch_cell['cell_name'] and cell['bsc_name'] == bcch_cell['bsc_name'],
            gsm_cells,
        ))
        if not one_trx_cells:
            gsm_cells.append(bcch_cell)
    
    return gsm_cells
