# Agregar el directorio padre al path
import sys
import os 
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# ==========================================
# IMPORTACIONES: Clases del modelo y librerías necesarias
# ==========================================

from Modelos.PacienteModelo import Paciente
from Modelos.CitaModelo import Cita
from Modelos.TratamientoModelo import Tratamiento
from datetime import datetime
from typing import List
import re

# ==========================================
# CLASE: PacienteControlador
# PROPÓSITO: Controlador para manejar la lógica de negocio de los pacientes
# ==========================================

class PacienteControlador:
    """Controlador para manejar la lógica de negocio de los pacientes"""
    
    def __init__(self):
        self.pacientes_registrados: List[Paciente] = []
        self.paciente_actual: Paciente = None
    
    # ==========================================
    # MÉTODOS DE VALIDACIÓN
    # PROPÓSITO: Validar datos de entrada para pacientes
    # ==========================================
    
    def validar_email(self, email: str) -> bool:
        """Valida el formato del email"""
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(patron, email) is not None
    
    def validar_dui(self, dui: str) -> bool:
        """Valida el formato del DUI (########-#)"""
        patron = r'^\d{8}-\d{1}$'
        return re.match(patron, dui) is not None
    
    def validar_telefono(self, telefono: str) -> bool:
        """Valida que el teléfono tenga al menos 8 dígitos"""
        return telefono.isdigit() and len(telefono) >= 8
    
    # ==========================================
    # MÉTODOS DE BÚSQUEDA Y VERIFICACIÓN
    # PROPÓSITO: Buscar y verificar existencia de pacientes
    # ==========================================
    
    def existe_paciente_con_dui(self, dui: str) -> bool:
        """Verifica si ya existe un paciente con el DUI dado"""
        return any(paciente.dui == dui for paciente in self.pacientes_registrados)
    
    def buscar_paciente_por_dui(self, dui: str) -> Paciente:
        """Busca un paciente por su DUI"""
        for paciente in self.pacientes_registrados:
            if paciente.dui == dui:
                return paciente
        return None
    
    # ==========================================
    # MÉTODOS DE GESTIÓN DE PACIENTES
    # PROPÓSITO: Crear y gestionar pacientes
    # ==========================================
    
    def crear_paciente(self, nombre: str, apellido: str, fecha_nacimiento: datetime, dui: str, 
                      telefono: int, correo: str, saldo_pendiente: float = 0.0) -> tuple[bool, str]:
        """
        Crea un nuevo paciente
        Retorna: (éxito: bool, mensaje: str)
        """
        # Validaciones
        if not all([nombre.strip(), apellido.strip(), dui.strip()]):
            return False, "Nombre, Apellido y DUI son campos obligatorios"
        
        if not self.validar_dui(dui):
            return False, "El DUI debe tener el formato: 12345678-9"
        
        if self.existe_paciente_con_dui(dui):
            return False, f"Ya existe un paciente registrado con el DUI: {dui}"
        
        if correo and not self.validar_email(correo):
            return False, "El email no tiene un formato válido"
        # Validar que la edad sea mayor a 0
        hoy = datetime.now()
        edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
        if edad <= 0:
            return False, "La edad debe ser mayor a 0"
        
        # Crear el nuevo paciente
        nuevo_paciente = Paciente(
            nombre.strip().title(),
            apellido.strip().title(),
            fecha_nacimiento,
            dui.strip(),
            telefono,
            correo.strip().lower() if correo else "",
            saldo_pendiente
        )
        
        # Agregar a la lista de pacientes registrados
        self.pacientes_registrados.append(nuevo_paciente)
        self.paciente_actual = nuevo_paciente
        
        return True, f"Paciente {nombre} {apellido} creado exitosamente"
    
    # ==========================================
    # MÉTODOS DE GESTIÓN DE TRATAMIENTOS Y CITAS
    # PROPÓSITO: Agregar tratamientos y citas a pacientes
    # ==========================================
    
    def agregar_tratamiento_a_paciente(self, tratamiento: Tratamiento) -> bool:
        """Agrega un tratamiento al paciente actual"""
        if self.paciente_actual:
            self.paciente_actual.agregar_tratamiento(tratamiento)
            return True
        return False
    
    def agregar_cita_a_paciente(self, cita: Cita) -> bool:
        """Agrega una cita al paciente actual"""
        if self.paciente_actual:
            self.paciente_actual.agregar_cita(cita)
            return True
        return False
    
    # ==========================================
    # MÉTODOS DE CONSULTA
    # PROPÓSITO: Obtener información de pacientes
    # ==========================================
    
    def get_paciente_actual(self) -> Paciente:
        """Retorna el paciente actual"""
        return self.paciente_actual
    
    def get_todos_los_pacientes(self) -> List[Paciente]:
        """Retorna la lista de todos los pacientes registrados"""
        return self.pacientes_registrados
    
    # ==========================================
    # MÉTODOS DE FORMATEO Y UTILIDADES
    # PROPÓSITO: Formatear datos para presentación
    # ==========================================
    
    def formatear_telefono(self, telefono: int) -> str:
        """Formatea el número de teléfono para mejor presentación"""
        if telefono == 0:
            return "No especificado"
        
        telefono_str = str(telefono)
        if len(telefono_str) == 8:
            return f"{telefono_str[:4]}-{telefono_str[4:]}"
        elif len(telefono_str) >= 8:
            return f"+503 {telefono_str[-8:-4]}-{telefono_str[-4:]}"
        return telefono_str
    
    def get_estado_icon(self, estado: str) -> str:
        """Devuelve un icono basado en el estado"""
        estado_lower = estado.lower()
        if 'completado' in estado_lower or 'finalizado' in estado_lower:
            return "✅"
        elif 'pendiente' in estado_lower or 'programado' in estado_lower:
            return "⏳"
        elif 'cancelado' in estado_lower:
            return "❌"
        elif 'en proceso' in estado_lower or 'activo' in estado_lower:
            return "🔄"
        else:
            return "📋"
    
    # ==========================================
    # MÉTODOS DE CÁLCULO
    # PROPÓSITO: Realizar cálculos relacionados con pacientes
    # ==========================================
    
    def calcular_edad(self, fecha_nacimiento):
        """Calcula la edad a partir de la fecha de nacimiento"""
        from datetime import datetime
        if isinstance(fecha_nacimiento, datetime):
            today = datetime.now()
            edad = today.year - fecha_nacimiento.year
            # Ajustar si el cumpleaños no ha ocurrido este año
            if today.month < fecha_nacimiento.month or (today.month == fecha_nacimiento.month and today.day < fecha_nacimiento.day):
                edad -= 1
            return edad
        return 0