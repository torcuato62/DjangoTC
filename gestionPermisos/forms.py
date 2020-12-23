from datetime import date, datetime 
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.utils.html import format_html
from django.urls import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from bootstrap_modal_forms.forms import BSModalModelForm
from .models import Permiso, ResponsableSector, UsuarioEmpleado, Empleado
from .mixins import SuperponeDiasMixin

class UsuarioEmpleadoDisplayForm(forms.ModelForm):
    legLegajo = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    legNombre = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    class Meta:
        model = Empleado
        fields = ('legLegajo','legNombre')

class permisoForm(forms.ModelForm):
    perFechaDesde = forms.DateField(widget=forms.SelectDateWidget)
    class Meta:
        model=Permiso
        fields=('perTPermiso','perMotivo','perFechaDesde',)

class permisoMarcaForm(BSModalModelForm):
    perVistoSolicitante = forms.DateTimeField(widget=forms.HiddenInput,required=False)
    class Meta:
        model=Permiso
        fields=['perVistoSolicitante']
    def clean_perVistoSolicitante(self):
        ahora = datetime.now()
        visto = self.cleaned_data['perVistoSolicitante']
        if visto is None:
            return ahora



class permisoTardeNew(forms.ModelForm):
    perMotivo = forms.CharField(widget=forms.Textarea(attrs={"rows":5,"cols":20}),label='Motivo',required=True)
    perHoraIngreso = forms.TimeField(label='Hora Ingreso')
    perIdpermiso = forms.HiddenInput()
    class Meta:
        model=Permiso
        fields = ['perMotivo','perHoraIngreso','perIdpermiso']
    def __init__(self, *args, **kwargs):
        edit = kwargs.pop('edit',None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-permisotarde'
        self.helper.form_method = 'post'
        if edit is not None:    # Si está editando
            self.helper.add_input(Submit('submit','Modificar'))
        else:
            self.helper.add_input(Submit('submit','Solicitar'))
        self.helper.add_input(Button('cancel', 'Cancelar', css_class='btn-primary',
                             onclick="window.location.href = '{}';".format(reverse('homeAgente'))))        
    def clean(self):
        cleaned_data = self.cleaned_data
        hoy = datetime.today()
        tpermiso = 1    #Llegada Tarde
        perIdEdit = self.instance.perIdpermiso  # Id de permiso al editar
        # Validando si fue solicitado un permiso similar o no
        try:
            permisocopy = Permiso.objects.get(perFechaHora__date=hoy,perTPermiso=tpermiso)
            perId = permisocopy.perIdpermiso
        except ObjectDoesNotExist: 
            permisocopy = None
        if permisocopy is not None and perId != perIdEdit: 
            raise forms.ValidationError(
                message=format_html('Ya existe registrado un permiso similar (<a href="{0}"> Haga clic aquí para ver</a>)',reverse('permiso_edit',kwargs={'pk':perId,'tpermiso':tpermiso})),
                code='Invalido',
                params={'id':perId})
        return cleaned_data

class permisoDiasNew(SuperponeDiasMixin,forms.ModelForm):
    perFechaDesde = forms.DateField(widget=forms.SelectDateWidget(attrs={'style':'display: inline-block; width: 33%'}),initial=date.today, label='Desde')
    perCantidadDias = forms.ChoiceField(choices=[(x, x) for x in range(1,3)],label='Cant. de Días')
    perMotivo = forms.CharField(widget=forms.Textarea(attrs={"rows":5,"cols":20}),label='Motivo',required=True)
    class Meta:
        model=Permiso
        fields = ['perMotivo','perFechaDesde','perCantidadDias']
    def __init__(self, *args, **kwargs):
        edit = kwargs.pop('edit',None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-permiso80'
        self.helper.form_method = 'post'
        if edit is not None:    # Si está editando
            self.helper.add_input(Submit('submit','Modificar'))
        else:
            self.helper.add_input(Submit('submit','Solicitar'))
        self.helper.add_input(Button('cancel', 'Cancelar', css_class='btn-primary',
                             onclick="window.location.href = '{}';".format(reverse('homeAgente'))))        


class permisoDiasENew(SuperponeDiasMixin,forms.ModelForm):
    perFechaDesde = forms.DateField(widget=forms.SelectDateWidget(attrs={'style':'display: inline-block; width: 33%'}),initial=date.today, label='Desde')
    perCantidadDias = forms.ChoiceField(choices=[(x, x) for x in range(1,8)],label='Cant. de Días')
    perMotivo = forms.CharField(widget=forms.Textarea(attrs={"rows":5,"cols":20}),label='Motivo',required=True)
    class Meta:
        model=Permiso
        fields = ['perMotivo','perFechaDesde','perCantidadDias']
    def __init__(self, *args, **kwargs):
        edit = kwargs.pop('edit',None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-permiso80'
        self.helper.form_method = 'post'
        if edit is not None:    # Si está editando
            self.helper.add_input(Submit('submit','Modificar'))
        else:
            self.helper.add_input(Submit('submit','Solicitar'))
        self.helper.add_input(Button('cancel', 'Cancelar', css_class='btn-primary',
                             onclick="window.location.href = '{}';".format(reverse('homeAgente'))))        

class permisoDias96New(SuperponeDiasMixin,forms.ModelForm):
    tdescuento = [
        (1,'Licencia'),
        (2,'Sueldo'),
    ]
    perDescuento96 = forms.ChoiceField(choices=tdescuento, widget=forms.RadioSelect,label='Tipo Descuento')
    perFechaDesde = forms.DateField(widget=forms.SelectDateWidget(attrs={'style':'display: inline-block; width: 33%'}),initial=date.today, label='Desde')
    perCantidadDias = forms.ChoiceField(choices=[(x, x) for x in range(1,7)],label='Cant. de días')
    perMotivo = forms.CharField(widget=forms.Textarea(attrs={"rows":5,"cols":20}),label='Motivo',required=True)
    class Meta:
        model=Permiso
        fields = ['perDescuento96','perMotivo','perFechaDesde','perCantidadDias']
    def __init__(self, *args, **kwargs):
        edit = kwargs.pop('edit',None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-permiso80'
        self.helper.form_method = 'post'
        if edit is not None:    # Si está editando
            self.helper.add_input(Submit('submit','Modificar'))
        else:
            self.helper.add_input(Submit('submit','Solicitar'))
        self.helper.add_input(Button('cancel', 'Cancelar', css_class='btn-primary',
                             onclick="window.location.href = '{}';".format(reverse('homeAgente'))))        
        
class permisoAut(forms.Form):
    choices = forms.ModelMultipleChoiceField(
        queryset = None, 
        widget  = forms.CheckboxSelectMultiple,
    )    
    
    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usrAut')
        super(permisoAut, self).__init__(*args, **kwargs)
        hoy = date.today()
        # Obtiene los sectores, usuarios y permisos a autorizar por el usuario
        sectorespropios = ResponsableSector.objects.filter(subrogaresponsable__subId__isnull=True,resUsuario=usuario).values_list('resSector',flat=True)
        sectoressubroga = ResponsableSector.objects.filter(subrogaresponsable__subUsuario=usuario,subrogaresponsable__subFechaDesde__lte=hoy,subrogaresponsable__subFechaHasta__gte=hoy).values_list('resSector',flat=True)
        sectores = sectorespropios | sectoressubroga
        usuarios = UsuarioEmpleado.objects.filter(uemEmpleado__legSector__in=sectores).values_list('uemUsuario',flat=True)
        permisos = Permiso.objects.select_related('perTPermiso','perEstado','perUsuarioAcepta').filter(perUsuario__in=usuarios,perEstado__exact=1)
        idpermisos = Permiso.objects.select_related('perTPermiso','perEstado','perUsuarioAcepta').filter(perUsuario__in=usuarios,perEstado__exact=1).values_list('perIdpermiso',flat=True)
        self.fields['choices'].queryset = idpermisos


