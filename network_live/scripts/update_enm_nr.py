"""Update network live with NR cells configured on ENM."""


from dotenv import load_dotenv
from network_live.enm.enm_main import enm_main

load_dotenv('.env')


def main():
    """Update network live with ENM nr cells."""
    print(enm_main('NR'))


if __name__ == '__main__':
    main()
