"""Update network live db with Kcell cells configured in own OSS and shared by Beeline/Tele2."""


from dotenv import load_dotenv
from network_live.beeline.beeline_main import beeline_main
from network_live.enm.enm_main import enm_main
from network_live.oss.oss_main import oss_main
from network_live.tele2.tele2_main import tele2_main

load_dotenv('.env')


def main():
    """Update network live db."""
    update_results = []

    enm_lte_result = enm_main('LTE', truncate=True)
    update_results.append(enm_lte_result)

    tele2_lte_result = tele2_main('LTE')
    update_results.append(tele2_lte_result)

    beeline_lte_huawei_result = beeline_main('LTE Huawei')
    update_results.append(beeline_lte_huawei_result)

    beeline_lte_nokia_result = beeline_main('LTE Nokia')
    update_results.append(beeline_lte_nokia_result)

    enm_wcdma_result = enm_main('WCDMA', truncate=True)
    update_results.append(enm_wcdma_result)

    oss_wcdma_result = oss_main('WCDMA')
    update_results.append(oss_wcdma_result)

    tele2_wcdma_result = tele2_main('WCDMA')
    update_results.append(tele2_wcdma_result)

    for update_result in update_results:
        print(update_result)


if __name__ == '__main__':
    main()
