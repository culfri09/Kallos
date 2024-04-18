import nacl.secret
import nacl.utils
from nacl.encoding import Base64Encoder


def encrypt(message, key):
    box = nacl.secret.SecretBox(key)
    encrypted = box.encrypt(message.encode(), encoder=Base64Encoder)
    return encrypted.decode('utf-8')

def decrypt(encrypted_message, key):
    box = nacl.secret.SecretBox(key)
    decrypted = box.decrypt(encrypted_message.encode(), encoder=Base64Encoder)
    return decrypted.decode('utf-8')

def generate_key():
    return nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)
