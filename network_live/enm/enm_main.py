"""Prepare cell data for network live for technologies for cells configured on ENM."""


from dotenv import load_dotenv
from enm import Enm

load_dotenv('.env')


def enm_lte_main():
    """Prepare neccessary lte cell data."""
    enm_eutran_data = Enm.execute_enm_command('lte_cells')
    print(enm_eutran_data)


if __name__ == '__main__':
    enm_lte_main()
