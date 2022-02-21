"""Update network live with LTE cells shared by Beeline on Huawei equipment."""


from dotenv import load_dotenv
from network_live.beeline.beeline_main import beeline_main

load_dotenv('.env')


def main():
    """Update network live with LTE cells shared by Beeline on Huawei equipment."""
    print(beeline_main('LTE Huawei'))


if __name__ == '__main__':
    main()
