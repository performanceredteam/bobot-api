from rest_framework import serializers
from .models import ApartamentoPh, TorresPh, ApartamentosPh, PlacaVehiculoVisita, ParqueaderosVisita, \
    IngresoSalidaVehiculoVisita, VisitanteDatos, IngresoDeVisita, Config, TipoVehiculo, Facturacion, Config, \
    Conjunto, Impresora
    
class TorresPhSerializer(serializers.ModelSerializer):
    class Meta:
        model = TorresPh
        fields = ["id","tr_torre"]
        
class ApartamentosCasasPhSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApartamentosPh
        fields = ["id","ph_apartamentocasa"]

class ApartamentoPhSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApartamentoPh
        fields = ["id", "ph_propietario", "ph_telefono", "ph_mail", "ph_torre", "ph_apartamento"]

class TipoVehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoVehiculo
        fields = "__all__"
        
class ParqueaderosVisitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParqueaderosVisita
        fields = ["pk_slot", "pk_status"]

class PlacaVehiculoVisitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlacaVehiculoVisita
        fields = ["pl_placa"]

class IngresoVisitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngresoSalidaVehiculoVisita
        fields = ["vi_fecha_hora_ingreso", "pl_placa", "vh_tipo", "pk_slot"]

class SalidaVisitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngresoSalidaVehiculoVisita
        fields = ["id", "vi_fecha_hora_salida", "pl_placa", "vi_status"]

class IngresoSalidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngresoSalidaVehiculoVisita
        fields = "__all__"
        
class VisitanteDatosSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitanteDatos
        fields = ["id", "vd_nombre", "vd_cedula", "vd_telefono"]
        
class IngresoDeVisitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngresoDeVisita
        fields = ["id", "iv_fecha", "vd_cedula", "ph_propietario", "pl_placa", "pk_slot", 'vi_status']
        
class IngresoDeVisitaReporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngresoDeVisita
        fields = ["id", "iv_fecha", "vd_cedula", "ph_propietario", "pl_placa", "pk_slot", 'vi_status']

class SalidaDeVisitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngresoDeVisita
        fields = ['vi_status']
        
class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Config
        fields = "__all__"

class FacturacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facturacion
        fields = ["vi_fecha_hora_salida", "fa_monto", "fa_tiempo", "ph_propietario", "vi_visitante"]

class ConjuntoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conjunto
        fields = "__all__"

class ImpresoraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Impresora
        fields = ["cg_nombre", "cg_impresora"]