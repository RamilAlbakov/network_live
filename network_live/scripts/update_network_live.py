"""Update network live db with Kcell cells configured in own OSS and shared by Beeline/Tele2."""


from datetime import datetime

from dotenv import load_dotenv
from network_live.enm.enm_main import enm_main

load_dotenv('.env')


def main():
    """Update network live db."""
    date_format = '%{d}%m%y'.format(d='d')
    date = datetime.now().strftime(date_format)

    enm_lte_cells = enm_main('lte', date)
    print(enm_lte_cells)


if __name__ == '__main__':
    main()
