
from django.urls import path
from .views import ApartamentoPhView, TorresApastamentosView, PlacasVheiculosVisitaView, ParqueaderoVisitaView, \
    IngresoSalidaVisitaVehiculoView, VisitanteDatosView, CalculoTiempoMontoView, TipoVehiculoView, ReporteParqueaderosDhView, \
    ReporteCarrosParqueadosDhView, ReporteParqueaderosLibresDhView, GetDateTimeView, ResumenVisitaVehiculoView, ReporteIngresosView

urlpatterns = [
    path('apartamentoph-registro/', ApartamentoPhView.as_view(), name='apartamentoph_registro'),
    path('apartamentos-buscar/', ApartamentoPhView.as_view(), name='apartamentos_buscar'),
    path('apartamentoscasas-buscar/', TorresApastamentosView.as_view(), name='apartamentoscasas_buscar'),
    path('placavisita-buscar/', PlacasVheiculosVisitaView.as_view(), name='placavisita_buscar'),
    path('placavisita-registro/', PlacasVheiculosVisitaView.as_view(), name='placavisita_registro'),
    path('parqueaderovisita-registro/', ParqueaderoVisitaView.as_view(), name='parqueaderovisita_registro'),
    path('parqueaderovisita-disponible/', ParqueaderoVisitaView.as_view(), name='parqueaderovisita_disponible'),
    path('parqueaderovisita-actdisponible/<str:pk>/', ParqueaderoVisitaView.as_view(), name='parqueaderovisita_actdisponible'),
    path('vehiculovisita-ingreso/', IngresoSalidaVisitaVehiculoView.as_view(), name='vehiculovisita_ingreso'),
    path('vehiculovisita-salida/<int:pk>/', IngresoSalidaVisitaVehiculoView.as_view(), name='vehiculovisita_salida'),
    path('vehiculovisita-info/', IngresoSalidaVisitaVehiculoView.as_view(), name='vehiculovisita_info'),
    path('personavisita-registro/', VisitanteDatosView.as_view(), name='personavisita_registro'),
    path('cedulavisita-buscar/', VisitanteDatosView.as_view(), name='cedulavisita_buscar'),
    path('cedulavisita-registro/', VisitanteDatosView.as_view(), name='cedulavisita_registro'),
    path('tiempo-calculo/', CalculoTiempoMontoView.as_view(), name='tiempo-calculo'),
    path('tipovehiculo-buscar/', TipoVehiculoView.as_view(), name='tipovehiculo_buscar'),
    path('vehiculosparq-dh/', ReporteParqueaderosDhView.as_view(), name='vehiculosparq_dh'),
    path('totvechiculos-dh/', ReporteCarrosParqueadosDhView.as_view(), name='totvehiculos-dh'),
    path('totparqueaderos-dh/', ReporteParqueaderosLibresDhView.as_view(), name='totparqueaderos-dh'),
    path('datetime-info/', GetDateTimeView.as_view(), name='datetime-info'),
    path('resumenvisitante-info/', ResumenVisitaVehiculoView.as_view(), name='resumenvisitante-info'),
    path('reporteingresos-rep/', ReporteIngresosView.as_view(), name='reporteingresos-rep'),
]
