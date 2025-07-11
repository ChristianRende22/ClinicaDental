import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from datetime import datetime
from typing import List
from Modelos.PacienteModelo import Paciente 

class Factura:
    def __init__(self, id_factura: str, 
                 paciente: Paciente, 
                 servicios: List[str], 
                 montos: List[float],
                 fecha_emision: datetime = datetime.now(),
                 estado_pago: str = "Pendiente"):
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
    # Modelo que maneja la lógica de negocio y la colección de facturas
    def __init__(self):
        self.facturas: List[Factura] = []

    def crear_factura(self, 
                     id_factura: str, 
                     paciente: Paciente,
                     servicios: List[str], 
                     montos: List[float],
                     fecha_emision: datetime = None,
                     estado_pago: str = "Pendiente") -> Factura: 
        if not fecha_emision:
            fecha_emision = datetime.now()  
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
    
    def obtener_facturas_por_paciente(self, paciente: Paciente) -> List[Factura]:
        # Filtra facturas por paciente
        return [f for f in self.facturas if f.paciente.dui == paciente.dui]
    
    def actualizar_saldo_paciente(self, paciente: Paciente):
        # Actualiza el saldo pendiente del paciente con sus facturas pendientes
        facturas_pendientes = [
            f for f in self.facturas 
            if f.paciente.dui == paciente.dui and f.estado_pago == "Pendiente"
        ]
        paciente.saldo_pendiente = sum(f.monto_total for f in facturas_pendientes)

    def obtener_todas_las_facturas(self) -> List[Factura]:
        """Retorna todas las facturas registradas."""
        return self.facturas
    
    def factura_existe(self, id_factura: str) -> bool:
        """Verifica si una factura con el ID dado ya existe."""
        return any(f.id_factura == id_factura for f in self.facturas)

