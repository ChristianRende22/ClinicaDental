import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from datetime import datetime

class MenuModelo:
    def __init__(self):
        self.usuario_actual = None
        self.tipo_usuario = None
        self.sesion_iniciada = False
        self.hora_inicio_sesion = None
        
        # Permisos por tipo de usuario
        self.permisos = {
            'admin': {
                'pacientes': True,
                'doctores': True,
                'citas': True,
                'tratamientos': True,
                'horarios': True,
                'facturas': True
            },
            'doctor': {
                'pacientes': True,
                'doctores': False,
                'citas': True,
                'tratamientos': True,
                'horarios': True,
                'facturas': False
            },
            'recepcionista': {
                'pacientes': True,
                'doctores': False,
                'citas': True,
                'tratamientos': False,
                'horarios': True,
                'facturas': True
            }
        }
    
    def inicializar_sesion(self, usuario, tipo_usuario):
        """Inicializa la sesión del usuario"""
        self.usuario_actual = usuario
        self.tipo_usuario = tipo_usuario
        self.sesion_iniciada = True
        self.hora_inicio_sesion = datetime.now()
        return True
    
    def cerrar_sesion(self):
        """Cierra la sesión actual"""
        self.usuario_actual = None
        self.tipo_usuario = None
        self.sesion_iniciada = False
        self.hora_inicio_sesion = None
        return True
    
    def obtener_usuario_actual(self):
        """Obtiene el usuario actual"""
        return self.usuario_actual
    
    def obtener_tipo_usuario(self):
        """Obtiene el tipo de usuario actual"""
        return self.tipo_usuario
    
    def tiene_permiso(self, modulo):
        """Verifica si el usuario actual tiene permiso para acceder a un módulo"""
        if not self.sesion_iniciada or not self.tipo_usuario:
            return False
        
        if self.tipo_usuario not in self.permisos:
            return False
        
        return self.permisos[self.tipo_usuario].get(modulo, False)
    
    def obtener_modulos_disponibles(self):
        """Obtiene los módulos disponibles para el usuario actual"""
        if not self.sesion_iniciada or not self.tipo_usuario:
            return []
        
        modulos_disponibles = []
        permisos_usuario = self.permisos.get(self.tipo_usuario, {})
        
        for modulo, tiene_acceso in permisos_usuario.items():
            if tiene_acceso:
                modulos_disponibles.append(modulo)
        
        return modulos_disponibles
    
    def obtener_estadisticas_sesion(self):
        """Obtiene estadísticas de la sesión actual"""
        if not self.sesion_iniciada:
            return None
        
        tiempo_sesion = datetime.now() - self.hora_inicio_sesion
        return {
            'usuario': self.usuario_actual,
            'tipo_usuario': self.tipo_usuario,
            'hora_inicio': self.hora_inicio_sesion,
            'tiempo_activo': tiempo_sesion
        }
    
    def validar_sesion(self):
        """Valida que la sesión esté activa"""
        return self.sesion_iniciada and self.usuario_actual is not None
    
    def obtener_mensaje_bienvenida(self):
        """Obtiene el mensaje de bienvenida personalizado"""
        if not self.sesion_iniciada:
            return "Usuario no identificado"
        
        hora_actual = datetime.now().hour
        
        if hora_actual < 12:
            saludo = "Buenos días"
        elif hora_actual < 18:
            saludo = "Buenas tardes"
        else:
            saludo = "Buenas noches"
        
        return f"{saludo}, {self.usuario_actual}!"
    
    def obtener_configuracion_usuario(self):
        """Obtiene la configuración específica del usuario"""
        configuraciones = {
            'admin': {
                'tema': 'completo',
                'notificaciones': True,
                'acceso_reportes': True,
                'puede_modificar_usuarios': True
            },
            'doctor': {
                'tema': 'medico',
                'notificaciones': True,
                'acceso_reportes': True,
                'puede_modificar_usuarios': False
            },
            'recepcionista': {
                'tema': 'basico',
                'notificaciones': False,
                'acceso_reportes': False,
                'puede_modificar_usuarios': False
            }
        }
        
        return configuraciones.get(self.tipo_usuario, {})
