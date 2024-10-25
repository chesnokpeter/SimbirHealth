import hashlib

def hash(message: str) -> str:
    return hashlib.sha256(message.encode('utf-8')).hexdigest()