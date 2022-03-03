"""Download Beeline Tele2 logs from FTP server."""


import os
from zipfile import ZipFile

import paramiko
from network_live.date import Date


def download_ftp_data(remote_path, local_path, ftp_type):
    """
    Download data from ftp server.

    Args:
        remote_path: string
        local_path: string
        ftp_type: string
    """
    if ftp_type == 'ftp_server':
        host = os.getenv('FTP_HOST')
        login = os.getenv('FTP_LOGIN')
        password = os.getenv('FTP_PASSWORD')
    elif ftp_type == 'oss':
        host = os.getenv('ASTOSS_HOST')
        login = os.getenv('ASTOSS_USER')
        password = os.getenv('ASTOSS_PASSWORD')

    with paramiko.Transport((host)) as transport:
        transport.connect(username=login, password=password)
        with paramiko.SFTPClient.from_transport(transport) as sftp:
            sftp.get(remote_path, local_path)


def delete_old_logs(logs_path):
    """
    Delete previous logs.

    Args:
        logs_path: string
    """
    for log in os.listdir(logs_path):
        os.remove('{logs_path}/{log}'.format(logs_path=logs_path, log=log))


def unzip_log(zipfile_path):
    """
    Extract the necessary files.

    Args:
        zipfile_path: string
    """
    zipfile_name = os.path.splitext(os.path.basename(zipfile_path))[0]
    zipfile_dir = os.path.dirname(zipfile_path)

    with ZipFile(zipfile_path, 'r') as zip_obj:
        if 'result_data' in zipfile_name:
            date = zipfile_name.split('_')[-1]
            filename = 'result_data_{date}.csv'.format(date=date)
            zip_obj.extract(
                filename,
                zipfile_dir,
            )
            os.rename(
                '{unzip_dir}/{filename}'.format(unzip_dir=zipfile_dir, filename=filename),
                '{unzip_dir}/tele2_lte_log.csv'.format(unzip_dir=zipfile_dir),
            )
        else:
            zip_obj.extractall(zipfile_dir)


def download_ftp_logs(operator):
    """
    Download lte cell data from ftp for required operator and vendor.

    Args:
        operator: string
    """
    if 'tele2' in operator:
        logs_path = 'logs/tele2'
        date = Date.get_date('tele2')
    elif 'beeline' in operator:
        logs_path = 'logs/beeline'
        date = Date.get_date('beeline')

    delete_old_logs(logs_path)

    ftp_paths = {
        'tele2_lte': '/reporter/tele2/mocn/{date}/Config_result_data_{date}.zip'.format(date=date),
        'tele2_wcdma': '/reporter/tele2/250plus/{date}/UNBI_Conf_Export_XML_RT_{date}.zip'.format(
            date=date,
        ),
        'beeline_huawei': '/reporter/beeline/cm/LTE/{date}.zip'.format(date=date),
        'beeline_nokia_moran': '/reporter/beeline/cm/Nokia/LTE/{date}.zip'.format(date=date),
        'beeline_nokia_mocn': '/reporter/beeline/cm/Nokia/LTE_MOCN/{date}.zip'.format(date=date),
    }

    remote_path = ftp_paths[operator]
    local_path = '{logs_path}/{log_name}'.format(
        logs_path=logs_path,
        log_name=os.path.basename(remote_path),
    )

    download_ftp_data(remote_path, local_path, 'ftp_server')
    unzip_log(local_path)
    os.remove(local_path)


def download_oss_logs(technology):
    """
    Download logs from OSS.

    Args:
        technology: string
    """
    if technology == 'WCDMA':
        remote_path = '/home/anpusr/bcg_filters/export/oss_utrancells.xml'
        log_name = os.path.basename(remote_path)

    logs_path = 'logs/oss'
    local_path = '{logs_path}/{log_name}'.format(logs_path=logs_path, log_name=log_name)
    delete_old_logs(logs_path)
    download_ftp_data(remote_path, local_path, 'oss')
