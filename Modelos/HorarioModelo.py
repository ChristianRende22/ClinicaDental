import mysql.connector
from mysql.connector import Error
from datetime import datetime, time as datetime_time
from typing import List

# Importar la clase Doctor
try:
    from .DoctorModelo import Doctor
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from DoctorModelo import Doctor

class Horario:
    def __init__(self, id_horario: str, hora_inicio: str, hora_fin: str, doctor: Doctor, disponible: bool = True):
        self.id_horario = id_horario
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.doctor = doctor
        self.disponible = disponible

    def __str__(self):
        status = "✅ Disponible" if self.disponible else "❌ Ocupado" 
        return (f"🆔 ID Horario: {self.id_horario}\n"
                f"⏰ {self.hora_inicio} - {self.hora_fin}\n"
                f"👨‍⚕️ Médico: Dr. {self.doctor.nombre} {self.doctor.apellido}\n"
                f"📋 Estado: {status}\n")
    
    def horario_ocupado(self, otro_horario):
        """Verifica si hay conflicto de horarios con el mismo doctor"""
        if self.doctor.id_doctor != otro_horario.doctor.id_doctor:
            return False
        
        def hora_a_minutos(hora_str):
            if isinstance(hora_str, str):
                h, m = map(int, hora_str.split(':'))
                return h * 60 + m
            elif isinstance(hora_str, datetime_time):
                return hora_str.hour * 60 + hora_str.minute
            else:
                return 0
    
        inicio1 = hora_a_minutos(self.hora_inicio)
        fin1 = hora_a_minutos(self.hora_fin)
        inicio2 = hora_a_minutos(otro_horario.hora_inicio)
        fin2 = hora_a_minutos(otro_horario.hora_fin)
        
        return max(inicio1, inicio2) < min(fin1, fin2)

    @staticmethod
    def insertar_horario_bd(horario: 'Horario') -> bool:
        """
        Inserta un nuevo horario en la base de datos.
        :param horario: Instancia de la clase Horario a insertar.
        :return: True si la inserción fue exitosa, False en caso contrario.
        """
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

            # Verificar que el doctor existe en la base de datos
            cursor.execute("SELECT ID_Doctor FROM Doctor WHERE ID_Doctor = %s", (horario.doctor.id_doctor,))
            if not cursor.fetchone():
                print(f"Error: El doctor con ID {horario.doctor.id_doctor} no existe en la base de datos.")
                return False

            query = """
            INSERT INTO Horario (ID_Horario, ID_Doctor, Hora_Inicio, Hora_Fin, Disponible)
            VALUES (%s, %s, %s, %s, %s)
            """

            # Convertir las horas a formato TIME si son strings
            hora_inicio = horario.hora_inicio
            hora_fin = horario.hora_fin
            
            if isinstance(hora_inicio, str):
                hora_inicio = f"{hora_inicio}:00"
            if isinstance(hora_fin, str):
                hora_fin = f"{hora_fin}:00"

            cursor.execute(query, (
                horario.id_horario,
                horario.doctor.id_doctor,
                hora_inicio,
                hora_fin,
                horario.disponible
            ))

            conexion.commit()
            print(f"Horario insertado correctamente con ID: {horario.id_horario}")
            return True

        except Error as e:
            print(f"Error al insertar el horario: {e}")
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
    def obtener_horarios_bd() -> List['Horario']:
        """
        Obtiene todos los horarios de la base de datos con información del doctor.
        :return: Lista de instancias de Horario.
        """
        conexion = None
        cursor = None
        horarios = []

        try:
            conexion = mysql.connector.connect(
                host='localhost',
                database='ClinicaDental',
                user='root',
                port=3306,
                password='1234'
            )

            cursor = conexion.cursor()

            # Query con JOIN para obtener información del doctor
            query = """
            SELECT 
                h.ID_Horario,
                h.Hora_Inicio,
                h.Hora_Fin,
                h.Disponible,
                d.ID_Doctor,
                d.Nombre AS doctor_nombre,
                d.Apellido AS doctor_apellido,
                d.Especialidad,
                d.Telefono AS doctor_telefono,
                d.Correo AS doctor_correo,
                d.Contrasena
            FROM Horario h
            INNER JOIN Doctor d ON h.ID_Doctor = d.ID_Doctor
            ORDER BY h.Hora_Inicio
            """
            
            cursor.execute(query)

            for row in cursor.fetchall():
                (id_horario, hora_inicio, hora_fin, disponible,
                 id_doctor, doctor_nombre, doctor_apellido, especialidad, 
                 doctor_telefono, doctor_correo, contrasena) = row

                # Convertir timedelta a string si es necesario
                if hasattr(hora_inicio, 'total_seconds'):
                    total_seconds = int(hora_inicio.total_seconds())
                    hours = total_seconds // 3600
                    minutes = (total_seconds % 3600) // 60
                    hora_inicio = f"{hours:02d}:{minutes:02d}"
                else:
                    hora_inicio = str(hora_inicio)

                if hasattr(hora_fin, 'total_seconds'):
                    total_seconds = int(hora_fin.total_seconds())
                    hours = total_seconds // 3600
                    minutes = (total_seconds % 3600) // 60
                    hora_fin = f"{hours:02d}:{minutes:02d}"
                else:
                    hora_fin = str(hora_fin)

                # Crear instancia de Doctor
                doctor = Doctor(
                    nombre=doctor_nombre,
                    apellido=doctor_apellido,
                    num_junta_medica=id_doctor,
                    especialidad=especialidad,
                    telefono=doctor_telefono,
                    correo=doctor_correo
                )
                doctor.id_doctor = id_doctor

                # Crear instancia de Horario
                horario = Horario(
                    id_horario=id_horario,
                    hora_inicio=hora_inicio,
                    hora_fin=hora_fin,
                    doctor=doctor,
                    disponible=bool(disponible)
                )

                horarios.append(horario)

            return horarios

        except Error as e:
            print(f"Error al obtener los horarios: {e}")
            return []

        finally:
            if cursor:
                cursor.close()
            if conexion and conexion.is_connected():
                conexion.close()

    @staticmethod
    def eliminar_horario_bd(id_horario: str) -> bool:
        """
        Elimina un horario de la base de datos.
        :param id_horario: ID del horario a eliminar.
        :return: True si la eliminación fue exitosa, False en caso contrario.
        """
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

            query = "DELETE FROM Horario WHERE ID_Horario = %s"
            cursor.execute(query, (id_horario,))
            conexion.commit()

            if cursor.rowcount > 0:
                print(f"Horario con ID {id_horario} eliminado exitosamente.")
                return True
            else:
                print(f"No se encontró el horario con ID {id_horario}")
                return False

        except Error as e:
            print(f"Error al eliminar el horario: {e}")
            if conexion:
                conexion.rollback()
            return False

        finally:
            if cursor:
                cursor.close()
            if conexion and conexion.is_connected():
                conexion.close()

    @staticmethod
    def actualizar_disponibilidad_bd(id_horario: str, disponible: bool) -> bool:
        """
        Actualiza la disponibilidad de un horario en la base de datos.
        :param id_horario: ID del horario a actualizar.
        :param disponible: Nueva disponibilidad (True/False).
        :return: True si la actualización fue exitosa, False en caso contrario.
        """
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

            query = "UPDATE Horario SET Disponible = %s WHERE ID_Horario = %s"
            cursor.execute(query, (disponible, id_horario))
            conexion.commit()

            if cursor.rowcount > 0:
                estado = "disponible" if disponible else "ocupado"
                print(f"Horario {id_horario} marcado como {estado} exitosamente.")
                return True
            else:
                print(f"No se encontró el horario con ID {id_horario}")
                return False

        except Error as e:
            print(f"Error al actualizar la disponibilidad del horario: {e}")
            if conexion:
                conexion.rollback()
            return False

        finally:
            if cursor:
                cursor.close()
            if conexion and conexion.is_connected():
                conexion.close()


