"""Update network live with LTE cells configured on ENM."""


from dotenv import load_dotenv
from network_live.enm.enm_main import enm_main
from network_live.sql import select_atoll_data

load_dotenv('.env')


def main():
    """Update network live with ENM LTE cells."""
    atoll_data = select_atoll_data('lte')
    print(enm_main('LTE', atoll_data))


if __name__ == '__main__':
    main()
