"""Present class to communicate with network live db."""

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
        :latitude,
        :longitude,
        :administrativeState,
        :rachRootSequence,
        :physicalLayerCellId,
        :ip_address,
        :vendor,
        :insert_date,
        :oss
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
        :UtranCellId,
        :localCellId,
        :uarfcnDl,
        :primaryScramblingCode,
        :LocationArea,
        :RoutingArea,
        :ServiceArea,
        :Ura,
        :primaryCpichPower,
        :maximumTransmissionPower,
        :IubLink,
        :MocnCellProfile,
        :ip_address,
        :vendor,
        :insert_date,
        :oss
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
        :oss
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

    atoll_dsn = cx_Oracle.makedsn(
        os.getenv('ATOLL_HOST'),
        os.getenv('ATOLL_PORT'),
        service_name=os.getenv('SERVICE_NAME'),
    )
    try:
        with cx_Oracle.connect(
            user=os.getenv('ATOLL_LOGIN'),
            password=os.getenv('ATOLL_PASSWORD'),
            dsn=atoll_dsn,
        ) as connection:
            cursor = connection.cursor()
            cursor.execute(delete_sql)
            for cell in cell_data:
                cursor.execute(insert_sqls[technology], cell)
            connection.commit()
            return '{technology} {oss} Success'.format(technology=technology, oss=oss)
    except:
        return '{technology} {oss} Fail'.format(technology=technology, oss=oss)
