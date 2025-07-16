# Agregar el directorio padre al path
import mysql.connector
from mysql.connector import Error
import sys
import os

import mysql.connector.opentelemetry 
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# ==========================================
# IMPORTACIONES: Clases del modelo y librerías necesarias
# ==========================================
from datetime import date, time
from typing import List
import re
from typing import TYPE_CHECKING

# CORREGIDO: Importar las clases reales para tiempo de ejecución
try:
    from .PacienteModelo import Paciente
    from .DoctorModelo import Doctor
    from .TratamientoModelo import Tratamiento
except ImportError:
    # Fallback para importaciones absolutas
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from PacienteModelo import Paciente
    from DoctorModelo import Doctor
    from TratamientoModelo import Tratamiento

# Para type hints adicionales si es necesario
if TYPE_CHECKING:
    pass  # Ya tenemos las importaciones reales arriba

class Cita:
    """
    Clase que representa una cita en la clínica dental.
    Contiene información sobre el paciente, el doctor, el horario y el estado de la cita.
    """
    _contador_id = 1
    _citas_existentes = []

    def __init__(self, paciente: Paciente, doctor: Doctor, fecha: date, hora_inicio: time, hora_fin: time, costo_cita: float = 25, id_cita: int = None):
        
        # CORREGIDO: Validaciones básicas en el modelo - ahora funcionarán
        if not isinstance(paciente, Paciente):
            raise ValueError("El paciente debe ser una instancia de la clase Paciente.")
        if not isinstance(doctor, Doctor):
            raise ValueError("El doctor debe ser una instancia de la clase Doctor.")
        
        if id_cita is None:
            self.id_cita = Cita._obtener_siguiente_id()  # Asignar un ID único
        else:
            self.id_cita = id_cita
            if id_cita >= Cita._contador_id:
                Cita._contador_id = id_cita + 1

        # CORREGIDO: Registrar id como usado en la lista correcta
        if self.id_cita not in Cita._citas_existentes:  # Cambiar Paciente por Cita
            Cita._citas_existentes.append(self.id_cita)

        # Validaciones de fecha y hora
        if costo_cita < 0:
            raise ValueError("El costo de la cita no puede ser negativo.")
    
        self.paciente = paciente                # Paciente asociado a la cita
        self.doctor = doctor                    # Doctor asociado a la cita
        self.fecha = fecha                      # Fecha de la cita
        self.hora_inicio = hora_inicio          # Hora de inicio de la cita
        self.hora_fin = hora_fin                # Hora de fin de la cita
        self.costo_cita = costo_cita            # Costo de la cita
        self.estado = "Pendiente"               # Por defecto, la cita está pendiente
    
    @classmethod
    def _obtener_siguiente_id(cls) -> int:
        """Obtiene el siguiente ID disponible de forma robusta"""
        # Buscar el siguiente ID que no esté en uso
        while cls._contador_id in cls._citas_existentes:
            cls._contador_id += 1
        
        # Retornar el ID actual y incrementar para el siguiente
        id_actual = cls._contador_id
        cls._contador_id += 1
        return id_actual
    
    @classmethod
    def get_next_id(cls) -> int:
        """Obtiene el próximo ID disponible sin incrementar el contador"""
        return cls._contador_id

    @classmethod
    def set_contador_id(cls, nuevo_contador: int):
        """Establece el contador de ID (útil para cargar datos existentes)"""
        if nuevo_contador > cls._contador_id:
            cls._contador_id = nuevo_contador

    @classmethod
    def inicializar_contador_desde_citas(cls, citas_existentes: List['Cita']):
        """Inicializa el contador de ID a partir de una lista de citas existentes"""
        if not citas_existentes:
            cls._contador_id = 1
            cls._citas_existentes = []
            return
        
        ids_existentes = [cita.id_cita for cita in citas_existentes]
        cls._citas_existentes = ids_existentes.copy()

        if ids_existentes:
            cls._contador_id = max(ids_existentes) + 1
        else:
            cls._contador_id = 1

    def calcular_monto_total(self, tratamiento: Tratamiento) -> float:  # CORREGIDO: sin comillas
        """ Calcula el monto total de la cita sumando el costo del tratamiento.
        :param tratamiento: Tratamiento asociado a la cita.
        :return: Monto total de la cita.
        """
        if not isinstance(tratamiento, Tratamiento):
            raise ValueError("El tratamiento debe ser una instancia válida.")
        
        total = self.costo_cita + tratamiento.costo
        
        return total
    
    def estado_cita(self, nuevo_estado: str) -> None:
        """ Actualiza el estado de la cita.
        :param nuevo_estado: Nuevo estado de la cita.
        """
        estados_validos = ["Pendiente", "Confirmada", "Cancelada", "Asistida", "Ausente"]
        
        if nuevo_estado not in estados_validos:
            raise ValueError(f"Estado inválido. Debe ser uno de: {', '.join(estados_validos)}")
        
        self.estado = nuevo_estado

    def to_dict(self) -> dict:
        """Convierte la cita a un diccionario para facilitar su almacenamiento o transmisión."""
        return {
            "id_cita": self.id_cita,
            "paciente": self.paciente.to_dict(),
            "doctor": self.doctor.to_dict(),
            "fecha": self.fecha.isoformat(),
            "hora_inicio": self.hora_inicio.isoformat(),
            "hora_fin": self.hora_fin.isoformat(),
            "costo_cita": self.costo_cita,
            "estado": self.estado
        }
    def __str__(self):
        return (
            f"ID Cita: {self.id_cita}\n"
            f"Paciente: {self.paciente.nombre} {self.paciente.apellido}\n"
            f"Doctor: {self.doctor.nombre} {self.doctor.apellido}\n"
            f"Fecha: {self.fecha.strftime('%d/%m/%Y')}\n\t{self.hora_inicio.strftime('%H:%M')}\n\t{self.hora_fin.strftime('%H:%M')}\n"      
            f"Estado: {self.estado}\n"
            f"Costo: ${self.costo_cita:.2f}\n"
        )

    @staticmethod
    def insert_Cita_bd(cita: 'Cita') -> bool:  # Aquí sí puedes usar comillas porque es el mismo tipo
        """
        Inserta una nueva cita en la base de datos.
        :param cita: Instancia de la clase Cita a insertar.
        :return: True si la inserción fue exitosa, False en caso contrario.
        """
        conexion = None
        cursor = None     

        try:
            conexion = mysql.connector.connect(
                host='localhost',
                database='ClinicaDental',
                user='root',
                password='1234'
            )

            cursor = conexion.cursor()

            # CORREGIDO: Agregar ID_Tratamiento a la query
            query = """
            INSERT INTO Cita (ID_Paciente, ID_Doctor, ID_Tratamiento, Fecha, Hora_Inicio, Hora_Fin, Estado, Costo)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """

            # Obtener ID de tratamiento si existe
            id_tratamiento = None
            if hasattr(cita, 'tratamiento') and cita.tratamiento:
                id_tratamiento = cita.tratamiento.id_tratamiento

            cursor.execute(query, (
                cita.paciente.id_paciente,
                cita.doctor.id_doctor,
                id_tratamiento,  # Puede ser None si no hay tratamiento
                cita.fecha,
                cita.hora_inicio.strftime('%H:%M:%S'),
                cita.hora_fin.strftime('%H:%M:%S'),
                cita.estado,
                cita.costo_cita
            ))

            conexion.commit()

            # Obtener el ID generado por la base de datos
            cita_id_bd = cursor.lastrowid
            print(f"Cita insertada correctamente con ID de BD: {cita_id_bd}")
            return True
        
        except Error as e:
            print(f"Error al insertar la cita: {e}")
            if conexion:
                conexion.rollback()
            return False
        
        finally:
            if cursor:
                cursor.close()
            if conexion and conexion.is_connected():
                conexion.close()
                print("Conexión a la base de datos cerrada.")
    
    @staticmethod
    def probar_insercion():
        """Función de prueba para insertar una cita"""
        from .PacienteModelo import Paciente
        from .DoctorModelo import Doctor
        from datetime import date, time
        
        # Crear objetos de prueba
        paciente_prueba = Paciente("Juan", "Pérez", "01-01-1990", "12345678-9", 12345678, "juan@test.com")
        doctor_prueba = Doctor("Dr. María", "García", 1234, "Odontología General", 87654321, "maria@test.com")
        
        # Crear cita de prueba
        cita_prueba = Cita(
            paciente=paciente_prueba,
            doctor=doctor_prueba,
            fecha=date(2025, 7, 15),
            hora_inicio=time(10, 0),
            hora_fin=time(11, 0),
            costo_cita=50.0
        )
        
        # Probar inserción
        resultado = Cita.insert_Cita_bd(cita_prueba)
        print(f"Resultado de la inserción: {resultado}")
        return resultado
