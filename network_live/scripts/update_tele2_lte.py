"""Update network live with LTE cells shared by Tele2."""

from dotenv import load_dotenv
from network_live.download_logs import download_lte_logs

load_dotenv('.env')


def main():
    """Update network live with LTE cells shared by Tele2."""
    download_lte_logs('beeline_nokia_moran')
