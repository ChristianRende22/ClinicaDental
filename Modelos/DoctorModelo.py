import mysql.connector

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
            port = 3306,
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
