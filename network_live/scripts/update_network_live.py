"""Update network live db with Kcell cells configured in own OSS and shared by Beeline/Tele2."""


from dotenv import load_dotenv
from network_live.beeline.beeline_main import beeline_main
from network_live.enm.enm_main import enm_main
from network_live.oss.oss_main import oss_main
from network_live.tele2.tele2_main import tele2_main

load_dotenv('.env')


def main():
    """Update network live db."""
    enm_lte_result = enm_main('LTE', truncate=True)
    print(enm_lte_result)

    tele2_lte_result = tele2_main('LTE')
    print(tele2_lte_result)

    beeline_lte_huawei_result = beeline_main('LTE Huawei')
    print(beeline_lte_huawei_result)

    beeline_lte_nokia_result = beeline_main('LTE Nokia')
    print(beeline_lte_nokia_result)

    enm_wcdma_result = enm_main('WCDMA', truncate=True)
    print(enm_wcdma_result)

    oss_wcdma_result = oss_main('WCDMA')
    print(oss_wcdma_result)

    tele2_wcdma_result = tele2_main('WCDMA')
    print(tele2_wcdma_result)

    beeline_wcdma_nokia_result = beeline_main('WCDMA Nokia')
    print(beeline_wcdma_nokia_result)

    beeline_wcdma_huawei_result = beeline_main('WCDMA Huawei')
    print(beeline_wcdma_huawei_result)

    enm_gsm_result = enm_main('GSM', truncate=True)
    print(enm_gsm_result)

    oss_gsm_result = oss_main('GSM')
    print(oss_gsm_result)


if __name__ == '__main__':
    main()
