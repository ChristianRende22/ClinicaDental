import mysql.connector
from mysql.connector import Error

class Doctor:
    def __init__(self, nombre, apellido, num_junta_medica, especialidad, telefono, correo):
        self.num_junta_medica = num_junta_medica
        self.nombre = nombre
        self.apellido = apellido
        self.especialidad = especialidad
        self.telefono = telefono
        self.correo = correo
        self.citas = [] 
        self.horario = []

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.especialidad})"

    def mostrar_citas(self, resultado_text):
        """Muestra todas las citas asociadas a este doctor en el QTextEdit resultado_text."""
        if not self.citas:
            resultado_text.append(f"No hay citas registradas para el Dr. {self.nombre} {self.apellido}.")
            return
        resultado_text.append(f"Citas del Dr. {self.nombre} {self.apellido}:")
        for cita in self.citas:
            resultado_text.append(str(cita))
        resultado_text.append("")
    
    @staticmethod
    def conectar_db():
        return mysql.connector.connect(
            host="localhost",
            port = 3307,
            user = 'root',
            password = '1234',
            database = 'ClinicaDental'            
        )

    @staticmethod
    def obtener_doctores_desde_db():
        """Obtiene todos los doctores de la base de datos y los devuelve como una lista de objetos Doctor."""
        try:
            conexion = Doctor.conectar_db()
            cursor = conexion.cursor(dictionary=True)
            query = """
            SELECT ID_Doctor, Nombre, Apellido, Especialidad, Telefono, Correo 
            FROM doctor 
            """
            cursor.execute(query)
            doctores = []
            for row in cursor.fetchall():
                print(f"Fila obtenida: {row}")  # Debug
                doctor = Doctor(
                    nombre=row['Nombre'],
                    apellido=row['Apellido'],
                    num_junta_medica=row['ID_Doctor'],
                    especialidad=row['Especialidad'],
                    telefono=row['Telefono'],
                    correo=row['Correo']
                )
                doctores.append(doctor)
            cursor.close()
            conexion.close()
            return doctores
        except Exception as e:
            print(f"Error en obtener_doctores_desde_db: {e}")
            raise

    @staticmethod
    def insert_doc_db(doctor: 'Doctor') -> bool:
        """
        Inserta un nuevo doctor en la base de datos.
        Args: doctor (Doctor): El objeto Doctor a insertar.
        Returns: bool: True si la inserción fue exitosa, False en caso contrario."""
        try:
            conexion = Doctor.conectar_db()
            cursor = conexion.cursor()
            query = """
            INSERT INTO doctor (ID_Doctor, Nombre, Apellido, Especialidad, Telefono, Correo) 
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (
                int(doctor.num_junta_medica),
                doctor.nombre,
                doctor.apellido,
                doctor.especialidad,
                doctor.telefono,
                doctor.correo
            )
            print(f"Insertando doctor: {values}")  # Debug
            cursor.execute(query, values)
            conexion.commit()
            cursor.close()
            conexion.close()
            print("Doctor insertado correctamente.")
            return True
        
        except Exception as e:
            print(f"Error en insert_doc_db: {e}")
            return False
        
        finally:
            # Cerrar cursor y conexión para liberar recursos
            if 'cursor' in locals():
                cursor.close()
            if 'conexion' in locals():
                conexion.close()

    @staticmethod
    def obtener_todos_doctores():
        """Obtiene todos los doctores de la base de datos"""
        conexion = None
        cursor = None
        doctores = []
        
        try:
            conexion = mysql.connector.connect(
                host='localhost',
                database='ClinicaDental',
                user='root',
                port=3307,
                password='1234'
            )
            
            cursor = conexion.cursor()
            query = "SELECT ID_Doctor, Nombre, Apellido, Especialidad, Telefono, Correo FROM Doctor"
            cursor.execute(query)
            
            resultados = cursor.fetchall()
            
            for row in resultados:
                doctor = Doctor(
                    nombre=row[1] if row[1] else "Sin nombre",
                    apellido=row[2] if row[2] else "Sin apellido",
                    num_junta_medica=row[0],  # Usar ID_Doctor como num_junta_medica
                    especialidad=row[3] if row[3] else "General",
                    telefono=row[4] if row[4] else 0,
                    correo=row[5] if row[5] else ""
                )
            
                doctor.id_doctor = row[0]  # Asignar ID de la BD
                doctores.append(doctor)
                print(f"Doctor agregado: {doctor.nombre} {doctor.apellido}")  # Debug
            
                
            return doctores
            
        except Error as e:
            print(f"Error al obtener doctores: {e}")
            return []
            
        finally:
            if cursor:
                cursor.close()
            if conexion and conexion.is_connected():
                conexion.close()

    @staticmethod
    def obtener_citas_por_doctor(num_junta_medica: int):
        """
        Obtiene todas las citas de un doctor específico según su número de junta médica.
        :param num_junta_medica: Número de junta médica del doctor
        :return: Lista de citas del doctor o lista vacía si no hay citas
        """
        conexion = None
        cursor = None
        citas = []
        
        try:
            conexion = mysql.connector.connect(
                host='localhost',
                database='ClinicaDental',
                user='root',
                port=3307,
                password='1234'
            )
            
            cursor = conexion.cursor()
            
            # Query para obtener las citas del doctor específico
            query = """
            SELECT 
                c.ID_Cita,
                c.Fecha,
                c.Hora_Inicio,
                c.Hora_Fin,
                c.Estado,
                c.Costo,
                p.Nombre AS paciente_nombre,
                p.Apellido AS paciente_apellido,
                p.DUI,
                p.Telefono AS paciente_telefono,
                t.Descripcion AS tratamiento_descripcion,
                t.Costo AS tratamiento_costo
            FROM Cita c
            INNER JOIN Doctor d ON c.ID_Doctor = d.ID_Doctor
            INNER JOIN Paciente p ON c.ID_Paciente = p.ID_Paciente
            LEFT JOIN Tratamiento t ON c.ID_Tratamiento = t.ID_Tratamiento
            WHERE d.ID_Doctor = %s
            ORDER BY c.Fecha DESC, c.Hora_Inicio DESC
            """
            
            cursor.execute(query, (num_junta_medica,))
            resultados = cursor.fetchall()
            
            for row in resultados:
                (id_cita, fecha, hora_inicio, hora_fin, estado, costo,
                 paciente_nombre, paciente_apellido, dui, paciente_telefono,
                 tratamiento_descripcion, tratamiento_costo) = row
                
                # Formatear las horas si vienen como timedelta
                from datetime import time as datetime_time, timedelta
                
                if isinstance(hora_inicio, timedelta):
                    total_seconds = int(hora_inicio.total_seconds())
                    hours = total_seconds // 3600
                    minutes = (total_seconds % 3600) // 60
                    hora_inicio_str = f"{hours:02d}:{minutes:02d}"
                elif isinstance(hora_inicio, datetime_time):
                    hora_inicio_str = hora_inicio.strftime('%H:%M')
                else:
                    hora_inicio_str = str(hora_inicio)
                
                if isinstance(hora_fin, timedelta):
                    total_seconds = int(hora_fin.total_seconds())
                    hours = total_seconds // 3600
                    minutes = (total_seconds % 3600) // 60
                    hora_fin_str = f"{hours:02d}:{minutes:02d}"
                elif isinstance(hora_fin, datetime_time):
                    hora_fin_str = hora_fin.strftime('%H:%M')
                else:
                    hora_fin_str = str(hora_fin)
                
                # Crear diccionario con información de la cita
                cita_info = {
                    'id_cita': id_cita,
                    'fecha': fecha.strftime('%d/%m/%Y') if fecha else "Sin fecha",
                    'hora_inicio': hora_inicio_str,
                    'hora_fin': hora_fin_str,
                    'estado': estado or "Pendiente",
                    'costo': f"${costo:.2f}" if costo else "$0.00",
                    'paciente_nombre': paciente_nombre or "Sin nombre",
                    'paciente_apellido': paciente_apellido or "Sin apellido",
                    'paciente_dui': dui or "Sin DUI",
                    'paciente_telefono': paciente_telefono or "Sin teléfono",
                    'tratamiento_descripcion': tratamiento_descripcion or "Sin tratamiento",
                    'tratamiento_costo': f"${tratamiento_costo:.2f}" if tratamiento_costo else "$0.00"
                }
                
                citas.append(cita_info)
            
            return citas
            
        except Error as e:
            print(f"Error al obtener citas del doctor: {e}")
            return []
            
        finally:
            if cursor:
                cursor.close()
            if conexion and conexion.is_connected():
                conexion.close()
