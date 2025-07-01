# Agregar el directorio padre al path
import sys
import os 
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Vistas.DoctorVista import Doctor
from Controladores.CitaControlador import Cita
from Vistas.TratamientoVista import Tratamiento
from datetime import datetime
from typing import List
import re





class Paciente:
    """Clase que representa un paciente de la clínica"""
    def __init__(self, nombre: str, apellido: str, fecha_nacimiento: datetime, dui: str, 
                 telefono: int, correo: str, saldo_pendiente: float = 0.0):
        self.nombre = nombre
        self.apellido = apellido
        self.fecha_nacimiento = fecha_nacimiento  # Se puede cambiar a fecha_nacimiento en el futuro
        self.dui = dui
        self.telefono = telefono
        self.correo = correo
        self.saldo_pendiente = saldo_pendiente
        self.historial_medico: List[Tratamiento] = []
        self.citas: List[Cita] = []
        self.fecha_registro = datetime.now().strftime('%d/%m/%Y - %H:%M:%S')
    
    def agregar_tratamiento(self, tratamiento: Tratamiento):
        """Agrega un tratamiento al historial médico del paciente"""
        self.historial_medico.append(tratamiento)
    
    def agregar_cita(self, cita: Cita):
        """Agrega una cita al paciente"""
        self.citas.append(cita)
    
    def calcular_total_tratamientos(self) -> float:
        """Calcula el costo total de todos los tratamientos"""
        return sum(tratamiento.costo for tratamiento in self.historial_medico)
    
    def calcular_total_citas(self) -> float:
        """Calcula el costo total de todas las citas"""
        return sum(cita.costo_cita for cita in self.citas)
    
    def get_balance_total(self) -> float:
        """Calcula el balance total del paciente"""
        return self.calcular_total_tratamientos() + self.calcular_total_citas() + self.saldo_pendiente
    
    def __str__(self):
        return f"Paciente: {self.nombre} {self.apellido} - DUI: {self.dui}"

class PacienteControlador:
    """Controlador para manejar la lógica de negocio de los pacientes"""
    
    def __init__(self):
        self.pacientes_registrados: List[Paciente] = []
        self.paciente_actual: Paciente = None
    
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
    
    def existe_paciente_con_dui(self, dui: str) -> bool:
        """Verifica si ya existe un paciente con el DUI dado"""
        return any(paciente.dui == dui for paciente in self.pacientes_registrados)
    
    def buscar_paciente_por_dui(self, dui: str) -> Paciente:
        """Busca un paciente por su DUI"""
        for paciente in self.pacientes_registrados:
            if paciente.dui == dui:
                return paciente
        return None
    
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
    
    def get_paciente_actual(self) -> Paciente:
        """Retorna el paciente actual"""
        return self.paciente_actual
    
    def get_todos_los_pacientes(self) -> List[Paciente]:
        """Retorna la lista de todos los pacientes registrados"""
        return self.pacientes_registrados
    
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