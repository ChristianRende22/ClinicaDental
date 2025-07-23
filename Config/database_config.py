"""
=================================================================
CONFIGURACIÓN DE BASE DE DATOS PARA CLÍNICA DENTAL
=================================================================
Archivo centralizado para manejar toda la configuración de conexiones
a la base de datos y otros puertos/servicios de la aplicación.

Autor: Sistema de Gestión Clínica Dental
Fecha: 2025
Versión: 1.0
=================================================================
"""

import mysql.connector
from mysql.connector import Error
import os
from typing import Optional

# =================================================================
# CONFIGURACIÓN DE BASE DE DATOS
# =================================================================

class DatabaseConfig:
    """Clase para centralizar toda la configuración de la base de datos"""
    
    # Configuración principal de MySQL
    HOST = 'localhost'
    PORT = 3307
    USER = 'root'
    PASSWORD = '1234'
    DATABASE = 'ClinicaDental'
    
    # Configuración de conexión
    AUTOCOMMIT = True
    CHARSET = 'utf8mb4'
    COLLATION = 'utf8mb4_unicode_ci'
    
    # Configuración de timeout y reintentos
    CONNECTION_TIMEOUT = 10
    MAX_RETRIES = 3
    RETRY_DELAY = 1  # segundos
    
    # Pool de conexiones (si se usa en el futuro)
    POOL_NAME = 'clinica_dental_pool'
    POOL_SIZE = 5
    POOL_RESET_SESSION = True

    @classmethod
    def get_connection_params(cls) -> dict:
        """
        Obtiene los parámetros de conexión como diccionario
        
        Returns:
            dict: Parámetros de conexión para mysql.connector
        """
        return {
            'host': cls.HOST,
            'port': cls.PORT,
            'user': cls.USER,
            'password': cls.PASSWORD,
            'database': cls.DATABASE,
            'charset': cls.CHARSET,
            'collation': cls.COLLATION,
            'autocommit': cls.AUTOCOMMIT,
            'connection_timeout': cls.CONNECTION_TIMEOUT
        }
    
    @classmethod
    def update_config(cls, **kwargs):
        """
        Actualiza la configuración dinámicamente
        
        Args:
            **kwargs: Parámetros a actualizar (host, port, user, password, database)
        """
        for key, value in kwargs.items():
            if hasattr(cls, key.upper()):
                setattr(cls, key.upper(), value)
                print(f"✅ Configuración actualizada: {key.upper()} = {value}")
            else:
                print(f"⚠️  Configuración no reconocida: {key}")

# =================================================================
# FUNCIONES DE CONEXIÓN CENTRALIZADAS
# =================================================================

def obtener_conexion() -> Optional[mysql.connector.MySQLConnection]:
    """
    Establece y devuelve una conexión segura a la base de datos MySQL
    usando la configuración centralizada.
    
    Returns:
        Optional[mysql.connector.MySQLConnection]: Conexión a la base de datos o None si falla
    """
    try:
        print("🔄 Intentando conectar a la base de datos...")
        
        # Usar parámetros de conexión centralizados
        connection_params = DatabaseConfig.get_connection_params()
        conexion = mysql.connector.connect(**connection_params)
        
        if conexion.is_connected():
            print("✅ Conexión exitosa a la base de datos")
            print(f"📊 Servidor: {DatabaseConfig.HOST}:{DatabaseConfig.PORT}")
            print(f"🗄️  Base de datos: {DatabaseConfig.DATABASE}")
            return conexion
            
    except mysql.connector.Error as e:
        print(f"❌ Error de MySQL al conectar a la base de datos: {e}")
        _handle_mysql_errors(e)
        return None
        
    except Exception as e:
        print(f"❌ Error inesperado al conectar a la base de datos: {e}")
        print("⚠️  Funcionando en modo sin base de datos")
        return None

def conectar_bd() -> Optional[mysql.connector.MySQLConnection]:
    """
    Función alternativa de conexión (mantiene compatibilidad con código existente)
    
    Returns:
        Optional[mysql.connector.MySQLConnection]: Conexión a la base de datos o None si falla
    """
    return obtener_conexion()

def probar_conexion() -> tuple[bool, str]:
    """
    Prueba la conexión a la base de datos
    
    Returns:
        tuple[bool, str]: (éxito, mensaje)
    """
    try:
        conexion = obtener_conexion()
        if not conexion:
            return False, "❌ No se pudo conectar a la base de datos"
        
        cursor = conexion.cursor()
        cursor.execute("SELECT 1")
        resultado = cursor.fetchone()
        
        cursor.close()
        conexion.close()
        
        if resultado:
            return True, "✅ Conexión a la base de datos exitosa"
        else:
            return False, "❌ Error en la consulta de prueba"
            
    except Exception as e:
        return False, f"❌ Error de conexión a la base de datos: {str(e)}"

