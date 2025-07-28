import sys
import os
import mysql.connector
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 

from PyQt6.QtWidgets import QApplication, QMessageBox 
from datetime import datetime
from typing import Dict, Any, List
from Modelos.PacienteModelo import Paciente 
from Modelos.FacturaModelo import Factura, FacturacionModel, Tratamiento
from Vistas.FacturaVista import FacturacionView 

class FacturacionController:
    def __init__(self, view: FacturacionView = None):
        try: 
            print("🔧 Inicializando FacturacionController...")
            self.view = view
            self.model = FacturacionModel()
            print("✅ Modelo creado exitosamente")
            
            if self.view:
                print("🔗 Configurando conexiones...")
                self.setup_connections()
                print("✅ Conexiones configuradas")
                
                print("📊 Cargando datos iniciales...")
                self.cargar_datos_iniciales()
                print("✅ FacturacionController inicializado completamente")
            else:
                print("⚠️ Vista no proporcionada al controlador")
                
        except Exception as e:
            print(f"❌ Error crítico al inicializar FacturacionController: {e}")
            import traceback
            traceback.print_exc()
            
            if self.view:
                self.view.mostrar_mensaje("error", "❌ Error de Inicialización", 
                                        f"No se pudo inicializar el controlador.\n\n"
                                        f"Error: {str(e)}")
    
    def setup_connections(self):
        """Conecta las señales de la vista con los métodos del controlador"""
        self.view.crear_factura_signal.connect(self.crear_factura)
        self.view.mostrar_facturas_signal.connect(self.mostrar_facturas)
        self.view.limpiar_campos_signal.connect(self.limpiar_campos)
        # self.view.actualizar_datos_signal.connect(self.cargar_datos_iniciales)
    
    def cargar_datos_iniciales(self):
        """Carga pacientes y tratamientos en los ComboBox"""
        try:
            # Cargar pacientes con timeout y manejo de errores
            print("Solicitando pacientes a la base de datos...")
            
            try:
                pacientes = self.model.obtener_pacientes()
                print(f"Total de pacientes recuperados: {len(pacientes)}")
                
                if pacientes:
                    self.view.cargar_pacientes(pacientes)
                    print("✅ Pacientes cargados exitosamente en la vista")
                else:
                    print("⚠️ No se encontraron pacientes en la base de datos")
                    self.view.mostrar_mensaje("info", "ℹ️ Información", 
                                            "No hay pacientes registrados en la base de datos.")
                    
            except mysql.connector.Error as db_error:
                print(f"❌ Error de base de datos al cargar pacientes: {db_error}")
                self.view.mostrar_mensaje("error", "❌ Error de Conexión", 
                                        f"No se pudo conectar a la base de datos.\n"
                                        f"Verifique que MySQL esté ejecutándose.\n\n"
                                        f"Error: {str(db_error)}")
                return
            except Exception as paciente_error:
                print(f"❌ Error general al cargar pacientes: {paciente_error}")
                import traceback
                traceback.print_exc()
                self.view.mostrar_mensaje("error", "❌ Error", 
                                        f"Error al cargar pacientes: {str(paciente_error)}")
                return
            
            # Cargar tratamientos solo si los pacientes se cargaron correctamente
            print("Solicitando tratamientos a la base de datos...")
            
            try:
                tratamientos = self.model.obtener_tratamientos()
                print(f"Total de tratamientos recuperados: {len(tratamientos)}")
                
                if tratamientos:
                    self.view.cargar_tratamientos(tratamientos)
                    print("✅ Tratamientos cargados exitosamente en la vista")
                else:
                    print("⚠️ No se encontraron tratamientos en la base de datos")
                    self.view.mostrar_mensaje("info", "ℹ️ Información", 
                                            "No hay tratamientos registrados en la base de datos.")
                    
            except mysql.connector.Error as db_error:
                print(f"❌ Error de base de datos al cargar tratamientos: {db_error}")
                self.view.mostrar_mensaje("error", "❌ Error de Conexión", 
                                        f"No se pudo cargar los tratamientos.\n\n"
                                        f"Error: {str(db_error)}")
            except Exception as tratamiento_error:
                print(f"❌ Error general al cargar tratamientos: {tratamiento_error}")
                import traceback
                traceback.print_exc()
                self.view.mostrar_mensaje("error", "❌ Error", 
                                        f"Error al cargar tratamientos: {str(tratamiento_error)}")
            
            # Generar y mostrar el próximo ID de factura automáticamente
            try:
                siguiente_id = self.model.generar_id_factura_automatico()
                self.view.mostrar_id_automatico(siguiente_id)
                print(f"✅ ID de factura generado y mostrado: {siguiente_id}")
            except Exception as id_error:
                print(f"❌ Error al generar ID automático: {id_error}")
                self.view.mostrar_id_automatico("F001")  # ID por defecto
            
            print("✅ Proceso de carga de datos completado")
            
        except Exception as e:
            print(f"❌ Error crítico al cargar datos iniciales: {e}")
            import traceback
            traceback.print_exc()
            self.view.mostrar_mensaje("error", "❌ Error Crítico", 
                                    f"Error crítico al inicializar datos: {str(e)}")
    
    def crear_factura(self, datos: Dict[str, Any]):
        """Crea una nueva factura"""
        try:
            # Generar ID automáticamente
            id_factura_automatico = self.model.generar_id_factura_automatico()
            print(f"🆔 ID generado automáticamente: {id_factura_automatico}")
            
            # Actualizar los datos con el ID generado
            datos['id_factura'] = id_factura_automatico
            
            # Validar datos
            if not self._validar_datos_factura(datos):
                return
            
            # Imprimir información de depuración
            print(f"ID Factura: {datos['id_factura']}")
            print(f"Paciente: {datos['paciente'].__class__.__name__} - {datos['paciente'].id_paciente} - {datos['paciente'].nombre} {datos['paciente'].apellido}")
            print(f"Tratamiento: {datos['tratamiento'].__class__.__name__} - {datos['tratamiento'].id_tratamiento} - {datos['tratamiento'].descripcion}")
            
            # Verificar si la factura ya existe (aunque no debería porque el ID es auto-generado)
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
                
                # Generar y mostrar el próximo ID automáticamente
                try:
                    siguiente_id = self.model.generar_id_factura_automatico()
                    self.view.mostrar_id_automatico(siguiente_id)
                    print(f"✅ Próximo ID generado: {siguiente_id}")
                except Exception as e:
                    print(f"❌ Error al generar próximo ID: {e}")
                    self.view.mostrar_id_automatico("F001")
            else:
                self.view.mostrar_mensaje("error", "❌ Error", 
                                        "Error al guardar la factura en la base de datos.")
                
        except Exception as e:
            print(f"Error al crear factura: {e}")
            import traceback
            traceback.print_exc()
            self.view.mostrar_mensaje("error", "❌ Error", 
                                    f"Error inesperado: {str(e)}")
            
    def _validar_datos_factura(self, datos: Dict[str, Any]) -> bool:
        """Valida los datos de la factura antes de crearla"""
        # Ya no validamos el ID porque se genera automáticamente
        
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
        
        # Generar y mostrar el próximo ID automáticamente después de limpiar
        try:
            siguiente_id = self.model.generar_id_factura_automatico()
            self.view.mostrar_id_automatico(siguiente_id)
            print(f"✅ ID regenerado después de limpiar: {siguiente_id}")
        except Exception as e:
            print(f"❌ Error al regenerar ID: {e}")
            self.view.mostrar_id_automatico("F001")
            
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
        try:
            if self.view:
                print("👁️ Mostrando vista de facturación...")
                self.view.show()
                print("✅ Vista mostrada exitosamente")
            else:
                print("❌ No hay vista para mostrar")
                
        except Exception as e:
            print(f"❌ Error al mostrar la vista: {e}")
            import traceback
            traceback.print_exc()

