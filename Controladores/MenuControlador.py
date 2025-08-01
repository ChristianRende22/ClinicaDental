import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Modelos.MenuModelo import MenuModelo
from Vistas.MenuVista import MenuVista

class MenuControlador:
    def __init__(self, usuario=None, tipo_usuario="admin"):
        self.modelo = MenuModelo()
        self.vista = MenuVista(tipo_usuario)
        self.usuario = usuario
        self.tipo_usuario = tipo_usuario
        
        # Referencias a controladores de módulos
        self.Paciente_window = None
        self.cita_window = None  # Inicializar cita_window como None
        self.Doctor_window = None
        self.Horario_window = None
        self.Factura_window = None
        self.Tratamiento_window = None
        self.cerrar_sesion_signal = None  # Placeholder para señal de cierre de sesión
        
        # Inicializar sesión si se proporcionaron datos
        if usuario and tipo_usuario:
            self.modelo.inicializar_sesion(usuario, tipo_usuario)
        
        self.conectar_eventos()
    
    def conectar_eventos(self):
        """Conecta los eventos entre la vista y el controlador"""
        # Conectar señales de navegación
        self.vista.ir_a_pacientes.connect(self.abrir_pacientes)
        self.vista.ir_a_doctores.connect(self.abrir_doctores)
        self.vista.ir_a_citas.connect(self.abrir_citas)
        self.vista.ir_a_tratamientos.connect(self.abrir_tratamientos)
        self.vista.ir_a_horarios.connect(self.abrir_horarios)
        self.vista.ir_a_facturas.connect(self.abrir_facturas)
        self.vista.cerrar_sesion.connect(self.cerrar_sesion)
    
    def mostrar(self):
        """Muestra la ventana del menú"""
        self.vista.show()
    
    def ocultar(self):
        """Oculta la ventana del menú"""
        self.vista.hide()
    
    def cerrar(self):
        """Cierra la ventana del menú"""
        self.vista.close()
    
    def actualizar_usuario(self, usuario, tipo_usuario):
        """Actualiza la información del usuario"""
        self.usuario = usuario
        self.tipo_usuario = tipo_usuario
        self.modelo.inicializar_sesion(usuario, tipo_usuario)
        self.vista.actualizar_usuario(tipo_usuario)
    
    def abrir_pacientes(self):
        if self.modelo.tiene_permiso('pacientes'):
            print("Abriendo módulo de Pacientes...")
            from Controladores.PacienteControlador import PacienteControlador   
            from Vistas.PacienteVista import PacienteWindow
            try:
                if self.Paciente_window:
                    self.Paciente_window.close()
                    
                controlador = PacienteControlador()
                self.Paciente_window = PacienteWindow()
                controlador.set_vista(self.Paciente_window)
                try:
                    controlador.inicializar_vista()
                    
                    self.Paciente_window.show()
                    
                except Exception as init_error:
                    self.show_error_message(
                        "Error al inicializar la vista de pacientes",
                        f"Detalles del error: {str(init_error)}"
                    )
            except ImportError:
                self.show_error_message(
                    "Error de módulo",
                    "No se pudo importar el módulo de pacientes. Asegúrate de que el archivo PacienteControlador.py existe y está correctamente configurado."
                )
            except Exception as e:
                self.show_error_message(
                    "Error al abrir pacientes",
                    f"Detalles del error: {str(e)}"
                )
        else:
            self.mostrar_error_permiso("Pacientes")
                    
                  
    def abrir_doctores(self):
        """Abre el módulo de gestión de doctores"""
        if self.modelo.tiene_permiso('doctores'):
            print("Abriendo módulo de Doctores...")
            try:
                from Controladores.DoctorControlador import ControladorDoctor   
                from Vistas.DoctorVista import DoctorWindow
                
                if hasattr(self, 'Doctor_window') and self.Doctor_window:
                    self.Doctor_window.close()
                    
                self.Doctor_window = DoctorWindow()
                controlador = ControladorDoctor(self.Doctor_window)
                
                # Simplemente mostrar la ventana sin inicializar_vista si no existe
                self.Doctor_window.show()
                
            except ImportError as ie:
                self.show_error_message(
                    "Error de módulo",
                    f"No se pudo importar el módulo de doctores: {str(ie)}. Asegúrate de que el archivo DoctorControlador.py existe y está correctamente configurado."
                )
                
            except Exception as e:
                self.show_error_message(
                    "Error al abrir doctores",
                    f"Detalles del error: {str(e)}"
                )
   
        else:
            self.mostrar_error_permiso("Doctores")
    
    def abrir_citas(self):
        """Abre el módulo de gestión de citas"""
        if self.modelo.tiene_permiso('citas'):
            print("Abriendo módulo de Citas...")
            # Aquí conectarás con el controlador de citas
            from Controladores.CitaControlador import ControladorCita   
            from Vistas.CitaVista import CitaWindow
            try:
                if self.cita_window:
                    self.cita_window.close()
                    
                controlador = ControladorCita()
                
                self.cita_window = CitaWindow()
                controlador.set_vista(self.cita_window)
                
                try:
                    controlador.inicializar_vista()
                    
                    self.cita_window.show()
                    
                except Exception as init_error:
                    self.show_error_message(
                        "Error al inicializar la vista de citas",
                        f"Detalles del error: {str(init_error)}"
                    )
            
            except ImportError:
                self.show_error_message(
                    "Error de módulo",
                    "No se pudo importar el módulo de citas. Asegúrate de que el archivo CitaControlador.py existe y está correctamente configurado."
                )
                
            except Exception as e:
                self.show_error_message(
                    "Error al abrir citas",
                    f"Detalles del error: {str(e)}"
                )
           
        else:
            self.mostrar_error_permiso("Citas")
    
    def abrir_tratamientos(self):
        """Abre el módulo de gestión de tratamientos"""
        if self.modelo.tiene_permiso('tratamientos'):
            print("Abriendo módulo de Tratamientos...")                
            try:
                from Controladores.TratamientoControlador import TratamientoControlador
                from Vistas.TratamientoVista import AgregarTratamientoDialog
                
                if self.Tratamiento_window:
                    self.Tratamiento_window.close()

                # Crear el controlador con un doctor por defecto
                # Usamos None o un doctor vacío por ahora
                controlador = TratamientoControlador(doctor=None)
                
                # Crear la ventana con el controlador
                self.Tratamiento_window = AgregarTratamientoDialog(controlador=controlador)
                
                # Asignar la vista al controlador
                controlador.vista = self.Tratamiento_window
                
                # Mostrar la ventana
                self.Tratamiento_window.show()
                    
            except ImportError as ie:
                self.show_error_message(
                    "Error de módulo",
                    f"No se pudo importar el módulo de tratamientos: {str(ie)}. Asegúrate de que el archivo TratamientoControlador.py existe y está correctamente configurado."
                )
                
            except Exception as e:
                self.show_error_message(
                    "Error al abrir tratamientos",
                    f"Detalles del error: {str(e)}"
                )
           
        else:
            self.mostrar_error_permiso("Tratamientos")

    def abrir_horarios(self):
        """Abre el módulo de gestión de horarios"""
        if self.modelo.tiene_permiso('horarios'):
            print("Abriendo módulo de Horarios...")
            try:
                from Controladores.HorarioControlador import HorarioController   
                from Vistas.HorarioVista import HorarioView
                
                if self.Horario_window:
                    self.Horario_window.close()
                    
                # Crear vista primero
                self.Horario_window = HorarioView()
                
                # Crear controlador con la vista
                controlador = HorarioController(self.Horario_window)
                
                # Mostrar la ventana
                self.Horario_window.show()
                    
            except ImportError as ie:
                self.show_error_message(
                    "Error de módulo",
                    f"No se pudo importar el módulo de horarios: {str(ie)}. Asegúrate de que el archivo HorarioControlador.py existe y está correctamente configurado."
                )
                
            except Exception as e:
                self.show_error_message(
                    "Error al abrir horarios",
                    f"Detalles del error: {str(e)}"
                )
           
        else:
            self.mostrar_error_permiso("Horarios")
    
    def abrir_facturas(self):
        """Abre el módulo de gestión de facturas"""
        if self.modelo.tiene_permiso('facturas'):
            print("Abriendo módulo de Facturas...")
            try:
                from Controladores.FacturaControlador import FacturacionController   
                from Vistas.FacturaVista import FacturacionView
                
                if self.Factura_window:
                    self.Factura_window.close()
                    
                # Crear vista primero
                self.Factura_window = FacturacionView()
                
                # Crear controlador con la vista y guardar referencia
                self.factura_controller = FacturacionController(self.Factura_window)
                
                # Mostrar la ventana
                self.Factura_window.show()
                    
            except ImportError as ie:
                self.show_error_message(
                    "Error de módulo",
                    f"No se pudo importar el módulo de facturas: {str(ie)}. Asegúrate de que el archivo FacturaControlador.py existe y está correctamente configurado."
                )
                
            except Exception as e:
                self.show_error_message(
                    "Error al abrir facturas",
                    f"Detalles del error: {str(e)}"
                )
           
        else:
            self.mostrar_error_permiso("Facturas")
    
    def cerrar_sesion(self):
        """Cierra la sesión actual"""
        print("Cerrando sesión...")
        self.modelo.cerrar_sesion()
        self.vista.close()
        
        # Aquí podrías emitir una señal para volver al login
        # o manejar el regreso al LoginControlador
        # self.regreso_login.emit()
    
    def mostrar_error_permiso(self, modulo):
        """Muestra un mensaje de error de permisos"""
        from PyQt6.QtWidgets import QMessageBox
        
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("⚠️ Acceso Denegado")
        msg.setText(f"No tienes permisos para acceder al módulo de {modulo}")
        msg.setInformativeText(f"Tu rol actual ({self.tipo_usuario}) no permite acceder a esta funcionalidad.")
        msg.setStyleSheet(f"""
            QMessageBox {{
                background-color: #ffffff;
                font-family: Segoe UI, Arial, sans-serif;
                font-size: 14px;
            }}
            QMessageBox QPushButton {{
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                min-width: 80px;
                font-weight: bold;
            }}
            QMessageBox QPushButton:hover {{
                background-color: #c0392b;
            }}
        """)
        msg.exec()
    
    def show_error_message(self, titulo, mensaje):
        """Muestra un mensaje de error general"""
        from PyQt6.QtWidgets import QMessageBox
        
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle(f"❌ {titulo}")
        msg.setText(titulo)
        msg.setInformativeText(mensaje)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #ffffff;
                font-family: Segoe UI, Arial, sans-serif;
                font-size: 14px;
            }
            QMessageBox QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                min-width: 80px;
                font-weight: bold;
            }
            QMessageBox QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        msg.exec()

    
    def obtener_estadisticas_sesion(self):
        """Obtiene las estadísticas de la sesión current"""
        return self.modelo.obtener_estadisticas_sesion()
    
    def obtener_modulos_disponibles(self):
        """Obtiene los módulos disponibles para el usuario actual"""
        return self.modelo.obtener_modulos_disponibles()

def main():
    """Función principal para ejecutar el controlador de menú"""
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication([])
    controlador = MenuControlador("admin", "admin")
    controlador.mostrar()
    app.exec()  # Sin sys.exit() para permitir continuar

if __name__ == "__main__":
    main()