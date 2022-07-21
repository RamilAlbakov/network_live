"""Update network live with ZTE WCDMA cells."""

from dotenv import load_dotenv
from network_live.sql import select_atoll_data
from network_live.zte.zte_main import zte_main

load_dotenv('.env')

atoll_data = select_atoll_data('wcdma')

def main():
    """Update network live with ZTE WCDMA cells."""
    print(zte_main('WCDMA', atoll_data))


if __name__ == '__main__':
    main()
