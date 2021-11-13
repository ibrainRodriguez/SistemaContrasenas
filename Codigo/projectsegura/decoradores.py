from django.shortcuts import redirect





def login_requerido(vista):
    def intena(request, *args, **kwargs):
        logueado = request.session.get('logueado', False)
        if not logueado:
            return redirect('/iniciar_sesion')
        return vista(request,*args, **kwargs) #continuar ejecucion normal
    return intena

def login_requeridom(vista):
    def intena(request, *args, **kwargs):
        logueado = request.session.get('logueado', False)
        tipou = request.session.get('tusuario','')
        if not logueado:
            return redirect('/loginma')
        if tipou == 'Alumno':
            return redirect('/mostrar_alumnos')
        return vista(request,*args, **kwargs) #continuar ejecucion normal
    return intena

def login_requeridoa(vista):
    def intena(request, *args, **kwargs):
        logueado = request.session.get('logueado', False)
        tipou = request.session.get('tusuario','')
        if not logueado:
            return redirect('/loginma')
        if tipou == 'Maestro':
            return redirect('/mostrar_maestros')
        return vista(request,*args, **kwargs) #continuar ejecucion normal
    return intena