"""Update network live with LTE cells shared by Beeline on Nokia equipment."""


from dotenv import load_dotenv
from network_live.beeline.beeline_main import beeline_main

load_dotenv('.env')


def main():
    """Update network live with LTE cells shared by Beeline on Nokia equipment."""
    print(beeline_main('LTE Nokia'))


if __name__ == '__main__':
    main()
