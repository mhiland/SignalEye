def detect_suspicious_networks(networks):
    ssid_counts = {}
    suspicious_networks = []
    seen_addresses = set()

    for net in networks:
        ssid = net.get('ESSID', '')
        encryption = net.get('Encryption', 'Unknown')
        address = net.get('Address', 'Unknown')
        
        # Check for multiple networks with the same SSID
        if ssid not in ssid_counts:
            ssid_counts[ssid] = []
        ssid_counts[ssid].append(address)

        # Check for open networks
        if encryption == 'Open' and address not in seen_addresses:
            net['Suspicious'] = True
            net['Reason'] = 'Open network'
            suspicious_networks.append(net)
            seen_addresses.add(address)

        # Check for very short or unusual SSID names
        if len(ssid) < 3 and ssid and address not in seen_addresses:
            net['Suspicious'] = True
            net['Reason'] = 'Short or unusual SSID name'
            suspicious_networks.append(net)
            seen_addresses.add(address)

    # Add networks with duplicate SSIDs to suspicious list
    for ssid, addresses in ssid_counts.items():
        if len(addresses) > 1:
            for net in networks:
                if net['ESSID'] == ssid and net['Address'] not in seen_addresses:
                    net['Suspicious'] = True
                    net['Reason'] = 'SSID spoofing'
                    suspicious_networks.append(net)
                    seen_addresses.add(net['Address'])

    return suspicious_networks
