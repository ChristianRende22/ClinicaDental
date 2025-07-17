import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 

from PyQt6.QtWidgets import QApplication, QMessageBox 
from datetime import datetime
from typing import Dict, Any, List
from Modelos.PacienteModelo import Paciente 
from Modelos.FacturaModelo import Factura, FacturacionModel, Tratamiento
from Vistas.FacturaVista import FacturacionView 

class FacturacionController:
    def __init__(self, view: FacturacionView = None):
        self.view = view
        self.model = FacturacionModel()
        self.setup_connections()
        self.cargar_datos_iniciales()
    
    def setup_connections(self):
        """Conecta las señales de la vista con los métodos del controlador"""
        self.view.crear_factura_signal.connect(self.crear_factura)
        self.view.mostrar_facturas_signal.connect(self.mostrar_facturas)
        self.view.limpiar_campos_signal.connect(self.limpiar_campos)
    
    def cargar_datos_iniciales(self):
        """Carga pacientes y tratamientos en los ComboBox"""
        try:
            # Cargar pacientes
            pacientes = self.model.obtener_pacientes()
            self.view.cargar_pacientes(pacientes)
            
            # Cargar tratamientos
            tratamientos = self.model.obtener_tratamientos()
            self.view.cargar_tratamientos(tratamientos)
            
        except Exception as e:
            self.view.mostrar_mensaje("error", "❌ Error", 
                                    f"Error al cargar datos: {str(e)}")

    def crear_factura(self, datos: Dict[str, Any]):
        """Crea una nueva factura"""
        try:
            # Validar datos
            if not self._validar_datos_factura(datos):
                return
            
            # Verificar si la factura ya existe
            if self.model.factura_existe(datos['id_factura']):
                self.view.mostrar_mensaje("error", "❌ Error", 
                                        "Ya existe una factura con este ID.")
                return
            
            # Obtener tratamiento seleccionado
            tratamiento = datos['tratamiento']
            
            # Crear la factura
            nueva_factura = Factura(
                id_factura=datos['id_factura'],
                paciente=datos['paciente'],
                servicios=[tratamiento.descripcion],
                montos=[tratamiento.costo],
                fecha_emision=datetime.now(),
                estado_pago="Pendiente"
            )
            
            # Insertar en la base de datos
            if self.model.insertar_factura_bd(nueva_factura):
                self.view.mostrar_mensaje("success", "✅ Éxito", 
                                        "Factura creada correctamente.")
                self.view.limpiar_formulario()
                self.view.agregar_factura_resultado(str(nueva_factura))
            else:
                self.view.mostrar_mensaje("error", "❌ Error", 
                                        "Error al guardar la factura en la base de datos.")
                
        except Exception as e:
            self.view.mostrar_mensaje("error", "❌ Error", 
                                    f"Error inesperado: {str(e)}")
    
    def _validar_datos_factura(self, datos: Dict[str, Any]) -> bool:
        """Valida los datos de la factura antes de crearla"""
        if not datos['id_factura']:
            self.view.mostrar_mensaje("error", "⚠️ Error", 
                                    "Debe ingresar un ID de factura.")
            return False
        
        if not datos['paciente']:
            self.view.mostrar_mensaje("error", "⚠️ Error", 
                                    "Debe seleccionar un paciente.")
            return False
            
        if not datos['tratamiento']:
            self.view.mostrar_mensaje("error", "⚠️ Error", 
                                    "Debe seleccionar un tratamiento.")
            return False
        
        return True
    
    def mostrar_facturas(self):
        """Muestra todas las facturas registradas"""
        try:
            facturas = self.model.obtener_todas_facturas_bd()
            
            if not facturas:
                self.view.mostrar_mensaje("info", "ℹ️ Información", 
                                        "No hay facturas registradas.")
                self.view.actualizar_resultado("No hay facturas registradas.", limpiar=True)
                return
            
            # Mostrar facturas en el área de resultados
            self.view.actualizar_resultado("📋 FACTURAS REGISTRADAS:\n", limpiar=True)
            
            for factura in facturas:
                self.view.agregar_factura_resultado(str(factura))
                
            self.view.actualizar_resultado(f"\n📊 Total de facturas: {len(facturas)}")
            
        except Exception as e:
            self.view.mostrar_mensaje("error", "❌ Error", 
                                    f"Error al obtener facturas: {str(e)}")
    
    def limpiar_campos(self):
        """Limpia todos los campos del formulario"""
        self.view.limpiar_formulario()
        self.view.mostrar_mensaje("info", "ℹ️ Información", 
                                "Formulario limpiado correctamente.")
    
    def actualizar_pacientes(self):
        """Actualiza la lista de pacientes en el ComboBox"""
        try:
            pacientes = self.model.obtener_pacientes()
            self.view.cargar_pacientes(pacientes)
        except Exception as e:
            self.view.mostrar_mensaje("error", "❌ Error", 
                                    f"Error al actualizar pacientes: {str(e)}")
    
    def actualizar_tratamientos(self):
        """Actualiza la lista de tratamientos en el ComboBox"""
        try:
            tratamientos = self.model.obtener_tratamientos()
            self.view.cargar_tratamientos(tratamientos)
        except Exception as e:
            self.view.mostrar_mensaje("error", "❌ Error", 
                                    f"Error al actualizar tratamientos: {str(e)}")
    
    def show(self):
        """Muestra la ventana de la aplicación"""
        if self.view:
            self.view.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    try:
        view = FacturacionView()
        controller = FacturacionController(view)
        controller.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        sys.exit(1)
