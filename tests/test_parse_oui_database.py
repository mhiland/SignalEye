from parse_oui_database import OUILookup
import pytest
import sys
import os
os.environ['UNIT_TESTING'] = 'True'
test_file_dir = os.path.dirname(os.path.abspath(__file__))
module_path = os.path.abspath(os.path.join(
    test_file_dir, '../backend/wifi_monitor'))
sys.path.insert(0, module_path)


def test_similarity_mac():
    mac1 = "B8:4E:3F:7B:03:51"
    essid1 = "BC Group 2024"
    mac2 = "BA:4E:3F:7B:03:52"
    essid2 = "BC Group 2024BC -5G"

    _ouilookup_instance = OUILookup()
    mac_similarity_score = _ouilookup_instance.similarity(mac1, mac2)
    essid_similarity_score = _ouilookup_instance.similarity(essid1, essid2)
    combined_score = (mac_similarity_score + essid_similarity_score) / 2

    assert mac_similarity_score == pytest.approx(0.8334, 0.0001)
    assert essid_similarity_score == pytest.approx(0.8125, 0.0001)
    assert combined_score == pytest.approx(0.8229, 0.0001)


def test_non_similarity_mac():
    mac1 = "A8:A8:A8:A8:A8:A8"
    essid1 = "TELUS5555"
    mac2 = "B9:B9:B9:B9:B9:B9"
    essid2 = "TELUS6666"

    _ouilookup_instance = OUILookup()
    mac_similarity_score = _ouilookup_instance.similarity(mac1, mac2)
    essid_similarity_score = _ouilookup_instance.similarity(essid1, essid2)
    combined_score = (mac_similarity_score + essid_similarity_score) / 2

    assert mac_similarity_score <= 0.0
    assert essid_similarity_score == pytest.approx(0.5556, 0.0001)
    assert combined_score < 0.28


@pytest.fixture
def validator():
    return OUILookup()


@pytest.mark.parametrize("mac", [
    "00:1A:2B:3C:4D:5E",
    "FF:FF:FF:FF:FF:FF",
    "01:23:45:67:89:AB"
])
def test_valid_mac_addresses(validator, mac):
    assert validator.is_mac_address(mac)


@pytest.mark.parametrize("mac", [
    "00:1A:2B:3C:4D",  # Too short
    "00:1A:2B:3C:4D:5E:6F",  # Too long
    "00:1G:2H:3I:4J:5K",  # Invalid characters
    "001A:2B:3C:4D:5E",  # Missing colon
    "00:1A:2B:3C:4D:ZZ"   # Invalid last byte
])
def test_invalid_mac_addresses(validator, mac):
    assert not validator.is_mac_address(mac)
