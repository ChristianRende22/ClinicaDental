import sys
import os 
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Importar configuración centralizada
from Config.database_config import obtener_conexion, conectar_bd, cerrar_conexion_segura
import mysql.connector  # Mantener para manejo de errores específicos
from mysql.connector import Error
from PyQt6.QtCore import QDate

from Modelos.DoctorModelo import Doctor
from datetime import datetime
from PyQt6.QtCore import QDate

class Tratamiento:
    def __init__(self, id_tratamiento, id_doctor, descripcion, costo, fecha, doctor):
        self.id_tratamiento = id_tratamiento
        self.id_doctor = id_doctor
        self.descripcion = descripcion
        self.costo = costo
        self.fecha = fecha
        self.doctor = doctor or self._obtener_doctor(id_doctor)
        
    @staticmethod
    def conectar_bd():
        """Usa la configuración centralizada para conectar a la base de datos"""
        return obtener_conexion()
        
    @staticmethod
    def buscar_doctor_por_codigo(codigo):
        """ Busca doctor por ID_Doctor (carnet) y devuelve nombre y apellido """
        conn = Tratamiento.conectar_bd()
        cursor = conn.cursor()
        query = "SELECT Nombre, Apellido FROM Doctor WHERE ID_Doctor = %s"
        cursor.execute(query, (codigo,))
        resultado = cursor.fetchone()
        cursor.close()
        conn.close()

        if resultado:
            nombre, apellido = resultado
            return nombre, apellido
        else:
            return None, None

    def _obtener_doctor(self, id_doctor):
        try:
            nombre, apellido = Tratamiento.buscar_doctor_por_codigo(id_doctor)
            if nombre and apellido:
                return f"{nombre} {apellido}"
        except Exception as e:
            print(f"❌ Error al obtener doctor: {e}")
        return "Doctor desconocido"
    
    @staticmethod
    def insertar_tratamiento(id_doctor, descripcion, costo, fecha):
        # Asegura que la fecha esté en formato correcto para MySQL
        if isinstance(fecha, QDate):
            fecha = fecha.toString("yyyy-MM-dd")
        elif isinstance(fecha, datetime):
            fecha = fecha.strftime("%Y-%m-%d")

        try:
            conn = Tratamiento.conectar_bd()
            cursor = conn.cursor()
            query = """
            INSERT INTO Tratamiento (ID_Doctor, Descripcion, Costo, Fecha)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (id_doctor, descripcion, costo, fecha))
            conn.commit()
            return cursor.lastrowid
        except mysql.connector.Error as e:
            print(f"❌ Error al insertar tratamiento: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def obtener_todos_tratamientos():
        """Obtiene todos los tratamientos de la base de datos"""
        conn = None
        cursor = None
        tratamientos = []
        
        try:
            conn = Tratamiento.conectar_bd()
            cursor = conn.cursor()
            # Consulta sin campo Estado
            query = "SELECT ID_Tratamiento, Descripcion, Costo, ID_Doctor, Fecha FROM Tratamiento"
            cursor.execute(query)
            
            resultados = cursor.fetchall()
            print(f"Resultados de tratamientos desde BD: {resultados}")  # Debug
            
            for row in resultados:
                # Constructor sin estado
                tratamiento = Tratamiento(
                    id_tratamiento=row[0],           # ID_Tratamiento
                    id_doctor=row[3] if row[3] else None,  # ID_Doctor
                    descripcion=row[1] if row[1] else "Sin descripción",  # Descripcion
                    costo=float(row[2]) if row[2] else 0.0,  # Costo
                    fecha=row[4] if row[4] else None,  # Fecha
                    doctor=None  # Se llenará automáticamente por el constructor
                )
                
                tratamientos.append(tratamiento)
                print(f"Tratamiento agregado: {tratamiento.descripcion}")  # CORREGIDO: usar descripcion
                        
            return tratamientos
            
        except Error as e:
            print(f"Error al obtener tratamientos: {e}")
            return []
            
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def __str__(self):
        return (f"Tratamiento ID: {self.id_tratamiento} \n " 
                f"Descripción: '{self.descripcion}' \n "
                f"Costo: ${self.costo:,.2f} \n " 
                f"Fecha de realización: {self.fecha} \n " 
                f"Doctor: {self.doctor} \n " )
