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
from Controladores.TratamientoControlador import TratamientoControlador  

class FacturacionController:
    def __init__(self, view=None):
        self.model = FacturacionModel()
        self.view = view  
        
        # Datos de ejemplo para pacientes
        self.pacientes_ejemplo = [
            Paciente("Juan", "Pérez", "06-12-05", "12345678-9", 12345567, "correo@gmail.com"), 
            Paciente("Ana", "Gomez", "07-31-07", "12345678-0", 12345678, "correo1@gmail.com")
        ]
        
        # Diccionario para almacenar tratamientos por paciente (simulación)
        self.tratamientos_por_paciente = {}
        
        if self.view:
            self.setup_connections()
            self.initialize_view()
    
    def set_view(self, view):
        """Método para establecer la vista después de la construcción"""
        self.view = view
        self.setup_connections()
        self.initialize_view()
    
    def setup_connections(self):
        # Conexiones entre vista y controlador
        self.view.crear_factura_signal.connect(self.crear_factura)
        self.view.mostrar_facturas_signal.connect(self.mostrar_facturas)
        self.view.limpiar_campos_signal.connect(self.limpiar_campos)
        self.view.agregar_tratamiento_signal.connect(self.abrir_tratamiento)  
    
    def initialize_view(self):
        # Inicializa la vista con los pacientes de ejemplo
        self.view.cargar_pacientes(self.pacientes_ejemplo)

    def crear_factura(self, datos: Dict[str, Any]):
        """
        Crea una nueva factura basada en los tratamientos del paciente.
        """
        try:
            # 1. Validar que no exista factura con el mismo ID
            if self.model.factura_existe(datos['id_factura']):
                self.view.mostrar_mensaje("error", "⚠️ Error", "Ya existe una factura con este ID.")
                return
            
            # 2. Obtener tratamientos del paciente
            paciente = datos['paciente']
            tratamientos = self.tratamientos_por_paciente.get(paciente.dui, [])
            
            if not tratamientos:
                self.view.mostrar_mensaje("error", "⚠️ Error", 
                                        "El paciente no tiene tratamientos registrados. "
                                        "Por favor, agregue tratamientos antes de crear la factura.")
                return
            
            # 3. Crear listas de servicios y montos desde los tratamientos
            servicios = []
            montos = []
            
            for tratamiento in tratamientos:
                servicios.append(tratamiento['descripcion'])
                montos.append(tratamiento['costo'])
            
            # 4. Crear la factura a través del modelo
            nueva_factura = self.model.crear_factura(
                id_factura=datos['id_factura'],
                paciente=paciente,
                servicios=servicios,
                montos=montos,
                fecha_emision=datetime.now(),
                estado_pago="Pendiente"
            )
            
            self.view.mostrar_mensaje("success", "✅ Éxito", 
                                    f"Factura '{datos['id_factura']}' creada correctamente.\n"
                                    f"Servicios: {len(servicios)}\n"
                                    f"Total: ${nueva_factura.monto_total:.2f}")
            
            # Mostrar la factura en el área de resultados
            self.view.agregar_factura_resultado(str(nueva_factura))
            
        except Exception as e:
            self.view.mostrar_mensaje("error", "⚠️ Error", f"Error inesperado al crear factura: {str(e)}")
    
    def mostrar_facturas(self):
        """Muestra todas las facturas registradas en el sistema."""
        facturas = self.model.obtener_todas_las_facturas()
        
        if not facturas:
            self.view.mostrar_mensaje("info", "ℹ️ Información", "No hay facturas registradas.")
            self.view.actualizar_resultado("No hay facturas registradas en el sistema.", limpiar=True)
            return
        
        resumen = f"📊 RESUMEN DE FACTURAS ({len(facturas)} total)\n"
        resumen += "="*60 + "\n\n"
        self.view.actualizar_resultado(resumen, limpiar=True)
        
        # Mostrar cada factura
        for i, factura in enumerate(facturas, 1):
            factura_texto = f"FACTURA #{i}\n{str(factura)}\n"
            self.view.actualizar_resultado(factura_texto)
        
        # Total general
        total_general = sum(f.monto_total for f in facturas)
        total_texto = f"{'='*60}\nTOTAL GENERAL: ${total_general:.2f}"
        self.view.actualizar_resultado(total_texto)
    
    def limpiar_campos(self):
        self.view.limpiar_formulario()
    
    def abrir_tratamiento(self):
        """Abre la ventana de tratamiento para el paciente seleccionado."""
        try:
            paciente_seleccionado = self.view.obtener_paciente_seleccionado()
            
            if not paciente_seleccionado:
                self.view.mostrar_mensaje("error", "⚠️ Error", "Debe seleccionar un paciente.")
                return
            
            # Crear controlador de tratamiento
            controlador_tratamiento = TratamientoControlador(paciente_seleccionado)
            
            # Mostrar la vista de tratamiento
            controlador_tratamiento.mostrar_vista()
            
            # Simular que se guardó un tratamiento (en una implementación real, 
            # esto se manejaría mediante callbacks o señales)
            self._simular_tratamiento_guardado(paciente_seleccionado)
            
        except Exception as e:
            self.view.mostrar_mensaje("error", "⚠️ Error", f"Error al abrir tratamiento: {str(e)}")
    
    def _simular_tratamiento_guardado(self, paciente):
        """
        Método temporal para simular que se guardó un tratamiento.
        En una implementación real, esto se manejaría con callbacks o señales.
        """
        # Ejemplo de tratamiento simulado
        tratamiento_ejemplo = {
            'descripcion': 'Limpieza dental',
            'costo': 100.0,
            'fecha': datetime.now().strftime('%d/%m/%Y'),
            'estado': 'Pendiente'
        }
        
        # Agregar a la lista de tratamientos del paciente
        if paciente.dui not in self.tratamientos_por_paciente:
            self.tratamientos_por_paciente[paciente.dui] = []
        
        self.tratamientos_por_paciente[paciente.dui].append(tratamiento_ejemplo)
        
        # Notificar en el area de resultados
        self.view.actualizar_resultado(
            f"✅ Tratamiento simulado agregado para {paciente.nombre} {paciente.apellido}:\n"
            f"   - {tratamiento_ejemplo['descripcion']}: ${tratamiento_ejemplo['costo']:.2f}\n"
        )
    
    def agregar_tratamiento_real(self, paciente, tratamiento_data):
        """
        Método para agregar un tratamiento real (llamado desde el controlador de tratamiento).
        """
        if paciente.dui not in self.tratamientos_por_paciente:
            self.tratamientos_por_paciente[paciente.dui] = []
        
        self.tratamientos_por_paciente[paciente.dui].append(tratamiento_data)
        
        # Actualizar vista 
        if self.view:
            self.view.actualizar_resultado(
                f"✅ Tratamiento agregado para {paciente.nombre} {paciente.apellido}:\n"
                f"   - {tratamiento_data['descripcion']}: ${tratamiento_data['costo']:.2f}\n"
            )
    
    def show(self):
        """Muestra la ventana principal de la vista."""
        if self.view:
            self.view.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = FacturacionView()
    controller = FacturacionController(view)
    view.show()
    sys.exit(app.exec())
