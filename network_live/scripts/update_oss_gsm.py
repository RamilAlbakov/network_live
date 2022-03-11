"""Update network live with GSM cells configured on OSS."""

from dotenv import load_dotenv
from network_live.oss.oss_main import oss_main

load_dotenv('.env')


def main():
    """Update network live with OSS WCDMA cells."""
    print(oss_main('GSM'))


if __name__ == '__main__':
    main()
