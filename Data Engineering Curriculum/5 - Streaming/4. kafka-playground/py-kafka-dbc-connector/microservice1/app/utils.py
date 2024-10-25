import json

def key_deserializer(key_bytes):
    return key_bytes.decode('utf-8') if key_bytes else None

def value_deserializer(value_bytes):
    return json.loads(value_bytes.decode('utf-8')) if value_bytes else None
