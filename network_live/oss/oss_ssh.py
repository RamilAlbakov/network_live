"""Run oss tools through ssh to generate cell logs."""

import os

import paramiko


def run_bcgtool():
    """
    Run oss bcgtool to generate wcdma cells xml file.

    Returns:
        string
    """
    filter_path = '~/bcg_filters/WCDMA_custom_filter.xml'
    export_path = '~/bcg_filters/export/oss_utrancells.xml'
    bcgtool_path = '/opt/ericsson/nms_umts_wran_bcg/bin/bcgtool.sh'
    bcg_command = '{bcgtool} -d {filter_path} -e {export_path}'.format(
        bcgtool=bcgtool_path,
        filter_path=filter_path,
        export_path=export_path,
    )
    with paramiko.SSHClient() as client:
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            hostname=os.getenv('ASTOSS_HOST'),
            username=os.getenv('ASTOSS_USER'),
            password=os.getenv('ASTOSS_PASSWORD'),
            port=os.getenv('ASTOSS_PORT'),
        )
        stdin, stdout, stderr = client.exec_command(bcg_command)
        bcg_result = stdout.read() + stderr.read()
        return bcg_result.decode()
