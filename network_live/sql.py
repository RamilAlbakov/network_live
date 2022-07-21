"""Comunicate with Atoll db."""

import os

import cx_Oracle

lte_insert_sql = """
    INSERT
        INTO ltecells2
    VALUES (
        :subnetwork,
        :enodeb_id,
        :site_name,
        :cell_name,
        :tac,
        :cellId,
        :eci,
        :earfcndl,
        :qRxLevMin,
        :administrativeState,
        :rachRootSequence,
        :physicalLayerCellId,
        :ip_address,
        :vendor,
        :insert_date,
        :oss,
        :azimut,
        :height,
        :longitude,
        :latitude
    )
"""

wcdma_insert_sql = """
    INSERT
        INTO wcdmacells2
    VALUES (
        :operator,
        :rnc_id,
        :rnc_name,
        :site_name,
        :cell_name,
        :localCellId,
        :cId,
        :uarfcnDl,
        :uarfcnUl,
        :primaryScramblingCode,
        :LocationArea,
        :RoutingArea,
        :ServiceArea,
        :Ura,
        :primaryCpichPower,
        :maximumTransmissionPower,
        :IubLink,
        :MocnCellProfile,
        :administrativeState,
        :ip_address,
        :vendor,
        :oss,
        :insert_date,
        :azimut,
        :height,
        :longitude,
        :latitude
    )
"""

gsm_insert_sql = """
    INSERT
        INTO gsmcells2
    VALUES (
        :operator,
        :bsc_id,
        :bsc_name,
        :site_name,
        :cell_name,
        :bcc,
        :ncc,
        :lac,
        :cell_id,
        :bcchNo,
        :hsn,
        :maio,
        :tch_freqs,
        :state,
        :vendor,
        :insert_date,
        :oss,
        :azimut,
        :height,
        :longitude,
        :latitude
    )
"""

nr_insert_sql = """
    INSERT
        INTO nrcells
    VALUES (
        :subnetwork,
        :gNBId,
        :site_name,
        :cell_name,
        :cellLocalId,
        :cellState,
        :nCI,
        :nRPCI,
        :nRTAC,
        :rachRootSequence,
        :qRxLevMin,
        :arfcnDL,
        :bSChannelBwDL,
        :configuredMaxTxPower,
        :ip_address,
        :vendor,
        :insert_date,
        :oss
    )
"""


def execute_sql(sql_command, insert_cells=(), delete_sql=''):
    """
    Execute sql_command.

    Args:
        sql_command: string
        insert_cells: list
        delete_sql: string

    Returns:
        list of tuples
    """
    atoll_dsn = cx_Oracle.makedsn(
        os.getenv('ATOLL_HOST'),
        os.getenv('ATOLL_PORT'),
        service_name=os.getenv('SERVICE_NAME'),
    )
    with cx_Oracle.connect(
        user=os.getenv('ATOLL_LOGIN'),
        password=os.getenv('ATOLL_PASSWORD'),
        dsn=atoll_dsn,
    ) as connection:
        cursor = connection.cursor()
        if insert_cells:
            cursor.execute(delete_sql)
            for cell in insert_cells:
                cursor.execute(sql_command, cell)
            connection.commit()
        else:
            return cursor.execute(sql_command).fetchall()


def update_network_live(cell_data, oss, technology):
    """
    Update Network Live with cell data for given oss and technology.

    Args:
        cell_data: list
        oss: str
        technology: str

    Returns:
        string
    """
    insert_sqls = {
        'LTE': lte_insert_sql,
        'WCDMA': wcdma_insert_sql,
        'GSM': gsm_insert_sql,
        'NR': nr_insert_sql,
    }
    network_live_tables = {
        'LTE': 'ltecells2',
        'WCDMA': 'wcdmacells2',
        'GSM': 'gsmcells2',
        'NR': 'nrcells',
    }

    delete_sql = "DELETE FROM {table} WHERE oss='{oss}'".format(
        table=network_live_tables[technology],
        oss=oss,
    )

    try:
        execute_sql(insert_sqls[technology], cell_data, delete_sql)
    except cx_Oracle.Error as err:
        err_obj, = err.args
        print(err_obj.code)
        print(err_obj.message)
        return '{technology} {oss} Fail'.format(technology=technology, oss=oss)

    return '{technology} {oss} Success'.format(technology=technology, oss=oss)


def handle_atoll_data(select_data):
    """
    Handle selected atoll data.

    Args:
        select_data: list of tuples

    Returns:
        dict
    """
    atoll_data = {}

    for cell in select_data:
        (
            cell_name,
            azimut,
            height,
            longitude,
            latitude,
        ) = cell
        atoll_data[cell_name] = {
            'azimut': azimut,
            'height': height,
            'longitude': longitude,
            'latitude': latitude,
        }
    return atoll_data


def select_atoll_data(technology):
    """
    Select physical parameters from Atoll by technology.

    Args:
        technology: string

    Returns:
        dict
    """
    lte_select = """
        SELECT
            atoll_mrat.xgcellslte.cell_id,
            atoll_mrat.xgtransmitters.azimut,
            atoll_mrat.xgtransmitters.height,
            atoll_mrat.sites.longitude,
            atoll_mrat.sites.latitude
        FROM atoll_mrat.xgtransmitters
            INNER JOIN atoll_mrat.sites
                ON atoll_mrat.xgtransmitters.site_name = atoll_mrat.sites.name
            INNER JOIN atoll_mrat.xgcellslte
                ON atoll_mrat.xgtransmitters.tx_id = atoll_mrat.xgcellslte.tx_id
    """

    wcdma_select = """
        SELECT
            atoll_mrat.ucells.cell_id,
            atoll_mrat.utransmitters.azimut,
            atoll_mrat.utransmitters.height,
            atoll_mrat.sites.longitude,
            atoll_mrat.sites.latitude
        FROM atoll_mrat.utransmitters
            INNER JOIN atoll_mrat.sites
                ON atoll_mrat.utransmitters.site_name = atoll_mrat.sites.name
            INNER JOIN atoll_mrat.ucells
                ON atoll_mrat.utransmitters.tx_id = atoll_mrat.ucells.tx_id
    """

    gsm_select = """
        SELECT
            atoll_mrat.gtransmitters.tx_id,
            atoll_mrat.gtransmitters.azimut,
            atoll_mrat.gtransmitters.height,
            atoll_mrat.sites.longitude,
            atoll_mrat.sites.latitude
        FROM atoll_mrat.gtransmitters
            INNER JOIN atoll_mrat.sites
                ON atoll_mrat.gtransmitters.site_name = atoll_mrat.sites.name
    """

    sql_selects = {
        'lte': lte_select,
        'wcdma': wcdma_select,
        'gsm': gsm_select,
    }

    select_data = execute_sql(sql_selects[technology])
    return handle_atoll_data(select_data)
