"""
Module for encryption methods.
"""
import nacl.secret
import nacl.utils
from nacl.encoding import Base64Encoder

def encrypt(message, key):
    """
    Encrypts the given message using the provided key.

    Args:
        message (str): The message to encrypt.
        key (bytes): The encryption key.

    Returns:
        str: The encrypted message.
    """
    box = nacl.secret.SecretBox(key)
    encrypted = box.encrypt(message.encode(), encoder=Base64Encoder)
    return encrypted.decode('utf-8')

def decrypt(encrypted_message, key):
    """
    Decrypts the given encrypted message using the provided key.

    Args:
        encrypted_message (str): The encrypted message.
        key (bytes): The decryption key.

    Returns:
        str: The decrypted message.
    """
    box = nacl.secret.SecretBox(key)
    decrypted = box.decrypt(encrypted_message.encode(), encoder=Base64Encoder)
    return decrypted.decode('utf-8')

def generate_key():
    """
    Generates a random encryption key.

    Returns:
        bytes: The generated encryption key.
    """
    return nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)
