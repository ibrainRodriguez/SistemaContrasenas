
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
import base64
import sys
from getpass import getpass

###### se recibe el password en cadena y se derivaa una llave ######
def generar_llave_aes_from_password(password):
    password = password.encode('utf-8')
    derived_key = HKDF(algorithm=hashes.SHA256(),
                       length=32,
                       salt=None,
                       info=b'handshake data ',
                       backend=default_backend()).derive(password)
    return derived_key
#resultado de llave en binario


####################### Cifrar y descifrar ###########################

def cifrar(mesage,llavepas, iv):   
    llave_aes = generar_llave_aes_from_password(llavepas)
    mensaje = bytes(mesage,'utf-8')
    aesCipher = Cipher(algorithms.AES(llave_aes), modes.CTR(iv),
                       backend=default_backend())
    cifrador = aesCipher.encryptor()
    cifrado = cifrador.update(mensaje)
    cifrador.finalize()
    return base64.b64encode(cifrado).decode('utf-8')

def descifrar(cif, llavepas, iv): #passc es la pas cifrada
    llave_aes = generar_llave_aes_from_password(llavepas)
    aesCipher = Cipher(algorithms.AES(llave_aes), modes.CTR(iv),
                       backend=default_backend())
    descifrador = aesCipher.decryptor()
    plano = descifrador.update(cifrado)
    descifrador.finalize()
    return plano

def cifrarr(mesage, llave_aes, iv):
    mensaje = base64.b64decode(mesage)
    aesCipher = Cipher(algorithms.AES(llave_aes), modes.CTR(iv),
                       backend=default_backend())
    cifrador = aesCipher.encryptor()
    cifrado = cifrador.update(mensaje)
    cifrador.finalize()
    return cifrado

def descifrarr(cifrado1, llave_aes, iv1):
    cifrado = base64.b64decode(cifrado1)
    iv = base64.b64decode(iv1)
    aesCipher = Cipher(algorithms.AES(llave_aes), modes.CTR(iv),
                       backend=default_backend())
    descifrador = aesCipher.decryptor()
    plano = descifrador.update(cifrado)
    descifrador.finalize()
    return plano.decode('utf-8')

######################################################################



    
if __name__ == '__main__':
    print('~~~~~ Cifrado ~~~~~')
    passwordc = 'passpass'
    #passwordc = passwordc.decode('utf-8')
    passwordm = 'PasMaster#1'
    iv = os.urandom(16)
    print (base64.b64encode(iv).decode('utf-8'))
    #llave = os.urandom(32)
    #print(llave)
    llave = generar_llave_aes_from_password(passwordm)
    print(llave)
    #cifrado = cifrarr(passwordc,llave, iv)#cifrado ejemplo FUNCIONA
    cifrado = cifrar(passwordc,passwordm, iv)#cifrado modificado FUNCIONA
    print(cifrado)

    print('\n')
    print('----------------- Descifrado -------------------------')
    iv = 'C3299yC8laXPwp0xIXutaw=='
    llave = b'\x83\x95v\xdb\x1a\xf1\x18dT*\xf4\x1e\x12\xfd4NZ\xeb:\xe4\x1cU\xd2v-\x03\x16\xb0\x07\xcfE\xa3'
    cifrado = 'nABr+GRGRiw='
    descifrado = descifrarr(cifrado,llave, iv)#cifrado ejemplo
    #descifrado = descifrar(passwordc,passwordm, iv)#cifrado modificado
    print(descifrado)
    
    #iv = b'\x9c,\xbe q\x82l"Q\xe1\xa7\xef\xd1W\r\xdc'
    #cifradopas = b'\x85\xafV}\xbe\x91'
    
    #descifrado = descifrar(cifradopas, passwordm,iv)
    #print(descifrado)
