"""Update network live with Beeline Nokia GSM cells."""

from dotenv import load_dotenv
from network_live.beeline.beeline_main import beeline_main

load_dotenv('.env')


def main():
    """Update network live with GSM cells shared by Beeline on Nokia equipment."""
    print(beeline_main('GSM Nokia'))


if __name__ == '__main__':
    main()
