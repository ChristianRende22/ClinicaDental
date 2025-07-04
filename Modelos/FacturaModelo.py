import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from datetime import datetime
from typing import List
from Modelos.Paciente import Paciente

class Factura:
    #Modelo para factura
    def __init__(self, id_factura: str, paciente: Paciente, 
                 servicios: List[str], montos: List[float], fecha_emision: datetime, 
                 estado_pago: str):
        self.id_factura = id_factura
        self.paciente = paciente
        self.servicios = servicios
        self.montos = montos
        self.monto_total = sum(montos)
        self.fecha_emision = fecha_emision
        self.estado_pago = estado_pago

    def __str__(self):
        servicios_str = "\n".join(f"   - {servicio}: ${monto:.2f}" 
                                 for servicio, monto in zip(self.servicios, self.montos))
        return (f"🧾 Factura ID: {self.id_factura}\n"
                f"📅 Fecha: {self.fecha_emision.strftime('%d/%m/%Y')}\n"
                f"👤 Paciente: {self.paciente.nombre} {self.paciente.apellido}\n"
                f"📋 DUI: {self.paciente.dui}\n"
                f"🩺 Servicios:\n{servicios_str}\n"
                f"💰 Estado: {self.estado_pago}\n"
                f"💵 Total: ${self.monto_total:.2f}\n"
                f"{'='*30}")

class FacturacionModel:
    #Modelo que maneja la lógica de negocio
    def __init__(self):
        self.facturas: List[Factura] = []
        self.pacientes: List[Paciente] = []
        self._inicializar_pacientes()
    
    def _inicializar_pacientes(self):
       # lista de pacientes (temporal, luego será desde BD)
        self.pacientes = [
            Paciente(nombre="Laura", apellido="Pérez", dui="12345678-9", edad=27),
            Paciente(nombre="Juan", apellido="Gómez", dui="87654321-0", edad=30),
            Paciente(nombre="María", apellido="González", dui="11111111-1", edad=35),
            Paciente(nombre="Carlos", apellido="Rodríguez", dui="22222222-2", edad=42)
        ]
    
    def obtener_pacientes(self) -> List[Paciente]:
       # lista de pacientes disponibles
        return self.pacientes
    
    def obtener_facturas(self) -> List[Factura]:
        # lista de facturas
        return self.facturas
    
    def factura_existe(self, id_factura: str) -> bool:
        #verifica si ya existe una factura con el ID dado
        return any(f.id_factura == id_factura for f in self.facturas)
    
    def crear_factura(self, id_factura: str, paciente: Paciente, 
                     servicios: List[str], montos: List[float], 
                     fecha_emision: datetime, estado_pago: str) -> Factura:
        #crea una nueva factura y la agrega a la lista
        nueva_factura = Factura(
            id_factura=id_factura,
            paciente=paciente,
            servicios=servicios,
            montos=montos,
            fecha_emision=fecha_emision,
            estado_pago=estado_pago
        )
        self.facturas.append(nueva_factura)
        return nueva_factura
    
    def obtener_total_general(self) -> float:
        #calcula el total general de todas las facturas
        return sum(factura.monto_total for factura in self.facturas)
    
    def obtener_factura_por_id(self, id_factura: str) -> Factura:
        #busca una factura por su ID
        for factura in self.facturas:
            if factura.id_factura == id_factura:
                return factura
        return None
    
    def agregar_paciente(self, paciente: Paciente):
        #agrega un nuevo paciente a la lista
        self.pacientes.append(paciente)
    
    def buscar_paciente_por_dui(self, dui: str) -> Paciente:
        #busca un paciente por su DUI
        for paciente in self.pacientes:
            if paciente.dui == dui:
                return paciente
        return None
