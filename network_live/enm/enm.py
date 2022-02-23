"""Get data from ENM for cells configured on ENM."""


import os

import enmscripting


class Enm(object):
    """Present ENM interface for getting data for cells configured on ENM."""

    eutrancellfdd_params = [
        'administrativeState',
        'cellId',
        'earfcndl',
        'latitude',
        'longitude',
        'physicalLayerCellIdGroup',
        'qRxLevMin',
        'rachRootSequence',
        'tac',
    ]

    utrancell_params = [
        'UtranCellId',
        'localCellId',
        'uarfcnDl',
        'primaryScramblingCode',
        'locationAreaRef',
        'routingAreaRef',
        'serviceAreaRef',
        'uraRef',
        'primaryCpichPower',
        'maximumTransmissionPower',
        'iubLinkRef',
        'mocnCellProfileRef',
    ]

    cli_commands = {
        'lte_cells': 'cmedit get * EutranCellFdd.({params})'.format(
            params=','.join(eutrancellfdd_params),
        ),
        'enodeb_id': 'cmedit get * ENodeBFunction.(enbid)',
        'wcdma_cells': 'cmedit get * UtranCell.({params})'.format(
            params=','.join(utrancell_params),
        ),
        'rnc_ids': 'cmedit get * RncFunction.(rncId)',
        'site_names': 'cmedit get * Iub.(rbsId)',
        'iublink': 'cmedit get *RNC* IubLink.(rbsId)',
        'dus_ip': 'cmedit get * Ip.(nodeIpAddress)',
        'bbu_ip': 'cmedit get * AddressIPv4.(address)',
    }

    @classmethod
    def execute_enm_command(cls, command):
        """
        Execute ENM CLI commands.

        Args:
            command: string

        Returns:
            list of strings
        """
        session = enmscripting.open(os.getenv('ENM_SERVER')).with_credentials(
            enmscripting.UsernameAndPassword(
                os.getenv('ENM_LOGIN'),
                os.getenv('ENM_PASSWORD'),
            ),
        )
        terminal = session.terminal()
        response = terminal.execute(cls.cli_commands[command])
        enm_data = response.get_output()
        enmscripting.close(session)

        return enm_data
