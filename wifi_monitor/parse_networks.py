def parse_networks(scan_output):
    networks = []
    lines = scan_output.split('\n')
    current_network = {}
    for line in lines:
        line = line.strip()
        if line.startswith('Cell'):
            if current_network:
                networks.append(current_network)
                current_network = {}
            address = line.split(' ')[4]
            current_network['Address'] = address
        elif 'ESSID' in line:
            essid = line.split(':')[1].strip().strip('"')
            current_network['ESSID'] = essid
        elif 'Frequency' in line:
            frequency = line.split(':')[1].split()[0]
            current_network['Frequency'] = frequency
        elif 'Quality' in line and 'Signal level' in line:
            quality = line.split('=')[1].split('/')[0]
            signal_level = line.split('Signal level=')[1].split(' ')[0]
            current_network['Quality'] = quality
            current_network['Signal level'] = signal_level
        elif 'Channel' in line:
            channel = line.split(':')[1].strip()
            current_network['Channel'] = channel
        elif 'Encryption key' in line:
            encryption = 'WPA/WPA2' if 'on' in line else 'Open'
            current_network['Encryption'] = encryption

    if current_network:
        networks.append(current_network)
    
    return networks
