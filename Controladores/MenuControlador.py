import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Modelos.MenuModelo import MenuModelo
from Vistas.MenuVista import MenuVista

class MenuControlador:
    def __init__(self, tipo_usuario):
        self.modelo = MenuModelo()
        self.vista = MenuVista()
        self.tipo_usuario = tipo_usuario
        
        # Establecer usuario en el modelo
        self.modelo.establecer_usuario(tipo_usuario)
        
        # Configurar la vista
        self.vista.establecer_usuario(tipo_usuario)
        
        # Cargar opciones del menú
        opciones = self.modelo.obtener_opciones_menu()
        self.vista.cargar_opciones_menu(opciones)
        
        # Conectar eventos
        self.conectar_eventos()
    
    def conectar_eventos(self):
        """Conecta los eventos entre la vista y el controlador"""
        self.vista.opcion_seleccionada.connect(self.manejar_opcion_seleccionada)
        self.vista.cerrar_sesion.connect(self.manejar_cerrar_sesion)
    
    def manejar_opcion_seleccionada(self, accion):
        """Maneja la selección de una opción del menú"""
        print(f"Opción seleccionada: {accion}")
        
        # Verificar si el usuario puede acceder a la opción
        if not self.modelo.puede_acceder_opcion(accion):
            self.mostrar_mensaje_error("No tienes permisos para acceder a esta opción")
            return
        
        # Abrir la ventana correspondiente según la acción
        if accion == 'pacientes':
            self.abrir_gestion_pacientes()
        elif accion == 'doctores':
            self.abrir_gestion_doctores()
        elif accion == 'citas':
            self.abrir_gestion_citas()
        elif accion == 'tratamientos':
            self.abrir_gestion_tratamientos()
        elif accion == 'facturas':
            self.abrir_gestion_facturas()
        elif accion == 'horarios':
            self.abrir_gestion_horarios()

        else:
            self.mostrar_mensaje_info(f"Funcionalidad '{accion}' en desarrollo")
    
    def abrir_gestion_pacientes(self):
        """Abre la ventana de gestión de pacientes"""
        try:
            from Controladores.PacienteControlador import PacienteControlador
            
            # Crear el controlador de pacientes
            self.controlador_pacientes = PacienteControlador()
            
            # Mostrar la vista a través del controlador
            self.controlador_pacientes.mostrar()
            
        except ImportError as e:
            self.mostrar_mensaje_error("Módulo de pacientes no disponible")
        except Exception as e:
            self.mostrar_mensaje_error(f"Error al abrir gestión de pacientes: {str(e)}")
    
    def abrir_gestion_doctores(self):
        """Abre la ventana de gestión de doctores"""
        try:
            from Controladores.DoctorControlador import DoctorControlador
            
            # Crear el controlador de doctores
            self.controlador_doctores = DoctorControlador()
            
            # Verificar si tiene método mostrar, si no usar inicializar_vista
            if hasattr(self.controlador_doctores, 'mostrar'):
                self.controlador_doctores.mostrar()
            elif hasattr(self.controlador_doctores, 'inicializar_vista'):
                self.controlador_doctores.inicializar_vista()
            else:
                self.mostrar_mensaje_info("Gestión de doctores en desarrollo")
            
        except ImportError:
            self.mostrar_mensaje_error("Módulo de doctores no disponible")
        except Exception as e:
            print(f"Error al abrir gestión de doctores: {e}")
            self.mostrar_mensaje_error(f"Error al abrir gestión de doctores: {str(e)}")
    
    def abrir_gestion_citas(self):
        """Abre la ventana de gestión de citas"""
        try:
            from Controladores.CitaControlador import CitaControlador
            
            # Crear el controlador de citas
            self.controlador_citas = CitaControlador()
            
            # Verificar si tiene método mostrar, si no usar inicializar_vista
            if hasattr(self.controlador_citas, 'mostrar'):
                self.controlador_citas.mostrar()
            elif hasattr(self.controlador_citas, 'inicializar_vista'):
                self.controlador_citas.inicializar_vista()
            else:
                self.mostrar_mensaje_info("Gestión de citas en desarrollo")
                
        except ImportError:
            self.mostrar_mensaje_error("Módulo de citas no disponible")
        except Exception as e:
            print(f"Error al abrir gestión de citas: {e}")
            self.mostrar_mensaje_error(f"Error al abrir gestión de citas: {str(e)}")
    
    def abrir_gestion_tratamientos(self):
        """Abre la ventana de gestión de tratamientos"""
        try:
            from Controladores.TratamientoControlador import TratamientoControlador
            
            # Crear el controlador de tratamientos
            self.controlador_tratamientos = TratamientoControlador()
            
            # Verificar si tiene método mostrar, si no usar inicializar_vista
            if hasattr(self.controlador_tratamientos, 'mostrar'):
                self.controlador_tratamientos.mostrar()
            elif hasattr(self.controlador_tratamientos, 'inicializar_vista'):
                self.controlador_tratamientos.inicializar_vista()
            else:
                self.mostrar_mensaje_info("Gestión de tratamientos en desarrollo")
                
        except ImportError:
            self.mostrar_mensaje_error("Módulo de tratamientos no disponible")
        except Exception as e:
            print(f"Error al abrir gestión de tratamientos: {e}")
            self.mostrar_mensaje_error(f"Error al abrir gestión de tratamientos: {str(e)}")
    
    def abrir_gestion_facturas(self):
        """Abre la ventana de gestión de facturas"""
        try:
            from Controladores.FacturaControlador import FacturaControlador
            
            # Crear el controlador de facturas
            self.controlador_facturas = FacturaControlador()
            
            # Verificar si tiene método mostrar, si no usar inicializar_vista
            if hasattr(self.controlador_facturas, 'mostrar'):
                self.controlador_facturas.mostrar()
            elif hasattr(self.controlador_facturas, 'inicializar_vista'):
                self.controlador_facturas.inicializar_vista()
            else:
                self.mostrar_mensaje_info("Gestión de facturas en desarrollo")
                
        except ImportError:
            self.mostrar_mensaje_error("Módulo de facturas no disponible")
        except Exception as e:
            print(f"Error al abrir gestión de facturas: {e}")
            self.mostrar_mensaje_error(f"Error al abrir gestión de facturas: {str(e)}")
    
    def abrir_gestion_horarios(self):
        """Abre la ventana de gestión de horarios"""
        try:
            from Controladores.HorarioControlador import HorarioControlador
            
            # Crear el controlador de horarios
            self.controlador_horarios = HorarioControlador()
            
            # Verificar si tiene método mostrar, si no usar inicializar_vista
            if hasattr(self.controlador_horarios, 'mostrar'):
                self.controlador_horarios.mostrar()
            elif hasattr(self.controlador_horarios, 'inicializar_vista'):
                self.controlador_horarios.inicializar_vista()
            else:
                self.mostrar_mensaje_info("Gestión de horarios en desarrollo")
                
        except ImportError:
            self.mostrar_mensaje_error("Módulo de horarios no disponible")
        except Exception as e:
            print(f"Error al abrir gestión de horarios: {e}")
            self.mostrar_mensaje_error(f"Error al abrir gestión de horarios: {str(e)}")
    

    def manejar_cerrar_sesion(self):
        """Maneja el cierre de sesión"""
        from PyQt6.QtWidgets import QMessageBox
        
        # Confirmar cierre de sesión
        reply = QMessageBox.question(
            self.vista,
            "🚪 Cerrar Sesión",
            "¿Estás seguro de que deseas cerrar sesión?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            print("Cerrando sesión...")
            self.vista.close()
            # Emitir señal para volver al login
            # TODO: Implementar regreso al login
    
    def mostrar_mensaje_info(self, mensaje):
        """Muestra un mensaje informativo"""
        from PyQt6.QtWidgets import QMessageBox
        
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("ℹ️ Información")
        msg.setText(mensaje)
        msg.exec()
    
    def mostrar_mensaje_error(self, mensaje):
        """Muestra un mensaje de error"""
        from PyQt6.QtWidgets import QMessageBox
        
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("⚠️ Error")
        msg.setText(mensaje)
        msg.exec()
    
    def mostrar(self):
        """Muestra la ventana del menú"""
        self.vista.show()
        self.vista.mostrar_mensaje_bienvenida()
    
    def ocultar(self):
        """Oculta la ventana del menú"""
        self.vista.hide()