
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
import base64
import sys
from getpass import getpass

# se recibe el password en cadena y se derivaa una llave
def generar_llave_aes_from_password(password):
    password = password.encode('utf-8')
    derived_key = HKDF(algorithm=hashes.SHA256(),
                       length=32,
                       salt=None,
                       info=b'handshake data ',
                       backend=default_backend()).derive(password)
    return derived_key

########## Permite almacenar las llaves en un archivo ##########
def almacenar_llave(llave, iv):
    llave_str = base64.b64encode(llave) # convertir de binario a texto
    llave_str = llave_str.decode('utf-8')
    iv_str = base64.b64encode(iv).decode('utf-8')
    contenido = '%s#%s' % (llave_str, iv_str)
    archivo = open(path_salida, 'w')
    archivo.write(contenido)
    archivo.close()
# esta en lugar de almacenarlas en un archivp, almacenarlas en la base

def recuperar_llave(path_llave):
    archivo = open(path_llave)
    contenido = archivo.read()
    archivo.close()
    partes = contenido.split('#')
    llave = partes[0]
    iv = partes[1]
    llave = base64.b64decode(llave)# de cadena a binario
    iv = base64.b64decode(iv)
    return llave, iv
######################################################################


####################### Cifrar y descifrar ###########################
def cifrar(mensaje, llave_aes, iv):
    aesCipher = Cipher(algorithms.AES(llave_aes), modes.CTR(iv),
                       backend=default_backend())
    cifrador = aesCipher.encryptor()
    cifrado = cifrador.update(mensaje)
    cifrador.finalize()
    return cifradodef cifrar(mensaje, llave_aes, iv):
    aesCipher = Cipher(algorithms.AES(llave_aes), modes.CTR(iv),
                       backend=default_backend())
    cifrador = aesCipher.encryptor()
    cifrado = cifrador.update(mensaje)
    cifrador.finalize()
    return cifrado

def cifrar(passc, passwordm, iv):#obtener la contraseña maestra, iv(creado en el views)
    llave_aes = generar_llave_aes_from_password(passwordm))#expandir la contraseña para generar la llave
    aesCipher = Cipher(algorithms.AES(llave_aes), modes.CTR(iv),
                       backend=default_backend())
    cifrador = aesCipher.encryptor()
    cifrado = cifrador.update(mensaje)
    cifrador.finalize()
    return (cifrado.hex())


def descifrar(passc, passwordm, iv): #passc es la pas cifrada
    llave_aes = generar_llave_aes_from_password(password)
    aesCipher = Cipher(algorithms.AES(llave_aes), modes.CTR(iv),
                       backend=default_backend())
    descifrador = aesCipher.decryptor()
    plano = descifrador.update(cifrado)
    descifrador.finalize()
    return plano


def descifrar(cifrado, llave_aes, iv):
    aesCipher = Cipher(algorithms.AES(llave_aes), modes.CTR(iv),
                       backend=default_backend())
    descifrador = aesCipher.decryptor()
    plano = descifrador.update(cifrado)
    descifrador.finalize()
    return plano

####################### Cifrar y descifrar ###########################
#obtener la contraseña maestra, iv(creado en el views)
 #expandir la contraseña para generar la llave

################# Para cifrar y descifrar un archivo #################
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

        

#primer main 
def main_archivos():
    operacion = sys.argv[1] # generar nuevas llaves, cifrar archivo, descifrar archivo
    if operacion == 'generar':
        llave, iv = generar_llaves()
        path_llaves = sys.argv[2]
        almacenar_llave(path_llaves, llave, iv)
    elif operacion == 'cifrar':
        path_llaves = sys.argv[2]
        llave, iv = recuperar_llave(path_llaves)
        path_entrada = sys.argv[3]
        path_salida = sys.argv[4]
        cifrar_archivo(path_entrada, path_salida, llave, iv)
    elif operacion == 'descifrar':
        path_llaves = sys.argv[2]
        llave, iv = recuperar_llave(path_llaves)
        path_entrada = sys.argv[3]
        path_salida = sys.argv[4]
        descifrar_archivo(path_entrada, path_salida, llave, iv)
    else:
        print('opciÃ³n no perimitida, se permiten: generar, cifrar, descifrar')

    
if __name__ == '__main__':
    #mensaje = b'holas'
    #llave = os.urandom(32)
    #iv = os.urandom(16)
    #cifrado = cifrar(mensaje, llave, iv)
    #print(cifrado)
    #plano=descifrar(cifrado, llave, iv)
    #print(plano)
    #cifrar_archivo('cifradoSimetrico.py','cifrado', llave, iv )
    #descifrar_archivo('cifrado','origin.py', llave, iv )
   # operacion = sys.argv[1]
   # if operacion == 'cifrar':
    #    path_entrada = sys.argv[2]
     #   path_salida = sys.argv[3]
      #  password = getpass()
       # cifrar_archivo_password(path_entrada, path_salida, password)
    #elif operacion == 'descifrar':
     #   path_entrada = sys.argv[2]
      #  path_salida = sys.argv[3]
       # password = getpass()
        #descifrar_archivo_password(path_entrada, path_salida, password)
    password = 'passpass'
    llave = generar_llave_aes_from_password(password)
    print(llave.hex())

