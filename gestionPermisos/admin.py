from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from gestionPermisos.models import Empleado,Sector,Estado,Permiso,TipoPermiso,ResponsableSector,SubrogaResponsable,UsuarioEmpleado, Feriado
from users.models import Profile

class ProfileAdmin(admin.ModelAdmin):
    model=Profile
    readonly_fields=('nombreUsuario','legajo',)

class ResponsableSectorInLine(admin.StackedInline):
    model=ResponsableSector
    can_delete=True
    verbose_name_plural="Sectores a cargo"
    fields=('resSector',)
    extra = 1

class UserAdmin(BaseUserAdmin):
    inlines=(ResponsableSectorInLine,)

class SubrogaResponsableInline(admin.TabularInline):
    model=SubrogaResponsable
    can_delete=True
    verbose_name_plural="Subrogantes"
    fields=('subUsuario','subFechaDesde','subFechaHasta',)
    extra=1

class ResponsableSectorAdmin(admin.ModelAdmin):
    inlines=(SubrogaResponsableInline,)
    list_display=('resUsuario','resSector','resUsrSubrogante',)
    readonly_fields=('resUsrSubrogante',)

class UsuarioEmpleadoInline(admin.StackedInline):
    model=UsuarioEmpleado 
    can_delete=True
    verbose_name_plural="Usuario Asociado"
    fields=('uemUsuario',)

class EmpleadoAdmin(admin.ModelAdmin):
    inlines=(UsuarioEmpleadoInline,)
    list_display=('legLegajo','legNombre','legEmailLaboral','legActivo','legUsuario')

class PermisoAdmin(admin.ModelAdmin):
    list_display=['perIdpermiso','perUsuario','perSectorUsuario']
    readonly_fields=('perSectorUsuario','perUltimoEstado',)

class UsuarioEmpleadoAdmin(admin.ModelAdmin):
    list_display=['uemUsuario','uemEmpleado']

# Register your models here.
admin.site.unregister(User)
admin.site.register(User,UserAdmin)

admin.site.register(Profile,ProfileAdmin)
admin.site.register(Empleado,EmpleadoAdmin)
admin.site.register(Sector)
admin.site.register(Estado)
admin.site.register(Permiso,PermisoAdmin)
admin.site.register(TipoPermiso)
admin.site.register(ResponsableSector,ResponsableSectorAdmin)
admin.site.register(SubrogaResponsable)
admin.site.register(UsuarioEmpleado,UsuarioEmpleadoAdmin)
admin.site.register(Feriado)

