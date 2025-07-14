import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from PyQt6.QtWidgets import QApplication
from Controladores.LoginControlador import LoginControlador
from Controladores.MenuControlador import MenuControlador

class ControladorClinica:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.login_controlador = None
        self.menu_controlador = None
        self.usuario_actual = None
        self.tipo_usuario = None
    
    def iniciar_aplicacion(self):
        """Inicia la aplicación mostrando primero el login"""
        self.mostrar_login()
        return self.app.exec()
    
    def mostrar_login(self):
        """Muestra la ventana de login"""
        self.login_controlador = LoginControlador()
        
        # Conectar el evento de login exitoso
        self.login_controlador.vista.login_exitoso.connect(self.on_login_exitoso)
        
        # Mostrar la ventana de login
        self.login_controlador.mostrar()
    
    def on_login_exitoso(self, tipo_usuario):
        """Maneja el login exitoso y abre la ventana principal del menú"""
        self.tipo_usuario = tipo_usuario
        print(f"Usuario {tipo_usuario} ha iniciado sesión correctamente")
        
        # Ocultar la ventana de login
        if self.login_controlador:
            self.login_controlador.vista.hide()
        
        # Mostrar el menú principal
        self.mostrar_menu()
    
    def mostrar_menu(self):
        """Muestra el menú principal según el tipo de usuario"""
        self.menu_controlador = MenuControlador(self.tipo_usuario)
        
        # Conectar la señal de logout para volver al login
        self.menu_controlador.vista.logout_signal.connect(self.on_logout)
        
        # Mostrar la ventana del menú
        self.menu_controlador.mostrar()
    
    def on_logout(self):
        """Maneja el logout y vuelve al login"""
        # Cerrar la ventana del menú
        if self.menu_controlador:
            self.menu_controlador.vista.close()
            self.menu_controlador = None
        
        # Limpiar variables de usuario
        self.usuario_actual = None
        self.tipo_usuario = None
        
        # Mostrar nuevamente el login
        self.mostrar_login()
        


# Punto de entrada de la aplicación
if __name__ == "__main__":
    controlador = ControladorClinica()
    sys.exit(controlador.iniciar_aplicacion())