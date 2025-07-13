# Agregar el directorio padre al path
import mysql.connector
from mysql.connector import Error
import sys
import os 
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# ==========================================
# IMPORTACIONES: Clases del modelo y librerías necesarias
# ==========================================

from datetime import datetime
from typing import List
import re

# ==========================================
# CLASE: Paciente
# PROPÓSITO: Clase que representa un paciente de la clínica (SOLO DATOS Y OPERACIONES DE DATOS)
# ==========================================

class Paciente:
    """Clase que representa un paciente de la clínica - Solo manejo de datos"""
    _contador_id = 1  # Contador de clase para generar IDs únicos
    _pacientes_existentes = []  # Lista para rastrear todos los IDs existentes
    
    def __init__(self, nombre: str, apellido: str, fecha_nacimiento: datetime, 
                 telefono: int, correo: str, dui: str = "", saldo_pendiente: float = 0.0, id_paciente: int = None):
        # Validaciones básicas en el modelo (solo las esenciales para integridad de datos)
        if not str(nombre).replace(" ", ""):
            raise ValueError("El nombre es obligatorio")
        if not str(apellido).replace(" ", ""):
            raise ValueError("El apellido es obligatorio")
        
        # Asignar ID único de forma robusta
        if id_paciente is None:
            # Encontrar el siguiente ID disponible
            self.id_paciente = Paciente._obtener_siguiente_id()
        else:
            self.id_paciente = id_paciente
            # Actualizar el contador si el ID proporcionado es mayor
            if id_paciente >= Paciente._contador_id:
                Paciente._contador_id = id_paciente + 1
        
        # Registrar este ID como usado
        if self.id_paciente not in Paciente._pacientes_existentes:
            Paciente._pacientes_existentes.append(self.id_paciente)
        
        self.nombre = str(nombre).replace("  ", " ") if nombre else ""
        if self.nombre.startswith(" "):
            self.nombre = self.nombre[1:]
        if self.nombre.endswith(" "):
            self.nombre = self.nombre[:-1]
        self.nombre = self.nombre.title()
        
        self.apellido = str(apellido).replace("  ", " ") if apellido else ""
        if self.apellido.startswith(" "):
            self.apellido = self.apellido[1:]
        if self.apellido.endswith(" "):
            self.apellido = self.apellido[:-1]
        self.apellido = self.apellido.title()
        
        self.fecha_nacimiento = fecha_nacimiento
        
        # DUI seguro
        self.dui = str(dui) if dui else ""
        if self.dui.startswith(" "):
            self.dui = self.dui[1:]
        if self.dui.endswith(" "):
            self.dui = self.dui[:-1]
        
        self.telefono = telefono
        
        # Correo seguro
        correo_str = str(correo) if correo else ""
        if correo_str.startswith(" "):
            correo_str = correo_str[1:]
        if correo_str.endswith(" "):
            correo_str = correo_str[:-1]
        self.correo = correo_str.lower() if correo_str else ""
        self.saldo_pendiente = saldo_pendiente
        self.historial_medico: List = []  # Evitamos importaciones circulares
        self.citas: List = []
        self.fecha_registro = datetime.now().strftime('%d/%m/%Y - %H:%M:%S')
    
    # ==========================================
    # MÉTODOS DE CLASE PARA GESTIÓN DE IDs
    # PROPÓSITO: Garantizar IDs secuenciales únicos y robustos
    # ==========================================
    


    @classmethod
    def _obtener_siguiente_id(cls) -> int:
        """Obtiene el siguiente ID disponible de forma robusta"""
        # Buscar el siguiente ID que no esté en uso
        while cls._contador_id in cls._pacientes_existentes:
            cls._contador_id += 1
        
        # Retornar el ID actual y incrementar para el siguiente
        id_actual = cls._contador_id
        cls._contador_id += 1
        return id_actual
    


    @classmethod
    def inicializar_contador_desde_pacientes(cls, pacientes_existentes: List['Paciente']):
        """Inicializa el contador basado en pacientes existentes"""
        if not pacientes_existentes:
            cls._contador_id = 1
            cls._pacientes_existentes = []
            return
        
        # Obtener todos los IDs existentes
        ids_existentes = [p.id_paciente for p in pacientes_existentes]
        cls._pacientes_existentes = ids_existentes.copy()
        
        # Establecer el contador como el mayor ID + 1
        if ids_existentes:
            cls._contador_id = max(ids_existentes) + 1
        else:
            cls._contador_id = 1

    # ==========================================
    # MÉTODOS DE GESTIÓN DE HISTORIAL MÉDICO
    # PROPÓSITO: Agregar y gestionar tratamientos y citas (SOLO OPERACIONES DE DATOS)
    # ==========================================
    
    def agregar_tratamiento(self, tratamiento):
        """Agrega un tratamiento al historial médico del paciente"""
        if tratamiento is None:
            raise ValueError("El tratamiento no puede ser None")
        self.historial_medico.append(tratamiento)
    
    def agregar_cita(self, cita):
        """Agrega una cita al paciente"""
        if cita is None:
            raise ValueError("La cita no puede ser None")
        self.citas.append(cita)
    
    def eliminar_tratamiento(self, id_tratamiento: str):
        """Elimina un tratamiento del historial médico"""
        self.historial_medico = [t for t in self.historial_medico if t.id_tratamiento != id_tratamiento]
    
    def eliminar_cita(self, id_cita: str):
        """Elimina una cita del paciente"""
        self.citas = [c for c in self.citas if c.id_cita != id_cita]
    
    def obtener_tratamiento_por_id(self, id_tratamiento: str):
        """Obtiene un tratamiento específico por su ID"""
        for tratamiento in self.historial_medico:
            if tratamiento.id_tratamiento == id_tratamiento:
                return tratamiento
        return None
    
    def obtener_cita_por_id(self, id_cita: str):
        """Obtiene una cita específica por su ID"""
        for cita in self.citas:
            if cita.id_cita == id_cita:
                return cita
        return None
    
    # ==========================================
    # MÉTODOS DE CÁLCULO FINANCIERO
    # PROPÓSITO: Calcular costos y balances del paciente (SOLO OPERACIONES DE DATOS)
    # ==========================================
    
    def calcular_total_tratamientos(self) -> float:
        """Calcula el costo total de todos los tratamientos"""
        return sum(tratamiento.costo for tratamiento in self.historial_medico)
    
    def calcular_total_citas(self) -> float:
        """Calcula el costo total de todas las citas"""
        return sum(cita.costo_cita for cita in self.citas)
    
    def get_balance_total(self) -> float:
        """Calcula el balance total del paciente"""
        return self.calcular_total_tratamientos() + self.calcular_total_citas() + self.saldo_pendiente
    
    def actualizar_saldo(self, nuevo_saldo: float):
        """Actualiza el saldo pendiente del paciente"""
        if nuevo_saldo < 0:
            raise ValueError("El saldo no puede ser negativo")
        self.saldo_pendiente = nuevo_saldo
    
    def tiene_saldo_pendiente(self) -> bool:
        """Verifica si el paciente tiene saldo pendiente"""
        return self.saldo_pendiente > 0
    
    def calcular_edad(self) -> int:
        """Calcula la edad actual del paciente"""
        hoy = datetime.now()
        edad = hoy.year - self.fecha_nacimiento.year
        # Ajustar si el cumpleaños no ha ocurrido este año
        if hoy.month < self.fecha_nacimiento.month or (hoy.month == self.fecha_nacimiento.month and hoy.day < self.fecha_nacimiento.day):
            edad -= 1
        return edad
    


    @classmethod
    def get_next_id(cls) -> int:
        """Obtiene el próximo ID disponible sin incrementar el contador"""
        return cls._contador_id
    


    @classmethod
    def set_contador_id(cls, nuevo_contador: int):
        """Establece el contador de ID (útil para cargar datos existentes)"""
        if nuevo_contador > cls._contador_id:
            cls._contador_id = nuevo_contador
    
    def tiene_dui(self) -> bool:
        """Verifica si el paciente tiene DUI registrado"""
        return bool(self.dui and len(str(self.dui).replace(" ", "")) > 0)
    
    def es_menor_de_edad(self) -> bool:
        """Verifica si el paciente es menor de edad"""
        return self.calcular_edad() < 18
    
    def obtener_tratamientos_por_estado(self, estado: str) -> List:
        """Obtiene tratamientos filtrados por estado"""
        return [t for t in self.historial_medico if t.estado.lower() == estado.lower()]
    
    def obtener_citas_por_estado(self, estado: str) -> List:
        """Obtiene citas filtradas por estado"""
        return [c for c in self.citas if c.estado.lower() == estado.lower()]
    
    def obtener_proximas_citas(self) -> List:
        """Obtiene las citas futuras del paciente"""
        ahora = datetime.now()
        return [c for c in self.citas if c.hora_inicio > ahora]
    
    def obtener_tratamientos_recientes(self, dias: int = 30) -> List:
        """Obtiene los tratamientos de los últimos N días"""
        from datetime import timedelta
        fecha_limite = datetime.now() - timedelta(days=dias)
        return [t for t in self.historial_medico if hasattr(t, 'fecha') and t.fecha >= fecha_limite]
    
    # ==========================================
    # MÉTODOS ESPECIALES Y UTILIDADES
    # PROPÓSITO: Representación y validaciones de datos
    # ==========================================
    


    @staticmethod
    def validar_formato_dui(dui: str) -> bool:
        """Valida que el DUI tenga el formato correcto (########-#)"""
        patron = r'^\d{8}-\d{1}$'
        return re.match(patron, dui) is not None
    


    @staticmethod
    def validar_formato_email(email: str) -> bool:
        """Valida que el email tenga un formato correcto"""
        if not email:
            return True  # Email es opcional
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(patron, email) is not None
    


    @staticmethod
    def validar_telefono(telefono: int) -> bool:
        """Valida que el teléfono tenga al menos 8 dígitos"""
        return len(str(telefono)) >= 8
    
    def to_dict(self) -> dict:
        """Convierte el paciente a un diccionario para serialización"""
        return {
            'id_paciente': self.id_paciente,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'fecha_nacimiento': self.fecha_nacimiento.isoformat(),
            'dui': self.dui,
            'telefono': self.telefono,
            'correo': self.correo,
            'saldo_pendiente': self.saldo_pendiente,
            'fecha_registro': self.fecha_registro,
            'cantidad_tratamientos': len(self.historial_medico),
            'cantidad_citas': len(self.citas)
        }
    
    def __str__(self):
        dui_info = f" - DUI: {self.dui}" if self.tiene_dui() else " (Sin DUI)"
        return f"Paciente #{self.id_paciente}: {self.nombre} {self.apellido}{dui_info}"
    
    def __repr__(self):
        return f"Paciente(id={self.id_paciente}, nombre='{self.nombre}', apellido='{self.apellido}', dui='{self.dui}')"
    
    # ==========================================
    # QUERYS PARA LLAMADO DE LA BASE DE DATOS 
    # ==========================================
    
    @staticmethod
    def buscar_pacientes_por_nombre_apellido(nombre="", apellido=""):
        """
        Consulta a la base de datos para buscar pacientes por nombre y/o apellido
        
        Args:
            nombre (str): Nombre del paciente a buscar (búsqueda parcial)
            apellido (str): Apellido del paciente a buscar (búsqueda parcial)
            
        Returns:
            List[Paciente]: Lista de objetos Paciente que coinciden con los criterios de búsqueda
        """
        try:
            print(f"📡 Ejecutando búsqueda SQL con: nombre='{nombre}', apellido='{apellido}'")
            
            # Establecer conexión con la base de datos MySQL
            conexion = mysql.connector.connect(
                host='localhost',
                port=3307,
                user='root',
                password='1234',
                database='ClinicaDental'
            )
            cursor = conexion.cursor()
            
            # Query con LIKE para búsqueda parcial en nombre y apellido
            query = """
                SELECT ID_Paciente, Nombre, Apellido, Fecha_Nacimiento, DUI
                FROM paciente
                WHERE Nombre LIKE %s AND Apellido LIKE %s
            """
            
            # Ejecutar consulta con parámetros de búsqueda (% para wildcards)
            cursor.execute(query, (f"%{nombre}%", f"%{apellido}%"))
            resultados = cursor.fetchall()
            print("✅ Resultados:", resultados)

            # Convertir resultados de BD a objetos Paciente
            pacientes = []
            for fila in resultados:
                id_paciente, nombre, apellido, fecha_nac, dui = fila
                # Crear objeto Paciente con los datos básicos de la BD
                paciente = Paciente(
                    nombre=nombre,
                    apellido=apellido,
                    fecha_nacimiento=fecha_nac,
                    telefono=0,  # Valor por defecto ya que no se consulta
                    correo="",   # Valor por defecto ya que no se consulta
                    dui=dui,
                    id_paciente=id_paciente
                )
                pacientes.append(paciente)
            return pacientes
            
        except mysql.connector.Error as e:
            print(f"❌ Error al buscar pacientes: {e}")
            return []  # Retornar lista vacía en caso de error
            
        finally:
            # Cerrar cursor y conexión para liberar recursos
            if 'cursor' in locals():
                cursor.close()
            if 'conexion' in locals():
                conexion.close()
                    
    @staticmethod
    def insertar_en_bd(paciente: 'Paciente') -> bool:
        """
        Inserta un nuevo paciente en la base de datos con todos sus datos
        
        Args:
            paciente (Paciente): Objeto Paciente a insertar en la BD
            
        Returns:
            bool: True si la inserción fue exitosa, False en caso contrario
        """
        try:
            # Establecer conexión con la base de datos MySQL
            conexion = mysql.connector.connect(
                host='localhost',
                port=3307,
                user='root',
                password='1234',
                database='ClinicaDental'
            )
            cursor = conexion.cursor()

            # Query INSERT con todos los campos del paciente
            query = """
            INSERT INTO paciente (Nombre, Apellido, Fecha_Nacimiento, DUI, Telefono, Correo)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            
            # Ejecutar INSERT con los datos del paciente
            cursor.execute(query, (
                paciente.nombre,
                paciente.apellido,
                paciente.fecha_nacimiento.strftime('%Y-%m-%d'),  # Formato fecha para MySQL
                paciente.dui,
                str(paciente.telefono),  # Convertir a string para consistencia
                paciente.correo
            ))
            
            # Confirmar transacción en la base de datos
            conexion.commit()

            print("✅ Paciente insertado en la base de datos.")
            return True

        except mysql.connector.Error as e:
            print(f"❌ Error al insertar paciente: {e}")
            return False  # Retornar False si hay error en la inserción

        finally:
            # Cerrar cursor y conexión para liberar recursos
            if 'cursor' in locals():
                cursor.close()
            if 'conexion' in locals():
                conexion.close()
    
    @staticmethod
    def obtener_todos_los_pacientes():
        """
        Consulta a la base de datos para obtener todos los pacientes registrados
        
        Returns:
            List[Paciente]: Lista de todos los objetos Paciente en la base de datos
        """
        try:
            print("📡 Cargando todos los pacientes desde la base de datos...")
            
            # Establecer conexión con la base de datos MySQL
            conexion = mysql.connector.connect(
                host='localhost',
                port=3307,
                user='root',
                password='1234',
                database='ClinicaDental'
            )
            cursor = conexion.cursor()
            
            # Query para obtener todos los pacientes con todos sus campos
            query = """
                SELECT ID_Paciente, Nombre, Apellido, Fecha_Nacimiento, DUI, Telefono, Correo
                FROM paciente
                ORDER BY ID_Paciente
            """
            
            # Ejecutar consulta
            cursor.execute(query)
            resultados = cursor.fetchall()
            print(f"✅ Se encontraron {len(resultados)} pacientes en la base de datos")

            # Primero, limpiar contadores para evitar conflictos
            Paciente._pacientes_existentes = []
            
            # Obtener todos los IDs existentes de la BD para inicializar correctamente
            ids_existentes = [fila[0] for fila in resultados]  # ID_Paciente es el primer campo
            if ids_existentes:
                # Establecer el contador al siguiente ID disponible
                Paciente._contador_id = max(ids_existentes) + 1
                print(f"🔧 Contador de IDs inicializado a: {Paciente._contador_id}")

            # Convertir resultados de BD a objetos Paciente
            pacientes = []
            for fila in resultados:
                id_paciente, nombre, apellido, fecha_nac, dui, telefono, correo = fila
                
                # Manejar valores nulos de la base de datos
                dui = dui if dui else ""
                telefono = int(telefono) if telefono and str(telefono).isdigit() else 0
                correo = correo if correo else ""
                
                # Crear objeto Paciente con todos los datos de la BD
                # Pasar explícitamente el id_paciente para evitar que se genere automáticamente
                paciente = Paciente(
                    nombre=nombre,
                    apellido=apellido,
                    fecha_nacimiento=fecha_nac,
                    telefono=telefono,
                    correo=correo,
                    dui=dui,
                    saldo_pendiente=0.0,  # Por ahora ponemos 0, luego se puede agregar este campo a la BD
                    id_paciente=id_paciente  # IMPORTANTE: Usar el ID de la BD
                )
                pacientes.append(paciente)
            
            print(f"📊 IDs cargados: {[p.id_paciente for p in pacientes]}")
            return pacientes
            
        except mysql.connector.Error as e:
            print(f"❌ Error al cargar pacientes: {e}")
            return []  # Retornar lista vacía en caso de error
            
        finally:
            # Cerrar cursor y conexión para liberar recursos
            if 'cursor' in locals():
                cursor.close()
            if 'conexion' in locals():
                conexion.close()

    # ==========================================
    # MÉTODOS DE HISTORIAL MÉDICO CON BASE DE DATOS
    # ==========================================
    
    @staticmethod
    def obtener_historial_medico_desde_bd(id_paciente: int) -> List[dict]:
        """
        Obtiene el historial médico de un paciente desde la base de datos
        
        Args:
            id_paciente (int): ID del paciente
            
        Returns:
            List[dict]: Lista de registros del historial médico
        """
        try:
            # Conectar a la base de datos
            conexion = mysql.connector.connect(
                host='localhost',
                port=3307,
                database='ClinicaDental',
                user='root',
                password='1234'
            )
            
            cursor = conexion.cursor()
            
            # Query para obtener el historial médico
            query = """
                SELECT ID_Historial, ID_Paciente, Fecha_Creacion, Notas_Generales, Estado
                FROM Historial_Medico
                WHERE ID_Paciente = %s
                ORDER BY Fecha_Creacion DESC
            """
            
            cursor.execute(query, (id_paciente,))
            resultados = cursor.fetchall()
            
            # Convertir resultados a lista de diccionarios
            historial = []
            for fila in resultados:
                id_historial, id_pac, fecha_creacion, notas, estado = fila
                historial.append({
                    'id_historial': id_historial,
                    'id_paciente': id_pac,
                    'fecha_creacion': fecha_creacion,
                    'notas_generales': notas if notas else 'Sin notas registradas',
                    'estado': estado if estado else 'Activo'
                })
            
            print(f"📋 Se encontraron {len(historial)} registros médicos para paciente #{id_paciente}")
            return historial
            
        except mysql.connector.Error as e:
            print(f"❌ Error al obtener historial médico: {e}")
            return []
            
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conexion' in locals():
                conexion.close()
    
    @staticmethod
    def insertar_historial_medico_en_bd(id_paciente: int, notas_generales: str, estado: str = "Activo") -> bool:
        """
        Inserta un nuevo registro de historial médico en la base de datos
        
        Args:
            id_paciente (int): ID del paciente
            notas_generales (str): Notas médicas generales
            estado (str): Estado del registro (por defecto "Activo")
            
        Returns:
            bool: True si se insertó exitosamente, False en caso contrario
        """
        try:
            # Conectar a la base de datos
            conexion = mysql.connector.connect(
                host='localhost',
                port=3307,
                database='ClinicaDental',
                user='root',
                password='1234'
            )
            
            cursor = conexion.cursor()
            
            # Query para insertar historial médico
            query = """
                INSERT INTO Historial_Medico (ID_Paciente, Fecha_Creacion, Notas_Generales, Estado)
                VALUES (%s, %s, %s, %s)
            """
            
            fecha_actual = datetime.now()
            cursor.execute(query, (id_paciente, fecha_actual, notas_generales, estado))
            
            # Confirmar los cambios
            conexion.commit()
            
            print(f"✅ Historial médico insertado para paciente #{id_paciente}")
            return True
            
        except mysql.connector.Error as e:
            print(f"❌ Error al insertar historial médico: {e}")
            return False
            
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conexion' in locals():
                conexion.close()

    # ==========================================
    # MÉTODOS DE HISTORIAL MÉDICO INTEGRADOS EN LA CLASE
    # ==========================================

    def obtener_historial_medico_completo(self) -> List[dict]:
        """
        Obtiene el historial médico completo del paciente desde la base de datos
        
        Returns:
            List[dict]: Lista completa del historial médico
        """
        return Paciente.obtener_historial_medico_desde_bd(self.id_paciente)
    
    def agregar_nota_historial_medico(self, notas: str, estado: str = "Activo") -> bool:
        """
        Agrega una nueva nota al historial médico del paciente
        
        Args:
            notas (str): Notas médicas a agregar
            estado (str): Estado del registro
            
        Returns:
            bool: True si se agregó exitosamente
        """
        return Paciente.insertar_historial_medico_en_bd(self.id_paciente, notas, estado)
    
    def tiene_historial_medico(self) -> bool:
        """
        Verifica si el paciente tiene historial médico registrado en la BD
        
        Returns:
            bool: True si tiene historial médico
        """
        historial = self.obtener_historial_medico_completo()
        return len(historial) > 0
