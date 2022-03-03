"""Update network live with Beeline Nokia WCDMA cells."""


from dotenv import load_dotenv
from network_live.beeline.beeline_main import beeline_main

load_dotenv('.env')


def main():
    """Update network live with WCDMA cells shared by Beeline on Nokia equipment."""
    print(beeline_main('WCDMA Nokia'))


if __name__ == '__main__':
    main()
