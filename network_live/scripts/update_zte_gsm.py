"""Update network live with ZTE GSM cells."""

from dotenv import load_dotenv
from network_live.sql import select_atoll_data
from network_live.zte.zte_main import zte_main

load_dotenv('.env')


def main():
    """Update network live with ZTE GSM cells."""
    atoll_data = select_atoll_data('gsm')
    print(zte_main('GSM', atoll_data))


if __name__ == '__main__':
    main()
