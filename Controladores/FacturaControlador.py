import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 

from PyQt6.QtWidgets import QApplication
from datetime import datetime
from typing import Dict, Any, List
from Modelos.PacienteModelo import Paciente 
from Modelos.FacturaModelo import Factura
from Modelos.FacturaModelo import FacturacionModel 
from Vistas.FacturaVista import FacturacionView 

class Tratamiento:
    """Clase temporal para tratamientos hasta conectar con BD"""
    def __init__(self, id_tratamiento, descripcion, costo):
        self.id_tratamiento = id_tratamiento
        self.descripcion = descripcion
        self.costo = costo
        
    def __str__(self):
        return f"{self.descripcion} (${self.costo:.2f})"

class FacturacionController:
    def __init__(self, view=None):
        self.model = FacturacionModel()
        self.view = view  
        
        # Datos simulados
        self.pacientes_ejemplo = [
            Paciente("Juan", "Pérez", "06-12-05", "12345678-9", 12345567, "correo@gmail.com"), 
            Paciente("Ana", "Gomez", "07-31-07", "12345678-0", 12345678, "correo1@gmail.com")
        ]
        
        self.tratamientos_disponibles = [
            Tratamiento(1, "Limpieza Dental", 50.0),
            Tratamiento(2, "Empaste Simple", 75.0),
            Tratamiento(3, "Extracción", 120.0),
            Tratamiento(4, "Blanqueamiento", 300.0),
            Tratamiento(5, "Ortodoncia (Inicial)", 500.0)
        ]
        
        if self.view:
            self.setup_connections()
            self.initialize_view()
    
    def set_view(self, view):
        self.view = view
        self.setup_connections()
        self.initialize_view()
    
    def setup_connections(self):
        self.view.crear_factura_signal.connect(self.crear_factura)
        self.view.mostrar_facturas_signal.connect(self.mostrar_facturas)
        self.view.limpiar_campos_signal.connect(self.limpiar_campos)
        self.view.agregar_tratamiento_signal.connect(self.abrir_tratamiento)
    
    def initialize_view(self):
        self.view.cargar_pacientes(self.pacientes_ejemplo)
        self.view.cargar_tratamientos(self.tratamientos_disponibles)

    def crear_factura(self, datos: Dict[str, Any]):
        try:
            id_factura = datos['id_factura']
            paciente = datos['paciente']
            tratamiento = datos['tratamiento']
            
            if self.model.factura_existe(id_factura):
                self.view.mostrar_mensaje("error", "⚠️ Error", "Ya existe una factura con este ID.")
                return
            
            if not paciente:
                self.view.mostrar_mensaje("error", "⚠️ Error", "Debe seleccionar un paciente.")
                return
            
            if not tratamiento:
                self.view.mostrar_mensaje("error", "⚠️ Error", "Debe seleccionar un tratamiento.")
                return
            
            nueva_factura = self.model.crear_factura(
                id_factura=id_factura,
                paciente=paciente,
                servicios=[tratamiento.descripcion],
                montos=[tratamiento.costo],
                fecha_emision=datetime.now(),
                estado_pago="Pendiente"
            )
            
            self.view.mostrar_mensaje("success", "✅ Éxito", 
                                    f"Factura '{id_factura}' creada correctamente.\n"
                                    f"Servicio: {tratamiento.descripcion}\n"
                                    f"Total: ${tratamiento.costo:.2f}")
            
            self.view.agregar_factura_resultado(str(nueva_factura))
            self.view.limpiar_formulario()
            
        except Exception as e:
            self.view.mostrar_mensaje("error", "⚠️ Error", f"Error inesperado: {str(e)}")
    
    def mostrar_facturas(self):
        facturas = self.model.obtener_todas_las_facturas()
        
        if not facturas:
            self.view.mostrar_mensaje("info", "ℹ️ Información", "No hay facturas registradas.")
            self.view.actualizar_resultado("No hay facturas registradas.", limpiar=True)
            return
        
        resumen = f"📊 RESUMEN DE FACTURAS ({len(facturas)} total)\n{'='*60}\n"
        self.view.actualizar_resultado(resumen, limpiar=True)
        
        for i, factura in enumerate(facturas, 1):
            self.view.actualizar_resultado(f"FACTURA #{i}\n{str(factura)}\n")
        
        total = sum(f.monto_total for f in facturas)
        self.view.actualizar_resultado(f"{'='*60}\nTOTAL GENERAL: ${total:.2f}")
    
    def limpiar_campos(self):
        self.view.limpiar_formulario()
    
    def abrir_tratamiento(self):
        self.view.mostrar_mensaje("info", "ℹ️ Información", 
                               "Los tratamientos se seleccionan del ComboBox.")
    
    def show(self):
        if self.view:
            self.view.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = FacturacionView()
    controller = FacturacionController(view)
    view.show()
    sys.exit(app.exec())
