from PyQt6.QtWidgets import QApplication
from datetime import datetime
from typing import Dict, Any
import sys
# importar el modelo y la vista
from modelo import FacturacionModel, Paciente, Factura
from vista import FacturacionView

class FacturacionController:
   #controlador principal
    def __init__(self):
        self.model = FacturacionModel()
        self.view = FacturacionView()
        self.setup_connections()
        self.initialize_view()
    
    def setup_connections(self):
        # conexiones entre vista y controlador
        self.view.crear_factura_signal.connect(self.crear_factura)
        self.view.mostrar_facturas_signal.connect(self.mostrar_facturas)
        self.view.limpiar_campos_signal.connect(self.limpiar_campos)
    
    def initialize_view(self):
        #inicializa la vista con datos del modelo
        pacientes = self.model.obtener_pacientes()
        self.view.cargar_pacientes(pacientes)
    
    def crear_factura(self, datos: Dict[str, Any]):
        try:
            # validar campos obligatorios
            if not self._validar_campos_obligatorios(datos):
                return
            # validar que no exista factura con el mismo ID
            if self.model.factura_existe(datos['id_factura']):
                self.view.mostrar_mensaje("error", "⚠️ Error", "Ya existe una factura con este ID")
                return
            # validar fecha
            try:
                fecha = datetime.strptime(datos['fecha'], '%d/%m/%Y')
            except ValueError:
                self.view.mostrar_mensaje("error", "⚠️ Error", "Formato de fecha inválido (DD/MM/YYYY)")
                return
            # servicios y montos
            servicios, montos = self._procesar_servicios_montos(datos['servicios'], datos['montos'])
            if not servicios:
                return
            # Crear la factura
            nueva_factura = self.model.crear_factura(
                id_factura=datos['id_factura'],
                paciente=datos['paciente'],
                servicios=servicios,
                montos=montos,
                fecha_emision=fecha,
                estado_pago=datos['estado_pago'])
            self.view.mostrar_mensaje("success", "✅ Éxito", 
                                    f"Factura '{datos['id_factura']}' creada correctamente\n"
                                    f"Servicios: {len(servicios)}\n"
                                    f"Total: ${nueva_factura.monto_total:.2f}")
            
            # mostrar la factura en los resultados 
            self.view.agregar_factura_resultado(str(nueva_factura))
        except Exception as e:
            self.view.mostrar_mensaje("error", "⚠️ Error", f"Error inesperado: {str(e)}")
    
    def mostrar_facturas(self):
        #muestra todas las facturas registradas
        facturas = self.model.obtener_facturas()
        if not facturas:
            self.view.mostrar_mensaje("info", "ℹ️ Información", "No hay facturas registradas")
            self.view.actualizar_resultado("📋 No hay facturas registradas en el sistema.", limpiar=True)
            return
        # resumen
        resumen = f"📊 RESUMEN DE FACTURAS ({len(facturas)} total)\n"
        resumen += "="*60 + "\n\n"
        self.view.actualizar_resultado(resumen, limpiar=True)
        
        # mostrar cada factura
        for i, factura in enumerate(facturas, 1):
            factura_texto = f"FACTURA #{i}\n{str(factura)}\n"
            self.view.actualizar_resultado(factura_texto)
        
        # total general
        total_general = self.model.obtener_total_general()
        total_texto = f"{'='*60}\nTOTAL GENERAL: ${total_general:.2f}"
        self.view.actualizar_resultado(total_texto)
    
    def limpiar_campos(self):
       #limpiar campos
        self.view.limpiar_formulario()
    
    def _validar_campos_obligatorios(self, datos: Dict[str, Any]) -> bool:
        #campos obligatorios
        if not datos['id_factura']:
            self.view.mostrar_mensaje("error", "⚠️ Error", "El ID de factura es obligatorio")
            return False
        
        if datos['paciente'] is None:
            self.view.mostrar_mensaje("error", "⚠️ Error", "Debe seleccionar un paciente")
            return False
        
        if not datos['servicios']:
            self.view.mostrar_mensaje("error", "⚠️ Error", "La descripción del servicio es obligatoria")
            return False
        
        return True
    
    def _procesar_servicios_montos(self, servicios_str: str, montos_str: str):
        #servicios y montos
        try:
            servicios = [s.strip() for s in servicios_str.split(',') if s.strip()]
            
            if montos_str:
                montos = [float(m.strip()) for m in montos_str.split(',') if m.strip()]
            else:
                montos = [0.0] * len(servicios)
            # verificar que coincidan las cantidades
            if len(servicios) != len(montos):
                self.view.mostrar_mensaje("error", "⚠️ Error", 
                                        f"Número de servicios ({len(servicios)}) no coincide con número de montos ({len(montos)})")
                return None, None
            # verificar que los montos sean positivos
            if any(m <= 0 for m in montos):
                self.view.mostrar_mensaje("error", "⚠️ Error", "Todos los montos deben ser mayores a 0")
                return None, None
            return servicios, montos 
        except ValueError:
            self.view.mostrar_mensaje("error", "⚠️ Error", "Los montos deben ser números válidos separados por comas")
            return None, None
    
    def show(self):
        #ventana principal
        self.view.show()
    def get_model(self):
        #retorna el modelo (para acceso desde otros controladores)
        return self.model
    def get_view(self):
        #retorna la vista (para acceso desde otros controladores)
        return self.view
def main():
    app = QApplication(sys.argv)
    #  controlador principal
    controller = FacturacionController()
    controller.show()
    sys.exit(app.exec())
if __name__ == "__main__":
    main()