# CORREGIDO: El bloque if __name__ debe estar al nivel del módulo (sin indentación dentro de la clase)
def main():
    """Función principal para ejecutar la aplicación de facturación"""
    print("🚀 Iniciando aplicación de facturación...")
    
    app = QApplication(sys.argv)
    
    try:
        print("🖼️ Creando vista...")
        view = FacturacionView()
        print("✅ Vista creada exitosamente")
        
        print("🎮 Creando controlador...")
        controller = FacturacionController(view)
        print("✅ Controlador creado exitosamente")
        
        print("👁️ Mostrando aplicación...")
        controller.show()
        
        print("▶️ Iniciando loop de eventos...")
        app.exec()  # Sin sys.exit() para permitir continuar
        
    except mysql.connector.Error as db_error:
        print(f"❌ Error de base de datos: {db_error}")
        QMessageBox.critical(None, "Error de Base de Datos", 
                           f"No se pudo conectar a la base de datos.\n\n"
                           f"Verifique que MySQL esté ejecutándose y que "
                           f"las credenciales sean correctas.\n\n"
                           f"Error: {str(db_error)}")
        sys.exit(1)
        
    except ImportError as import_error:
        print(f"❌ Error de importación: {import_error}")
        QMessageBox.critical(None, "Error de Módulos", 
                           f"No se pudieron cargar todos los módulos necesarios.\n\n"
                           f"Error: {str(import_error)}")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Error crítico al iniciar la aplicación: {e}")
        import traceback
        traceback.print_exc()
        QMessageBox.critical(None, "Error Crítico", 
                           f"Error inesperado al iniciar la aplicación:\n\n{str(e)}")
        sys.exit(1)
        
if __name__ == "__main__":
    main()
