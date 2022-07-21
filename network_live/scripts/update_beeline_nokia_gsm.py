"""Update network live with Beeline Nokia GSM cells."""

from dotenv import load_dotenv
from network_live.beeline.beeline_main import beeline_main
from network_live.sql import select_atoll_data

load_dotenv('.env')


def main():
    """Update network live with GSM cells shared by Beeline on Nokia equipment."""
    atoll_data = select_atoll_data('gsm')
    print(beeline_main('GSM Nokia', atoll_data))


if __name__ == '__main__':
    main()
