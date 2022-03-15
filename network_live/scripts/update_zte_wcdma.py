"""Update network live with ZTE WCDMA cells."""

from dotenv import load_dotenv
from network_live.zte.zte_main import zte_main

load_dotenv('.env')


def main():
    """Update network live with ZTE WCDMA cells."""
    print(zte_main('WCDMA'))


if __name__ == '__main__':
    main()
