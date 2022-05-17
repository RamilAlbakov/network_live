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
        UARFCNUL,
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

gsm_cells_select = """
    SELECT
        GV3_BTS_CELL.BSSFUNCTIONID,
        GV3_BSC.USERLABEL as bsc_name,
        GV3_BTS_CELL.SITENAME,
        GV3_BTS_CELL.USERLABEL,
        GV3_BTS_CELL.BCC,
        GV3_BTS_CELL.NCC,
        GV3_BTS_CELL.LAC,
        GV3_BTS_CELL.CELLIDENTITY,
        GV3_BTS_CELL.BCCHFREQUENCY,
        GV3_BTS_IBTSTRX.GHOPPINGFREQUENCYARFCN
    FROM
        EMS_RM4X.GV3_BTS_CELL
    LEFT JOIN EMS_RM4X.GV3_BSC
        ON EMS_RM4X.GV3_BTS_CELL.BSSFUNCTIONID=EMS_RM4X.GV3_BSC.BSSFUNCTIONID
    LEFT JOIN EMS_RM4X.GV3_BTS_IBTSTRX
        ON EMS_RM4X.GV3_BTS_CELL.OID=EMS_RM4X.GV3_BTS_IBTSTRX.PARENTOID
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
        'gsm_cell': gsm_cells_select,
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
