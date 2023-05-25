from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication

from .models import ApartamentoPh, TorresPh, ApartamentosPh, PlacaVehiculoVisita, \
    ParqueaderosVisita, IngresoSalidaVehiculoVisita, VisitanteDatos, IngresoDeVisita, \
    TipoVehiculo, Config, Facturacion

from .serializer import ApartamentoPhSerializer, \
    TorresPhSerializer, ApartamentosCasasPhSerializer, \
    PlacaVehiculoVisitaSerializer, ParqueaderosVisitaSerializer, \
    IngresoVisitaSerializer, SalidaVisitaSerializer, IngresoSalidaSerializer, \
    VisitanteDatosSerializer, IngresoDeVisitaSerializer, SalidaDeVisitaSerializer, \
    TipoVehiculoSerializer, ConfigSerializer, FacturacionSerializer


from rest_framework.permissions import DjangoModelPermissions
from datetime import *

from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import get_template
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# Create your views here.

def SendEmail(asunto, mensaje, emails):
    #send_mail(subjet=asunto, menssage=mensaje, from_email=settings.EMAIL_HOST_USER, recipient_list=emails)
    template = settings.TEMPLATES[0]['DIRS']
    message = get_template(template[0]+"/email.html").render({'datos':mensaje})

    
    mail = EmailMessage(
        subject=asunto,
        body=message,
        from_email=settings.EMAIL_HOST_USER,
        to=[emails, settings.EMAIL_HOST_USER],
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
                'pk_status': request.data.get('pk_status')
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
            asunto="Ingreso de Visitante al Conjunto la Sierra PH - Madrid"
            #"Registro de Ingreso </br> Placa: "+serializer.data['pl_placa']+"Fecha y Hora Ingreso: "+serializer_info.data['vi_fecha_hora_ingreso']+ \
            #    " Parqueadero: "+serializer_info.data['pk_slot']+" Vistante: "+serializer_visitante.data['vd_nombre']+" Cédula: "+str(serializer_visitante.data['vd_cedula'])+ \
            #    " Teléfono: "+serializer_visitante.data['vd_telefono']+" Residente: "+serializer_prop.data['ph_propietario']+" Teléfono: "+serializer_prop.data['ph_telefono']+ \
            #    " Torre: "+str(serializer_prop.data["ph_torre"])+" Apartamento/Casa: "+str(serializer_prop.data["ph_apartamento"])
            mensaje="Registro de Ingreso Placa: "+serializer.data['pl_placa']+" Fecha y Hora Ingreso: "+serializer_info.data['vi_fecha_hora_ingreso']+ \
                " Parqueadero: "+serializer_info.data['pk_slot']+" Vistante: "+serializer_visitante.data['vd_nombre']+" Cédula: "+str(serializer_visitante.data['vd_cedula'])+ \
                " Teléfono: "+serializer_visitante.data['vd_telefono']+" Residente: "+serializer_prop.data['ph_propietario']+" Teléfono: "+serializer_prop.data['ph_telefono']+ \
                " Torre: "+str(serializer_prop.data["ph_torre"])+" Apartamento/Casa: "+str(serializer_prop.data["ph_apartamento"])
            print(mensaje)
            emails = serializer_prop.data["ph_mail"]
            SendEmail(asunto,mensaje,emails)
            
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
            
            
            asunto="Salida de Visitante del Conjunto la Sierra PH - Madrid"
            mensaje="Registro de Salida Placa: "+serializerinstance.data['pl_placa']+"\n Fecha y Hora Ingreso: "+serializer_info.data['vi_fecha_hora_ingreso']+" Fecha y Hora Salida: "+data['vi_fecha_hora_salida']+"\r\n" + \
                " Monto: $"+data['fa_monto']+" Tiempo: "+str(data['fa_tiempo'])+" horas, Parqueadero: "+serializer_info.data['pk_slot']+"\r\n Visitante: "+serializer_visitante.data['vd_nombre']+" Cédula: "+str(serializer_visitante.data['vd_cedula'])+ \
                " Teléfono: "+serializer_visitante.data['vd_telefono']+"\r\n Residente: "+serializer_prop.data['ph_propietario']+" Teléfono: "+serializer_prop.data['ph_telefono']+"\r\n"+ \
                " Torre: "+str(serializer_prop.data["ph_torre"])+" Apartamento/Casa: "+str(serializer_prop.data["ph_apartamento"])
            emails = serializer_prop.data["ph_mail"]
            SendEmail(asunto,mensaje,emails)
            
            
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
            hora = request.query_params.get("hora", None)
            cobro = request.query_params.get("cobro", None)
                
            info = IngresoSalidaVehiculoVisita.objects.get(pl_placa=placa, vi_status=True)
            serializer_info = IngresoSalidaSerializer(info)
            ingreso = serializer_info.data['vi_fecha_hora_ingreso']
        
            fecha_hora_ingreso = datetime.strptime(serializer_info.data['vi_fecha_hora_ingreso'], '%Y-%m-%dT%H:%M:%S')
            #print(fecha_hora_ingreso)
            fecha_hora_salida = datetime.strptime(hora, '%Y-%m-%dT%H:%M:%S')
            #print(fecha_hora_salida)
            time_calculado = (fecha_hora_salida - fecha_hora_ingreso)/60

            #print(str(time_calculado))
            
            tiempo = str(time_calculado).split(":")
            #print("split", tiempo)
            horas = (int(tiempo[1])*60)
            minutos = int(float(tiempo[2]))
            #print(minutos)
            minutos_totales = (horas+minutos)
            #print("horas",((horas+minutos)/60))
            
            config_instance = Config.objects.get(cn_status=True, cn_config=cobro)
            config_serializer = ConfigSerializer(config_instance)
            
            #Variables de Configuracion
            config_cobro = config_serializer.data['cn_config']
            if config_cobro == 1:
                costo_minuto = config_serializer.data['cn_monto']
                tiempo_libre = config_serializer.data['cn_hgratis'] #minutos
            elif config_cobro == 2:
                costo_hora = config_serializer.data['cn_monto']
                tiempo_libre = config_serializer.data['cn_hgratis'] #minutos
            
            cobro = None
            
            #Cobro por Minuto
            if config_cobro == 1:
                if minutos_totales <= tiempo_libre: #tiempo de horas (minutos) libres
                    cobro = '0.00'
                elif minutos_totales >= (tiempo_libre+1):
                    cobro = format( (minutos_totales - tiempo_libre) * costo_minuto ,".2f")

                return Response({'FechaHoraIngreso': ingreso, 'FechaHoraSalida':fecha_hora_salida, 'DuracionHoraFrac': int(minutos_totales), 'MontoPagar': cobro, 'TiempoLibreMin': int(tiempo_libre)})
            
            #Cobro Hora o Fraccion  
            elif config_cobro == 2:
                #print("entra en 2")
                hora = (int(tiempo[1]))
                if hora < (tiempo_libre/60): #Hora(s) Gratis
                    cobro = "0.00"
                    horas_totales = str(hora)+":"+str(minutos)
                    hora_gratis = (tiempo_libre/60)
                elif hora >= 1 or hora >= (tiempo_libre/60):
                    #print(hora)
                    
                    plushora = 0
                    if minutos > 0:
                        sumhora = (60 - minutos)
                        #print("min",minutos)
                        #print(sumhora)
                        plushora = (sumhora + minutos) / 60 
                        #print("plushora",plushora)
                    horas_totales = str(int((hora + plushora)))
                    horas_totales_cobro = int((hora + plushora))
                    hora_gratis = (tiempo_libre/60)
                    #print(horas_totales)
                    cobro =  format( (horas_totales_cobro - hora_gratis) * costo_hora ,".2f") #Menos Hora(s) Gratis
            

                return Response({'FechaHoraIngreso': ingreso, 'FechaHoraSalida':fecha_hora_salida,  'DuracionHoraFrac':horas_totales, 'MontoPagar': cobro, 'HoraGratis': int(hora_gratis) })
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
import requests
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