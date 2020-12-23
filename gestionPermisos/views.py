from datetime import datetime, date
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.db.models import Q 
from django.views.generic import ListView, FormView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.forms.models import model_to_dict
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ImproperlyConfigured
from bootstrap_modal_forms.generic import (
  BSModalCreateView,
  BSModalUpdateView,
  BSModalReadView,
  BSModalDeleteView
)
from users.models import Profile
from gestionPermisos.models import Permiso, Empleado, UsuarioEmpleado, ResponsableSector, SubrogaResponsable, Estado, TipoPermiso 
from .forms import permisoForm, permisoAut, permisoTardeNew, permisoDiasNew, permisoDiasENew, permisoDias96New, permisoMarcaForm

# Create your views here.
def inicio(request):
#       return render(request,'gestionPermisos/homeAgente.html')
#        return redirect('homeAgente')
        return render(request,'gestionPermisos/index.html')

def informacion(request):
        empleados = Empleado.objects.filter(legActivo=True)
        return render(request,'gestionPermisos/informacion.html',{"empleados":empleados})

def permisos(request):
        return HttpResponse("Permisos")

def permiso_new(request):
    if request.method == 'POST':
        form = permisoForm(request.POST)
        if form.is_valid():
            permiso = form.save(commit=False)
            permiso.perUsuario = request.user
            permiso.save()
            return redirect('homeAgente')
    else:
        form=permisoForm()
    return render(request,'gestionPermisos/permiso_edit.html',{'form':form})

def permiso_edit(request,pk):
    permiso = get_object_or_404(Permiso,pk=pk)
    if request.method == 'POST':
        form = permisoForm(request.POST,instance=permiso)
        if form.is_valid():
            permiso = form.save(commit=False)
            permiso.perUsuario = request.user
            permiso.save()
            return redirect('homeAgente')
    else:
        form=permisoForm(instance=permiso)
    return render(request,'gestionPermisos/permiso_edit.html',{'form':form})
