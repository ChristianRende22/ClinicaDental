import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from PyQt6.QtWidgets import QApplication
from Controladores.LoginControlador import LoginControlador

class ControladorClinica:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.login_controlador = None
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
        """Maneja el login exitoso y abre la ventana principal"""
        self.tipo_usuario = tipo_usuario
        print(f"Usuario {tipo_usuario} ha iniciado sesión correctamente")
        


# Punto de entrada de la aplicación
if __name__ == "__main__":
    controlador = ControladorClinica()
    sys.exit(controlador.iniciar_aplicacion())