def cerrar_conexion_segura(conexion: Optional[mysql.connector.MySQLConnection], 
                          cursor: Optional[mysql.connector.cursor.MySQLCursor] = None):
    """
    Cierra de forma segura la conexión y el cursor
    
    Args:
        conexion: Conexión a cerrar
        cursor: Cursor a cerrar (opcional)
    """
    try:
        if cursor:
            cursor.close()
            print("🔒 Cursor cerrado correctamente")
            
        if conexion and conexion.is_connected():
            conexion.close()
            print("🔒 Conexión a la base de datos cerrada correctamente")
            
    except Exception as e:
        print(f"⚠️  Error al cerrar conexión: {e}")

# =================================================================
# FUNCIONES DE MANEJO DE ERRORES
# =================================================================

def _handle_mysql_errors(error: mysql.connector.Error):
    """
    Maneja errores específicos de MySQL con mensajes informativos
    
    Args:
        error: Error de MySQL a manejar
    """
    if error.errno == 2003:
        print("⚠️  Error 2003: No se puede conectar al servidor MySQL.")
        print(f"   Verifica que MySQL esté ejecutándose en {DatabaseConfig.HOST}:{DatabaseConfig.PORT}")
    elif error.errno == 1049:
        print(f"⚠️  Error 1049: Base de datos '{DatabaseConfig.DATABASE}' no existe.")
        print("   Ejecuta el script SQL para crear la base de datos.")
    elif error.errno == 1045:
        print("⚠️  Error 1045: Acceso denegado.")
        print(f"   Verifica usuario '{DatabaseConfig.USER}' y contraseña.")
    elif error.errno == 1251:
        print("⚠️  Error 1251: Plugin de autenticación no soportado.")
        print("   Puede ser necesario actualizar la configuración de MySQL.")
    else:
        print(f"⚠️  Error MySQL {error.errno}: {error.msg}")
    
    print("⚠️  La aplicación funcionará en modo sin base de datos")

# =================================================================
# CONFIGURACIÓN DE OTROS SERVICIOS (FUTURO)
# =================================================================

class ServiceConfig:
    """Configuración para otros servicios y puertos"""
    
    # Puerto de la aplicación (si se usa servidor web)
    APP_PORT = 8000
    
    # Configuración de email (si se implementa)
    SMTP_HOST = 'smtp.gmail.com'
    SMTP_PORT = 587
    
    # Configuración de logging
    LOG_LEVEL = 'INFO'
    LOG_FILE = 'clinica_dental.log'
    
    # Configuración de backup
    BACKUP_INTERVAL = 24  # horas
    BACKUP_PATH = './backups/'

# =================================================================
# CONFIGURACIÓN DE DESARROLLO VS PRODUCCIÓN
# =================================================================

class EnvironmentConfig:
    """Configuración por ambiente"""
    
    DEVELOPMENT = {
        'DATABASE': 'ClinicaDental_dev',
        'DEBUG': True,
        'LOG_LEVEL': 'DEBUG'
    }
    
    PRODUCTION = {
        'DATABASE': 'ClinicaDental',
        'DEBUG': False,
        'LOG_LEVEL': 'ERROR'
    }
    
    @classmethod
    def load_environment(cls, env: str = 'DEVELOPMENT'):
        """
        Carga configuración según el ambiente
        
        Args:
            env: Ambiente a cargar ('DEVELOPMENT' o 'PRODUCTION')
        """
        config = getattr(cls, env, cls.DEVELOPMENT)
        
        # Actualizar configuración de base de datos si es necesario
        if 'DATABASE' in config:
            DatabaseConfig.DATABASE = config['DATABASE']
            
        print(f"🔧 Configuración cargada para ambiente: {env}")
        return config

# =================================================================
# EXPORTACIONES PRINCIPALES
# =================================================================

__all__ = [
    'DatabaseConfig',
    'ServiceConfig', 
    'EnvironmentConfig',
    'obtener_conexion',
    'conectar_bd',
    'probar_conexion',
    'cerrar_conexion_segura'
]

# =================================================================
# INICIALIZACIÓN
# =================================================================

if __name__ == "__main__":
    """Prueba de configuración cuando se ejecuta directamente"""
    print("🧪 Probando configuración de base de datos...")
    print(f"📊 Host: {DatabaseConfig.HOST}:{DatabaseConfig.PORT}")
    print(f"🗄️  Base de datos: {DatabaseConfig.DATABASE}")
    print(f"👤 Usuario: {DatabaseConfig.USER}")
    
    # Probar conexión
    exito, mensaje = probar_conexion()
    print(mensaje)
    
    if exito:
        print("✅ Configuración lista para usar")
    else:
        print("❌ Revisar configuración de base de datos")
