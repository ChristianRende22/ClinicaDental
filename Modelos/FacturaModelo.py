import mysql.connector
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from datetime import datetime
from typing import List, Optional, Dict, Any
from Modelos.PacienteModelo import Paciente 
from mysql.connector import Error

class Tratamiento:
    """Clase para representar un tratamiento"""
    def __init__(self, id_tratamiento: int, id_doctor: str, descripcion: str, 
                 costo: float, fecha: datetime, estado: str = "Pendiente"):
        self.id_tratamiento = id_tratamiento
        self.id_doctor = id_doctor
        self.descripcion = descripcion
        self.costo = costo
        self.fecha = fecha
        self.estado = estado
    
    def __str__(self):
        return f"{self.descripcion} - ${self.costo:.2f}"

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
    def _get_connection():
        """Obtiene una conexión a la base de datos"""
        try:
            return mysql.connector.connect(
                host='localhost',
                port=3306,
                database='ClinicaDental',
                user='root',
                password='1234',
                buffered=True,
                consume_results=True
            )
        except Error as e:
            print(f"Error al conectar con la base de datos: {e}")
            return None

    @staticmethod
    def obtener_pacientes() -> List[Paciente]:
        """Obtiene todos los pacientes de la base de datos"""
        conexion = FacturacionModel._get_connection()
        if not conexion:
            return []
        
        pacientes = []
        cursor = None
        try:
            cursor = conexion.cursor(dictionary=True)
            query = "SELECT ID_Paciente, Nombre, Apellido, DUI FROM Paciente ORDER BY Nombre, Apellido"
            cursor.execute(query)
            
            rows = cursor.fetchall()

            for row in rows:
                paciente = Paciente(
                    id_paciente=row['ID_Paciente'],
                    nombre=row['Nombre'],
                    apellido=row['Apellido'],
                    fecha_nacimiento=None,
                    dui=row.get('DUI', 'N/A'),  # Manejar DUI opcional
                    telefono='N/A',  
                    correo='N/A' 
                )
                pacientes.append(paciente)
        except Error as e:
            print(f"Error al obtener pacientes: {e}")
        finally:
            if cursor:
                cursor.close()
            if conexion.is_connected():
                conexion.close()
        
        return pacientes

    @staticmethod
    def obtener_tratamientos() -> List[Tratamiento]:
        """Obtiene todos los tratamientos de la base de datos"""
        conexion = FacturacionModel._get_connection()
        if not conexion:
            return []
        
        tratamientos = []
        cursor = None
        try:
            cursor = conexion.cursor(dictionary=True)
            query = "SELECT * FROM Tratamiento ORDER BY Descripcion"
            cursor.execute(query)
            
            rows = cursor.fetchall()

            for row in rows:
                tratamiento = Tratamiento(
                    id_tratamiento=row['ID_Tratamiento'],
                    id_doctor=row['ID_Doctor'],
                    descripcion=row['Descripcion'],
                    costo=float(row['Costo']),
                    fecha=row['Fecha'],
                    estado=row['Estado']
                )
                tratamientos.append(tratamiento)
        except Error as e:
            print(f"Error al obtener tratamientos: {e}")
        finally:
            if cursor:
                cursor.close()
            if conexion.is_connected():
                conexion.close()
        
        return tratamientos

    @staticmethod
    def insertar_factura_bd(factura: Factura) -> bool:
        """Inserta una nueva factura en la base de datos"""
        conexion = FacturacionModel._get_connection()
        if not conexion:
            return False
        
        cursor = None
        try:
            cursor = conexion.cursor()
            
            query = """
            INSERT INTO Factura (
                ID_Factura_Custom, 
                ID_Paciente, 
                Fecha_Emision, 
                Descripcion_Servicio,
                Monto_Servicio,
                Monto_Total, 
                Estado_Pago
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
        
            # Insertar la factura con todos los campos necesarios
            cursor.execute(query, (
                factura.id_factura,  # ID_Factura_Custom
                factura.paciente.id_paciente,
                factura.fecha_emision,
                factura.servicios[0],  # Descripción del primer servicio
                factura.montos[0],     # Monto del primer servicio
                factura.monto_total,
                factura.estado_pago
            ))
                    
            conexion.commit()
            return True
            
        except Error as e:
            print(f"Error al insertar la factura: {e}")
            if conexion:
                conexion.rollback()
            return False
        finally:
            if cursor:
                cursor.close()
            if conexion.is_connected():
                conexion.close()
    





    @staticmethod
    def obtener_todas_facturas_bd() -> List[Factura]:
        """Obtiene todas las facturas de la base de datos"""
        conexion = FacturacionModel._get_connection()
        if not conexion:
            return []
        
        facturas = []
        cursor = None
        try:
            cursor = conexion.cursor(dictionary=True)
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
            
            # Agrupar por ID_Factura_Custom para manejar múltiples servicios
            facturas_dict = {}
            for row in cursor:
                id_factura = row['ID_Factura_Custom']
                
                if id_factura not in facturas_dict:
                    paciente = Paciente(
                        id_paciente=row['ID_Paciente'],
                        nombre=row['Nombre'],
                        apellido=row['Apellido'],
                        fecha_nacimiento=row['Fecha_Nacimiento'],
                        dui=row['DUI'],
                        telefono=row['Telefono'],
                        correo=row['Correo']
                    )
                    
                    facturas_dict[id_factura] = {
                        'paciente': paciente,
                        'fecha_emision': row['Fecha_Emision'],
                        'estado_pago': row['Estado_Pago'],
                        'servicios': [],
                        'montos': []
                    }
                
                facturas_dict[id_factura]['servicios'].append(row['Descripcion_Servicio'])
                facturas_dict[id_factura]['montos'].append(float(row['Monto_Servicio']))
            
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
            if conexion.is_connected():
                conexion.close()
        
        return facturas

    @staticmethod
    def factura_existe(id_factura: str) -> bool:
        """Verifica si una factura con el ID dado ya existe"""
        conexion = FacturacionModel._get_connection()
        if not conexion:
            return False
        
        cursor = None
        try:
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
            if conexion.is_connected():
                conexion.close()

    @staticmethod
    def obtener_paciente_por_id(id_paciente: int) -> Optional[Paciente]:
        """Obtiene un paciente específico por su ID"""
        conexion = FacturacionModel._get_connection()
        if not conexion:
            return None
        
        cursor = None
        try:
            cursor = conexion.cursor(dictionary=True)
            query = "SELECT * FROM Paciente WHERE ID_Paciente = %s"
            cursor.execute(query, (id_paciente,))
            row = cursor.fetchone()
            
            if row:
                return Paciente(
                    id_paciente=row['ID_Paciente'],
                    nombre=row['Nombre'],
                    apellido=row['Apellido'],
                    fecha_nacimiento=row['Fecha_Nacimiento'],
                    dui=row['DUI'],
                    telefono=row['Telefono'],
                    correo=row['Correo']
                )
        except Error as e:
            print(f"Error al obtener paciente: {e}")
        finally:
            if cursor:
                cursor.close()
            if conexion.is_connected():
                conexion.close()
        
        return None

    @staticmethod
    def obtener_tratamiento_por_id(id_tratamiento: int) -> Optional[Tratamiento]:
        """Obtiene un tratamiento específico por su ID"""
        conexion = FacturacionModel._get_connection()
        if not conexion:
            return None
        
        cursor = None
        try:
            cursor = conexion.cursor(dictionary=True)
            query = "SELECT * FROM Tratamiento WHERE ID_Tratamiento = %s"
            cursor.execute(query, (id_tratamiento,))
            row = cursor.fetchone()
            
            if row:
                return Tratamiento(
                    id_tratamiento=row['ID_Tratamiento'],
                    id_doctor=row['ID_Doctor'],
                    descripcion=row['Descripcion'],
                    costo=float(row['Costo']),
                    fecha=row['Fecha'],
                    estado=row['Estado']
                )
        except Error as e:
            print(f"Error al obtener tratamiento: {e}")
        finally:
            if cursor:
                cursor.close()
            if conexion.is_connected():
                conexion.close()
        
        return None
