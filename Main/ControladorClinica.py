import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from PyQt6.QtWidgets import QApplication
from Controladores.LoginControlador import LoginControlador
from Controladores.MenuControlador import MenuControlador

class ControladorClinica:
    def __init__(self):
        self.login_controlador = None
        self.menu_controlador = None
        self.usuario_actual = None
        self.tipo_usuario_actual = None
        
    def iniciar_aplicacion(self):
        """Inicia la aplicación mostrando la ventana de login"""
        self.login_controlador = LoginControlador()
        
        # Conectar la señal de login exitoso
        self.login_controlador.vista.login_exitoso.connect(self.on_login_exitoso)
        
        # Mostrar ventana de login
        self.login_controlador.mostrar()
    
    def on_login_exitoso(self, tipo_usuario):
        """Maneja el evento cuando el login es exitoso"""
        self.tipo_usuario_actual = tipo_usuario
        
        # Cerrar ventana de login
        self.login_controlador.vista.close()
        
        # Abrir menú principal
        self.abrir_menu()
    
    def abrir_menu(self):
        """Abre la ventana del menú principal"""
        self.menu_controlador = MenuControlador(
            usuario=self.usuario_actual,
            tipo_usuario=self.tipo_usuario_actual
        )
        
        # Conectar señal de cerrar sesión para volver al login
        self.menu_controlador.vista.cerrar_sesion.connect(self.cerrar_sesion)
        
        # Mostrar menú
        self.menu_controlador.mostrar()
    
    def cerrar_sesion(self):
        """Cierra la sesión actual y vuelve al login"""
        # Cerrar ventana de menú
        if self.menu_controlador:
            self.menu_controlador.cerrar()
            self.menu_controlador = None
        
        # Limpiar datos de sesión
        self.usuario_actual = None
        self.tipo_usuario_actual = None
        
        # Volver a mostrar login
        self.iniciar_aplicacion()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controlador = ControladorClinica()
    controlador.iniciar_aplicacion()
    sys.exit(app.exec())
