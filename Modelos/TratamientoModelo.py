import sys
import os 
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import mysql.connector
from Modelos.DoctorModelo import Doctor
from datetime import datetime

class Tratamiento:
    def __init__(self, id_tratamiento, id_paciente, id_doctor, descripcion, costo, fecha, estado, doctor, paciente):
        self.id_tratamiento = id_tratamiento
        self.id_paciente = id_paciente
        self.id_doctor = id_doctor
        self.descripcion = descripcion
        self.costo = costo
        self.fecha = fecha
        self.estado = estado
        self.doctor = doctor
        self.paciente = paciente
        
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
        
    @staticmethod
    def insertar_tratamiento(id_paciente, id_doctor, descripcion, costo, fecha, estado):
        conn = Tratamiento.conectar_bd()
        cursor = conn.cursor()
        query = """
        INSERT INTO Tratamiento (ID_Paciente, ID_Doctor, Descripcion, Costo, Fecha, Estado)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (id_paciente, id_doctor, descripcion, costo, fecha, estado))
        conn.commit()
        id_tratamiento = cursor.lastrowid
        cursor.close()
        conn.close()
        return id_tratamiento

    def __str__(self):
        return (f"Tratamiento ID: {self.id_tratamiento} \n " 
                f"Descripción: '{self.descripcion}' \n "
                f"Costo: ${self.costo:,.2f} \n " 
                f"Fecha de realización: {self.fecha} \n " 
                f"Estado: '{self.estado}' \n "
                f"Doctor: {self.doctor} \n " 
                f"Paciente: {self.paciente.nombre} {self.paciente.apellido}")
