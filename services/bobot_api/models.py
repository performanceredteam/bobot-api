from django.db import models
from django.utils import timezone

# Create your models here.
#Torres
class TorresPh(models.Model):
    tr_torre = models.PositiveSmallIntegerField()
    def __str__(self):
        return str(self.tr_torre)
    
#Apartmanetos
class ApartamentosPh(models.Model):
    ph_apartamentocasa = models.PositiveBigIntegerField()
    def __str__(self):
        return str(self.ph_apartamentocasa)
    
#Apartemento
class ApartamentoPh(models.Model):
    ph_propietario = models.CharField(max_length=50)
    ph_telefono = models.CharField(max_length=12)
    ph_mail = models.EmailField()
    ph_torre = models.PositiveIntegerField()
    #ph_torre = models.ForeignKey(TorresPh,on_delete=models.CASCADE)
    ph_apartamento = models.PositiveIntegerField()
    #ph_apartamento = models.ForeignKey(ApartamentosPh, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.ph_propietario

#Parqueaderos
class ParqueaderosVisita(models.Model):
    pk_slot = models.CharField(max_length=5, unique=True, primary_key=True)
    pk_status = models.BooleanField(default=False)
    
    def __str__(self):
        return self.pk_slot

#Placa de Vehiculos Visita
class PlacaVehiculoVisita(models.Model):
    pl_placa = models.CharField(max_length=7, unique=True, primary_key=True)
    
    def __str__(self):
        return self.pl_placa

#Tipo de Vehiculo
class TipoVehiculo(models.Model):
    vh_tipo = models.IntegerField(unique=True, primary_key=True)
    vh_desc = models.CharField(max_length=10)
    
    def __str__(self):
        return self.vh_desc
    
#Resgistro Ingreso-Salida Vehiculo
class IngresoSalidaVehiculoVisita(models.Model):
    vi_fecha_hora_ingreso = models.DateTimeField(format('%Y-%m-%d %H:%M:%s'), auto_now=False)
    vi_fecha_hora_salida = models.DateTimeField(format('%Y-%m-%d %H:%M:%s'), auto_now=False, blank=True, null=True)
    pl_placa = models.ForeignKey(PlacaVehiculoVisita, on_delete=models.CASCADE)
    pk_slot = models.ForeignKey(ParqueaderosVisita, on_delete=models.CASCADE)
    vh_tipo = models.ForeignKey(TipoVehiculo, on_delete=models.CASCADE)
    vi_status = models.BooleanField(default=True)
    
    def __str__(self):
        return str(self.pl_placa)
    
#Registro de Visitante
class VisitanteDatos(models.Model):
    vd_nombre = models.CharField(max_length=50, null=False)
    vd_cedula = models.PositiveBigIntegerField(null=False, unique=True)
    vd_telefono = models.CharField(max_length=12)
    vd_fecha = models.DateField(default=timezone.now)
    
    def __str__(self):
        return self.vd_nombre
    


#Ingreso de Visita 
class IngresoDeVisita(models.Model):
    iv_fecha = models.DateTimeField(format('%Y-%m-%d %H:%M:%s'), default=timezone.now)
    vd_cedula = models.PositiveBigIntegerField(null=False)
    ph_propietario = models.ForeignKey(ApartamentoPh, on_delete=models.CASCADE)
    pl_placa = models.ForeignKey(PlacaVehiculoVisita, on_delete=models.CASCADE)
    pk_slot = models.ForeignKey(ParqueaderosVisita, on_delete=models.CASCADE)
    vi_status = models.BooleanField(default=True)
    
    def __str__(self):
        return str(self.vd_cedula)

#Configuracion de Cobros
class Config(models.Model):
    cn_desc = models.CharField(max_length=10)
    cn_monto = models.BigIntegerField()
    cn_config = models.IntegerField()
    cn_hgratis = models.IntegerField()
    cn_status = models.BooleanField()
    
    def __str__(self):
        return self.cn_desc

#Facturacion
class Facturacion(models.Model):
    vi_fecha_hora_salida = models.DateTimeField(format('%Y-%m-%dT%H:%M:%s'), auto_now=False)
    fa_monto = models.DecimalField(max_digits=10, decimal_places=2)
    fa_tiempo = models.IntegerField()
    ph_propietario = models.ForeignKey(ApartamentoPh, on_delete=models.CASCADE)
    vi_visitante = models.ForeignKey(IngresoDeVisita, on_delete=models.CASCADE)
    
    