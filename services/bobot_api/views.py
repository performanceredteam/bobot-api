from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from .models import ApartamentoPh, TorresPh, ApartamentosPh, PlacaVehiculoVisita, \
    ParqueaderosVisita, IngresoSalidaVehiculoVisita, VisitanteDatos, IngresoDeVisita, \
    TipoVehiculo, Config, Facturacion, Conjunto, Impresora, Pension, CostoPension, Caja, Log, \
    TicketId

from .serializer import ApartamentoPhSerializer, \
    TorresPhSerializer, ApartamentosCasasPhSerializer, \
    PlacaVehiculoVisitaSerializer, ParqueaderosVisitaSerializer, \
    IngresoVisitaSerializer, SalidaVisitaSerializer, IngresoSalidaSerializer, \
    VisitanteDatosSerializer, IngresoDeVisitaSerializer, SalidaDeVisitaSerializer, \
    TipoVehiculoSerializer, ConfigSerializer, FacturacionSerializer, IngresoDeVisitaReporteSerializer, \
    ConjuntoSerializer, ImpresoraSerializer, PensionSerializer, CostoPensionSerializer, PensionStatusSerializer, \
    CajaSerializer, CajaAperturaSerializer, CajaCierreSerializer, StatusFacturacionCajaSerializer, StatusPensionCajaSerializer, \
    LogSerializer, TicketIdSerializer

from rest_framework.permissions import DjangoModelPermissions
from datetime import *

from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import get_template

import requests
# Create your views here.

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': user.username,
            'name': user.first_name,
            'last': user.last_name
        })

def SendEmail(asunto, mensaje, emails, admin):
    #send_mail(subjet=asunto, menssage=mensaje, from_email=settings.EMAIL_HOST_USER, recipient_list=emails)
    template = settings.TEMPLATES[0]['DIRS']
    message = get_template(template[0]+"/email.html").render({'datos':mensaje})

    
    mail = EmailMessage(
        subject=asunto,
        body=message,
        from_email=settings.EMAIL_HOST_USER,
        to=[emails], # settings.EMAIL_HOST_USER
        cc=[admin],
    )
    mail.content_subtype = "html"
    return mail.send()
    
    

