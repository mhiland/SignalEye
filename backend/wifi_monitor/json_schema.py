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
            "Signal Level": {"type": "string"},
            "Mode": {"type": "string"},
            "Encryption Info": {
                "type": "object",
                "properties": {
                    "Encryption": {"type": "string"},
                    "WPA3": {"type": ["string", "null"]},
                    "WPA2": {
                        "type": ["object", "null"],
                        "properties": {
                            "Group Cipher": {"type": "string"},
                            "Pairwise Ciphers": {"type": "string"},
                            "Authentication Suites": {"type": "string"}
                        },
                        "additionalProperties": False
                    },
                    "WPA": {
                        "type": ["object", "null"],
                        "properties": {
                            "Group Cipher": {"type": "string"},
                            "Pairwise Ciphers": {"type": "string"},
                            "Authentication Suites": {"type": "string"}
                        },
                        "additionalProperties": False
                    },
                    "WEP": {"type": ["string", "null"]}
                },
                "required": ["Encryption"],
                "additionalProperties": False
            },
            "Active": {"type": "boolean"},
            "Last Seen": {"type": "string", "format": "date-time"},
            "First Seen": {"type": "string", "format": "date-time"},
            "Suspicious": {"type": "boolean"},
            "Reason": {"type": "string"}
        },
        "required": ["Address", "Manufacturer", "Frequency", "Channel", "Quality", "Signal Level", "Encryption Info", "Active", "Last Seen", "First Seen"],
        "additionalProperties": False
    }
}
