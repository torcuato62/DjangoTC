from datetime import datetime, timedelta, date
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ValidationError, ObjectDoesNotExist


# Create your models here.

class Feriado(models.Model):
    ferId=models.AutoField(primary_key=True)
    ferFecha=models.DateField(unique=True)
    ferDescripcion=models.CharField(max_length=40,blank=True)
    def __str__(self):
        return "%s (%s)" % (self.ferDescripcion,self.ferFecha)

class Sector(models.Model):
    secCodigo=models.IntegerField(verbose_name="Codigo",primary_key=True,auto_created=True)
    secSector=models.CharField(verbose_name="Sector",max_length=40)
    def __str__(self):
        return self.secSector
    
class Empleado(models.Model):
    legCodigo=models.IntegerField(verbose_name="Código",primary_key=True)
    legLegajo=models.CharField(max_length=15)
    legNombre=models.CharField(max_length=40)
    legActivo=models.BooleanField(default=True,null=True)
    legSector=models.ForeignKey(Sector,on_delete=models.RESTRICT)
    legFechaEgreso=models.DateField(verbose_name="Fecha Egreso",null=True,blank=True)
    legTarjeta=models.CharField(verbose_name="Tarjeta",max_length=8,null=True,blank=True)
    legCUIL=models.CharField(verbose_name="CUIL",max_length=18,null=True,blank=True)
    legTelefono=models.CharField(verbose_name="Teléfono",max_length=18,null=True,blank=True)
    legTipodeDocumento=models.IntegerField(verbose_name="Tipo Documento",null=True,blank=True)
    legDocumento=models.CharField(verbose_name="Documento",max_length=20,null=True,blank=True)
    legSuspendido=models.BooleanField(null=True)
    legFechadeNacimiento=models.DateField(verbose_name="Fecha Nacimiento",null=True,blank=True)
    legGenero=models.IntegerField(verbose_name="Género",null=True,blank=True)
    legEmailPersonal=models.EmailField(verbose_name="Email Personal",null=True,blank=True)
    legEmailLaboral=models.EmailField(verbose_name="Email Laboral",null=True,blank=True)
    class Meta:
        ordering = ['legNombre']
    
    def _get_usuario(self):
        usuario = UsuarioEmpleado.objects.get(uemEmpleado__exact=self.legCodigo)
        return usuario.uemUsuario

    legUsuario = property(_get_usuario)


class UsuarioEmpleado(models.Model):
    uemId=models.AutoField(primary_key=True)
    uemUsuario=models.OneToOneField(User,on_delete=models.RESTRICT)
    uemEmpleado=models.OneToOneField(Empleado,on_delete=models.RESTRICT)

class ResponsableSector(models.Model):
    ressecId=models.AutoField(primary_key=True)
    resUsuario=models.ForeignKey(User,on_delete=models.RESTRICT,related_name='resUsr',verbose_name='Usuario Responsable')
    resSector=models.ForeignKey(Sector,on_delete=models.RESTRICT,related_name='resSec',verbose_name='Sector a Cargo')
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['resUsuario','resSector'], name='UsrSecUnica'),
        ]
    def __str__(self):
        return "%s - %s" % (self.resUsuario.get_full_name(),self.resSector.secSector)

    def _get_subrogancia(self):
        sector = self.resSector
        subrogancia = SubrogaResponsable.objects.get(subResSecSubroga__exact=self.ressecId)
        if subrogancia.activo()=='Activa':
            return subrogancia.subUsuario
        else:
            return None
    resUsrSubrogante=property(_get_subrogancia)

class SubrogaResponsable(models.Model):
    subId=models.AutoField(primary_key=True)
    subUsuario=models.ForeignKey(User,on_delete=models.RESTRICT)
    subResSecSubroga=models.ForeignKey(ResponsableSector,on_delete=models.CASCADE,null=True)
    subFechaDesde=models.DateField()
    subFechaHasta=models.DateField(blank=True,null=True)
    def __str__(self):
        return "%s - %s - %s" % (self.subUsuario.get_full_name(),self.subResSecSubroga.resSector,self.activo())
    def activo(self):
            """
            Método que indica si es una subrogancia activa
            """
            from datetime import date
            hoy = date.today()
            if self.subFechaDesde <= hoy and self.subFechaHasta >= hoy:
                return "Activa"
            else:
                return "Inactiva"

