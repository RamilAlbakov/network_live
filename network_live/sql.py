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
        :physicalLayerCellIdGroup,
        :ip_address,
        :vendor,
        :insert_date
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
        :insert_date
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
        :insert_date
    )
"""


class Sql(object):
    """Sql data to communicate with network live db."""

    insert_sqls = {
        'LTE': lte_insert_sql,
        'WCDMA': wcdma_insert_sql,
        'GSM': gsm_insert_sql,
    }

    insert_tables = {
        'LTE': 'ltecells2',
        'WCDMA': 'wcdmacells2',
        'GSM': 'gsmcells2',
    }

    @classmethod
    def insert(cls, cell_data, oss, technology, truncate=False):
        """
        Isert cell data to Network Live db.

        Args:
            cell_data: list of dicts
            oss: string
            technology: string
            truncate: bool

        Returns:
            string
        """
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
                if truncate:
                    cursor.execute('TRUNCATE TABLE {table}'.format(
                        table=cls.insert_tables[technology],
                    ))
                for cell in cell_data:
                    cursor.execute(cls.insert_sqls[technology], cell)
                connection.commit()
                return '{technology} {oss} Success'.format(technology=technology, oss=oss)
        except cx_Oracle.Error as err:
            err_obj, = err.args
            print(err_obj.message)
            return '{technology} {oss} Fail'.format(technology=technology, oss=oss)
