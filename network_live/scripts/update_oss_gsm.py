"""Update network live with GSM cells configured on OSS."""

from dotenv import load_dotenv
from network_live.oss.oss_main import oss_main
from network_live.sql import select_atoll_data

load_dotenv('.env')


def main():
    """Update network live with OSS WCDMA cells."""
    atoll_data = select_atoll_data('gsm')
    print(oss_main('GSM', atoll_data))


if __name__ == '__main__':
    main()
