"""Update network live with LTE cells configured on ENM."""


from datetime import datetime

from dotenv import load_dotenv
from network_live.enm.enm_main import enm_main

load_dotenv('.env')


def main():
    """Update network live with ENM LTE cells."""
    date_format = '%{d}%m%y'.format(d='d')
    date = datetime.now().strftime(date_format)

    print(enm_main('LTE', date))


if __name__ == '__main__':
    main()
