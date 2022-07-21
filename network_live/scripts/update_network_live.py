"""Update network live db with Kcell cells configured in own OSS and shared by Beeline/Tele2."""

from dotenv import load_dotenv
from network_live.beeline.beeline_main import beeline_main
from network_live.enm.enm_main import enm_main
from network_live.oss.oss_main import oss_main
from network_live.send_mail import send_email
from network_live.sql import select_atoll_data
from network_live.tele2.tele2_main import tele2_main
from network_live.zte.zte_main import zte_main

load_dotenv('.env')

atoll_data = {
    'GSM': select_atoll_data('gsm'),
    'WCDMA': select_atoll_data('wcdma'),
    'LTE': select_atoll_data('lte'),
    'NR': None,
}


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
        ran_tech = tech.split(' ')[0]
        try:
            execute_result = main_func(tech, atoll_data[ran_tech])
        except:
            execute_result = '{tech} {oss} Fail'.format(tech=tech, oss=oss_type)
        print(execute_result)
        execute_results.append(execute_result)
    return execute_results


def main():
    """Update network live db."""
    update_results = []
    enm_technologies = ['LTE', 'WCDMA', 'GSM', 'NR']
    update_results += execute_main_func(enm_main, enm_technologies, 'ENM')

    oss_technologies = ['WCDMA', 'GSM']
    update_results += execute_main_func(oss_main, oss_technologies, 'OSS')

    zte_technologies = ['WCDMA', 'GSM']
    update_results += execute_main_func(zte_main, zte_technologies, 'ZTE')

    beeline_technologies = ['LTE Huawei', 'LTE Nokia', 'WCDMA Huawei', 'WCDMA Nokia', 'GSM Nokia']
    update_results += execute_main_func(beeline_main, beeline_technologies, 'Beeline')

    tele2_technologies = ['LTE', 'WCDMA', 'GSM']
    update_results += execute_main_func(tele2_main, tele2_technologies, 'Tele2')

    to_addr = 'Ramil.Albakov@kcell.kz,Osman.Mamedov@kcell.kz'
    subject = 'Network Live update report'
    message = '\n'.join(sorted(update_results))
    send_email(to_addr, subject, message)


if __name__ == '__main__':
    main()
