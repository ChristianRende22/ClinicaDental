import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 

from PyQt6.QtWidgets import QApplication
from datetime import datetime
from typing import Dict, Any, List
from Modelos.PacienteModelo import Paciente 
from Modelos.FacturaModelo import Factura
from Modelos.FacturaModelo import FacturacionModel 

class FacturacionController:
    def __init__(self, view=None):
        self.model = FacturacionModel()
        self.view = view  # Recibir la vista como parámetro
        
        # Datos de ejemplo para pacientes
        self.pacientes_ejemplo = [
            Paciente("Juan", "Pérez", "06-12-05", "12345678-9", 12345567, "correo@gmail.com"), 
            Paciente("Ana", "Gomex", "07-31-07", "12345678-0", 12345678, "correo1@gmail.com")
        ]
        
        # Solo configurar conexiones si la vista ya existe
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
    
    def initialize_view(self):
        # Inicializa la vista con los pacientes de ejemplo
        self.view.cargar_pacientes(self.pacientes_ejemplo)

    def crear_factura(self, datos: Dict[str, Any]):
        """
        Crea una nueva factura después de validar los datos.
        """
        try:
            # 1. Validar campos obligatorios
            if not self._validar_campos_obligatorios(datos):
                return
            
            # 2. Validar que no exista factura con el mismo ID
            if self.model.factura_existe(datos['id_factura']):
                self.view.mostrar_mensaje("error", "⚠️ Error", "Ya existe una factura con este ID.")
                return
            
            # 3. Validar y parsear la fecha
            try:
                fecha = datetime.strptime(datos['fecha'], '%d/%m/%Y')
            except ValueError:
                self.view.mostrar_mensaje("error", "⚠️ Error", "Formato de fecha inválido (DD/MM/YYYY).")
                return
            
            # 4. Procesar y validar servicios y montos
            servicios, montos = self._procesar_servicios_montos(datos['servicios'], datos['montos'])
            if servicios is None: # Si _procesar_servicios_montos encontró un error
                return
            
            # 5. Crear la factura a través del modelo
            nueva_factura = self.model.crear_factura(
                id_factura=datos['id_factura'],
                paciente=datos['paciente'],
                servicios=servicios,
                montos=montos,
                fecha_emision=fecha,
                estado_pago=datos['estado_pago']
            )  
            self.view.mostrar_mensaje("success", "✅ Éxito", 
                                    f"Factura '{datos['id_factura']}' creada correctamente.\n"
                                    f"Servicios: {len(servicios)}\n"
                                    f"Total: ${nueva_factura.monto_total:.2f}")
            
            # Mostrar la factura en el área de resultados de la vista
            self.view.agregar_factura_resultado(str(nueva_factura))
        except Exception as e:
            self.view.mostrar_mensaje("error", "⚠️ Error", f"Error inesperado al crear factura: {str(e)}")
    
    def mostrar_facturas(self):
        """Muestra todas las facturas registradas en el sistema."""
        facturas = self.model.obtener_todas_las_facturas() # Obtener facturas del modelo
        
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
        total_general = sum(f.monto_total for f in facturas) # Calcular total general en el controlador
        total_texto = f"{'='*60}\nTOTAL GENERAL: ${total_general:.2f}"
        self.view.actualizar_resultado(total_texto)
    
    def limpiar_campos(self):
        """Limpia los campos del formulario en la vista."""
        self.view.limpiar_formulario()
    
    def _validar_campos_obligatorios(self, datos: Dict[str, Any]) -> bool:
        """Valida que los campos obligatorios no estén vacíos."""
        if not datos['id_factura']:
            self.view.mostrar_mensaje("error", "⚠️ Error", "El ID de factura es obligatorio.")
            return False
        
        if datos['paciente'] is None: # Verifica que se haya seleccionado un objeto Paciente
            self.view.mostrar_mensaje("error", "⚠️ Error", "Debe seleccionar un paciente.")
            return False
        
        if not datos['servicios']:
            self.view.mostrar_mensaje("error", "⚠️ Error", "La descripción del servicio es obligatoria.")
            return False
        
        return True
    
    def _procesar_servicios_montos(self, servicios_str: str, montos_str: str):
        """
        Procesa las cadenas de servicios y montos, y realiza validaciones.
        """
        try:
            servicios = [s.strip() for s in servicios_str.split(',') if s.strip()]
            
            if montos_str:
                montos = [float(m.strip()) for m in montos_str.split(',') if m.strip()]
            else:
                # Si no se proporcionan montos, se asume 0.0 para cada servicio
                montos = [0.0] * len(servicios)
            
            # Verificar que coincidan las cantidades de servicios y montos
            if len(servicios) != len(montos):
                self.view.mostrar_mensaje("error", "⚠️ Error", 
                                        f"Número de servicios ({len(servicios)}) no coincide con número de montos ({len(montos)}).")
                return None, None
            
            # Verificar que los montos sean positivos 
            if any(m < 0 for m in montos): 
                self.view.mostrar_mensaje("error", "⚠️ Error", "Los montos no pueden ser negativos.")
                return None, None
            
            return servicios, montos 
        except ValueError:
            self.view.mostrar_mensaje("error", "⚠️ Error", "Los montos deben ser números válidos separados por comas.")
            return None, None
    
    def show(self):
        """Muestra la ventana principal de la vista."""
        if self.view:
            self.view.show()
