"""Update network live db with Kcell cells configured in own OSS and shared by Beeline/Tele2."""


from dotenv import load_dotenv
from network_live.beeline.beeline_main import beeline_main
from network_live.enm.enm_main import enm_main
from network_live.oss.oss_main import oss_main
from network_live.tele2.tele2_main import tele2_main
from network_live.zte.zte_main import zte_main

load_dotenv('.env')


def execute_main_func(main_func, technologies, oss_type):
    """
    Execute main functions for oss_type.

    Args:
        main_func: function
        technologies: list of strings
        oss_type: string

    Returns:
        list of strings
    """
    execute_results = []
    for tech in technologies:
        try:
            execute_results.append(main_func(tech))
        except:
            execute_results.append('{tech} {oss} Fail'.format(tech=tech, oss=oss_type))
    return execute_results


def main():
    """Update network live db."""
    update_results = []
    enm_technologies = ['LTE', 'WCDMA', 'GSM']
    for enm_tech in enm_technologies:
        try:
            update_results.append(enm_main(enm_tech, truncate=True))
        except:
            update_results.append('{enm_tech} ENM Fail'.format(enm_tech=enm_tech))

    oss_technologies = ['WCDMA', 'GSM']
    update_results += execute_main_func(oss_main, oss_technologies, 'OSS')

    zte_technologies = ['WCDMA', 'GSM']
    update_results += execute_main_func(zte_main, zte_technologies, 'ZTE')

    beeline_technologies = ['LTE Huawei', 'LTE Nokia', 'WCDMA Huawei', 'WCDMA Nokia']
    update_results += execute_main_func(beeline_main, beeline_technologies, 'Beeline')

    tele2_technologies = ['LTE', 'WCDMA', 'GSM']
    update_results += execute_main_func(tele2_main, tele2_technologies, 'Tele2')

    for line in update_results.sort():
        print(line)


if __name__ == '__main__':
    main()
