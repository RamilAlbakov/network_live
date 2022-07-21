"""Update network live with WCDMA cells configured on OSS."""

from dotenv import load_dotenv
from network_live.oss.oss_main import oss_main
from network_live.sql import select_atoll_data

load_dotenv('.env')


def main():
    """Update network live with OSS WCDMA cells."""
    atoll_data = select_atoll_data('wcdma')
    print(oss_main('WCDMA', atoll_data))


if __name__ == '__main__':
    main()
