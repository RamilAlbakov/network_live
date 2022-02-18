"""Update network live db with Kcell cells configured in own OSS and shared by Beeline/Tele2."""


from dotenv import load_dotenv
from network_live.enm.enm_main import enm_main
from network_live.tele2.tele2_main import tele2_main

load_dotenv('.env')


def main():
    """Update network live db."""
    update_results = []

    enm_lte_result = enm_main('LTE')
    update_results.append(enm_lte_result)

    tele2_lte_result = tele2_main('LTE')
    update_results.append(tele2_lte_result)

    print(update_results)


if __name__ == '__main__':
    main()
