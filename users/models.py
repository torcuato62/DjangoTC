from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from gestionPermisos.models import UsuarioEmpleado 

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    mostrarNombre = models.CharField(max_length=20,null=True,blank=True)
    maxPermisos = models.IntegerField(default=5)
    def _get_nombre(self):
        if self.mostrarNombre is None:
            return self.user.get_full_name()
        else:
            return self.mostrarNombre
    def _get_legajo(self):
        usr = self.user
        try:
            legajo = usr.usuarioempleado.uemEmpleado.legLegajo
        except ObjectDoesNotExist:
            legajo = 'Sin Legajo'
        return legajo
    def _get_genero(self):
        usr = self.user
        try:
            genero = usr.usuarioempleado.uemEmpleado.legGenero
        except ObjectDoesNotExist:
            genero = ''
        return genero 
    def __str__(self):
        return '%s %s' % (self.user, self.mostrarNombre)

    nombreUsuario = property(_get_nombre)
    legajo = property(_get_legajo)
    genero = property(_get_genero)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except ObjectDoesNotExist:
        Profile.objects.create(user=instance)
