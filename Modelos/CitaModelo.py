import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Importar configuración centralizada
from Config.database_config import obtener_conexion, conectar_bd, cerrar_conexion_segura
import mysql.connector  # Mantener para manejo de errores específicos
from mysql.connector import Error
    
import sys
import os



sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# ==========================================
# IMPORTACIONES: Clases del modelo y librerías necesarias
# ==========================================
from datetime import date, time
from typing import List
import re
from typing import TYPE_CHECKING

# Importar las clases reales para tiempo de ejecución
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

if TYPE_CHECKING:
    pass  

class Cita:
    """
    Clase que representa una cita en la clínica dental.
    Contiene información sobre el paciente, el doctor, el horario y el estado de la cita.
    """
    _contador_id = 1
    _citas_existentes = []

    def __init__(self, paciente: Paciente, doctor: Doctor, fecha: date, hora_inicio: time, hora_fin: time, costo_cita: float = 25, id_cita: int = None):
        
        # Validaciones básicas en el modelo 
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

        if self.id_cita not in Cita._citas_existentes:  
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

    def calcular_monto_total(self, tratamiento: Tratamiento) -> float: 
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
        from datetime import timedelta, time as datetime_time
        
        # Asegurar que las horas sean objetos time
        hora_inicio_str = ""
        hora_fin_str = ""
        
        if isinstance(self.hora_inicio, timedelta):
            total_seconds = int(self.hora_inicio.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            hora_inicio_str = f"{hours:02d}:{minutes:02d}"
        elif isinstance(self.hora_inicio, datetime_time):
            hora_inicio_str = self.hora_inicio.strftime('%H:%M')
        else:
            hora_inicio_str = str(self.hora_inicio)
        
        if isinstance(self.hora_fin, timedelta):
            total_seconds = int(self.hora_fin.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            hora_fin_str = f"{hours:02d}:{minutes:02d}"
        elif isinstance(self.hora_fin, datetime_time):
            hora_fin_str = self.hora_fin.strftime('%H:%M')
        else:
            hora_fin_str = str(self.hora_fin)
        
        return (
            f"ID Cita: {self.id_cita}\n"
            f"Paciente: {self.paciente.nombre} {self.paciente.apellido}\n"
            f"Doctor: {self.doctor.nombre} {self.doctor.apellido}\n"
            f"Fecha: {self.fecha.strftime('%d/%m/%Y')}\n"
            f"Hora inicio: {hora_inicio_str}\n"
            f"Hora fin: {hora_fin_str}\n"      
            f"Estado: {self.estado}\n"
            f"Costo: ${self.costo_cita:.2f}\n"
        )

    @staticmethod
    def insert_Cita_bd(cita: 'Cita') -> bool: 
        """
        Inserta una nueva cita en la base de datos.
        :param cita: Instancia de la clase Cita a insertar.
        :return: True si la inserción fue exitosa, False en caso contrario.
        """
        conexion = None
        cursor = None     

        try:
            conexion= conectar_bd()
            if not conexion:
                print("No se pudo establecer conexión con la base de datos.")
                return False
            cursor = conexion.cursor()

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
                id_tratamiento,  
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
    def obtener_citas_bd() -> List['Cita']:
        """
        Obtiene todas las citas de la base de datos.
        :return: Lista de instancias de Cita.
        """
        conexion = None
        cursor = None
        citas = []

        try:
            conexion= conectar_bd()
            if not conexion:
                print("No se pudo establecer conexión con la base de datos.")
                return False

            cursor = conexion.cursor()

            # Query con JOINs para obtener toda la información en una consulta
            query = """
            SELECT 
                c.ID_Cita,
                c.Fecha,
                c.Hora_Inicio,
                c.Hora_Fin,
                c.Estado,
                c.Costo,
                p.ID_Paciente,
                p.Nombre AS paciente_nombre,
                p.Apellido AS paciente_apellido,
                p.Fecha_Nacimiento,
                p.DUI,
                p.Telefono AS paciente_telefono,
                p.Correo AS paciente_correo,
                d.ID_Doctor,
                d.Nombre AS doctor_nombre,
                d.Apellido AS doctor_apellido,
                d.Especialidad,
                d.Telefono AS doctor_telefono,
                d.Correo AS doctor_correo,
                d.Contrasena,
                t.ID_Tratamiento,
                t.Descripcion AS tratamiento_descripcion,
                t.Costo AS tratamiento_costo,
                t.Fecha AS tratamiento_fecha,
                t.Estado AS tratamiento_estado
            FROM Cita c
            INNER JOIN Paciente p ON c.ID_Paciente = p.ID_Paciente
            INNER JOIN Doctor d ON c.ID_Doctor = d.ID_Doctor
            LEFT JOIN Tratamiento t ON c.ID_Tratamiento = t.ID_Tratamiento
            ORDER BY c.Fecha, c.Hora_Inicio
            """
            cursor.execute(query)

            for row in cursor.fetchall():
                (id_cita, fecha, hora_inicio, hora_fin, estado, costo,
                 id_paciente, paciente_nombre, paciente_apellido, fecha_nacimiento, dui, paciente_telefono, paciente_correo,
                 id_doctor, doctor_nombre, doctor_apellido, especialidad, doctor_telefono, doctor_correo, contrasena,
                 id_tratamiento, tratamiento_descripcion, tratamiento_costo, tratamiento_fecha, tratamiento_estado) = row
                
                from datetime import time as datetime_time, timedelta
                
                if isinstance(hora_inicio, timedelta):
                    total_seconds = int(hora_inicio.total_seconds())
                    hours = total_seconds // 3600
                    minutes = (total_seconds % 3600) // 60
                    hora_inicio = datetime_time(hours, minutes)
                
                if isinstance(hora_fin, timedelta):
                    total_seconds = int(hora_fin.total_seconds())
                    hours = total_seconds // 3600
                    minutes = (total_seconds % 3600) // 60
                    hora_fin = datetime_time(hours, minutes)

                # Creacion de la instancia de Paciente con los datos obtenidos de los joins
                paciente = Paciente(
                    nombre=paciente_nombre,
                    apellido=paciente_apellido,
                    fecha_nacimiento=fecha_nacimiento,
                    telefono=int(paciente_telefono) if paciente_telefono else 0,
                    correo=paciente_correo or "",
                    dui=dui or "",
                    id_paciente=id_paciente
                )

                # Creacion de la instancia de Doctor con los datos obtenidos de los joins
                doctor = Doctor(
                    nombre=doctor_nombre,
                    apellido=doctor_apellido,
                    num_junta_medica=id_doctor,
                    especialidad=especialidad,
                    telefono=doctor_telefono,
                    correo=doctor_correo
                )
                
                doctor.id_doctor = id_doctor
                
                # Crear la cita
                cita = Cita(
                    paciente=paciente,
                    doctor=doctor,
                    fecha=fecha,
                    hora_inicio=hora_inicio,
                    hora_fin=hora_fin,
                    costo_cita=costo,
                    id_cita=id_cita
                )
                
                
                cita.estado = estado
        
                if id_tratamiento and tratamiento_descripcion:
                    tratamiento = Tratamiento(
                        id_tratamiento=id_tratamiento,
                        id_doctor=id_doctor,
                        descripcion=tratamiento_descripcion,
                        costo=tratamiento_costo,
                        fecha=tratamiento_fecha,
                        estado=tratamiento_estado,
                        doctor=doctor
                    )
                    cita.tratamiento = tratamiento
                
                citas.append(cita)

            return citas
        
        except Error as e:
            print(f"Error al obtener las citas: {e}")
            return []
        
        finally:
            if cursor:
                cursor.close()
            if conexion and conexion.is_connected():
                conexion.close()
    
    @staticmethod
    def actualizar_estado_bd(id_cita: int, nuevo_estado: str) -> bool:
        """
        Actualiza el estado de una cita en la base de datos.
        :param id_cita: ID de la cita a actualizar.
        :param nuevo_estado: Nuevo estado de la cita.
        :return: True si la actualización fue exitosa, False en caso contrario.
        """
        conexion = None
        cursor = None

        try:
            conexion= conectar_bd()
            if not conexion:
                print("No se pudo establecer conexión con la base de datos.")
                return False

            cursor = conexion.cursor()

            # Validar que el estado sea válido
            estados_validos = ["Pendiente", "Confirmada", "Cancelada", "Asistida", "Ausente"]
            if nuevo_estado not in estados_validos:
                print(f"Estado inválido: {nuevo_estado}")
                return False

            # Query para actualizar el estado
            query = """
            UPDATE Cita 
            SET Estado = %s 
            WHERE ID_Cita = %s
            """

            cursor.execute(query, (nuevo_estado, id_cita))
            conexion.commit()

            # Verificar si se actualizó alguna fila
            if cursor.rowcount > 0:
                print(f"Estado de la cita {id_cita} actualizado a '{nuevo_estado}' exitosamente.")
                return True
            else:
                print(f"No se encontró la cita con ID {id_cita}")
                return False

        except Error as e:
            print(f"Error al actualizar el estado de la cita: {e}")
            if conexion:
                conexion.rollback()
            return False

        finally:
            if cursor:
                cursor.close()
            if conexion and conexion.is_connected():
                conexion.close()
                print("Conexión a la base de datos cerrada.")