class TipoPermiso(models.Model):
    tperId=models.AutoField(primary_key=True)
    tperDescripcion=models.CharField(max_length=50)
    tperCtaCte=models.BooleanField(null=True,blank=True)
    tperActivo=models.BooleanField(default=True)
    def __str__(self):
        return "%s (%s)" % (self.tperDescripcion,self.tperId,)

class Estado(models.Model):
    estId=models.AutoField(primary_key=True)
    estDescripcion=models.CharField(max_length=50)
    def __str__(self):
        return "%s (%s)" % (self.estDescripcion,self.estId)
                
class Permiso(models.Model):
    perIdpermiso=models.AutoField(primary_key=True)
    perUsuario=models.ForeignKey(User,on_delete=models.RESTRICT,related_name="perUsr")
    perFechaHora=models.DateTimeField()
    perMotivo=models.TextField(null=True,blank=True)
    perFechaDesde=models.DateField(null=True,blank=True)
    perFechaHasta=models.DateField(null=True,blank=True)
    perTPermiso=models.ForeignKey(TipoPermiso,on_delete=models.RESTRICT)
    perEstado=models.ForeignKey(Estado,on_delete=models.RESTRICT,default=1)
    perHoraIngreso=models.TimeField(null=True,blank=True)
    perHoraRetiro=models.TimeField(null=True,blank=True)
    perCantidadDias=models.IntegerField(null=True,blank=True)
    perCertificado=models.BooleanField(null=True,blank=True)
    perCertificadoVisita=models.BooleanField(null=True,blank=True)
    perMotivor=models.IntegerField(null=True,blank=True)
    perDescuento96=models.IntegerField(null=True,blank=True)
    perArticuloE=models.BooleanField(null=True,blank=True)
    perUsuarioVisa=models.ForeignKey(User,on_delete=models.RESTRICT,null=True,related_name="perUsrVisa",blank=True)
    perFechaVisado=models.DateTimeField(null=True,blank=True)
    perIPVisado=models.GenericIPAddressField(null=True,blank=True)
    perUsuarioAutoriza=models.ForeignKey(User,on_delete=models.RESTRICT,null=True,related_name="perUsrAutoriza",blank=True)
    perFechaAutorizado=models.DateTimeField(null=True,blank=True)
    perIPAutorizado=models.GenericIPAddressField(null=True,blank=True)
    perUsuarioAcepta=models.ForeignKey(User,on_delete=models.RESTRICT,null=True,related_name="perUsrAcepta",blank=True)
    perFechaAceptado=models.DateTimeField(null=True,blank=True)
    perIPAceptado=models.GenericIPAddressField(null=True,blank=True)
    perVistoSolicitante=models.DateTimeField(null=True,blank=True,default=datetime.now())
    perAnioLicencia=models.IntegerField(null=True,blank=True)
    perDiasdeViaje=models.IntegerField(null=True,blank=True)
    perProcesadoRRHH=models.DateTimeField(null=True,blank=True)
    perCodigoCargado=models.DateTimeField(null=True,blank=True)
    perFechaFinSolicitud=models.DateTimeField(null=True,blank=True)
    perDetalleCargado=models.DateTimeField(null=True,blank=True)
    class Meta:
        ordering = ['-perFechaHora']

    def _get_ultimo_estado(self):
        estado = self.perEstado.estId
        if estado == 1: return 'Iniciado'
        if estado == 2: return '{} {} {}'.format(self.perEstado,self.perUsuarioAutoriza.get_full_name(),self.perFechaAutorizado)
        if estado == 3: return '{} {} {}'.format(self.perEstado,self.perUsuarioAcepta.get_full_name(),self.perFechaAceptado)
        if estado == 4: return '{} {}'.format(self.perEstado,self.perUsuarioAutoriza.get_full_name() )
        if estado == 5: return '{} {}'.format(self.perEstado,self.perUsuarioAcepta.get_full_name() )
        if estado == 6: return '{} {} {}'.format(self.perEstado,self.perUsuarioVisa.get_full_name(),self.perFechaVisado )
        if estado == 7: return '{} {}'.format(self.perEstado,self.perUsuarioVisa.get_full_name() )
    perUltimoEstado = property(_get_ultimo_estado)

    def _get_sector_usuario(self):
        usuario = self.perUsuario
        usuarioempleado = UsuarioEmpleado.objects.get(uemUsuario__exact=usuario)
        sector = usuarioempleado.uemEmpleado.legSector
        return sector
    perSectorUsuario = property(_get_sector_usuario)

    def __str__(self):
        return "%s - %s - %s - %s" % (self.perFechaHora,self.perUsuario.get_full_name,self.perTPermiso,self.perMotivo)
    def clean(self):
        super().clean()
