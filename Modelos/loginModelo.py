class LoginModelo:
    def __init__(self):
        # Usuarios hardcodeados para la validación
        self.usuarios_validos = {
            "admin": "123456",
            "doctor": "doctor123",
            "recepcionista": "recep123"
        }
    
    def validar_usuario(self, usuario, password):
        """
        Valida las credenciales del usuario
        Returns: True si las credenciales son válidas, False en caso contrario
        """
        if usuario in self.usuarios_validos:
            return self.usuarios_validos[usuario] == password
        return False
    
    def obtener_tipo_usuario(self, usuario):
        """
        Obtiene el tipo de usuario basado en el nombre de usuario
        Returns: El tipo de usuario (admin, doctor, recepcionista)
        """
        return usuario if usuario in self.usuarios_validos else None