class ApartamentoPhView(APIView):
    authentication_classes=[TokenAuthentication,]
    permission_classes = [DjangoModelPermissions]
   
    queryset = ApartamentoPh.objects.all()
    serializer_class = ApartamentoPhSerializer
    
    #Registro Apartamento
    def post(self, request, *args, **kwargs):
        data = {
            'ph_propietario': request.data.get('ph_propietario'),
            'ph_telefono': request.data.get('ph_telefono'),
            'ph_mail': request.data.get('ph_mail'),
            'ph_torre': request.data.get('ph_torre'),
            'ph_apartamento': request.data.get('ph_apartamento')
        }
        
        serializer = ApartamentoPhSerializer(data=data)
    
        if serializer.is_valid():
            serializer.save()
            return Response({'Message' : 'Success', "Registro" :serializer.data}, status=status.HTTP_201_CREATED)
        
        return Response({'Message' : 'Error', "Detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    #Buscar Torre y Apartamento o por Propietario
    def get(self, request, *args, **kwargs):
        try:
            torre = request.query_params.get("torre", None)
            apto = request.query_params.get("apto", None)
            prop = request.query_params.get("prop", None)
            
            prop_intance = None
            
            if (torre != None and apto != None):
                prop_intance = ApartamentoPh.objects.get(ph_torre__exact=torre,ph_apartamento__exact=apto)
                serializer = ApartamentoPhSerializer(prop_intance)
            elif prop != None:
                prop_intance = ApartamentoPh.objects.get(ph_propietario=prop)
                serializer = ApartamentoPhSerializer(prop_intance)
            else: 
                prop_intance = ApartamentoPh.objects.all()
                serializer = ApartamentoPhSerializer(prop_intance, many=True)           
                 
        except Exception as e:
           print(e)
        
        if prop_intance is None:
            return Response({'Message':"Propietario No Encontrado"}, status=status.HTTP_409_CONFLICT)
        
        return Response({'Message' : 'Success', 'Propietario': serializer.data}, status=status.HTTP_200_OK)


class TorresApastamentosView(APIView):
    authentication_classes=[TokenAuthentication,]
    permission_classes = [DjangoModelPermissions]
    
    queryset = TorresPh.objects.all()
    serializer_class = TorresPhSerializer
    
     #Buscar Torres y Apartamentos
    def get(self, request, *args, **kwargs):
        try:
            
            torres_intance = TorresPh.objects.all()
            torres_serializer = TorresPhSerializer(torres_intance, many=True)
            
            apartamentos = ApartamentosPh.objects.all()
            apartamentos_serializer = ApartamentosCasasPhSerializer(apartamentos, many=True)
            
        except Exception as e:
            print(e)
        
        if not torres_intance:
            return Response({'Message':'Torres No Encontradas'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not apartamentos:
            return Response({'Message':'Apartamentos No Encontrados'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'Message':'Success', 'Torres':torres_serializer.data, 'ApartamentosCasas':apartamentos_serializer.data}, status=status.HTTP_200_OK)

class TipoVehiculoView(APIView):
    authentication_classes=[TokenAuthentication,]
    permission_classes = [DjangoModelPermissions]
    
    queryset = TipoVehiculo.objects.all()
    serializer_class = TipoVehiculoSerializer
    
    #Buscar Tipo de Vehiculo
    def get(self, request, *args, **kwargs):
        try:
            #tipo_vheiculo = request.query_params.get('tipo', None)
            
            #if tipo_vheiculo != None:
            tipo_intance = TipoVehiculo.objects.all()
            tipo_serializer = TipoVehiculoSerializer(tipo_intance, many=True)
        except Exception as e:
            print(e)
        
        if tipo_intance is None:
            return Response({'Message':'Tipo de Vehiculo Error'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'Message' : 'Success', 'TipoVehiculo': tipo_serializer.data}, status=status.HTTP_200_OK)
                
     
class PlacasVheiculosVisitaView(APIView):
    authentication_classes=[TokenAuthentication,]
    permission_classes = [DjangoModelPermissions]
     
    queryset = PlacaVehiculoVisita.objects.all()
    serializer_class = PlacaVehiculoVisitaSerializer
    
    #Buscar Placa Si Existe
    def get(self, request, *args, **kwargs):
        try:
            placa = request.query_params.get("placa", None)
            placa_intance = None
            
            if placa != None:
                placa_intance = PlacaVehiculoVisita.objects.get(pl_placa__exact=placa)
                placa_serializer = PlacaVehiculoVisitaSerializer(placa_intance)

        except Exception as e:
            print(e)
        
        if placa_intance is None:
            return Response({'Message':'Placa No Encontrada'}, status=status.HTTP_409_CONFLICT)
        return Response({'Message':'Success','Placa':placa_serializer.data}, status=status.HTTP_200_OK)
    
    #Registrar Placa
    def post(self, request, *args, **kwargs):
        data = {
            'pl_placa': request.data.get('pl_placa')
        }
        
        serializer = PlacaVehiculoVisitaSerializer(data=data)
    
        if serializer.is_valid():
            serializer.save()
            return Response({'Message' : 'Success', "Placa" :serializer.data}, status=status.HTTP_201_CREATED)
        
        return Response({'Message' : 'Error', "Detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class ParqueaderoVisitaView(APIView):
    authentication_classes=[TokenAuthentication,]
    permission_classes = [DjangoModelPermissions]
     
    queryset = ParqueaderosVisita.objects.all()
    serializer_class = ParqueaderosVisitaSerializer
    
    #Registrar Parqueadero
    def post(self, request, *args, **kwargs):
        data = {
            'pk_slot': request.data.get('pk_slot'),
            'pk_status': request.data.get('pk_status')
        }
        
        serializer = ParqueaderosVisitaSerializer(data=data)
    
        if serializer.is_valid():
            serializer.save()
            return Response({'Message' : 'Success', "Parqueadero" :serializer.data}, status=status.HTTP_201_CREATED)
        
        return Response({'Message' : 'Error', "Detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    #Mostrar Parquedaero Disponibles
    def get(self, request, *args, **kwargs):
        try:
            pk_disponible = request.query_params.get("disponible", None)
            tipo_vehiculo = request.query_params.get("tipovehiculo", None)
            slot_intance = None
            
            if pk_disponible != None:
                slot_intance = ParqueaderosVisita.objects.all().filter(pk_status=pk_disponible, pk_slot__contains=tipo_vehiculo[0])
                slot_serializer = ParqueaderosVisitaSerializer(slot_intance, many=True)

        except Exception as e:
            print(e)
        
        if slot_intance is None:
            return Response({'Message':'Error en Parquedaros'}, status=status.HTTP_409_CONFLICT)
        return Response({'Message':'Success','ParqueaderosDisponibles':slot_serializer.data}, status=status.HTTP_200_OK)
    
    #Actualizar Disponibilidad de Parquedaero
    def put(self, request, pk, format=None):
        try:
            parquedaro = ParqueaderosVisita.objects.get(pk_slot=pk)
            serializer = ParqueaderosVisitaSerializer(parquedaro, data=request.data, many=False)
        except Exception as e:
            print(e)
            
        if serializer.is_valid():
            serializer.save()
            return Response({'Message':'Updated', 'ParqueaderoDisponible':serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class IngresoSalidaVisitaVehiculoView(APIView):
    authentication_classes=[TokenAuthentication,]
    permission_classes = [DjangoModelPermissions]
     
    queryset = IngresoSalidaVehiculoVisita.objects.all()
    serializer_class = IngresoVisitaSerializer
    
    #Registro de Ingreso de Vehiculo Visita
    #Asignacion de Parqueadero Libre
    def post(self, request, *args, **kwargs):
        try: 
            data = {
                'vi_fecha_hora_ingreso': request.data.get('vi_fecha_hora_ingreso'),
                'pl_placa': request.data.get('pl_placa'),
                'vh_tipo': request.data.get('vh_tipo'),
                'pk_slot' : request.data.get('pk_slot'),
                'pk_status': request.data.get('pk_status'),
                'in_tk_id' :request.data.get('in_tk_id')
            }
            
            serializer = IngresoVisitaSerializer(data=data)
            parquedaro = ParqueaderosVisita.objects.get(pk_slot=data['pk_slot'])
            serializerpk = ParqueaderosVisitaSerializer(parquedaro, data=request.data, many=False)
           
        except Exception as e:
            print(e)
        
        if serializer.is_valid() and serializerpk.is_valid():
            serializer.save()
            serializerpk.save()
            return Response({'Message' : 'Success', "Ingreso" :serializer.data, 'Parqueadero': serializerpk.data }, status=status.HTTP_201_CREATED)
        
        return Response({'Message' : 'Error', "Detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    #Consultar Info de Placa 
    def get(self, request, *args, **kwargs):
        try:
            placa = request.query_params.get("placa", None)
            status = request.query_params.get("status", None)
            intance = None
            serializer_info= None
            serializer= None
            visitante = None
            serializer_visitante = None
            option = None
            
            instance_conjunto = Conjunto.objects.all()
            serializer_conjunto = ConjuntoSerializer(instance_conjunto, many=True)

            if placa != None and status != None:
                option = 1
                
                intance = PlacaVehiculoVisita.objects.get(pl_placa__exact=placa)
                serializer = PlacaVehiculoVisitaSerializer(intance)

                info = IngresoSalidaVehiculoVisita.objects.get(pl_placa=placa, vi_status=status)
                serializer_info = IngresoSalidaSerializer(info)
                
                ingresovisita = IngresoDeVisita.objects.get(pl_placa=placa, vi_status=status)
                serializer_ingresovisita = IngresoDeVisitaSerializer(ingresovisita)
                
                visitante = VisitanteDatos.objects.get(vd_cedula=serializer_ingresovisita.data['vd_cedula'])
                serializer_visitante = VisitanteDatosSerializer(visitante)
                             
                prop_intance = ApartamentoPh.objects.get(id=serializer_ingresovisita.data['ph_propietario'])
                serializer_prop = ApartamentoPhSerializer(prop_intance)    
            elif placa != None:
                option = 2
                intance = PlacaVehiculoVisita.objects.get(pl_placa__exact=placa)
                serializer = PlacaVehiculoVisitaSerializer(intance)

                info = IngresoSalidaVehiculoVisita.objects.filter(pl_placa=placa)
                serializer_info = IngresoSalidaSerializer(info, many=True)
                
                ingresovisita = IngresoDeVisita.objects.filter(pl_placa=placa)
                serializer_ingresovisita = IngresoDeVisitaSerializer(ingresovisita, many=True)

                tot_visitante =[]
                for i in range(len(serializer_ingresovisita.data)):
                    visitante = VisitanteDatos.objects.get(vd_cedula=serializer_ingresovisita.data[i]['vd_cedula'])
                    serializer_visitante = VisitanteDatosSerializer(visitante)
                    
                    tot_visitante.append(serializer_visitante.data)
                
                prop_visitados =[]
                for i in range(len(serializer_ingresovisita.data)):       
                    prop_intance= ApartamentoPh.objects.get(id=serializer_ingresovisita.data[i]['ph_propietario'])
                    serializer_prop = ApartamentoPhSerializer(prop_intance)
                   
                    prop_visitados.append(serializer_prop.data)
            else:
                return Response({'Message':'Ingresa una Placa'})
              
        except Exception as e:
            print(e)
        
        if intance is None:
            return Response({'Message':'Error al Buscar Placa'}, status=status.HTTP_409_CONFLICT)
        
        if option == 1:
            asunto="Ingreso de Visitante al Conjunto"
            #"Registro de Ingreso </br> Placa: "+serializer.data['pl_placa']+"Fecha y Hora Ingreso: "+serializer_info.data['vi_fecha_hora_ingreso']+ \
            #    " Parqueadero: "+serializer_info.data['pk_slot']+" Vistante: "+serializer_visitante.data['vd_nombre']+" Cédula: "+str(serializer_visitante.data['vd_cedula'])+ \
            #    " Teléfono: "+serializer_visitante.data['vd_telefono']+" Residente: "+serializer_prop.data['ph_propietario']+" Teléfono: "+serializer_prop.data['ph_telefono']+ \
            #    " Torre: "+str(serializer_prop.data["ph_torre"])+" Apartamento/Casa: "+str(serializer_prop.data["ph_apartamento"])
            mensaje="Registro de Ingreso Placa: "+serializer.data['pl_placa']+" Fecha y Hora Ingreso: "+serializer_info.data['vi_fecha_hora_ingreso']+ \
                " Parqueadero: "+serializer_info.data['pk_slot']+" Vistante: "+serializer_visitante.data['vd_nombre']+" Cédula: "+str(serializer_visitante.data['vd_cedula'])+ \
                " Teléfono: "+serializer_visitante.data['vd_telefono']+" Residente: "+serializer_prop.data['ph_propietario']+" Teléfono: "+serializer_prop.data['ph_telefono']+ \
                " Torre: "+str(serializer_prop.data["ph_torre"])+" Apartamento/Casa: "+str(serializer_prop.data["ph_apartamento"])
            print("regitro => ",mensaje)
            emails = serializer_prop.data["ph_mail"]
            admin = serializer_conjunto.data[0]["cj_mail"]
            print("mail => ",emails,",",admin)
            SendEmail(asunto,mensaje,emails,admin)
            
            return Response({'Message':'Success','InfoPlacaVisitante':serializer.data, 'InfoIngreso':serializer_info.data, 'VisitanteInfo':serializer_visitante.data, \
            'RegistroVisitante':serializer_ingresovisita.data, 'PropietarioVisitado':serializer_prop.data})
        elif option == 2:
            return Response({'Message':'Success','InfoPlacaVisitante':serializer.data, 'InfoIngreso':serializer_info.data, 'VisitanteInfo':tot_visitante, \
            'RegistroVisitante':serializer_ingresovisita.data, 'PropietarioVisitado':prop_visitados})
        
    #Registro Salida de Vehiculo Visita
    #Liberacion de Parquedaro
    def put(self, request, pk, format=None):
        data = {
                'vi_fecha_hora_salida': request.data.get('vi_fecha_hora_salida'),
                'pl_placa': request.data.get('pl_placa'),
                'pk_slot' : request.data.get('pk_slot'),
                'vi_visitante' : request.data.get('vi_visitante'),
                'fa_monto' : request.data.get('fa_monto'),
                'fa_tiempo' : request.data.get('fa_tiempo'),
                'ph_propietario' : request.data.get('ph_propietario'),
                'pk_status': request.data.get('pk_status'),
                'vi_status' : request.data.get('vi_status')
            }
        
        instance_conjunto = Conjunto.objects.all()
        serializer_conjunto = ConjuntoSerializer(instance_conjunto, many=True)
        
        intance = PlacaVehiculoVisita.objects.get(pl_placa__exact=data['pl_placa'])
        serializerinstance = PlacaVehiculoVisitaSerializer(intance)

        info = IngresoSalidaVehiculoVisita.objects.get(pl_placa=data['pl_placa'], vi_status=True)
        serializer_info = IngresoSalidaSerializer(info)
            
        ingresovisita = IngresoDeVisita.objects.get(pl_placa=data['pl_placa'], vi_status=True)
        serializer_ingresovisita = IngresoDeVisitaSerializer(ingresovisita)
            
        visitante = VisitanteDatos.objects.get(vd_cedula=serializer_ingresovisita.data['vd_cedula'])
        serializer_visitante = VisitanteDatosSerializer(visitante)
                            
        prop_intance = ApartamentoPh.objects.get(id=serializer_ingresovisita.data['ph_propietario'])
        serializer_prop = ApartamentoPhSerializer(prop_intance)  
        #-------------------------------------------------------------------------------------------    
        salida = IngresoSalidaVehiculoVisita.objects.get(id=pk)
        serializer = SalidaVisitaSerializer(salida, data=data, many=False)
        
        parquedaro = ParqueaderosVisita.objects.get(pk_slot=data['pk_slot'])
        serializerpk = ParqueaderosVisitaSerializer(parquedaro, data=request.data, many=False)
        
        visita = IngresoDeVisita.objects.get(pl_placa=data['pl_placa'],vi_status=True)
        serializervisita = SalidaDeVisitaSerializer(visita, data=request.data, many=False)
        
        facturaserializer = FacturacionSerializer(data=data)

        if serializer.is_valid() and serializerpk.is_valid() and serializervisita.is_valid() and facturaserializer.is_valid():
            serializer.save()
            serializerpk.save()
            serializervisita.save()
            facturaserializer.save()
            
            
            asunto="Salida de Visitante del Conjunto"
            mensaje="Registro de Salida Placa: "+serializerinstance.data['pl_placa']+"\n Fecha y Hora Ingreso: "+serializer_info.data['vi_fecha_hora_ingreso']+" Fecha y Hora Salida: "+data['vi_fecha_hora_salida']+"\r\n" + \
                " Monto: $"+data['fa_monto']+" Tiempo: "+str(data['fa_tiempo'])+" horas, Parqueadero: "+serializer_info.data['pk_slot']+"\r\n Visitante: "+serializer_visitante.data['vd_nombre']+" Cédula: "+str(serializer_visitante.data['vd_cedula'])+ \
                " Teléfono: "+serializer_visitante.data['vd_telefono']+"\r\n Residente: "+serializer_prop.data['ph_propietario']+" Teléfono: "+serializer_prop.data['ph_telefono']+"\r\n"+ \
                " Torre: "+str(serializer_prop.data["ph_torre"])+" Apartamento/Casa: "+str(serializer_prop.data["ph_apartamento"])
            emails = serializer_prop.data["ph_mail"]
            admin = serializer_conjunto.data[0]["cj_mail"]
            #emails.append(serializer_prop.data["ph_mail"])
            #emails.append(serializer_conjunto.data[0]["cj_mail"])
            print("mails => ", emails,",", admin)
            SendEmail(asunto,mensaje,emails,admin)
            
            
            return Response({'Message' : 'Success', "Salida" :serializer.data, 'Parqueadero': serializerpk.data, 'InfoVisitante': serializervisita.data, 'Facturacion' : facturaserializer.data}, status=status.HTTP_200_OK)
        
        return Response({'Message' : 'Error', "Detail": serializervisita.errors}, status=status.HTTP_400_BAD_REQUEST)


class ResumenVisitaVehiculoView(APIView):
    authentication_classes=[TokenAuthentication,]
    permission_classes = [DjangoModelPermissions]
     
    queryset = IngresoSalidaVehiculoVisita.objects.all()
    serializer_class = IngresoVisitaSerializer
    
     #Consultar Info de Placa 
    def get(self, request, *args, **kwargs):
        try:
            placa = request.query_params.get("placa", None)
            status = request.query_params.get("status", None)
            intance = None
            serializer_info= None
            serializer= None
            visitante = None
            serializer_visitante = None
                       
            intance = PlacaVehiculoVisita.objects.get(pl_placa__exact=placa)
            serializer = PlacaVehiculoVisitaSerializer(intance)

            info = IngresoSalidaVehiculoVisita.objects.get(pl_placa=placa, vi_status=status)
            serializer_info = IngresoSalidaSerializer(info)
                
            ingresovisita = IngresoDeVisita.objects.get(pl_placa=placa, vi_status=status)
            serializer_ingresovisita = IngresoDeVisitaSerializer(ingresovisita)
                
            visitante = VisitanteDatos.objects.get(vd_cedula=serializer_ingresovisita.data['vd_cedula'])
            serializer_visitante = VisitanteDatosSerializer(visitante)
                             
            prop_intance = ApartamentoPh.objects.get(id=serializer_ingresovisita.data['ph_propietario'])
            serializer_prop = ApartamentoPhSerializer(prop_intance)    
           
              
        except Exception as e:
            print(e)
        
        if intance is None:
            return Response({'Message':'Error al Buscar Placa'}, status=status.HTTP_409_CONFLICT)
        
            
        return Response({'Message':'Success','InfoPlacaVisitante':serializer.data, 'InfoIngreso':serializer_info.data, 'VisitanteInfo':serializer_visitante.data, \
            'RegistroVisitante':serializer_ingresovisita.data, 'PropietarioVisitado':serializer_prop.data})

class VisitanteDatosView(APIView):
    authentication_classes=[TokenAuthentication,]
    permission_classes = [DjangoModelPermissions]
     
    queryset = VisitanteDatos.objects.all()
    serializer_class = VisitanteDatosSerializer
    
    #Existe Visistante
    def get(self, request, *args, **kwargs):
        try:
            cedula = request.query_params.get("cedula", None)
            cedula_intance = None
            
            if cedula != None:
                cedula_intance = VisitanteDatos.objects.get(vd_cedula__exact=cedula)
                cedula_serializer = VisitanteDatosSerializer(cedula_intance)

        except Exception as e:
            print(e)
        
        if cedula_intance is None:
            return Response({'Message':'No Existe la Cedula'}, status=status.HTTP_409_CONFLICT)
        return Response({'Message':'Success','CedulaVisitante':cedula_serializer.data}, status=status.HTTP_200_OK)
    
    #Registro de Visitante
    def post(self, request, *args, **kwargs):
        try: 
            data = {
                'vd_nombre': request.data.get('vd_nombre'),
                'vd_cedula': request.data.get('vd_cedula'),
                'vd_telefono': request.data.get('vd_telefono'),
                'ph_propietario': request.data.get('ph_propietario'),
                'pl_placa': request.data.get('pl_placa'),
                'pk_slot': request.data.get('pk_slot'),
            }

            serializer = VisitanteDatosSerializer(data=data)
            serializer_visita = IngresoDeVisitaSerializer(data=data)

        except Exception as e:
            print(e)
        
        if serializer.is_valid() and serializer_visita.is_valid():
            serializer.save()
            serializer_visita.save()
            return Response({'Message' : 'Success', 'Visitante' : serializer.data, 'Registro': serializer_visita.data }, status=status.HTTP_201_CREATED)
        
        return Response({'Message' : 'Error', 'Detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    #Ingresa Registro de Visita
    def put(self, request, format=None):
        try:
            data = {
                    'vd_cedula': request.data.get('vd_cedula'),
                    'ph_propietario': request.data.get('ph_propietario'),
                    'pl_placa': request.data.get('pl_placa'),
                    'pk_slot': request.data.get('pk_slot')
                }
            serializer_visita = IngresoDeVisitaSerializer(data=data)
            #print(serializer_visita)
        except Exception as e:
            print(e)
            
        if serializer_visita.is_valid():
            serializer_visita.save()
            return Response({'Message' : 'Success', "VisitaRegistro" :serializer_visita.data,}, status=status.HTTP_201_CREATED)
        
        return Response({'Message' : 'Error', "Detail": serializer_visita.errors}, status=status.HTTP_400_BAD_REQUEST)
    
class CalculoTiempoMontoView(APIView):
    authentication_classes=[TokenAuthentication,]
    permission_classes = [DjangoModelPermissions]
     
    queryset = IngresoSalidaVehiculoVisita.objects.all()
    serializer_class = IngresoVisitaSerializer
    
    def get(self, request, *args, **kwargs):
        try: 
            placa = request.query_params.get("placa", None)
            fecha_hora_salida = request.query_params.get("hora", None) #'2024-07-12T11:30:00'
            cobro = request.query_params.get("cobro", None)
                
            info = IngresoSalidaVehiculoVisita.objects.get(pl_placa=placa, vi_status=True)
            serializer_info = IngresoSalidaSerializer(info)
            #fecha_hora_ingreso = serializer_info.data['vi_fecha_hora_ingreso']
            
            # Activacion de Tarifa Plena y Variables de Configuracion
            config_instance = Config.objects.get(cn_status=True, cn_config=cobro)
            config_serializer = ConfigSerializer(config_instance)
            hora_inicial_plena = config_serializer.data['cn_hora_inicial'] 
            hora_final_plena = config_serializer.data['cn_hora_final']
            status_tarifa_plena = config_serializer.data['cn_plena_status']
            costo_tarifa_plena = config_serializer.data['cn_plena_monto']
            
            # Costo Tarifa Pension
            costo_pension = None
            costopension = CostoPension.objects.all()
            costo_pension_serializer = CostoPensionSerializer(costopension, many=True) 
            if(costo_pension_serializer.data[0]['cp_monto'] != "0.00"):
                costo_pension = costo_pension_serializer.data[0]['cp_monto']
            
             #Variables de Configuracion
            config_cobro = config_serializer.data['cn_config']
            if config_cobro == 1:
                costo_minuto = config_serializer.data['cn_monto']
                tiempo_libre = config_serializer.data['cn_hgratis'] #minutos
            elif config_cobro == 2:
                costo_hora = config_serializer.data['cn_monto']
                tiempo_libre = config_serializer.data['cn_hgratis'] #minutos
                
            hora_gratis = int((tiempo_libre/60))
            
            
            # Convertir Fechas
            fecha_hora_ingreso = datetime.strptime(serializer_info.data['vi_fecha_hora_ingreso'], '%Y-%m-%dT%H:%M:%S')
            fecha_hora_salida = datetime.strptime(fecha_hora_salida, '%Y-%m-%dT%H:%M:%S')
            
            print('Ingreso:',fecha_hora_ingreso)
            print('Salida:',fecha_hora_salida)
            print('HoraGratis:',str(hora_gratis))
            
            # Regla 1 -- Cobro por Horas
            if(fecha_hora_salida > fecha_hora_ingreso and status_tarifa_plena == False):
                print('Regla 1')
                horas_totales = (fecha_hora_salida - fecha_hora_ingreso)/60
                tiempo_total = str(horas_totales).split(":")
                horas_cobro = (int(tiempo_total[1]))
                minutos_cobro = int(float(tiempo_total[2]))
                
                #Si esta dentro de las horas gratis
                if(horas_cobro < hora_gratis):
                    print("1.1")
                    monto_total = '0.00'
                #Si supero las horas gratis
                elif(horas_cobro >= hora_gratis and minutos_cobro > 0): 
                    print("1.2")
                    if minutos_cobro > 0:
                        sum_hora = (60 - minutos_cobro)
                        plus_hora = (sum_hora + minutos_cobro) / 60 
                    monto_total = format(((horas_cobro + plus_hora) - hora_gratis) * costo_hora,".2f")
                else:
                    print("1.3")
                    monto_total = format((horas_cobro - hora_gratis) * costo_hora,".2f")
                
                print('hrs',str(horas_cobro))
                print('min',str(minutos_cobro))
                print('monto',str(monto_total))
                
            # Regla 2 Cobro por Horas mas Tarifa Plena
            elif(fecha_hora_salida > fecha_hora_ingreso and status_tarifa_plena == True):
                horas_cobro = None
                               
                #Fecha Actual
                response = requests.get("http://worldtimeapi.org/api/timezone/America/Bogota")
                dataFechaActual = response.json()
                
                fechaActualHoraIniPlena = dataFechaActual['datetime'][0:10]+" "+hora_inicial_plena
                fechaActualHoraFinPlena = dataFechaActual['datetime'][0:10]+" "+hora_final_plena
                
                print('fecha_ini_plena', fechaActualHoraIniPlena)
                #print('h_plena_ini',hora_inicial_plena)
                from datetime import timedelta
                td = timedelta(1)
                fechaActualHoraIniPlena = datetime.strptime(fechaActualHoraIniPlena, '%Y-%m-%d %H:%M:%S')
                fechaActualHoraFinPlena = datetime.strptime(fechaActualHoraFinPlena, '%Y-%m-%d %H:%M:%S')
                fechaActualHoraFinPlena =fechaActualHoraFinPlena+td
                print('fecha_fin_plena',fechaActualHoraFinPlena)
                #print('h_plena_fin',hora_final_plena)
                
                if(fecha_hora_ingreso < fechaActualHoraIniPlena and fecha_hora_salida < fechaActualHoraIniPlena or fecha_hora_salida > fechaActualHoraIniPlena):
                    print('2')
                    
                    #Horas Plenas
                    horas_plenas = (fechaActualHoraFinPlena - fechaActualHoraIniPlena)/60
                    hora_plena_total = str(horas_plenas).split(":")
                    hora_plena = (int(hora_plena_total[1]))
                    
                    #Horas de Parkeo
                    horas_totales = (fecha_hora_salida - fecha_hora_ingreso)/60
                    tiempo_total = str(horas_totales).split(":")
                    horas_cobro = (int(tiempo_total[1]))
                    minutos_cobro = int(float(tiempo_total[2]))
                    
                    dif_dias_hr = abs((fecha_hora_salida - fecha_hora_ingreso).days)
                    dias_pension = dif_dias_hr
                    dif_dias_hr = dif_dias_hr * 24
                    
                    
                    print('dif_dias_hr',dif_dias_hr)
                    print('dias_pension',dias_pension)
                    print('horas_totales',horas_totales)
                    print('hora_plena',hora_plena)
                    print('horas_cobro',horas_cobro)
                    print('minutos_cobro',minutos_cobro)
                    
                    if((horas_cobro >= hora_plena and dif_dias_hr == 0) or (horas_cobro < hora_plena and dif_dias_hr == 0)):
                        #Cobra una plena mas horas adicionales
                        
                        if(horas_cobro <= hora_gratis):
                            print('Regla 2.1')
                            horas_totales = (fecha_hora_salida - fecha_hora_ingreso)/60
                            tiempo_total = str(horas_totales).split(":")
                            horas_cobro = (int(tiempo_total[1]))
                            minutos_cobro = int(float(tiempo_total[2]))
                            
                            #Si esta dentro de las horas gratis
                            if(horas_cobro < hora_gratis):
                                print("3.1")
                                monto_total = '0.00'
                            #Si supero las horas gratis
                            elif(horas_cobro >= hora_gratis and minutos_cobro > 0): 
                                print("3.2")
                                if minutos_cobro > 0:
                                    sum_hora = (60 - minutos_cobro)
                                    plus_hora = (sum_hora + minutos_cobro) / 60 
                                monto_total = format(((horas_cobro + plus_hora) - hora_gratis) * costo_hora,".2f")
                                horas_cobro = horas_cobro + 1
                            else:
                                print("3.3")
                                monto_total = format((horas_cobro - hora_gratis) * costo_hora,".2f")
                        else:
                            print('Regla 2.2')   
                            hora_gratis = 0
                            calculo_hrs_plena = 0
                            if(horas_cobro > hora_plena):
                                calculo_hrs_plena = float(str(horas_cobro - hora_plena)+"."+str(minutos_cobro)) * costo_hora
                            calculo_plena = costo_tarifa_plena + calculo_hrs_plena
                            print('calculo_hrs_plena',calculo_hrs_plena)
                            print('calculo_plena',calculo_plena)
                            monto_total = calculo_plena
                        
                    elif(dif_dias_hr >= 24):
                        #Cobra Pension completa por dias
                        print('Regla 2.3')
                        calculo_pension = (costo_pension * dias_pension)
                        calculo_hrs_pension = float(str(horas_cobro)+"."+str(minutos_cobro)) * costo_hora
                        print('calculo_pension', calculo_pension)
                        print('calculo_hrs_pension',calculo_hrs_pension)
                        hora_gratis = 0
                        hora_adicional = 0
                        monto_total = calculo_pension + calculo_hrs_pension
                        if(minutos_cobro >= 1):
                            hora_adicional = 1
                        horas_cobro = dif_dias_hr + horas_cobro + hora_adicional
                        
                else:
                    print('Regla 3')
                    horas_totales = (fecha_hora_salida - fecha_hora_ingreso)/60
                    tiempo_total = str(horas_totales).split(":")
                    horas_cobro = (int(tiempo_total[1]))
                    minutos_cobro = int(float(tiempo_total[2]))
                    
                    #Si esta dentro de las horas gratis
                    if(horas_cobro < hora_gratis):
                        print("3.1")
                        monto_total = '0.00'
                    #Si supero las horas gratis
                    elif(horas_cobro >= hora_gratis and minutos_cobro > 0): 
                        print("3.2")
                        if minutos_cobro > 0:
                            sum_hora = (60 - minutos_cobro)
                            plus_hora = (sum_hora + minutos_cobro) / 60 
                        monto_total = format(((horas_cobro + plus_hora) - hora_gratis) * costo_hora,".2f")
                        horas_cobro = horas_cobro + 1
                    else:
                        print("3.3")
                        monto_total = format((horas_cobro - hora_gratis) * costo_hora,".2f")
                    
                    print('hrs',str(horas_cobro))
                    print('min',str(minutos_cobro))
                    print('monto',str(monto_total))
                    
                    #if(fecha_hora_salida > fechaActualHoraIniPlena and fecha_hora_salida < fechaActualHoraFinPlena):
                     #   print('2.1.1')
                
           
           

                return Response({'FechaHoraIngreso': fecha_hora_ingreso, 'FechaHoraSalida':fecha_hora_salida,  'DuracionHoraFrac':horas_cobro, 'MontoPagar': monto_total, 'HoraGratis': hora_gratis })
        except Exception as e:
            print(e)
            return(Response({'Message':'No Existe la Placa'}, status=status.HTTP_400_BAD_REQUEST))

class ReporteParqueaderosDhView(APIView):
    authentication_classes=[TokenAuthentication,]
    permission_classes = [DjangoModelPermissions]
     
    queryset = IngresoSalidaVehiculoVisita.objects.all()
    serializer_class = IngresoVisitaSerializer
    
    def get(self, request, *args, **kwargs):
        try:
            datos = []
                
            info_vehiculo = IngresoSalidaVehiculoVisita.objects.filter(vi_status=True)
            serializer_info_vehiculo = IngresoSalidaSerializer(info_vehiculo, many=True)
            
            for i in range(len(serializer_info_vehiculo.data)):
                #print(serializer_info_vehiculo.data[i])
                #datos.append(serializer_info_vehiculo.data[i])
                ingresovisita = IngresoDeVisita.objects.filter(vi_status=True)
                serializer_ingresovisita = IngresoDeVisitaSerializer(ingresovisita, many=True)
             
                visitante = VisitanteDatos.objects.get(vd_cedula=serializer_ingresovisita.data[i]['vd_cedula'])
                serializer_visitante = VisitanteDatosSerializer(visitante)
                
                prop_intance= ApartamentoPh.objects.get(id=serializer_ingresovisita.data[i]['ph_propietario'])
                serializer_prop = ApartamentoPhSerializer(prop_intance)
                
                id_tx={'id':i}
               
                lista = id_tx,serializer_info_vehiculo.data[i],serializer_ingresovisita.data[i],serializer_visitante.data, serializer_prop.data
                
                datos.append(lista)

        except Exception as e:
            print(e)
        
        
        if info_vehiculo is None:
            return Response({'Message':'Error al Buscar Placa'}, status=status.HTTP_409_CONFLICT)
        
        return Response({'Message':'Success','VehiculosParqueaderoDh':datos})

class ReporteCarrosParqueadosDhView(APIView):
    authentication_classes=[TokenAuthentication,]
    permission_classes = [DjangoModelPermissions]
    
    queryset = IngresoSalidaVehiculoVisita.objects.all()
    serializer_class = IngresoVisitaSerializer
    
    def get(self, request, *args, **kwargs):
        try:
            vehiculos = []
            tipo_vehiculo = TipoVehiculo.objects.all()
            serializer_tipo_vehiculo = TipoVehiculoSerializer(tipo_vehiculo, many=True)
            #print(serializer_tipo_vehiculo.data)
            for i in range(len(serializer_tipo_vehiculo.data)):
                #print(serializer_tipo_vehiculo.data[i]['vh_desc'])            
                info_vehiculo = IngresoSalidaVehiculoVisita.objects.filter(vi_status=True, vh_tipo=serializer_tipo_vehiculo.data[i]['vh_tipo'])
                serializer_info_vehiculo = IngresoSalidaSerializer(info_vehiculo, many=True)
                #print(serializer_tipo_vehiculo.data[i]['vh_desc'], len(serializer_info_vehiculo.data))
                lista = {serializer_tipo_vehiculo.data[i]['vh_desc']: len(serializer_info_vehiculo.data)}
    
                vehiculos.append(lista)
        except Exception as e:
            print(e)
        
        return Response({'Message':'Success','TotalVehiculosParqueadosDh':vehiculos})
    
class ReporteParqueaderosLibresDhView(APIView):
    authentication_classes=[TokenAuthentication,]
    permission_classes = [DjangoModelPermissions]
    
    queryset = ParqueaderosVisita.objects.all()
    serializer_class = ParqueaderosVisitaSerializer
    
    def get(self, request, *args, **kwargs):
        try:
            parqueaderos_libres_carro=[]
            parqueaderos_libres_moto=[]
            libres = ParqueaderosVisita.objects.filter(pk_status=True)
            serializer_libres = ParqueaderosVisitaSerializer(libres, many=True)
            
            for i in range(len(serializer_libres.data)):
                #print(serializer_libres.data[i]['pk_slot'][0] )
                if serializer_libres.data[i]['pk_slot'][0] == 'C':
                    parqueaderos_libres_carro.append(serializer_libres.data[i]['pk_slot'])
                elif serializer_libres.data[i]['pk_slot'][0] == 'M':
                    parqueaderos_libres_moto.append(serializer_libres.data[i]['pk_slot'])
            
            print(len(parqueaderos_libres_carro), len(parqueaderos_libres_moto))
        
        except Exception as e:
            print(e)
            
        return Response({'Message':'Success','ParquedaroCarrosDisponibles':len(parqueaderos_libres_carro), 'ParquedaroMotosDisponibles': len(parqueaderos_libres_moto)})
    
    
    
#Fecha y Hora

class GetDateTimeView(APIView):
    authentication_classes=[TokenAuthentication,]
    permission_classes = [DjangoModelPermissions]
    
    queryset = IngresoSalidaVehiculoVisita.objects.all()
    serializer_class = IngresoVisitaSerializer
    
    def get(self, request, *args, **kwargs):
        response = requests.get("http://worldtimeapi.org/api/timezone/America/Bogota")
        data = response.json()
        
        fecha = data['datetime'][0:10]
        hora = data['datetime'][11:19]
        fecha_hora_f1 = fecha+" "+hora
        fecha_hora_f2 = data['datetime'][0:19]
        
        return Response({'FechaHoraIngreso' : fecha_hora_f1, 'FechaHoraSalida' : fecha_hora_f2})
    
#Reporte de Ingresos
class ReporteIngresosView(APIView):
    authentication_classes=[TokenAuthentication,]
    permission_classes = [DjangoModelPermissions]
    
    queryset = IngresoSalidaVehiculoVisita.objects.all()
    serializer_class = IngresoVisitaSerializer
    
    
    def get(self, request, *args, **kwargs):
        try:
            fecha_inicial = request.query_params.get("fechaini", None)
            fecha_final = request.query_params.get("fechafin", None)
            datos=[]
   
            
            if(fecha_final < fecha_inicial):
                return Response({'Error' : 'Fechas no validas'})
            else:
                ingreso_salida_vehiculo = IngresoSalidaVehiculoVisita.objects.filter(vi_fecha_hora_ingreso__gte=fecha_inicial+(' 00:00:00')).filter(vi_fecha_hora_salida__lte=fecha_final+(' 23:59:59'))
                serializer_vehiculo= IngresoSalidaSerializer(ingreso_salida_vehiculo, many=True)
                #print(serializer_vehiculo.data)
                
                for i in range(len(serializer_vehiculo.data)):
                   #print(serializer_vehiculo.data[i]['pl_placa'])
                    
                    ingresovisita = IngresoDeVisita.objects.filter(pl_placa__exact=serializer_vehiculo.data[i]['pl_placa']).filter(vi_status=False)
                    #print(ingresovisita)
                    serializer_ingresovisita = IngresoDeVisitaReporteSerializer(ingresovisita, many=True)
                    #print(serializer_ingresovisita.data[0]['vd_cedula'])
                    
                    visitante = VisitanteDatos.objects.get(vd_cedula=serializer_ingresovisita.data[0]['vd_cedula'])
                    serializer_visitante = VisitanteDatosSerializer(visitante)
                    #print(serializer_visitante.data)
           
                    prop_intance = ApartamentoPh.objects.get(id=serializer_ingresovisita.data[0]['ph_propietario'])
                    serializer_prop = ApartamentoPhSerializer(prop_intance)
                    #print(serializer_prop)
                    
                    fact_intance = Facturacion.objects.filter(vi_visitante=serializer_ingresovisita.data[0]['id']).filter(vi_fecha_hora_salida__gte=fecha_inicial+(' 00:00:00')).filter(vi_fecha_hora_salida__lte=fecha_final+(' 23:59:59'))
                    serializer_fact = FacturacionSerializer(fact_intance, many=True)
                    #print(serializer_fact.data)
                    
                    #print(serializer_vehiculo.data[i]['vi_fecha_hora_ingreso'])
                    #print(serializer_vehiculo.data[i]['vi_fecha_hora_salida'])
                    #print(serializer_vehiculo.data[i]['pl_placa'])
                    #print(serializer_vehiculo.data[i]['pk_slot'])
                    #print(serializer_ingresovisita.data[0]['vd_cedula'])
                    #print(serializer_visitante.data['vd_nombre'])
                    #print(serializer_prop.data['ph_propietario'])
                    #print(serializer_prop.data['ph_apartamento'])
                    #print(serializer_prop.data['ph_torre'])
                    #print(serializer_fact.data[0]['fa_tiempo'])
                    #print(serializer_fact.data[0]['fa_monto'])
                    
                    lista = {'vi_fecha_hora_ingreso':serializer_vehiculo.data[i]['vi_fecha_hora_ingreso'],'vi_fecha_hora_salida':serializer_vehiculo.data[i]['vi_fecha_hora_salida'],'pl_placa':serializer_vehiculo.data[i]['pl_placa'], \
                        'pk_slot':serializer_vehiculo.data[i]['pk_slot'], 'vd_cedula':serializer_ingresovisita.data[0]['vd_cedula'], 'vd_nombre':serializer_visitante.data['vd_nombre'], \
                        'ph_propietario':serializer_prop.data['ph_propietario'],'ph_apartamento':serializer_prop.data['ph_apartamento'],'ph_torre':serializer_prop.data['ph_torre'], \
                        'fa_tiempo':serializer_fact.data[0]['fa_tiempo'], 'fa_monto':serializer_fact.data[0]['fa_monto']}
                    
                    datos.append(lista)
             
                
        except Exception as e:
            print(e)
        return Response({'Generando' : datos })
    
#Recaudo por dia
class ReporteRecaudoView(APIView):
    authentication_classes=[TokenAuthentication,]
    permission_classes = [DjangoModelPermissions]
    
    queryset = Facturacion.objects.all()
    serializer_class = FacturacionSerializer
    
    
    def get(self, request, *args, **kwargs):
        try:
            datos=[]
            datos_pension=[]
            datos_total=[]
            #fecha_inicial = request.query_params.get("fechaini", None)
            fecha_final = request.query_params.get("fechafin", None)
            
            #fact_intance = Facturacion.objects.filter(vi_fecha_hora_salida__gte=fecha_inicial+(' 00:00:00')).filter(vi_fecha_hora_salida__lte=fecha_final+(' 23:59:59'))
            fact_intance = Facturacion.objects.filter(vi_fecha_hora_salida__lte=fecha_final+(' 23:59:59')).filter(fa_status_caja=True)
            serializer_fact = FacturacionSerializer(fact_intance, many=True)
            
            #print(serializer_fact.data)
            for i in range(len(serializer_fact.data)):
               #print(serializer_fact.data[i]['fa_monto'])
                lista = float(serializer_fact.data[i]['fa_monto'])
                datos.append(lista)
            
            parking = format(sum(datos),'.2f')
            
            pension_instance = Pension.objects.filter(pe_fecha_ini__lte=fecha_final+(' 23:59:59')).filter(pe_status_caja=True)
            serializer_pension = PensionSerializer(pension_instance, many=True)
            
            for i in range(len(serializer_pension.data)):
                lista = float(serializer_pension.data[i]['pe_monto'])
                datos_pension.append(lista)
            
            pension = format(sum(datos_pension),'.2f')
            
            caja_instance = Caja.objects.filter(cj_fecha_apertura__lte=fecha_final+(' 23:59:59')).filter(cj_status_caja=True)
            serializer_caja = CajaSerializer(caja_instance, many=True)
            print(serializer_caja.data[0]['cj_base_caja'])
            if serializer_caja.data[:]:
                lista = float(serializer_caja.data[0]['cj_base_caja'])
                datos_total.append(lista)
            else:
                datos_total.append(float('0.00'))
            
            datos_total.append(sum(datos))
            datos_total.append(sum(datos_pension))
            #datos_total.append(serializer_caja.data['cj_base_caja'])
            total = format(sum(datos_total),'.2f')
            #print(sum(datos))
            #print(datos)
        except Exception as e:
            print(e)
        return Response({'Parking': parking, 'Pension': pension, 'Total': total})
    
    
    
    
class ConfigTipoPagoView(APIView):
    authentication_classes=[TokenAuthentication,]
    permission_classes = [DjangoModelPermissions]
    
    queryset = Config.objects.all()
    serializer_class = ConfigSerializer
    
    def get(self, request, *args, **kwargs):
        try:
            config_instance = Config.objects.filter(cn_status=True)
            #print(config_instance)
            serializer_config = ConfigSerializer(config_instance, many=True)
            #print(serializer_config)
        except Exception as e:
            print(e)
        
        return Response({'Configuracion':serializer_config.data})
        
    
class ConjuntoView(APIView):
    authentication_classes=[TokenAuthentication,]
    permission_classes = [DjangoModelPermissions]
    
    queryset = Conjunto.objects.all()
    serializer_class = ConjuntoSerializer
    
    def get(self, request, *args, **kwargs):
        try:
            conjunto_instance = Conjunto.objects.all()
            serializer_conjunto = ConjuntoSerializer(conjunto_instance, many=True)
        except Exception as e:
            print(e)
            
        return Response({'Conjunto':serializer_conjunto.data})

class ImpresoraView(APIView):
    authentication_classes=[TokenAuthentication,]
    permission_classes = [DjangoModelPermissions]
    
    queryset = Impresora.objects.all()
    serilizer_class = ImpresoraSerializer
    
    def get(self, request, *args, **kwargs):
        try:
            impresora_instance = Impresora.objects.all()
            serializer_impresora = ImpresoraSerializer(impresora_instance, many=True)
        except Exception as e:
            print(e)
            
        return Response({'Impresora':serializer_impresora.data})
    
class CostoPensionView(APIView):
    authentication_classes=[TokenAuthentication,]
    permission_classes = [DjangoModelPermissions]
    
    queryset = CostoPension.objects.all()
    serializer_class = CostoPensionSerializer
    
    def get(self, request, *args, **kwargs):
        try:
            costopension_instance = CostoPension.objects.all()
            serializer_costopension = CostoPensionSerializer(costopension_instance, many=True)
        except Exception as e:
            print(e)
        
        return Response({'Monto':serializer_costopension.data})
    
class PensionView(APIView):
    authentication_classes=[TokenAuthentication,]
    permission_classes = [DjangoModelPermissions]
    
    queryset = Pension.objects.all()
    serializer_pension = PensionSerializer
    
    def post(self, request, *args, **kwargs):
        try: 
            data = {
                'pe_placa': request.data.get('pe_placa'),
                'pe_nombre': request.data.get('pe_nombre'),
                'pe_cedula': request.data.get('pe_cedula'),
                'pe_fecha_ini': request.data.get('pe_fecha_ini'),
                'pe_fecha_fin': request.data.get('pe_fecha_fin'),
                'pe_monto': request.data.get('pe_monto'),
                'pe_slot': request.data.get('pe_slot'),
                'pe_tipo_vehiculo': request.data.get('pe_tipo_vehiculo'),
                'pe_tk_id' :  request.data.get('pe_tk_id')
            }
            
            serializer = PensionSerializer(data=data)

        except Exception as e:
            print(e)
        
        if serializer.is_valid():
            #print(serializer.is_valid())
            serializer.save()
            return Response({'Message' : 'Success', 'Pension' : serializer.data}, status=status.HTTP_201_CREATED)
        
        return Response({'Message' : 'Error', 'Detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    
    def get(self, request, *args, **kwargs):
        try:
            #placa = request.query_params.get("placa", None)
            #pension_instance = Pension.objects.filter(pe_placa = placa)
            pension_instance = Pension.objects.all().filter(pe_status=True)
            serializer_pension = PensionSerializer(pension_instance, many=True)
        except Exception as e:
            print(e)
        
        return Response({'Pension':serializer_pension.data})
    
    def put(self, request, pk, format=None):
        try:
            data = {
                    'pe_placa': request.data.get('pe_placa'),
                    'pe_status': request.data.get('pe_status')
                }
            pension_instance = Pension.objects.get(pe_id=pk)
            serializer_pension = PensionStatusSerializer(pension_instance,data=data, many=False)
           # print(serializer_pension.is_valid())
        except Exception as e:
            print(e)
            
        if serializer_pension.is_valid():
            serializer_pension.save()
            return Response({'Message' : 'Success', "Updated" :serializer_pension.data,}, status=status.HTTP_201_CREATED)
        
        return Response({'Message' : 'Error', "Detail": serializer_pension.errors}, status=status.HTTP_400_BAD_REQUEST)


class PensionReporteView(APIView):
    authentication_classes=[TokenAuthentication,]
    permission_classes = [DjangoModelPermissions]
    
    queryset = Pension.objects.all()
    serializer_pension = PensionSerializer
    
    def get(self, request, *args, **kwargs):
        try:
            fecha_ini = request.query_params.get("fechaini", None)
            fecha_fin = request.query_params.get("fechafin", None)
            pension_instance = Pension.objects.filter(pe_fecha_ini__gte=fecha_ini+(' 00:00:00')).filter(pe_fecha_ini__lte=fecha_fin+(' 23:59:59'))
            #pension_instance = Pension.objects.all().filter(pe_status=True)
            serializer_pension = PensionSerializer(pension_instance, many=True)
            #print(serializer_pension.data)
        except Exception as e:
            print(e)
        
        return Response({'Reporte':serializer_pension.data})
    
#Caja
class CajaView(APIView):
    authentication_classes=[TokenAuthentication,]
    permission_classes = [DjangoModelPermissions]
    
    queryset = Caja.objects.all()
    serializer = CajaAperturaSerializer
    
    def post(self, request, *args, **kwargs):
        try:
            data = {
                'cj_base_caja' : request.data.get('cj_base_caja'),
                'cj_fecha_apertura' : request.data.get('cj_fecha_apertura'),
                'cj_usuario': request.data.get('cj_usuario')
            }
            
            serializer_caja = CajaAperturaSerializer(data=data)
            
        except Exception as e:
            print(e)
            
        if serializer_caja.is_valid():
            serializer_caja.save()
            return Response({'Message' : 'Success', 'Caja' : serializer_caja.data}, status=status.HTTP_201_CREATED)
        
        return Response({'Message' : 'Error', 'Detail': serializer_caja.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs):
        try:
            fecha_apertura = request.query_params.get('fechaapertura', None)
            #print(fecha_apertura)
            caja_instance = Caja.objects.filter(cj_fecha_apertura__lte=fecha_apertura+(' 23:59:59')).filter(cj_status_caja=True)
            serializer_caja = CajaSerializer(caja_instance, many=True)
           # print(serializer_caja.data[:])
            if serializer_caja.data[:]:
                return Response({'Caja':serializer_caja.data})
            else:
                return Response({'Caja':[{"cj_status_caja":False}]})
                
        except Exception as e:
            print(e)
            
    def put(self, request, pk, format=None):
        try:
            data = {
                    'cj_fecha_cierre': request.data.get('cj_fecha_cierre'),
                    'cj_total_parking': request.data.get('cj_total_parking'),
                    'cj_total_pension': request.data.get('cj_total_pension'),
                    'cj_gran_total': request.data.get('cj_gran_total'),
                    'cj_status_caja': request.data.get('cj_status_caja')
                }
            caja_instance = Caja.objects.get(id=pk)
            serializer_caja = CajaCierreSerializer(caja_instance,data=data, many=False)
        except Exception as e:
            print(e)
            
        if serializer_caja.is_valid():
            serializer_caja.save()
            return Response({'Message' : 'Success', "Updated" :serializer_caja.data,}, status=status.HTTP_201_CREATED)
        
        return Response({'Message' : 'Error', "Detail": serializer_caja.errors}, status=status.HTTP_400_BAD_REQUEST)

class CorteCajaView(APIView):
    authentication_classes=[TokenAuthentication,]
    permission_classes = [DjangoModelPermissions]
    
    queryset = Caja.objects.all()
    serializer = CajaAperturaSerializer
    
    def put(self, request, format=None):
        try:
            datos_pension=[]
            get_pension_instance = Pension.objects.filter(pe_status_caja=True)
            get_pension_serializer = PensionSerializer(get_pension_instance, many=True)
            #print(get_pension_serializer.data)
            #i=0
            #j=0
            for i in range(len(get_pension_serializer.data)):
                #print(get_pension_serializer.data[i]['pe_id'])
                data={
                    #'pe_id': get_pension_serializer.data[i]['pe_id'],
                    #'pe_fecha_ini':request.data.get('pe_fecha_ini'),
                    'pe_status_caja': request.data.get('status_caja')
                }
                
                pension_instance = Pension.objects.get(pe_id=get_pension_serializer.data[i]['pe_id'])
                serializer_pension = StatusPensionCajaSerializer(pension_instance,data=data, many=False)
                if serializer_pension.is_valid():
                    serializer_pension.save()
                datos_pension.append(i)
            
            datos_facturacion=[]
            get_factura_instance = Facturacion.objects.filter(fa_status_caja=True)
            get_factura_serializer = FacturacionSerializer(get_factura_instance, many=True)
            #print(get_factura_serializer.data)
            for j in range(len(get_factura_serializer.data)):
                #print(get_factura_serializer.data[j]['id'])
                dataj={
                    'fa_status_caja': request.data.get('status_caja')
                }
               
                factura_instance = Facturacion.objects.get(id=get_factura_serializer.data[j]['id'])
                factura_serializer = StatusFacturacionCajaSerializer(factura_instance,data=dataj, many=False)
                #print(factura_serializer.is_valid())
                if factura_serializer.is_valid():
                    factura_serializer.save()
                #print(factura_serializer.data)
                datos_facturacion.append(j)
                
                
            return Response({'Message' : 'Success', "Parking": len(datos_facturacion), "Pension" :len(datos_pension)}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
        
        return Response({'Message' : 'Error', "Detail": serializer_pension.errors}, status=status.HTTP_400_BAD_REQUEST)  

class LogView(APIView):
    authentication_classes=[TokenAuthentication,]
    permission_classes = [DjangoModelPermissions]
    
    queryset = Log.objects.all()[:1]
    serializer = LogSerializer
    
    def post(self, request, *args, **kwargs):
        try:
            
            response = requests.get("http://worldtimeapi.org/api/timezone/America/Bogota")
            data_date = response.json()
            
            fecha = data_date['datetime'][0:10]
            hora = data_date['datetime'][11:19]
            lg_fecha = fecha+" "+hora
          
            data = {
                'lg_usuario' : request.data.get('lg_usuario'),
                'lg_log' : request.data.get('lg_log'),
                'lg_fecha' : lg_fecha
            }
     
            serializer_log = LogSerializer(data=data)
            
        except Exception as e:
            print(e)
            
        if serializer_log.is_valid():
            serializer_log.save()
            return Response({'Message' : 'Success', 'Log' : serializer_log.data}, status=status.HTTP_201_CREATED)
        
        return Response({'Message' : 'Error', 'Detail': serializer_log.errors}, status=status.HTTP_400_BAD_REQUEST)

class TiketIdView(APIView):
    authentication_classes=[TokenAuthentication,]
    permission_classes = [DjangoModelPermissions]
    
    queryset = TicketId.objects.all()[:1]
    serializer = TicketIdSerializer
    
    def get(self, request, *args, **kwargs):
        try:
            ticketid_instance = TicketId.objects.last()
            #pension_instance = Pension.objects.all().filter(pe_status=True)
            serializer_ticketid = TicketIdSerializer(ticketid_instance, many=False)
            #print(serializer_ticketid.data)
        except Exception as e:
            print(e)
        
        return Response({'TicketId':serializer_ticketid.data})

    def post(self, request, *args, **kwargs):
        try:
            data = {
                'tk_id' : request.data.get('tk_id')
            }
     
            serializer_ticketid = TicketIdSerializer(data=data)
        except Exception as e:
            print(e)
            
        if serializer_ticketid.is_valid():
            serializer_ticketid.save()
            return Response({'Message' : 'Success', 'Ticket' : serializer_ticketid.data}, status=status.HTTP_201_CREATED)
        
        return Response({'Message' : 'Error', 'Detail': serializer_ticketid.errors}, status=status.HTTP_400_BAD_REQUEST)