"""projectsegura URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from projectsegura.views import registrar_usuario, iniciar_sesion, registrar_credencial, ver_detalles_credencial, ver_listado_cuentas, editar_credencial, compartir, salir_login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registrar',registrar_usuario),
    path('iniciar_sesion',iniciar_sesion),
    path('registrar_credencial',registrar_credencial),
    path('ver_listado', ver_listado_cuentas),
    path('ver_detalles_credencial', ver_detalles_credencial),
    path('editar_credencial',editar_credencial),
    path('compartir', compartir),
    path('logout', salir_login)
]
