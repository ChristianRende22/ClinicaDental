class MenuModelo:
    def __init__(self):
        self.usuario_actual = None
        self.tipo_usuario = None
        
        # Menú unificado para todos los tipos de usuario
        self.opciones_menu_unificado = [
            {'nombre': '👥 Gestión de Pacientes', 'accion': 'pacientes', 'descripcion': 'Registrar, editar y consultar pacientes'},
            {'nombre': '👨‍⚕️ Gestión de Doctores', 'accion': 'doctores', 'descripcion': 'Administrar doctores y especialidades'},
            {'nombre': '📅 Gestión de Citas', 'accion': 'citas', 'descripcion': 'Programar y gestionar citas médicas'},
            {'nombre': '💊 Gestión de Tratamientos', 'accion': 'tratamientos', 'descripcion': 'Administrar tratamientos dentales'},
            {'nombre': '💰 Gestión de Facturas', 'accion': 'facturas', 'descripcion': 'Control de facturación y pagos'},
            {'nombre': '⏰ Gestión de Horarios', 'accion': 'horarios', 'descripcion': 'Configurar horarios de trabajo'},
            {'nombre': '📊 Reportes', 'accion': 'reportes', 'descripcion': 'Generar reportes del sistema'},
            {'nombre': '⚙️ Configuración', 'accion': 'configuracion', 'descripcion': 'Configuración del sistema'}
        ]
    
    def establecer_usuario(self, tipo_usuario, usuario=None):
        """Establece el usuario actual y su tipo"""
        self.tipo_usuario = tipo_usuario
        self.usuario_actual = usuario
    
    def obtener_opciones_menu(self):
        """Obtiene las opciones del menú unificado para todos los usuarios"""
        return self.opciones_menu_unificado
    
    def es_administrador(self):
        """Verifica si el usuario actual es administrador"""
        return self.tipo_usuario == 'admin'
    
    def puede_acceder_opcion(self, accion):
        """Verifica si el usuario puede acceder a una opción específica - ahora todos pueden acceder a todo"""
        opciones = self.obtener_opciones_menu()
        return any(opcion['accion'] == accion for opcion in opciones)