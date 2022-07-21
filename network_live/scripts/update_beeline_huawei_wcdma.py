"""Update network live with WCDMA cells shared by Beeline on Huawei equipment."""


from dotenv import load_dotenv
from network_live.beeline.beeline_main import beeline_main
from network_live.sql import select_atoll_data

load_dotenv('.env')


def main():
    """Update network live with LTE cells shared by Beeline on Nokia equipment."""
    atoll_data = select_atoll_data('wcdma')
    print(beeline_main('WCDMA Huawei', atoll_data))


if __name__ == '__main__':
    main()
