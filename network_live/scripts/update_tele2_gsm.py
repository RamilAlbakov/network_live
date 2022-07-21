"""Update network live with GSM cells shared by Tele2."""

from dotenv import load_dotenv
from network_live.sql import select_atoll_data
from network_live.tele2.tele2_main import tele2_main

load_dotenv('.env')


def main():
    """Update network live with WCDMA cells shared by Tele2."""
    atoll_data = select_atoll_data('gsm')
    print(tele2_main('GSM', atoll_data))


if __name__ == '__main__':
    main()
