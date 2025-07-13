import sys
import os 
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import mysql.connector

from Modelos.DoctorModelo import Doctor
from datetime import datetime
from PyQt6.QtCore import QDate

class Tratamiento:
    def __init__(self, id_tratamiento, id_doctor, descripcion, costo, fecha, estado, doctor):
        self.id_tratamiento = id_tratamiento
        self.id_doctor = id_doctor
        self.descripcion = descripcion
        self.costo = costo
        self.fecha = fecha
        self.estado = estado
        self.doctor = doctor or self._obtener_doctor(id_doctor)
        
    @staticmethod
    def conectar_bd():
        return mysql.connector.connect(
            host="localhost",
            port=3307,
            user="root",
            password="1234",
            database="ClinicaDental"
        )
        
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
    def insertar_tratamiento(id_doctor, descripcion, costo, fecha, estado):
        # Asegura que la fecha esté en formato correcto para MySQL
        if isinstance(fecha, QDate):
            fecha = fecha.toString("yyyy-MM-dd")
        elif isinstance(fecha, datetime):
            fecha = fecha.strftime("%Y-%m-%d")

        try:
            conn = Tratamiento.conectar_bd()
            cursor = conn.cursor()
            query = """
            INSERT INTO Tratamiento (ID_Doctor, Descripcion, Costo, Fecha, Estado)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (id_doctor, descripcion, costo, fecha, estado))
            conn.commit()
            return cursor.lastrowid
        except mysql.connector.Error as e:
            print(f"❌ Error al insertar tratamiento: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def __str__(self):
        return (f"Tratamiento ID: {self.id_tratamiento} \n " 
                f"Descripción: '{self.descripcion}' \n "
                f"Costo: ${self.costo:,.2f} \n " 
                f"Fecha de realización: {self.fecha} \n " 
                f"Estado: '{self.estado}' \n "
                f"Doctor: {self.doctor} \n " )
