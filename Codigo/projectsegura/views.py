from django.http import HttpResponse
from django.template import Template,Context
from django.shortcuts import render,redirect
import os
from modelo import models
import base64
import datetime
from datetime import timezone
from pathlib import Path
from projectsegura.decoradores import login_requerido
from projectsegura.passHash import cif, des
import re
from projectsegura.cifradoSimetrico import generar_llave_aes_from_password,cifrar, descifrar

#----------------------------------------------------------------------------
import requests
    
def mandar_mensaje_bot_post(mensaje):
    token = os.environ.get('token')
    chat_id = os.environ.get('chat_id')
    datos = {'chat_id': chat_id, 'text': mensaje}
    url = 'https://api.telegram.org/bot'+ token +'/sendMessage'
    response = requests.post(url = url, data = datos)

#----------------------------------------------------------------

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

#----------------------------------------------------------------
def diferencia_tiempo(tiempoPasado):
    ahora = datetime.datetime.now(timezone.utc)
    diferencia = ahora - tiempoPasado
    return diferencia.seconds

#----------------------------------------------------------------
#Intentaer 3 intentos por menos de 1 mnuto te bloquea
def puede_intentar(ip):
    """ Determina si una ip puede volver a intentar enviar el formulario
        3 intentos maximo por minutos
        tiene efectos en la base de datos
    """
    #Primer caso la ip es nueva
    registro_guardado = models.intentos_por_ip.objects.filter(pk=ip)
    if not registro_guardado: #si no hay registros guardamos
        registro = models.intentos_por_ip(ip=ip, contador=1, ultima_peticion=datetime.datetime.now(timezone.utc))
        registro.save()
        return True
    registro_guardado = registro_guardado[0]
    diferencia_tiempo_segundos = diferencia_tiempo(registro_guardado.ultima_peticion)
    if diferencia_tiempo_segundos >= 60: #debemos resetear
        registro_guardado.ultima_peticion = datetime.datetime.now(timezone.utc)
        registro_guardado.contador = 1
        registro_guardado.save()
        return True
    else:
        if registro_guardado.contador < 3:
            registro_guardado.ultima_peticion = datetime.datetime.now(timezone.utc)
            registro_guardado.contador += 1
            registro_guardado.save()
            return True
        else:
            registro_guardado.ultima_peticion = datetime.datetime.now(timezone.utc)
            return False


#------------------------------------------------------------------------------
def nombre_exite(usuario1): #comprobar si el nombre de usuario esta repetido
    usuarioRepetido = models.usuarios.objects.filter(nombre=usuario1.nombre)
    if len(usuarioRepetido) > 0:
        return True
    return False

#----------------------------------------------------------------------------
def usuario_exite(usuario1): #comprobar si el usuario esta repetido
    usuarioRepetido = models.usuarios.objects.filter(usuario=usuario1.usuario)
    if len(usuarioRepetido) > 0:
        return True
    return False
#---------------------------------------------------------------------------
def tiene_errores_usuario(usuario1,contrac):
    errores = []  
    if nombre_exite(usuario1):
        errores.append('El Usuario %s ya existe' % usuario1.nombre)
    if usuario_exite(usuario1):
        errores.append('El Usuario %s ya existe' % usuario1.usuario)
    if usuario1.nombre == '':
        errores.append('Nombre vacio')
    if usuario1.usuario == '':
        errores.append('Usuario vacio')
    if usuario1.correo == '':
        errores.append('Correo vacio')
    if usuario1.contra == '':
        errores.append('Contraseña vacia')
    if usuario1.contra != contrac:
        errores.append('Las contraseñas no coinciden')
    if not re.match('^(?=(?:.*\d))(?=.*[A-Z])(?=.*[a-z])(?=.*[.,*!?@¿¡/#$%&])\S{8,20}$', usuario1.contra):
        errores.append('La contrasena debe cumplir las politicas')
    return errores


#----------------------------------------------------------------
def tiene_errores_credencial(credencial1):
    errores = []  
    if credencial1.nombre_cuenta == '':
        errores.append('Nombre de cuenta vacio')
    if credencial1.usuario_cuenta == '':
        errores.append('Usuario de cuenta vacio')
    if credencial1.contra_cuenta == '':
        errores.append('Contraseña vacia')
    if credencial1.url == '':
        errores.append('Url vacia')
    return errores

