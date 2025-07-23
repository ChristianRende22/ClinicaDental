import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Modelos.loginModelo import LoginModelo
from Vistas.LoginVista import LoginVista

class LoginControlador:
    def __init__(self):
        self.modelo = LoginModelo()
        self.vista = LoginVista()
        self.conectar_eventos()
    
    def conectar_eventos(self):
        """Conecta los eventos entre la vista y el controlador"""
        # Sobrescribir el método de validación de credenciales de la vista
        self.vista.validar_credenciales = self.validar_login
        
        # Conectar señal de login exitoso
        self.vista.login_exitoso.connect(self.on_login_exitoso)
    
    def validar_login(self, usuario, password):
        """Valida las credenciales usando el modelo"""
        try:
            if self.modelo.validar_usuario(usuario, password):
                tipo_usuario = self.modelo.obtener_tipo_usuario(usuario)
                self.vista.mostrar_exito(tipo_usuario)
            else:
                self.vista.mostrar_error("Usuario o contraseña incorrectos")
                self.vista.limpiar_campos()
        except Exception as e:
            self.vista.mostrar_error(f"Error durante la validación: {str(e)}")
    
    def on_login_exitoso(self, tipo_usuario):
        """Maneja el evento de login exitoso"""
        print(f"Login exitoso para usuario tipo: {tipo_usuario}")
        # Aquí puedes agregar lógica adicional como:
        # - Registrar el login en logs
        # - Configurar permisos según el tipo de usuario
        
        # Abrir la ventana principal (menú)
        self.abrir_ventana_principal(tipo_usuario)
    
    def mostrar(self):
        """Muestra la ventana de login"""
        self.vista.show()
    
    def abrir_ventana_principal(self, tipo_usuario):
        """Abre la ventana principal según el tipo de usuario"""
        print(f"Abriendo ventana principal para: {tipo_usuario}")
        
        # Importar el MenuControlador
        from Controladores.MenuControlador import MenuControlador
        
        # Crear y mostrar el menú principal
        self.menu_controlador = MenuControlador("usuario", tipo_usuario)
        self.menu_controlador.mostrar()
        
        # Mantener referencia a la aplicación en el menú si existe
        if hasattr(self, 'app'):
            self.menu_controlador.app = self.app
        
        # Cerrar la ventana de login
        self.vista.close()

def main():
    """Función principal para ejecutar el controlador de login"""
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication([])
    controlador = LoginControlador()
    controlador.mostrar()
    
    # Mantener referencia a la aplicación para evitar que se cierre
    controlador.app = app
    
    app.exec()  # Sin sys.exit() para permitir continuar

if __name__ == "__main__":
    main()
        