import re
import os
#cadena = input("ingresar cadena: ")

def validar_password(password):
    try:
        re.match('^(?=(?:.*\d))(?=.*[A-Z])(?=.*[a-z])(?=.*[.,*!?@¿¡/#$%&])\S{8,20}$',password)
        return True
    except:
        return False
                                   
#if __name__ == '__main__':
 #   password = 'Pass$segura2'
    
 #   res = validar_password(password)
 #   print(res)
