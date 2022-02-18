"""Update network live with LTE cells shared by Tele2."""

from dotenv import load_dotenv
from network_live.tele2.tele2_main import tele2_main

load_dotenv('.env')


def main():
    """Update network live with LTE cells shared by Tele2."""
    print(tele2_main('LTE'))


if __name__ == '__main__':
    main()
