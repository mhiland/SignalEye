import threading
from abc import ABC, abstractmethod
import logging
import logging_config

# Observer pattern


class Observer(ABC):
    @abstractmethod
    def update(self, network):
        pass


class SuspiciousNetworkObserver(Observer):
    def __init__(self):
        self.suspicious_networks = []
        self.lock = threading.Lock()

    def update(self, network):
        with self.lock:
            self.suspicious_networks.append(network)


# Adapter pattern
class NetworkAdapter:
    def __init__(self, network):
        self.network = network

    def get_ssid(self):
        return self.network.get('ESSID', '')

    def get_encryption(self):
        encryption_info = self.network.get('EncryptionInfo', {})
        encryption_status = encryption_info.get('Encryption', 'Unknown')
        return encryption_status

    def get_address(self):
        return self.network.get('Address', 'Unknown')

    def get_channel(self):
        return self.network.get('Channel', 'Unknown')

    def get_frequency(self):
        return self.network.get('Frequency', 'Unknown')

    def get_signal_strength(self):
        return self.network.get('SignalLevel', 'Unknown')

    def get_manufacturer(self):
        return self.network.get('Manufacturer', 'Unknown')

    def mark_suspicious(self, reason):
        self.network['Suspicious'] = True
        if 'Reason' in self.network:
            existing_reasons = self.network['Reason'].split('; ')
            if reason not in existing_reasons:
                self.network['Reason'] += f"; {reason}"
                logging.info(
                    f"Suspicious Network: SSID={self.get_ssid()}, MAC={self.get_address()}, Reason={reason}")

        else:
            self.network['Reason'] = reason
            logging.info(
                f"Suspicious Network: SSID={self.get_ssid()}, MAC={self.get_address()}, Reason={reason}")

# Factory pattern


class NetworkFactory:
    @staticmethod
    def create_network(network_data):
        return NetworkAdapter(network_data)


