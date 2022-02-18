"""Update network live with LTE cells configured on ENM."""


from dotenv import load_dotenv
from network_live.enm.enm_main import enm_main

load_dotenv('.env')


def main():
    """Update network live with ENM LTE cells."""
    print(enm_main('LTE'))


if __name__ == '__main__':
    main()
