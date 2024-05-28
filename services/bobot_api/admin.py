from django.contrib import admin
from .models import ApartamentoPh, TorresPh, ApartamentosPh, PlacaVehiculoVisita, ParqueaderosVisita, \
    IngresoSalidaVehiculoVisita, VisitanteDatos, Config, TipoVehiculo, Impresora, Conjunto

# Register your models here.
#Admin Torres
class TorresPhAdmin(admin.ModelAdmin):
    list_display = ("tr_torre",)
    
#Admin Apartamentos y Casas
class ApartamentoCasaPhAdmin(admin.ModelAdmin):
    list_display = ("ph_apartamentocasa",)
    
#Admin Apartamentos
class ApartamentoPhAdmin(admin.ModelAdmin):
    list_display = ("ph_propietario", "ph_telefono", "ph_mail", "ph_torre", "ph_apartamento",)

#Admin Parqueadeto
class ParqueaderoVisitaAdmin(admin.ModelAdmin):
    list_display = ["pk_slot", "pk_status",]

#Admin Placa
class PlacaVehiculoVisitaAdmin(admin.ModelAdmin):
    list_display = ["pl_placa"]
    
#Admin Ingreso Vehiculo Visita
class IngresoVehiculoVisitaAdmin(admin.ModelAdmin):
    list_display = ["vi_fecha_hora_ingreso", "pl_placa"]
    
class VisitanteDatosAdmin(admin.ModelAdmin):
    list_display = ["vd_nombre", "vd_cedula", "vd_telefono", "vd_fecha"]
    
class ConfigAdmin(admin.ModelAdmin):
    list_display = ["cn_desc", "cn_monto", "cn_config", "cn_hgratis", "cn_status"]

class TipoVehiculoAdmin(admin.ModelAdmin):
    list_display = ["vh_tipo", "vh_desc"]

class ConjuntoAdmin(admin.ModelAdmin):
    list_display = ["cj_nombre", "cj_direccion", "cj_ciudad", "cj_tel", "cj_msn"]

class ImpresoraAdmin(admin.ModelAdmin):
    list_display = ["cg_nombre","cg_impresora"]

    
admin.site.register(TorresPh, TorresPhAdmin)
admin.site.register(ApartamentosPh, ApartamentoCasaPhAdmin)
admin.site.register(ApartamentoPh, ApartamentoPhAdmin)
admin.site.register(ParqueaderosVisita, ParqueaderoVisitaAdmin)
admin.site.register(PlacaVehiculoVisita, PlacaVehiculoVisitaAdmin)
admin.site.register(IngresoSalidaVehiculoVisita, IngresoVehiculoVisitaAdmin)
admin.site.register(VisitanteDatos, VisitanteDatosAdmin)
admin.site.register(Config, ConfigAdmin)
admin.site.register(TipoVehiculo, TipoVehiculoAdmin)
admin.site.register(Conjunto,ConjuntoAdmin)
admin.site.register(Impresora,ImpresoraAdmin)
