import jsonschema
from jsonschema import validate

# Example schema for the JSON structure
schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "ESSID": {"type": "string"},
            "Address": {"type": "string"},
            "Manufacturer": {"type": "string"},
            "Frequency": {"type": "string"},
            "Channel": {"type": "string"},
            "Quality": {"type": "string"},
            "SignalLevel": {"type": "string"},
            "Mode": {"type": "string"},
            "EncryptionInfo": {
                "type": "object",
                "properties": {
                    "Encryption": {"type": "string"},
                    "WPA3": {"type": ["string", "null"]},
                    "WPA2": {
                        "type": ["object", "null"],
                        "properties": {
                            "GroupCipher": {"type": "string"},
                            "PairwiseCiphers": {"type": "string"},
                            "AuthenticationSuites": {"type": "string"}
                        },
                        "additionalProperties": False
                    },
                    "WPA": {
                        "type": ["object", "null"],
                        "properties": {
                            "GroupCipher": {"type": "string"},
                            "PairwiseCiphers": {"type": "string"},
                            "AuthenticationSuites": {"type": "string"}
                        },
                        "additionalProperties": False
                    },
                    "WEP": {"type": ["string", "null"]}
                },
                "required": ["Encryption"],
                "additionalProperties": False
            },
            "Active": {"type": "boolean"},
            "LastSeen": {"type": "string", "format": "date-time"},
            "FirstSeen": {"type": "string", "format": "date-time"},
            "Suspicious": {"type": "boolean"},
            "Reason": {"type": "string"}
        },
        "required": ["Address", "Manufacturer", "Frequency", "Channel", "Quality", "SignalLevel", "EncryptionInfo", "Active", "LastSeen", "FirstSeen"],
        "additionalProperties": False
    }
}
