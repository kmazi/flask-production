"""Define utility functions for user/auth views."""

import base64
from hashlib import scrypt
from os import urandom
from typing import Tuple


def _generate_salt(no_bytes=32) -> bytes:
    salt = urandom(no_bytes)
    salt = base64.b64encode(salt)
    return salt


def hash_password(password: str, salt: bytes | None = None,
                  n=4096, r=4, p=1) -> Tuple[str, str]:
    salt = salt or _generate_salt()
    hash = scrypt(password.encode(), salt=salt, n=n, r=r, p=p)
    decoded_hash = base64.b64encode(hash).decode()
    decoded_salt = salt.decode()
    return decoded_hash, decoded_salt


def verify_password(password: str, pass_hash: str, salt: str):
    decoded_hashed_password, _ = hash_password(password=password,
                                               salt=salt.encode())
    return decoded_hashed_password == pass_hash
