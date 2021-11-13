from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.backends import default_backend
# generar hash seguro

def cif(password, salt):
    passbytes = password.encode('utf-8')
    kdf = Scrypt(salt=salt, length=32,
               n=2**14, r=8, p=1,
               backend=default_backend())
    key = kdf.derive (passbytes)
    return (key.hex())

def des(password,key,salt):
    passbin = password.encode('utf-8')
    keybin = bytes.fromhex(key)
    
    kdf = Scrypt(salt=salt, length=32,
               n=2**14, r=8, p=1,
               backend=default_backend())
    try:
        kdf.verify(passbin, keybin)
        return True
    except:
        return False
