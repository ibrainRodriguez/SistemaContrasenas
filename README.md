# Sistema Contrasenas Desarrolado en Django
Proyecto sistema de administracion de contraseñas, de la experiencia educativa Programacion Segura

# Descripcion
El proyecto final de la Experiencia Educativa Programación Segura,
consiste en desarrollar una plataforma web que permita el
almacenamiento y recuperación segura de credenciales asociadas a
cuentas que los usuarios del sistema poseen en otros sistemas, esto
es, un sistema de administración de contraseñas. Este tipo de sistemas
le permite esencialmente a los usuarios tener contraseñas diferentes
para cada cuenta que posean, sin la necesidad de tener que recordarlas
todas.


# Requisitos funcionales
El sistema cuentan con las siguientes funcionalidades:

+ Registrar usuario: se captura información de identificación, esto
  es, nombre completo, usuario y contraseña, así como información de
  contacto como correo electrónico
+ Identificar usuario (login): se valida usuario y contraseña para
  determinar la identidad del usuario y darle acceso al repositorio de
  credenciales correspondiente
+ Registrar credencial: le permite a los usuarios crear asociaciones
  entre cuentas y credenciales. Los datos de registro son los
  siguientes:
  * Nombre de la cuenta
  * Usuario asociado
  * Contraseña asociada: se tiene la opción de auto-generar de forma
    aleatoria la contraseña
  * URL del sistema asociado a la cuenta
  * Detalles extra
+ Editar credencial: permite actualizar la información de registro
  para una entrada
+ Ver listado de cuentas con credenciales registradas: al interactuar
  con un elemento de la lista se pueden desplegar detalles del
  elemento o bien editarlo
+ Ver detalle de credencial: se despliega la información registrada de
  la cuenta
+ Compartir con otro usuario el repositorio de contraseñas en caso de
  emergencia: permite que en caso de algún accidente o fatalidad
  usuarios de confianza puedan recuperar las credenciales de otro
  usuario sin necesidad de conocer su contraseña