# Verifica y calcula automáticamente fechas del permiso
        if self.perFechaDesde is not None:
            fd = self.perFechaDesde
            try:
                diaferiado = Feriado.objects.get(ferFecha=fd)
            except ObjectDoesNotExist:
                diaferiado = None
            if fd.isoweekday() == 6 or fd.isoweekday() == 7 or diaferiado is not None:
                raise ValidationError('La fecha inicial no es un dia habil')
            if self.perCantidadDias is not None:
                fh = fd + timedelta(days=1)
                x = self.perCantidadDias - 1
                for i in range(x):
                    print('FH: ',fh, '(',fh.isoweekday(),')')
                    ftest = False
                    while not ftest:
                        try:
                            diaferiado = Feriado.objects.get(ferFecha=fh)
                        except ObjectDoesNotExist:
                            diaferiado = None
                        if fh.isoweekday() == 6 or fh.isoweekday() == 7 or diaferiado is not None:
                            fh = fh + timedelta(days=1)
                        else:
                            ftest = True
                    fh = fh + timedelta(days=1)
                self.perFechaHasta = fh + timedelta(days=-1)
        if self.perFechaHasta is not None and self.perFechaDesde is None:
            raise ValidationError('No registra Fecha Desde')
class EstadoSolicitud(models.Model):
    esolId=models.AutoField(primary_key=True)
    esolDescripcion=models.TextField(max_length=50,null=True,blank=True,default=None)

class TipoSolicitud(models.Model):
    tsolId=models.AutoField(primary_key=True)
    tsolDescripcion=models.TextField(max_length=100,null=True,blank=True,default=None)
    tsolFormulario=models.TextField(max_length=255,blank=True,null=True,default=None)
    tsolActivo=models.BooleanField(blank=True,null=True,default=None)
    tsolRespXMail=models.BooleanField(blank=True,null=True,default=None)

class Solicitud(models.Model):
    solId=models.AutoField(primary_key=True)
    solUsuario=models.TextField(max_length=45)
    solTipoSolicitud=models.ForeignKey(TipoSolicitud,null=True,blank=True, on_delete=models.RESTRICT,related_name='solTipoSol')
    solFecha=models.DateTimeField()
    solNotas=models.TextField(max_length=1000,blank=True,null=True,default=None)
    solEstado=models.ForeignKey(EstadoSolicitud,on_delete=models.RESTRICT,null=True,blank=True,default=None,related_name='solEstado')
    solFechaleidorrhh=models.DateTimeField(null=True,blank=True,default=None)
    solUsrleidorrhh=models.ForeignKey(User,on_delete=models.RESTRICT,blank=True,null=True,default=None,related_name='solUsrRRHH')
    solFechacumplido=models.DateTimeField(null=True,blank=True,default=None)
    solUsrcumplido=models.ForeignKey(User,on_delete=models.RESTRICT,blank=True,null=True,default=None,related_name='solUsrCumplido')
    solFechaleidousr=models.DateTimeField(blank=True,null=True,default=None)
    solFechaaccionusr=models.DateTimeField(blank=True,null=True,default=None)
    solDescaccionusr=models.TextField(max_length=1000,null=True,blank=True,default=None)