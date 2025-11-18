from pathlib import Path
from typing import Dict
import json
import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

_KEY_FILE = Path("private.pem")


def sign_payload(payload: Dict) -> str:
    if not _KEY_FILE.is_file():
        raise FileNotFoundError("Error: lack private.pem")

    key_bytes = _KEY_FILE.read_bytes()
    try:
        private_key = serialization.load_pem_private_key(
            key_bytes, password=None)
    except ValueError as e:
        raise ValueError("Error: The format of the private key is incorrect") from e

    data = json.dumps(payload, separators=(",", ":")).encode()
    signature = private_key.sign(
        data,
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    return base64.b64encode(signature).decode()
