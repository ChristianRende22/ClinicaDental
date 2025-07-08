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
    def obtener_Paciente():
        """Obtiene todos los pacientes de la base de datos"""
        try:
            conexion = mysql.connector.connect(
                host='localhost',
                port=3307,  
                user='root',
                password='1234',
                database='ClinicaDental'
            )

            cursor = conexion.cursor()
            cursor.execute("SELECT P.ID_Paciente, P.Nombre, P.Apellido, P.Fecha_Nacimiento, P.DUI FROM paciente P;")
            
            resultados = cursor.fetchall()
            pacientes = []
            
        except mysql.connector.Error as error:
            print(f"Error en la base de datos: {error}")
            return []
            
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conexion' in locals():
                conexion.close()
