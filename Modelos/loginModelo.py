import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Config.database_config import obtener_conexion

class LoginModelo:
    def __init__(self):
        pass
    
    def validar_usuario(self, usuario, password):
        """
        Valida las credenciales del usuario consultando la base de datos
        Returns: True si las credenciales son válidas, False en caso contrario
        """
        conexion = None
        try:
            conexion = obtener_conexion()
            if conexion and conexion.is_connected():
                cursor = conexion.cursor()
                
                # Consulta para validar usuario y contraseña en la tabla Asistente
                query = "SELECT COUNT(*) FROM Asistente WHERE Nombre = %s AND Contrasena = %s"
                cursor.execute(query, (usuario, password))
                
                resultado = cursor.fetchone()
                return resultado[0] > 0
                
        except Exception as e:
            print(f"Error al validar usuario: {e}")
            return False
            
        finally:
            if conexion and conexion.is_connected():
                cursor.close()
                conexion.close()
        
        return False
    
    def obtener_tipo_usuario(self, usuario):
        """
        Obtiene información del usuario desde la base de datos
        Returns: 'asistente' si el usuario existe en la tabla Asistente, None en caso contrario
        """
        conexion = None
        try:
            conexion = obtener_conexion()
            if conexion and conexion.is_connected():
                cursor = conexion.cursor()
                
                # Consulta para verificar si el usuario existe en la tabla Asistente
                query = "SELECT Nombre, Apellido FROM Asistente WHERE Nombre = %s"
                cursor.execute(query, (usuario,))
                
                resultado = cursor.fetchone()
                if resultado:
                    return 'asistente'
                
        except Exception as e:
            print(f"Error al obtener tipo de usuario: {e}")
            return None
            
        finally:
            if conexion and conexion.is_connected():
                cursor.close()
                conexion.close()
        
        return None
    
    def obtener_datos_usuario(self, usuario):
        """
        Obtiene los datos completos del usuario desde la base de datos
        Returns: Diccionario con los datos del usuario o None si no existe
        """
        conexion = None
        try:
            conexion = obtener_conexion()
            if conexion and conexion.is_connected():
                cursor = conexion.cursor(dictionary=True)
                
                # Consulta para obtener todos los datos del usuario
                query = "SELECT ID_Asistente, Nombre, Apellido, Telefono, Correo FROM Asistente WHERE Nombre = %s"
                cursor.execute(query, (usuario,))
                
                resultado = cursor.fetchone()
                return resultado
                
        except Exception as e:
            print(f"Error al obtener datos del usuario: {e}")
            return None
            
        finally:
            if conexion and conexion.is_connected():
                cursor.close()
                conexion.close()
        
        return None
    
    def listar_usuarios_disponibles(self):
        """
        Lista todos los usuarios disponibles en la base de datos
        Returns: Lista de diccionarios con información de usuarios o lista vacía si hay error
        """
        conexion = None
        try:
            conexion = obtener_conexion()
            if conexion and conexion.is_connected():
                cursor = conexion.cursor(dictionary=True)
                
                # Consulta para obtener todos los usuarios de la tabla Asistente
                query = "SELECT Nombre, Apellido, Correo FROM Asistente ORDER BY Nombre"
                cursor.execute(query)
                
                usuarios = cursor.fetchall()
                return usuarios
                
        except Exception as e:
            print(f"Error al listar usuarios: {e}")
            return []
            
        finally:
            if conexion and conexion.is_connected():
                cursor.close()
                conexion.close()
        
        return []
    
    def mostrar_usuarios_disponibles(self):
        """
        Muestra en consola todos los usuarios disponibles para login
        """
        print("=" * 50)
        print("🔐 USUARIOS DISPONIBLES PARA LOGIN")
        print("=" * 50)
        
        usuarios = self.listar_usuarios_disponibles()
        
        if usuarios:
            print(f"📊 Total de usuarios registrados: {len(usuarios)}")
            print("-" * 50)
            
            for i, usuario in enumerate(usuarios, 1):
                print(f"👤 {i}. Usuario: {usuario['Nombre']}")
                print(f"   Nombre completo: {usuario['Nombre']} {usuario['Apellido']}")
                print(f"   Email: {usuario['Correo']}")
                print("-" * 30)
                
            print("\n💡 NOTAS:")
            print("• Usa el campo 'Nombre' como usuario para hacer login")
            print("• Las contraseñas están configuradas en la base de datos")
            print("• Ya no se usan usuarios hardcodeados")
        else:
            print("❌ No se encontraron usuarios en la base de datos")
            print("🔧 Verifica que:")
            print("   • La base de datos esté ejecutándose")
            print("   • Los datos hayan sido insertados correctamente")
            print("   • La configuración de conexión sea correcta")
        
        print("=" * 50)


# Función para mostrar usuarios desde el terminal o para testing
if __name__ == "__main__":
    modelo = LoginModelo()
    modelo.mostrar_usuarios_disponibles()