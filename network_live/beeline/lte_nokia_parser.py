"""Parse Beeline Nokia LTE xml files for network live."""

import os
import re

from network_live.date import Date


def read_file(path):
    """
    Read file content.

    Args:
        path: string

    Returns:
        list of dicts
    """
    with open(path) as log:
        return log.readlines()


def parse_parameter_value(line):
    """
    Parse parameter value from line of file content.

    Args:
        line: string

    Returns:
        string
    """
    start_index = line.index('>') + 1
    last_index = line.index('</')
    return line[start_index:last_index]


def parse_cell_id(line):
    """
    Parse cell id from line of file content.

    Args:
        line: string

    Returns:
        string
    """
    re_pattern = r'LNCEL-\d{1,}'
    cell_id_mo = re.search(re_pattern, line).group()
    return cell_id_mo.split('-')[-1]


def parse_lnbts_params(log_lines):
    """
    Parse necessary parameters from LNBTS class.

    Args:
        log_lines: list of strings

    Returns:
        dict
    """
    lnbts_params = {}
    re_pattern = r'MRBTS-\d{2,}'
    lnbts_class = False
    for line in log_lines:
        if 'class="LNBTS"' in line:
            lnbts_class = True
            enodeb_id_mo = re.search(re_pattern, line).group()
            lnbts_params['enodeb_id'] = enodeb_id_mo.split('-')[-1]
        if lnbts_class:
            if 'name="name"' in line:
                lnbts_params['site_name'] = parse_parameter_value(line)
                return lnbts_params


def parse_lcellfdd_params(log_lines):
    """
    Parse necessary paraneters from LNCEL_FDD class.

    Args:
        log_lines: list of strings

    Returns:
        dict
    """
    lncellfdd_params = {}
    lncellfdd_class = False
    for line in log_lines:
        if 'class="LNCEL_FDD"' in line:
            lncellfdd_class = True
            cell_id = parse_cell_id(line)
        if lncellfdd_class:
            if 'name="earfcnDL"' in line:
                earfcndl = parse_parameter_value(line)
            if 'name="rootSeqIndex"' in line:
                rach_root_sequence = parse_parameter_value(line)
                lncellfdd_params[cell_id] = {
                    'earfcndl': earfcndl,
                    'rachRootSequence': rach_root_sequence,
                }
                lncellfdd_class = False
    return lncellfdd_params


def parse_sib_params(log_lines):
    """
    Parse necessary parameters from SIB class.

    Args:
        log_lines: list of strings

    Returns:
        dict
    """
    sib_params = {}
    sib_class = False
    for line in log_lines:
        if 'class="SIB"' in line:
            sib_class = True
            cell_id = parse_cell_id(line)
        if sib_class:
            if 'name="qrxlevmin"' in line:
                sib_params[cell_id] = parse_parameter_value(line)
                sib_class = False
    return sib_params


def parse_lncel_params(log_lines):
    """
    Parse necessary parameters from LNCEL class.

    Args:
        log_lines: list of strings

    Returns:
        list of dicts
    """
    lncel_params = []
    lncel_class = False
    for line in log_lines:
        if 'class="LNCEL"' in line:
            lncel_class = True
            cell = {'cellId': parse_cell_id(line)}
        if lncel_class:
            if 'name="name"' in line:
                cell['cell_name'] = parse_parameter_value(line)
            if 'name="administrativeState"' in line:
                cell['administrativeState'] = parse_parameter_value(line)
            if 'name="eutraCelId"' in line:
                cell['eci'] = parse_parameter_value(line)
            if 'name="phyCellId"' in line:
                cell['physicalLayerCellIdGroup'] = parse_parameter_value(line)
            if 'name="tac"' in line:
                cell['tac'] = parse_parameter_value(line)
                lncel_class = False
                lncel_params.append(cell)
    return lncel_params


def parse_nokia_xml(xml_path):
    """
    Parse all necessary parameters from xml file.

    Args:
        xml_path: string

    Returns:
        list of dicts
    """
    log_lines = read_file(xml_path)

    lnbts_params = parse_lnbts_params(log_lines)
    lncellfdd_params = parse_lcellfdd_params(log_lines)
    sib_params = parse_sib_params(log_lines)
    lncel_params = parse_lncel_params(log_lines)

    for lncel in lncel_params:
        lncel['enodeb_id'] = lnbts_params['enodeb_id']
        lncel['site_name'] = lnbts_params['site_name']

        cell_id = lncel['cellId']
        lncel['earfcndl'] = lncellfdd_params[cell_id]['earfcndl']
        lncel['rachRootSequence'] = lncellfdd_params[cell_id]['rachRootSequence']
        lncel['qRxLevMin'] = sib_params[cell_id]
        lncel['subnetwork'] = 'Beeline'
        lncel['vendor'] = 'nokia'
        lncel['latitude'] = None
        lncel['longitude'] = None
        lncel['ip_address'] = None
        lncel['insert_date'] = Date.get_date('network_live')

    return lncel_params


def parse_lte_nokia(logs_path):
    """
    Parse all necessary parameters from all xml files.

    Args:
        logs_path: string

    Returns:
        list of dicts
    """
    cell_data = []
    for log in os.listdir(logs_path):
        xml_path = '{logs_path}/{log}'.format(logs_path=logs_path, log=log)
        cell_data += parse_nokia_xml(xml_path)

    return cell_data
