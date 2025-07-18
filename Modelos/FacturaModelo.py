import sys
import os
import mysql.connector
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from datetime import datetime
from typing import List, Optional, Dict, Any
from mysql.connector import Error

# Importar los modelos existentes que ya funcionan
try:
    from .PacienteModelo import Paciente
    from .TratamientoModelo import Tratamiento
except ImportError:
    from PacienteModelo import Paciente
    from TratamientoModelo import Tratamiento

class Factura:
    def __init__(self, id_factura: str, 
                 paciente: Paciente, 
                 servicios: List[str], 
                 montos: List[float],
                 fecha_emision: datetime = None,
                 estado_pago: str = "Pendiente"):
        self.id_factura = id_factura
        self.paciente = paciente
        self.servicios = servicios
        self.montos = montos
        self.monto_total = sum(montos)
        self.fecha_emision = fecha_emision or datetime.now()
        self.estado_pago = estado_pago

    def __str__(self):
        servicios_str = "\n".join(f"   - {servicio}: ${monto:.2f}" 
                                 for servicio, monto in zip(self.servicios, self.montos))
        return (f"🧾 Factura ID: {self.id_factura}\n"
                f"📅 Fecha: {self.fecha_emision.strftime('%d/%m/%Y')}\n"
                f"👤 Paciente: {self.paciente.nombre} {self.paciente.apellido}\n"
                f"📋 DUI: {self.paciente.dui}\n"
                f"🩺 Servicios:\n{servicios_str}\n"
                f"💰 Estado: {self.estado_pago}\n"
                f"💵 Total: ${self.monto_total:.2f}\n"
                f"{'='*30}")

class FacturacionModel:
    """Modelo que maneja la lógica de negocio y conexión con la BD"""
    
    @staticmethod
    def obtener_pacientes() -> List[Paciente]:
        """Obtiene todos los pacientes usando el método que ya funciona en CitaModelo"""
        try:
            pacientes = Paciente.obtener_todos_los_pacientes()
            print(f"Pacientes obtenidos para facturación: {len(pacientes)}")
            return pacientes
        except Exception as e:
            print(f"Error al obtener pacientes: {e}")
            return []
    
    @staticmethod
    def obtener_tratamientos() -> List[Tratamiento]:
        """Obtiene todos los tratamientos usando el método que ya funciona en CitaModelo"""
        try:
            tratamientos = Tratamiento.obtener_todos_tratamientos()
            print(f"Tratamientos obtenidos para facturación: {len(tratamientos)}")
            return tratamientos
        except Exception as e:
            print(f"Error al obtener tratamientos: {e}")
            return []

    @staticmethod
    def insertar_factura_bd(factura: Factura) -> bool:
        """Inserta una nueva factura en la base de datos usando el patrón de CitaModelo"""
        conexion = None
        cursor = None
        
        try:
            conexion = mysql.connector.connect(
                host='localhost',
                database='ClinicaDental',
                user='root',
                port=3306,
                password='1234'
            )
            
            cursor = conexion.cursor()
            
            # Insertar cada servicio como una fila separada
            for servicio, monto in zip(factura.servicios, factura.montos):
                query = """
                INSERT INTO Factura (ID_Factura_Custom, ID_Paciente, Fecha_Emision, 
                                   Descripcion_Servicio, Monto_Servicio, Monto_Total, Estado_Pago)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                valores = (
                    factura.id_factura,
                    factura.paciente.id_paciente,
                    factura.fecha_emision,
                    servicio,
                    monto,
                    factura.monto_total,
                    factura.estado_pago
                )
                cursor.execute(query, valores)
            
            conexion.commit()
            print(f"Factura {factura.id_factura} insertada correctamente")
            return True
            
        except Error as e:
            print(f"Error al insertar la factura: {e}")
            if conexion:
                conexion.rollback()
            return False
        finally:
            if cursor:
                cursor.close()
            if conexion and conexion.is_connected():
                conexion.close()

    @staticmethod
    def obtener_todas_facturas_bd() -> List[Factura]:
        """Obtiene todas las facturas de la base de datos usando el patrón de CitaModelo"""
        conexion = None
        cursor = None
        facturas = []
        
        try:
            conexion = mysql.connector.connect(
                host='localhost',
                database='ClinicaDental',
                user='root',
                port=3306,
                password='1234'
            )
            
            cursor = conexion.cursor()
            query = """
            SELECT 
                f.ID_Factura_Custom, f.Fecha_Emision, f.Descripcion_Servicio, 
                f.Monto_Servicio, f.Monto_Total, f.Estado_Pago,
                p.ID_Paciente, p.Nombre, p.Apellido, p.DUI, p.Telefono, p.Correo, p.Fecha_Nacimiento
            FROM Factura f
            JOIN Paciente p ON f.ID_Paciente = p.ID_Paciente
            ORDER BY f.Fecha_Emision DESC
            """
            cursor.execute(query)
            resultados = cursor.fetchall()
            
            # Agrupar por ID_Factura_Custom para manejar múltiples servicios
            facturas_dict = {}
            for row in resultados:
                id_factura = row[0]
                if id_factura not in facturas_dict:
                    # Crear paciente
                    paciente = Paciente(
                        nombre=row[7],
                        apellido=row[8], 
                        dui=row[9],
                        telefono=row[10],
                        correo=row[11],
                        fecha_nacimiento=row[12],
                        id_paciente=row[6]
                    )
                    
                    facturas_dict[id_factura] = {
                        'fecha_emision': row[1],
                        'paciente': paciente,
                        'servicios': [],
                        'montos': [],
                        'monto_total': row[4],
                        'estado_pago': row[5]
                    }
                
                # Agregar servicio y monto
                facturas_dict[id_factura]['servicios'].append(row[2])
                facturas_dict[id_factura]['montos'].append(float(row[3]))
            
            # Crear objetos Factura
            for id_factura, datos in facturas_dict.items():
                factura = Factura(
                    id_factura=id_factura,
                    paciente=datos['paciente'],
                    servicios=datos['servicios'],
                    montos=datos['montos'],
                    fecha_emision=datos['fecha_emision'],
                    estado_pago=datos['estado_pago']
                )
                facturas.append(factura)
                
        except Error as e:
            print(f"Error al obtener facturas: {e}")
        finally:
            if cursor:
                cursor.close()
            if conexion and conexion.is_connected():
                conexion.close()
        
        return facturas

    @staticmethod
    def factura_existe(id_factura: str) -> bool:
        """Verifica si una factura con el ID dado ya existe"""
        conexion = None
        cursor = None
        
        try:
            conexion = mysql.connector.connect(
                host='localhost',
                database='ClinicaDental',
                user='root',
                port=3306,
                password='1234'
            )
            
            cursor = conexion.cursor()
            query = "SELECT COUNT(*) FROM Factura WHERE ID_Factura_Custom = %s"
            cursor.execute(query, (id_factura,))
            count = cursor.fetchone()[0]
            return count > 0
        except Error as e:
            print(f"Error al verificar factura: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conexion and conexion.is_connected():
                conexion.close()
