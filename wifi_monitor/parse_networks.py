from parse_oui_database import lookup_manufacturer

def parse_networks(scan_output):
    networks = {}
    lines = scan_output.split('\n')
    current_network = {}

    for line in lines:
        line = line.strip()
        if line.startswith('Cell'):
            if current_network:
                address = current_network['Address']
                # Update existing entry if already exists
                if address in networks:
                    networks[address].update(current_network)
                else:
                    networks[address] = current_network
                current_network = {}
            address = line.split()[4]
            current_network['Address'] = address
            if address:
                manufacturer = lookup_manufacturer(address)
                current_network['Manufacturer'] = manufacturer
        elif 'Frequency' in line and 'Channel' in line:
            frequency = line.split('Frequency:')[1].split(' ')[0]
            channel = line.split('Channel')[1].split(')')[0].strip()
            current_network['Frequency'] = frequency
            current_network['Channel'] = channel
        elif 'Quality' in line and 'Signal level' in line:
            quality = line.split('=')[1].split('/')[0]
            signal_level = line.split('Signal level=')[1].split(' ')[0]
            current_network['Quality'] = quality
            current_network['Signal level'] = signal_level
        elif 'Encryption key' in line:
            encryption_key_status = line.split(':')[1].strip()
            encryption = 'Open' if encryption_key_status == 'off' else 'Encrypted'
            current_network['Encryption'] = encryption
        elif 'ESSID' in line:
            essid = line.split(':')[1].strip().strip('"')
            current_network['ESSID'] = essid
        elif 'Mode' in line:
            mode = line.split(':')[1].strip()
            if mode == 'Unknown/bug':
                mode = 'Unknown'
            current_network['Mode'] = mode

    if current_network:
        address = current_network['Address']
        if address in networks:
            networks[address].update(current_network)
        else:
            networks[address] = current_network

    return list(networks.values())
