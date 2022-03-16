"""Update network live with ZTE GSM cells."""

from dotenv import load_dotenv
from network_live.zte.zte_main import zte_main

load_dotenv('.env')


def main():
    """Update network live with ZTE GSM cells."""
    print(zte_main('GSM'))


if __name__ == '__main__':
    main()
