"""Select data from ZTE db."""


import os

import cx_Oracle
from dotenv import load_dotenv

load_dotenv('.env')

rnc_select = """
    SELECT
        USERLABEL as rnc_name,
        MANAGEDELEMENTID as rnc_id
    FROM
        NAF_CM.V_CM_RNC_MANAGED_ELEMENT_V3
"""

wcdma_cells_select = """
    SELECT
        NEID,
        NODEBNAME,
        USERLABEL,
        CID,
        UARFCNDL,
        PRIMARYSCRAMBLINGCODE,
        LAC,
        RAC,
        SAC,
        URALIST,
        PRIMARYCPICHPOWER,
        MAXIMUMTRANSMISSIONPOWER,
        UTRANCELLIUBLINK
    FROM
        NAF_CM.V_CM_UTRAN_CELL_V3
"""


def select_zte_data(mo_type):
    """
    Select data from ZTE db according to technology.

    Args:
        mo_type: string

    Returns:
        list
    """
    sql_selects = {
        'rnc': rnc_select,
        'wcdma_cell': wcdma_cells_select,
    }

    zte_dsn = cx_Oracle.makedsn(
        os.getenv('ZTE_HOST'),
        os.getenv('ZTE_PORT'),
        service_name=os.getenv('ZTE_SERVICE_NAME'),
    )
    with cx_Oracle.connect(
        user=os.getenv('ZTE_LOGIN'),
        password=os.getenv('ZTE_PASSWORD'),
        dsn=zte_dsn,
    ) as connection:
        cursor = connection.cursor()
        return cursor.execute(sql_selects[mo_type]).fetchall()


if __name__ == '__main__':
    print(select_zte_data('wcdma_cell'))
