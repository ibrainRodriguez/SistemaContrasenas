
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
import base64
import sys
from getpass import getpass


def generar_llave_aes_from_password(password):
    password = password.encode('utf-8')
    derived_key = HKDF(algorithm=hashes.SHA256(),
                       length=32,
                       salt=None,
                       info=b'handshake data ',
                       backend=default_backend()).derive(password)
    return derived_key


def almacenar_llave(llave, iv):
    llave_str = base64.b64encode(llave) # convertir de binario a texto
    llave_str = llave_str.decode('utf-8')
    iv_str = base64.b64encode(iv).decode('utf-8')
    contenido = '%s#%s' % (llave_str, iv_str)
    archivo = open(path_salida, 'w')
    archivo.write(contenido)
    archivo.close()


def recuperar_llave(path_llave):
    archivo = open(path_llave)
    contenido = archivo.read()
    archivo.close()
    partes = contenido.split('#')
    llave = partes[0]
    iv = partes[1]
    llave = base64.b64decode(llave)
    iv = base64.b64decode(iv)
    return llave, iv


def cifrar(mensaje, llave_aes, iv):
    aesCipher = Cipher(algorithms.AES(llave_aes), modes.CTR(iv),
                       backend=default_backend())
    cifrador = aesCipher.encryptor()
    cifrado = cifrador.update(mensaje)
    cifrador.finalize()
    return cifrado



def descifrar(cifrado, llave_aes, iv):
    aesCipher = Cipher(algorithms.AES(llave_aes), modes.CTR(iv),
                       backend=default_backend())
    descifrador = aesCipher.decryptor()
    plano = descifrador.update(cifrado)
    descifrador.finalize()
    return plano

########## Para cifrar y descifrar un archivo ##########
def cifrar_archivo(path_entrada: str, path_salida: str, llave, iv):
    archivo = open(path_entrada, 'br')
    contenido = archivo.read()
    archivo.close()
    cifrado = cifrar(contenido, llave, iv)
    archivo = open(path_salida, 'bw')
    archivo.write(cifrado)
    archivo.close()
    

def descifrar_archivo(path_entrada: str, path_salida: str, llave, iv):
    archivo = open(path_entrada, 'br')
    contenido = archivo.read()
    archivo.close()
    plano = descifrar(contenido, llave, iv)
    archivo = open(path_salida, 'bw')
    archivo.write(plano)
    archivo.close()
########################################################

def generar_llaves():
    llave = os.urandom(32)
    iv = os.urandom(16)
    return llave, iv
    

def cifrar_archivo_password(path_entrada: str, path_salida: str, password):
    llave = generar_llave_aes_from_password(password)
    iv = os.urandom(16)
    archivo = open(path_entrada, 'br')
    contenido = archivo.read()
    archivo.close()
    cifrado = cifrar(contenido, llave, iv)
    archivo = open(path_salida, 'bw')
    archivo.write(iv)
    archivo.write(cifrado)
    archivo.close()


def descifrar_archivo_password(path_entrada: str, path_salida: str, password):
    llave = generar_llave_aes_from_password(password)
    archivo = open(path_entrada, 'br')
    contenido = archivo.read()
    archivo.close()
    iv = contenido[:16]
    contenido = contenido[16:]
    plano = descifrar(contenido, llave, iv)
    archivo = open(path_salida, 'bw')
    archivo.write(plano)
    archivo.close()    
    
if __name__ == '__main__':
    mensaje = b'holas'
    llave = os.urandom(32)
    iv = os.urandom(16)
    cifrado = cifrar(mensaje, llave, iv)
    print(cifrado)
    plano=descifrar(cifrado, llave, iv)
    print(plano)
    cifrar_archivo('cifradoSimetrico.py','cifrado', llave, iv )
    descifrar_archivo('cifrado','origin.py', llave, iv )
    

