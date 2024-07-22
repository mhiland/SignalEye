import threading
from abc import ABC, abstractmethod

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
        encryption_info = self.network.get('Encryption Info', {})
        encryption_status = encryption_info.get('Encryption', 'Unknown')
        
        if encryption_status == 'Enabled':
            wpa3_info = encryption_info.get('WPA3')
            wpa2_info = encryption_info.get('WPA2')
            wpa_info = encryption_info.get('WPA')
            wep_info = encryption_info.get('WEP')

            if wpa3_info:
                return "WPA3"            
            elif wpa2_info:
                return "WPA2"
            elif wpa_info:
                return "WPA"
            elif wep_info == "Enabled":
                return "WEP"
            else:
                return "Unknown"
        else:
            return "Open"

    def get_address(self):
        return self.network.get('Address', 'Unknown')

    def get_channel(self):
        return self.network.get('Channel', 'Unknown')

    def get_signal_strength(self):
        return self.network.get('Signal', 'Unknown')

    def get_manufacturer(self):
        return self.network.get('Manufacturer', 'Unknown')

    def mark_suspicious(self, reason):
        self.network['Suspicious'] = True
        if 'Reason' in self.network:
            existing_reasons = self.network['Reason'].split('; ')
            if reason not in existing_reasons:
                self.network['Reason'] += f"; {reason}"
        else:
            self.network['Reason'] = reason

# Factory pattern
class NetworkFactory:
    @staticmethod
    def create_network(network_data):
        return NetworkAdapter(network_data)

# Concurrency pattern
class NetworkScanner(threading.Thread):
    HAK5_MAC_PREFIXES = ['00:13:37', '02:CA:FF', '02:13:37']
    RASPBERRY_MAC_PREFIXES = ['28:CD:C1', 'B8:27:EB', 'D8:3A:DD', 'DC:A6:32', 'E4:5F:01', '2C:CF:67']

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
        signal_strength = network.get_signal_strength()

        with self.lock:
            # Check for hidden SSID
            if not ssid:
                network.mark_suspicious('Hidden SSID')
                self.observer.update(network.network)
                self.seen_addresses.add(address)
            # Check for short or unusual SSID names
            elif len(ssid) < 3:
                network.mark_suspicious('Short or unusual SSID name')
                self.observer.update(network.network)
                self.seen_addresses.add(address)

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
            if channel not in map(str, range(1, 12)):
                network.mark_suspicious('Unusual channel')
                self.observer.update(network.network)
                self.seen_addresses.add(address)

            # Manually check for known Hak5 MAC address prefixes
            if any(address.startswith(prefix) for prefix in self.HAK5_MAC_PREFIXES):
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
            for ssid_list in self.ssid_counts.values():
                unique_ssids = set(ssid_list)
                if len(unique_ssids) > 1:
                    for ssid in unique_ssids:
                        for net_data in self.networks:
                            network = NetworkFactory.create_network(net_data)
                            if network.get_ssid() == ssid and network.get_address() in self.ssid_counts:
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
