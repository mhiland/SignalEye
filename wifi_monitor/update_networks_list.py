from datetime import datetime

def update_networks_list(persistent_networks, current_networks):
    current_essids = {net['ESSID'] for net in current_networks if 'ESSID' in net}
    
    for net in persistent_networks:
        if net['ESSID'] in current_essids:
            net['Active'] = True
            net['Last Seen'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for current_net in current_networks:
                if 'ESSID' in current_net and current_net['ESSID'] == net['ESSID']:
                    net.update(current_net)
        else:
            net['Active'] = False
    
    persistent_essids = {net['ESSID'] for net in persistent_networks}
    for current_net in current_networks:
        if 'ESSID' in current_net and current_net['ESSID'] not in persistent_essids:
            current_net['Active'] = True
            current_net['Last Seen'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            current_net['First Seen'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            persistent_networks.append(current_net)
        elif 'ESSID' in current_net and current_net['ESSID'] in persistent_essids:
            for net in persistent_networks:
                if net['ESSID'] == current_net['ESSID']:
                    net['Last Seen'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    net.update(current_net) 

    persistent_networks.sort(key=lambda x: x['ESSID'].lower() if x['ESSID'] else "")