# Concurrency pattern
class NetworkScanner(threading.Thread):
    HAK5_MAC_PREFIXES = ['00:13:37', '02:CA:FF', '02:13:37']
    RASPBERRY_MAC_PREFIXES = [
        '28:CD:C1',
        'B8:27:EB',
        'D8:3A:DD',
        'DC:A6:32',
        'E4:5F:01',
        '2C:CF:67']

    def __init__(self, networks, observer):
        threading.Thread.__init__(self)
        self.networks = networks
        self.observer = observer
        self.ssid_counts = {}
        self.seen_addresses = set()
        self.lock = threading.Lock()

    def run(self):
        for net_data in self.networks:
            network = NetworkFactory.create_network(net_data)
            self.check_network(network)
        self.check_duplicate_ssids()

    def check_network(self, network):
        ssid = network.get_ssid()
        encryption = network.get_encryption()
        address = network.get_address()
        channel = network.get_channel()
        frequency = network.get_frequency()
        signal_strength = network.get_signal_strength()

        with self.lock:
            # Check for hidden SSID
            # if not ssid:
            #     network.mark_suspicious('Hidden SSID')
            #     self.observer.update(network.network)
            #     self.seen_addresses.add(address)
            # # Check for short or unusual SSID names
            # elif len(ssid) < 3:
            #     network.mark_suspicious('Short or unusual SSID name')
            #     self.observer.update(network.network)
            #     self.seen_addresses.add(address)

            # Check for open networks
            if encryption == 'Open':
                network.mark_suspicious('Open network')
                self.observer.update(network.network)
                self.seen_addresses.add(address)

            # Check for weak encryption
            if encryption == 'WEP':
                network.mark_suspicious('Weak encryption (WEP)')
                self.observer.update(network.network)
                self.seen_addresses.add(address)

            if encryption == 'WPA':
                network.mark_suspicious('Weak encryption (WPA)')
                self.observer.update(network.network)
                self.seen_addresses.add(address)

            # Check for abnormally high signal strength
            try:
                signal_strength_value = int(signal_strength)
                if signal_strength_value > -30:
                    network.mark_suspicious('Abnormally high signal strength')
                    self.observer.update(network.network)
                    self.seen_addresses.add(address)
            except ValueError:
                pass  # Ignore invalid signal strength values

            # Check for unusual channels
            # Channels 1 to 11 as strings. 12,13,14 uncommon or restricted
            all_channels_24ghz = list(map(str, range(1, 12)))

            highly_suspicious_channels = list(map(str, [
                120, 124, 128,  # U-NII-2C channels less commonly used or requiring DFS
                169, 173, 177   # U-NII-3 channels often restricted or unauthorized
            ]))

            moderately_suspicious_channels = list(map(str, [
                52, 56, 60, 64,     # U-NII-2A channels requiring DFS
                100, 104, 108, 112,  # U-NII-2C channels requiring DFS
                # Remaining U-NII-2C and U-NII-3 channels of moderate concern
                116, 165, 132, 136, 140, 144
            ]))

            channels_of_interest = list(map(str, [
                36, 40, 44, 48,     # U-NII-1 channels commonly used
                149, 153, 157, 161  # U-NII-3 channels commonly used
            ]))

            # Default value if no condition meets
            suspicious_message = None

            # Check if the channel is not in the valid channels list based on
            # the frequency
            if frequency.startswith('2'):
                if channel not in all_channels_24ghz:
                    if channel == "14":
                        suspicious_message = 'Restricted channel'
                    else:
                        suspicious_message = 'Unusual channel'
            elif frequency.startswith('5'):
                if channel in highly_suspicious_channels:
                    suspicious_message = 'Highly suspicious channel'
               # elif channel in moderately_suspicious_channels:
               #     suspicious_message = 'Moderately suspicious channel'
               # elif channel in channels_of_interest:
               #     suspicious_message = 'Channel of interest'

            if suspicious_message:
                network.mark_suspicious(suspicious_message)
                self.observer.update(network.network)
                self.seen_addresses.add(address)

            # Manually check for known Hak5 MAC address prefixes
            if any(address.startswith(prefix)
                   for prefix in self.HAK5_MAC_PREFIXES):
                network.mark_suspicious('Possible WiFi Pineapple device')
                self.observer.update(network.network)
                self.seen_addresses.add(address)

            if ssid.startswith("Pineapple"):
                network.mark_suspicious('Possible WiFi Pineapple device')
                self.observer.update(network.network)
                self.seen_addresses.add(address)

            # Track SSID count per address for later analysis
            if address not in self.ssid_counts:
                self.ssid_counts[address] = []
            self.ssid_counts[address].append(ssid)

    def check_duplicate_ssids(self):
        with self.lock:
            # Collect addresses by SSID and frequency band
            unique_addresses_by_ssid = {}

            for net_data in self.networks:
                network = NetworkFactory.create_network(net_data)
                ssid = network.get_ssid()
                address = network.get_address()
                frequency = network.get_frequency()

                # Skip empty SSIDs
                if not ssid:
                    continue

                # Determine the frequency band (2.4 GHz or 5 GHz)
                frequency_band = '2.4GHz' if frequency.startswith('2') else '5GHz'

                if ssid not in unique_addresses_by_ssid:
                    unique_addresses_by_ssid[ssid] = {}

                if frequency_band not in unique_addresses_by_ssid[ssid]:
                    unique_addresses_by_ssid[ssid][frequency_band] = set()

                unique_addresses_by_ssid[ssid][frequency_band].add(address)

            # Check for duplicate SSIDs across different addresses within the same frequency band
            for ssid, frequency_bands in unique_addresses_by_ssid.items():
                for band, addresses in frequency_bands.items():
                    if len(addresses) > 1:  # More than one address using the same SSID and frequency band
                        for net_data in self.networks:
                            network = NetworkFactory.create_network(net_data)
                            if (network.get_ssid() == ssid and
                                network.get_address() in addresses and
                                (network.get_frequency().startswith('2') if band == '2.4GHz' else network.get_frequency().startswith('5'))):
                                network.mark_suspicious('SSID spoofing detected')
                                self.observer.update(network.network)
                                self.seen_addresses.add(network.get_address())


# Usage
def detect_suspicious_networks(networks):
    observer = SuspiciousNetworkObserver()
    scanner = NetworkScanner(networks, observer)
    scanner.start()
    scanner.join()
    return observer.suspicious_networks
