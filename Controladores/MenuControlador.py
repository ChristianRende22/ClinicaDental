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
        self.controlador_pacientes = None
        
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
            try:
                from Controladores.PacienteControlador import PacienteControlador
                if not hasattr(self, 'controlador_pacientes') or self.controlador_pacientes is None:
                    self.controlador_pacientes = PacienteControlador()
                
                # Intenta mostrar la vista incluso si hay error en BD
                self.controlador_pacientes.mostrar()
                
                # Manejar error sin cerrar la aplicación
                if self.controlador_pacientes.vista is None:
                    from PyQt6.QtWidgets import QMessageBox
                    QMessageBox.warning(
                        None,
                        "Error de conexión",
                        "No se pudo conectar a la base de datos.\n\n"
                        "Funcionando en modo local sin base de datos."
                    )
                
                self.controlador_pacientes.vista.raise_()
                self.controlador_pacientes.vista.activateWindow()
            except Exception as e:
                print(f"Error al abrir pacientes: {e}")
                # Muestra error sin cerrar la aplicación
                from PyQt6.QtWidgets import QMessageBox
                QMessageBox.critical(
                    None,
                    "Error crítico",
                    f"No se pudo abrir el módulo de pacientes:\n{str(e)}"
                )
        else:
            self.mostrar_error_permiso("Pacientes")
                    
                  
    def abrir_doctores(self):
        """Abre el módulo de gestión de doctores"""
        if self.modelo.tiene_permiso('doctores'):
            print("Abriendo módulo de Doctores...")
            # Aquí conectarás con el controlador de doctores
            # from Controladores.DoctorControlador import DoctorControlador
            # self.controlador_doctores = DoctorControlador()
            # self.controlador_doctores.mostrar()
        else:
            self.mostrar_error_permiso("Doctores")
    
    def abrir_citas(self):
        """Abre el módulo de gestión de citas"""
        if self.modelo.tiene_permiso('citas'):
            print("Abriendo módulo de Citas...")
            # Aquí conectarás con el controlador de citas
            # from Controladores.CitaControlador import CitaControlador
            # self.controlador_citas = CitaControlador()
            # self.controlador_citas.mostrar()
        else:
            self.mostrar_error_permiso("Citas")
    
    def abrir_tratamientos(self):
        """Abre el módulo de gestión de tratamientos"""
        if self.modelo.tiene_permiso('tratamientos'):
            print("Abriendo módulo de Tratamientos...")
            # Aquí conectarás con el controlador de tratamientos
            # from Controladores.TratamientoControlador import TratamientoControlador
            # self.controlador_tratamientos = TratamientoControlador()
            # self.controlador_tratamientos.mostrar()
        else:
            self.mostrar_error_permiso("Tratamientos")
    
    def abrir_horarios(self):
        """Abre el módulo de gestión de horarios"""
        if self.modelo.tiene_permiso('horarios'):
            print("Abriendo módulo de Horarios...")
            # Aquí conectarás con el controlador de horarios
            # from Controladores.HorarioControlador import HorarioControlador
            # self.controlador_horarios = HorarioControlador()
            # self.controlador_horarios.mostrar()
        else:
            self.mostrar_error_permiso("Horarios")
    
    def abrir_facturas(self):
        """Abre el módulo de gestión de facturas"""
        if self.modelo.tiene_permiso('facturas'):
            print("Abriendo módulo de Facturas...")
            # Aquí conectarás con el controlador de facturas
            # from Controladores.FacturaControlador import FacturaControlador
            # self.controlador_facturas = FacturaControlador()
            # self.controlador_facturas.mostrar()
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
    
    def obtener_estadisticas_sesion(self):
        """Obtiene las estadísticas de la sesión current"""
        return self.modelo.obtener_estadisticas_sesion()
    
    def obtener_modulos_disponibles(self):
        """Obtiene los módulos disponibles para el usuario actual"""
        return self.modelo.obtener_modulos_disponibles()

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    controlador = MenuControlador("admin", "admin")
    controlador.mostrar()
    sys.exit(app.exec())