#----------------------------------------------------------------
def registrar_usuario(request):
    if request.method == 'GET':
        t = 'registrar.html'
        logueado = request.session.get('logueado', False) #redireccionar si ya estas logueado
        if logueado:
            return redirect('/ver_listado')
        return render(request,t)
    elif request.method == 'POST':
        t = 'registrar.html'

        nombre = request.POST.get('nombre','').strip()
        usuario = request.POST.get('nick','').strip()
        correo = request.POST.get('correo','').strip()
        contra = request.POST.get('contra','').strip()
        contrac = request.POST.get('contrac','').strip()

        usuariox = models.usuarios()
        usuariox.nombre = nombre
        usuariox.usuario = usuario
        usuariox.correo = correo
        usuariox.contra = contra

        errores = tiene_errores_usuario(usuariox, contrac)

        if not errores:
            salt = os.urandom(16)
            usuariox.contra = cif(contra, salt)
            salt = base64.b64encode(salt).decode('utf-8')
            print(salt)
            print(usuariox.contra)
            usuariox.salt = salt
            usuariox.save() 
            request.session['logueado'] = False
            return redirect('/iniciar_sesion')
        else:
            c = {'errores': errores, 'usuario': usuariox}
            return render(request,t,c)

#----------------------------------------------------------------

def iniciar_sesion(request):
    if request.method == 'GET':
        t = 'iniciar_sesion.html'
        logueado = request.session.get('logeado',False)
        if logueado:
            return redirect('/ver_listado')
        return render(request,t)
    elif request.method == 'POST':
        if request.POST.get("form_type") == 'formUno':
            usuariob = request.POST.get('usuario','').strip()
            contra = request.POST.get('password','').strip()
            ip = get_client_ip(request)

            if puede_intentar(ip):
                try:
                    usuarioc = models.usuarios.objects.get(usuario=usuariob)
                    saltbd = usuarioc.salt
                    salt = base64.b64decode(saltbd)
                    key = usuarioc.contra
                    contrades = des(contra,key,salt) # aqui verificas la contraseña cifrafa

                    if contrades:
                        codigo = base64.b64encode(os.urandom(6)).decode('utf-8')
                        usuariobd = models.usuarios.objects.get(usuario=usuariob)
                        usuariobd.codigo = codigo
                        usuariobd.duracion = datetime.datetime.now(timezone.utc)
                        usuariobd.save()
                        mandar_mensaje_bot_post(codigo)
                        t = 'iniciar_sesion.html'
                        c = {'okay': True, 'usuario': usuariob, 'contra': contra}
                        return render(request,t,c)
                    else:
                        t = 'iniciar_sesion.html'
                        errores = ['usuario o contraseña invalidos']
                        c = {'errores': errores, 'usuario': usuariob, 'contra': contra}
                        return render(request,t,c)

                except:
                    t = 'iniciar_sesion.html'
                    errores = ['usuario o contraseña invalidos']
                    c = {'errores': errores, 'usuario': usuariob, 'contra': contra}
                    return render(request,t,c)
            else:
                t = 'iniciar_sesion.html'
                error = ['Intentos Agotados Por favor Espere 1 minuto']
                c = {'errores': error}
                return render(request,t,c)
        elif request.POST.get("form_type") == 'formDos':
            usuariob = request.POST.get('usuario','').strip()
            contra = request.POST.get('password','').strip()
            codigou = request.POST.get('codigo').strip()
            usuariobd = models.usuarios.objects.get(usuario=usuariob)
            diferencia_tiempo_segundos = diferencia_tiempo(usuariobd.duracion)
            if diferencia_tiempo_segundos <= 180:
                if codigou == usuariobd.codigo:
                    request.session['logueado'] = True
                    request.session['usuario'] = usuariob
                    return redirect('/ver_listado')
                else:
                    t = 'iniciar_sesion.html'
                    error = ['Error el codigo no era el correcto']
                    c = {'okay':True, 'erroresf2': error, 'usuario': usuariob, 'contra': contra, 'codigo': codigou}
                    return render(request,t,c)
            else:
                usuariobd.duracion = datetime.datetime.now(timezone.utc)
                t = 'iniciar_sesion.html'
                error = ['Intentos Agotados Por favor Espere 3 minuto']
                c = {'errores': error, 'usuario': usuariob, 'contra': contra}
                return render(request,t,c)

