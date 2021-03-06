DOMAIN = "alveo"

SUPPORTED_STORAGE_KEYS = {
    'id': {
        'type': str,
        'required': False
    },
    'start': {
        'type': float,
        'required': True
    },
    'end': {
        'type': float,
        'required': True
    },
    'speaker': {
        'type': str,
        'required': True
    },
    'caption': {
        'type': str,
        'required': True
    },
    'cap_type': {
        'type': str,
        'required': False
    }
}
