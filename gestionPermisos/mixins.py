from datetime import date, datetime 
from django import forms
from django.urls import reverse
from django.utils.html import format_html
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from .models import Permiso

class SuperponeDiasMixin(forms.Form):
    # Verifica si un permiso superpone días con otro solicitado anteriormente
    # Se aplica a formularios
    def clean(self,*args, **kargs):
        super().clean(*args, **kargs)
        hoy = date.today()
        cleaned_data = self.cleaned_data
        fecha = cleaned_data.get('perFechaDesde')
        print ('Fecha Desde:', fecha, hoy)
        perIdEdit = self.instance.perIdpermiso  # Id de permiso al editar
        if fecha < hoy and perIdEdit is None:
            raise forms.ValidationError(
                message='La fecha inicial no puede ser anterior a hoy',
                code='Dato inválido')
        # Validando si fue solicitado un permiso similar o no
        try:
            permisocopy = Permiso.objects.get(perFechaDesde__lte=fecha,perFechaHasta__gte=fecha)
            perId = permisocopy.perIdpermiso
        except ObjectDoesNotExist:
            permisocopy = None
        except MultipleObjectsReturned:
            pass
        if permisocopy is not None and perId != perIdEdit: 
            raise forms.ValidationError(
                message=format_html('Ya existe registrado un permiso similar (<a href="{0}"> Haga clic aquí para ver</a>)',reverse('permiso_edit',kwargs={'pk':perId,'tpermiso':permisocopy.perTPermiso.tperId})),
                code='Invalido',
                params={'id':perId})
        return cleaned_data