class HorarioModel:
    def __init__(self):
        self.horarios: List[Horario] = []
        self.doctores: List[Doctor] = []
        self.cargar_datos_desde_bd()
    
    def cargar_datos_desde_bd(self):
        """Carga todos los datos necesarios desde la base de datos"""
        try:
            # Cargar doctores desde la base de datos
            self.doctores = Doctor.obtener_todos_doctores()
            print(f"Doctores cargados desde BD: {len(self.doctores)}")
            
            # Cargar horarios desde la base de datos
            self.horarios = Horario.obtener_horarios_bd()
            print(f"Horarios cargados desde BD: {len(self.horarios)}")
            
        except Exception as e:
            print(f"Error al cargar datos desde BD: {e}")
            self.doctores = []
            self.horarios = []

    def agregar_horario(self, nuevo_horario: Horario) -> bool:
        """Agrega un nuevo horario a la base de datos y a la colección local."""
        if Horario.insertar_horario_bd(nuevo_horario):
            self.horarios.append(nuevo_horario)
            return True
        return False
    
    def eliminar_horario(self, id_horario: str) -> bool:
        """Elimina un horario de la base de datos y de la colección local."""
        if Horario.eliminar_horario_bd(id_horario):
            # Eliminar de la lista local
            self.horarios = [h for h in self.horarios if h.id_horario != id_horario]
            return True
        return False
        
    def obtener_horarios(self) -> List[Horario]:
        """Retorna todos los horarios actualizados desde la base de datos."""
        self.horarios = Horario.obtener_horarios_bd()
        return self.horarios.copy()

    def obtener_doctores(self) -> List[Doctor]:
        """Retorna todos los doctores actualizados desde la base de datos."""
        self.doctores = Doctor.obtener_todos_doctores()
        return self.doctores.copy()
    
    def obtener_horarios_agrupados_por_dia(self):
        """Retorna horarios agrupados por día."""
        # Actualizar horarios desde BD
        self.horarios = Horario.obtener_horarios_bd()
        
        # Por ahora agrupamos todos los horarios bajo "Hoy" ya que no tenemos fecha específica
        horarios_por_dia = {"Hoy": self.horarios}
        return horarios_por_dia
