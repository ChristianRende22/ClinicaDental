# Agregar el directorio padre al path
import sys
import os 
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Controladores.DoctorControlador import Doctor
from Controladores.CitaControlador import Cita
from Controladores.TratamientoControlador import Tratamiento
from datetime import datetime
from typing import List

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