class PermisoDeleteView(DeleteView):
    model = Permiso
    template_name = 'gestionPermisos/permiso_delete.html'
    context_object_name = 'permiso'
    def post(self,request,*args,**kwargs):
        x = request.POST.get('cancela')
        if x is not None:
            return redirect('homeAgente')
        else:
            return super().post(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(PermisoDeleteView, self).get_context_data(**kwargs)
        idtp = self.kwargs['tpermiso']
        tpermiso = TipoPermiso.objects.get(tperId=idtp)
        context['titulo'] = 'Permiso %s' % tpermiso.tperDescripcion
        return context
    def get_success_url(self):
        return reverse('homeAgente')

class PermisoMarcaView(BSModalUpdateView):
    model = Permiso
    template_name = 'gestionPermisos/permiso_marca_view.html' 
    form_class = permisoMarcaForm   
    success_message = 'El permiso ha sido marcado como visto.'
    success_url = reverse_lazy('homeAgente')

class PermisoVerView(BSModalReadView):
    model = Permiso
    template_name = 'gestionPermisos/permiso_read_view.html' 

class PermisoEditView(UpdateView):
    model = Permiso
    template_name = 'gestionPermisos/permiso_edit.html'
    def get_form_class(self):
        arg = self.kwargs['tpermiso']
        if arg == 1: return permisoTardeNew
        if arg == 3: return permisoDiasNew
        if arg == 4: return permisoDiasENew
        if arg == 5: return permisoDias96New
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['edit'] = True
        return kwargs
    def form_valid(self,form):
        form.instance.perUsuario = self.request.user
        tpermiso = TipoPermiso.objects.get(tperId=self.kwargs['tpermiso'])
        success_message = 'Se modificó el permiso %s correctamente' % tpermiso.tperDescripcion
        messages.success (self.request, (success_message)) 
        return super(PermisoEditView,self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(PermisoEditView, self).get_context_data(**kwargs)
        idtp = self.kwargs['tpermiso']
        tpermiso = TipoPermiso.objects.get(tperId=idtp)
        context['titulo'] = 'Permiso %s' % tpermiso.tperDescripcion
        return context
    def get_success_url(self):
        return reverse('homeAgente')

class PermisoDetailView(DetailView):
    pass 
class PermisoNewView(CreateView):
    model = Permiso
    # form_class = permisoTardeNew
    template_name = 'gestionPermisos/permiso_edit.html'

    def get_form_class(self):
        arg = self.kwargs['tpermiso']
        if arg == 1: return permisoTardeNew
        if arg == 3: return permisoDiasNew
        if arg == 4: return permisoDiasENew
        if arg == 5: return permisoDias96New

        
    def form_valid(self,form):
        hoy = date.today()
#        self.perIdpermiso = self.kwargs['perIdpermiso']
#        permiso = Permiso.objects.get(perIdPermiso=self.perIdpermiso)
        form.instance.perUsuario = self.request.user
        form.instance.perFechaHora = datetime.now()
        tpermiso = TipoPermiso.objects.get(tperId=self.kwargs['tpermiso'])
        form.instance.perTPermiso = tpermiso 
        success_message = 'Se creó el permiso %s correctamente' % tpermiso.tperDescripcion
        messages.success (self.request, (success_message)) 
        return super(PermisoNewView,self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(PermisoNewView, self).get_context_data(**kwargs)
        idtp = self.kwargs['tpermiso']
        tpermiso = TipoPermiso.objects.get(tperId=idtp)
        context['titulo'] = 'Permiso %s' % tpermiso.tperDescripcion
        return context
    def get_success_url(self):
        return reverse('homeAgente')

class permiso_aut_list(SuccessMessageMixin,ListView):
    template_name = 'gestionPermisos/permisosAutACargo.html'
    context_object_name = 'permisos'
    def get_paginate_by(self,queryset):
        return self.request.user.profile.maxPermisos
    def get_queryset(self):
        hoy = date.today()
        usuario = self.request.user.id
    # Obtiene los sectores a cargo del usuario
    #    sectorespropios = ResponsableSector.objects.filter(subrogaresponsable__subId__isnull=True,resUsuario=usuario).values_list('resSector',flat=True)
    #    sectoressubroga = ResponsableSector.objects.filter(subrogaresponsable__subUsuario=usuario,subrogaresponsable__subFechaDesde__lte=hoy,subrogaresponsable__subFechaHasta__gte=hoy).values_list('resSector',flat=True)
    #    sectores = sectorespropios | sectoressubroga
        sectores = self.request.session['sectores']
        usuarios = UsuarioEmpleado.objects.filter(uemEmpleado__legSector__in=sectores).values_list('uemUsuario',flat=True)
        return Permiso.objects.select_related('perUsuario','perTPermiso','perEstado','perUsuarioAcepta').filter(perUsuario__in=usuarios,perEstado__exact=1)

    def post(self, request, *args, **kwargs):
        hoy = datetime.now()
        idpermisosaut = request.POST.getlist('idpermiso')
        c = 0
        x = request.POST.get('autoriza',False)
        y = request.POST.get('rechaza',False)
        if x is not None:   #Se eligió autorizar
            estado = Estado.objects.get(estId=x)
        if y is not None:   #Se eligió rechazar
            estado = Estado.objects.get(estId=y)
        
        for id in idpermisosaut:
            permisoupd = Permiso.objects.get(perIdpermiso=id)
            permisoupd.perEstado = estado
            permisoupd.perUsuarioAutoriza = request.user
            permisoupd.perFechaAutorizado = hoy
            permisoupd.save()
            c = c + 1
        success_message = 'Se autorizaron %s permisos' % c
        messages.success (self.request, (success_message))    
        return redirect('permiso_aut_list')
class permiso_acepta_list(PermissionRequiredMixin,SuccessMessageMixin,ListView):
    template_name = 'gestionPermisos/permisosAcepta.html'
    context_object_name = 'permisos'
    permission_required = 'gestionPermisos.change_permiso'
    permission_denied_message = 'Usted no está autorizado para ver esta página'
    raise_exception = True
           
    def get_paginate_by(self,queryset):
        return self.request.user.profile.maxPermisos
    def get_queryset(self):
        return Permiso.objects.select_related('perUsuario','perTPermiso','perEstado','perUsuarioAcepta').filter(perEstado__exact=2)

    def post(self, request, *args, **kwargs):
        hoy = datetime.now()
        idpermisosacepta = request.POST.getlist('idpermiso')
        c = 0
        x = request.POST.get('acepta',None)
        y = request.POST.get('rechaza',None)
        if x is not None:   #Se eligió aceptar
            estado = Estado.objects.get(estId=x)
            tmp_message = 'Se aceptaron'
        if y is not None:   #Se eligió rechazar
            estado = Estado.objects.get(estId=y)
            tmp_message = 'Se rechazaron'
        
        for id in idpermisosacepta:
            permisoupd = Permiso.objects.get(perIdpermiso=id)
            permisoupd.perEstado = estado
            permisoupd.perUsuarioAcepta = request.user
            permisoupd.perFechaAceptado = hoy
            permisoupd.save()
            c = c + 1
        success_message = '{} {} permisos'.format(tmp_message,c)
        messages.success (self.request, (success_message))    
        return redirect('permiso_acepta_list')

class homeAgente(LoginRequiredMixin,SuccessMessageMixin,ListView):
    login_url='/users/login'
    template_name='gestionPermisos/homeAgente.html'
    context_object_name='ultimoPermiso'
    def get_paginate_by(self,queryset):
        return self.request.user.profile.maxPermisos
    def get_context_data(self, **kwargs):
        hoy = date.today()
        usuario = self.request.user.id
        context = super(homeAgente, self).get_context_data(**kwargs)
        try:
            usuarioempleado = UsuarioEmpleado.objects.get(uemUsuario__exact=usuario)
        except UsuarioEmpleado.DoesNotExist:
            usuarioempleado = None
        if usuarioempleado is not None:    
            sectorusuario=usuarioempleado.uemEmpleado.legSector
            permisosSinVer = Permiso.objects.filter(perUsuario__exact=usuario,perVistoSolicitante__isnull=True,perEstado__gte=2).count()
        # Obtiene los sectores a cargo del usuario
            sectorespropios = ResponsableSector.objects.filter(subrogaresponsable__subId__isnull=True,resUsuario=usuario).values_list('resSector',flat=True)
            sectoressubroga = ResponsableSector.objects.filter(subrogaresponsable__subUsuario=usuario,subrogaresponsable__subFechaDesde__lte=hoy,subrogaresponsable__subFechaHasta__gte=hoy).values_list('resSector',flat=True)
            sectores = sectorespropios | sectoressubroga
        # Guardo datos de sectores a cargo en la sesión del usuario
            data = []
            for item in sectores:
                data.append(item)
            self.request.session['sectores'] = data
            context['permisosSinVer']=permisosSinVer
            context['sector']=sectorusuario
        return context

    def get_queryset(self):
        usuario = self.request.user.id
        return Permiso.objects.select_related('perTPermiso','perEstado','perUsuarioAutoriza').filter(perUsuario__exact=usuario)

'''
def homeAgente(request):
    # Si estamos identificados
    hoy = date.today()
    if request.user.is_superuser:
        return render(request,'gestionPermisos/homeAgente.html')
    if request.user.is_authenticated:
        usuario = request.user.id
        limite = request.user.profile.maxPermisos
        usuarioempleado = UsuarioEmpleado.objects.get(uemUsuario__exact=usuario)
        sectorusuario=usuarioempleado.uemEmpleado.legSector
        ultimoPermiso = Permiso.objects.select_related('perTPermiso','perEstado','perUsuarioAutoriza').filter(perUsuario__exact=usuario)[:limite] 
        ultsPermisos = Permiso.objects.select_related('perTPermiso','perEstado','perUsuarioAutoriza').filter(perUsuario__exact=usuario)[:limite].count() 
        permisosSinVer = Permiso.objects.filter(perUsuario__exact=usuario,perVistoSolicitante__isnull=True,perEstado__gte=2).count()
    # Obtiene los sectores a cargo del usuario
        sectorespropios = ResponsableSector.objects.filter(subrogaresponsable__subId__isnull=True,resUsuario=usuario).values_list('resSector',flat=True)
        sectoressubroga = ResponsableSector.objects.filter(subrogaresponsable__subUsuario=usuario,subrogaresponsable__subFechaDesde__lte=hoy,subrogaresponsable__subFechaHasta__gte=hoy).values_list('resSector',flat=True)
        sectores = sectorespropios | sectoressubroga
    # Guardo datos de sectores a cargo en la sesión del usuario
        data = []
        for item in sectores:
            data.append(item)
        request.session['sectores'] = data
    # Renderizamos el home del usuario
        return render(request,'gestionPermisos/homeAgente.html',{'usuario':usuario,'ultimoPermiso':ultimoPermiso,'permisosSinVer':permisosSinVer,'ultspermisos':ultsPermisos,'sector':sectorusuario})
    # En otro caso redireccionamos al login
    return redirect('/users/login')
'''
class reporteAgente(SuccessMessageMixin,ListView):
    template_name = 'gestionPermisos/reporteAgente.html'
    context_object_name = 'permisos'
    def get_paginate_by(self,queryset):
        return self.request.user.profile.maxPermisos
    def get_queryset(self):
        usuario = self.request.user.id 
        permisos = Permiso.objects.select_related('perTPermiso','perEstado','perUsuarioAutoriza').filter(perUsuario__exact=usuario,perEstado__gt=1)
        return permisos 


class reporteAgentesACargo(SuccessMessageMixin,ListView):
    template_name = 'gestionPermisos/reporteAgentesACargo.html'
    context_object_name = 'permisos'
    def get_paginate_by(self,queryset):
        return self.request.user.profile.maxPermisos
    def get_queryset(self):
        hoy = date.today()
        usuario = self.request.user.id
    # Obtiene los sectores a cargo del usuario
        sectorespropios = ResponsableSector.objects.filter(subrogaresponsable__subId__isnull=True,resUsuario=usuario).values_list('resSector',flat=True)
        sectoressubroga = ResponsableSector.objects.filter(subrogaresponsable__subUsuario=usuario,subrogaresponsable__subFechaDesde__lte=hoy,subrogaresponsable__subFechaHasta__gte=hoy).values_list('resSector',flat=True)
        sectores = sectorespropios | sectoressubroga
        usuarios = UsuarioEmpleado.objects.filter(uemEmpleado__legSector__in=sectores).values_list('uemUsuario',flat=True)
        return Permiso.objects.select_related('perTPermiso','perEstado','perUsuarioAcepta').filter(perUsuario__in=usuarios)
    def get_context_data(self, **kwargs):
        context = super(reporteAgentesACargo, self).get_context_data(**kwargs)
        hoy = date.today()
        usuario = self.request.user.id
    # Obtiene la cantidad de permisos del personal de los sectores a cargo
        sectorespropios = ResponsableSector.objects.filter(subrogaresponsable__subId__isnull=True,resUsuario=usuario).values_list('resSector',flat=True)
        sectoressubroga = ResponsableSector.objects.filter(subrogaresponsable__subUsuario=usuario,subrogaresponsable__subFechaDesde__lte=hoy,subrogaresponsable__subFechaHasta__gte=hoy).values_list('resSector',flat=True)
        sectores = sectorespropios | sectoressubroga
        usuarios = UsuarioEmpleado.objects.filter(uemEmpleado__legSector__in=sectores).values_list('uemUsuario',flat=True)
        cantidad = Permiso.objects.select_related('perTPermiso','perEstado','perUsuarioAcepta').filter(perUsuario__in=usuarios).count()
        context['cantidad']=cantidad
        return context
