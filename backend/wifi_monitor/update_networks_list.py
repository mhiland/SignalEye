import logging
import logging_config
import pytz
from datetime import datetime


def update_networks_list(persistent_networks, current_networks):
    current_network_identifiers = {(net['ESSID'], net['Address'])
                                   for net in current_networks if 'ESSID' in net and 'Address' in net}

    for net in persistent_networks:
        network_identifier = (net.get('ESSID'), net.get('Address'))
        if network_identifier in current_network_identifiers:
            net['Active'] = True
            net['LastSeen'] = datetime.now(pytz.UTC).strftime("%Y-%m-%d %H:%M:%S")
            for current_net in current_networks:
                if 'ESSID' in current_net and 'Address' in current_net:
                    if current_net['ESSID'] == net['ESSID'] and current_net['Address'] == net['Address']:
                        net.update(current_net)
        else:
            net['Active'] = False

    persistent_network_identifiers = {
        (net['ESSID'], net['Address']) for net in persistent_networks
    }

    for current_net in current_networks:
        if 'ESSID' in current_net and 'Address' in current_net:
            network_identifier = (current_net['ESSID'], current_net['Address'])

            if network_identifier not in persistent_network_identifiers:
                timestamp = datetime.now(pytz.UTC).strftime("%Y-%m-%d %H:%M:%S")
                current_net['Active'] = True
                current_net['LastSeen'] = timestamp
                current_net['FirstSeen'] = timestamp
                persistent_networks.append(current_net)
                persistent_network_identifiers.add(network_identifier)
                logging.info(f"New network detected: {current_net['ESSID']} {current_net['Address']}")
            else:
                for net in persistent_networks:
                    if net['ESSID'] == current_net['ESSID'] and net['Address'] == current_net['Address']:
                        net['LastSeen'] = datetime.now(pytz.UTC).strftime("%Y-%m-%d %H:%M:%S")
                        net.update(current_net)

    persistent_networks.sort(
        key=lambda x: x['ESSID'].lower() if x['ESSID'] else "")