#----------------------------------------------------------------
@login_requerido
def salir_login(request):
    request.session.flush()
    return redirect('/iniciar_sesion')

#---------------------------------------------------------------- 

@login_requerido
def registrar_credencial(request):
    if request.method == 'GET':
        t = 'registrarcredencial.html'
        return render(request,t)
    elif request.method == 'POST':
        if request.POST.get("form_type") == 'formUno':
            nomCuenta = request.POST.get('nomCuenta','').strip()
            usuarioC = request.POST.get('usuarioC','').strip()
            contrasena = request.POST.get('contrasena','').strip()
            url = request.POST.get('url','').strip()        

            t = 'registrarcredencial.html'
            c = {'okay':True, 'nomCuenta': nomCuenta, 'usuarioC': usuarioC, 'contrasena': contrasena, 'url': url}
            return render(request,t,c)
            
        elif request.POST.get("form_type") == 'formDos':
            nomCuenta = request.POST.get('nomCuenta','').strip()
            usuarioC = request.POST.get('usuarioC','').strip()
            contrasena = request.POST.get('contrasena','').strip()
            url = request.POST.get('url','').strip()
            contram = request.POST.get('contrasenaM','').strip()
            usuariocokie = request.session.get('usuario','').strip()

            try:
                usuariopw = models.usuarios.objects.get(usuario=usuariocokie)
                saltbd = usuariopw.salt
                salt = base64.b64decode(saltbd)
                key = usuariopw.contra
                contrades = des(contram,key,salt) # aqui verificas la contraseña cifrafa

                if contrades:
                    credencialx = models.credenciales()
                    credencialx.nombre_cuenta = nomCuenta
                    credencialx.usuario_cuenta = usuarioC
                    credencialx.contra_cuenta = contrasena
                    credencialx.url = url
                    credencialx.usuario_asociado = usuariopw
                
                    errores = tiene_errores_credencial(credencialx)

                    if not errores:
                        iv = os.urandom(16)
                        llave_aes = generar_llave_aes_from_password(contram)
                        contracif = cifrar(contrasena,llave_aes,iv)
                        contracif = base64.b64encode(contracif).decode('utf-8')
                        credencialx.contra_cuenta = contracif
                        iv = base64.b64encode(iv).decode('utf-8')
                        credencialx.iv = iv
                        credencialx.save()
                        return redirect('/ver_listado')
                    else:
                        t = 'registrarcredencial.html'
                        c = {'errores': errores, 'nomCuenta': nomCuenta, 'usuarioC': usuarioC, 'contrasena': contrasena, 'url': url}
                        return render(request,t,c)
                else:
                    t = 'registrarcredencial.html'
                    errores = ['Contraseña invalida']
                    c = {'errores': errores, 'nomCuenta': nomCuenta, 'usuarioC': usuarioC, 'contrasena': contrasena, 'url': url, 'contrasenaM': contram}
                    return render(request,t,c) 
            except:
                 t = 'registrarcredencial.html'
                 errores = ['Ocurrio un error, porfavor comunicate con el administrador']
                 c = {'errores': errores, 'nomCuenta': nomCuenta, 'usuarioC': usuarioC, 'contrasena': contrasena, 'url': url}
                 return render(request,t,c)
            
             

#-----------------------------------------------------------------
@login_requerido
def ver_detalles_credencial(request):
    if request.method == 'GET':
        t = 'verdetallescredencial.html'
        return render(request,t)
    elif request.method == 'POST':
        t = 'registrar.html'
        return render(request,t)

#----------------------------------------------------------------
@login_requerido
def editar_credencial(request):
    if request.method == 'GET':
        t = 'editarcredencial.html'
        return render(request,t)
    elif request.method == 'POST':
        t = 'registrar.html'
        return render(request,t)

#----------------------------------------------------------------
@login_requerido
def ver_listado_cuentas(request):
    if request.method == 'GET':
        t = 'verlistado.html'
        return render(request,t)
    elif request.method == 'POST':
        t = 'registrar.html'
        return render(request,t)

#----------------------------------------------------------------
@login_requerido
def compartir(request):
    if request.method == 'GET':
        t = 'compartir.html'
        return render(request,t)
    elif request.method == 'POST':
        t = 'registrar.html'
        return render(request,t)
