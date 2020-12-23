from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout as do_logout
from django.contrib.auth import login as do_login
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from users.forms import LoginForm, ProfileForm, UserForm
from gestionPermisos.forms import UsuarioEmpleadoDisplayForm

# Create your views here.

def welcome(request):
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        return render(request, "users/welcome.html")
    # En otro caso redireccionamos al login
    return redirect('/users/login')

def register(request):
    return render(request, "users/register.html")

def login(request):
    # Creamos el formulario de autenticación vacío
    form = AuthenticationForm()
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = AuthenticationForm(data=request.POST)
        # Si el formulario es válido...
        if form.is_valid():
            # Recuperamos las credenciales validadas
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Verificamos las credenciales del usuario
            user = authenticate(username=username, password=password)

            # Si existe un usuario con ese nombre y contraseña
            if user is not None:
                # Hacemos el login manualmente
                do_login(request, user)
                # Y le redireccionamos a la portada correspondiente
                # Verificamos que el usuario tenga legajo asociado
                try:
                    conLegajo = user.usuarioempleado.uemEmpleado.legLegajo
                except ObjectDoesNotExist:
                    conLegajo = None
                if conLegajo is not None: 
                    return redirect('homeAgente')
                else:
                    return redirect('index')

    # Si llegamos al final renderizamos el formulario
    return render(request, "users/login.html", {'form': form})

def logout(request):
    # Finalizamos la sesión
    do_logout(request)
    # Redireccionamos a la portada
    return redirect('/')

@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
#        empleado_form = EmpleadoDisplayForm(request.POST, instance=)
        user_form = UserForm(request.POST, instance=request.user)         
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Se han modificado los datos de su configuración personal!')
            return redirect('/gestionPermisos')
        else:
            messages.error(request, 'Se han producido errores.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'users/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })