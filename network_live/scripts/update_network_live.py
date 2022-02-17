"""Update network live db with Kcell cells configured in own OSS and shared by Beeline/Tele2."""


from datetime import datetime

from dotenv import load_dotenv
from network_live.enm.enm_main import enm_main

load_dotenv('.env')


def main():
    """Update network live db."""
    date_format = '%{d}%m%y'.format(d='d')
    date = datetime.now().strftime(date_format)

    update_results = []

    enm_lte_result = enm_main('LTE', date)
    update_results.append(enm_lte_result)

    print(update_results)


if __name__ == '__main__':
    main()
