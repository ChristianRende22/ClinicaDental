import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QGridLayout, QFrame, QScrollArea)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap

class MenuVista(QMainWindow):
    # Señales para comunicar con el controlador
    opcion_seleccionada = pyqtSignal(str)  # Emite la acción seleccionada
    cerrar_sesion = pyqtSignal()
    logout_signal = pyqtSignal()  # Señal para cerrar sesión
    
    def __init__(self):
        super().__init__()
        # Esquema de colores consistente con el login
        self.colors = {
            'primary': '#130760',
            'secondary': '#756f9f',
            'accent': '#10b8b9',
            'background': '#f7f8fa',
            'surface': '#ffffff',
            'text_light': '#2c3e50',
            'text_dark': '#34495e'
        }
        self.opciones = []
        self.tipo_usuario = ""
        self.inicializar_ui()
    
    def inicializar_ui(self):
        """Inicializa la interfaz de usuario"""
        self.setWindowTitle("🏥 Sistema de Gestión Clínica Dental - Menú Principal")
        self.setGeometry(100, 100, 800, 600)
        self.centrar_ventana()
        self.configurar_estilo()
        self.crear_widgets()
    
    def centrar_ventana(self):
        """Centra la ventana en la pantalla"""
        from PyQt6.QtGui import QScreen
        screen = self.screen()
        screen_geometry = screen.availableGeometry()
        window_geometry = self.frameGeometry()
        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())
    
    def configurar_estilo(self):
        """Configura el estilo de la ventana"""
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {self.colors['background']};
                font-family: Segoe UI, Arial, sans-serif;
            }}
            
            QWidget {{
                background-color: {self.colors['background']};
                font-family: Segoe UI, Arial, sans-serif;
                font-size: 14px;
                color: {self.colors['text_dark']};
            }}
            
            QLabel {{
                color: {self.colors['text_light']};
                background-color: transparent;
                font-family: Segoe UI, Arial, sans-serif;
            }}
            
            QPushButton {{
                font-family: Segoe UI, Arial, sans-serif;
                font-size: 14px;
                font-weight: bold;
                color: #ffffff;
                background-color: {self.colors['accent']};
                border: none;
                border-radius: 12px;
                padding: 15px 20px;
                min-height: 25px;
                text-align: left;
            }}
            
            QPushButton:hover {{
                background-color: {self.colors['primary']};
            }}
            
            QPushButton:pressed {{
                background-color: {self.colors['secondary']};
            }}
            
            QPushButton#logout_btn {{
                background-color: #e74c3c;
                color: white;
            }}
            
            QPushButton#logout_btn:hover {{
                background-color: #c0392b;
            }}
            
            QFrame {{
                background-color: {self.colors['surface']};
                border: 2px solid {self.colors['secondary']};
                border-radius: 15px;
            }}
            
            QScrollArea {{
                border: none;
                background-color: {self.colors['background']};
            }}
        """)
    
    def crear_widgets(self):
        """Crea y organiza los widgets de la interfaz"""
        # Widget central
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        
        # Layout principal
        layout_principal = QVBoxLayout(widget_central)
        layout_principal.setSpacing(20)
        layout_principal.setContentsMargins(30, 20, 30, 20)
        
        # Header con título y usuario
        self.crear_header(layout_principal)
        
        # Área de scroll para las opciones
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Widget contenedor para las opciones
        self.widget_opciones = QWidget()
        scroll_area.setWidget(self.widget_opciones)
        
        layout_principal.addWidget(scroll_area)
        
        # Footer con botón de cerrar sesión
        self.crear_footer(layout_principal)
    
    def crear_header(self, layout_principal):
        """Crea el header con título y información del usuario"""
        # Frame del header
        frame_header = QFrame()
        frame_header.setFixedHeight(120)
        layout_header = QHBoxLayout(frame_header)
        layout_header.setContentsMargins(25, 15, 25, 15)
        
        # Título
        titulo = QLabel("🏥 Clínica Dental")
        titulo.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        titulo.setStyleSheet(f"color: {self.colors['primary']};")
        
        # Información del usuario
        self.label_usuario = QLabel()
        self.label_usuario.setFont(QFont("Segoe UI", 14))
        self.label_usuario.setStyleSheet(f"color: {self.colors['secondary']};")
        self.label_usuario.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        
        layout_header.addWidget(titulo)
        layout_header.addStretch()
        layout_header.addWidget(self.label_usuario)
        
        layout_principal.addWidget(frame_header)
    
    def crear_footer(self, layout_principal):
        """Crea el footer con botón de cerrar sesión"""
        layout_footer = QHBoxLayout()
        layout_footer.addStretch()
        
        btn_cerrar_sesion = QPushButton("🚪 Cerrar Sesión")
        btn_cerrar_sesion.setObjectName("logout_btn")
        btn_cerrar_sesion.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        btn_cerrar_sesion.clicked.connect(self.logout_signal.emit)
        
        layout_footer.addWidget(btn_cerrar_sesion)
        layout_principal.addLayout(layout_footer)
    
    def establecer_usuario(self, tipo_usuario):
        """Establece la información del usuario en la interfaz"""
        self.tipo_usuario = tipo_usuario
        
        iconos_usuario = {
            'admin': '👨‍💼',
            'doctor': '👨‍⚕️',
            'recepcionista': '👩‍💼'
        }
        
        nombres_usuario = {
            'admin': 'Administrador',
            'doctor': 'Doctor',
            'recepcionista': 'Recepcionista'
        }
        
        icono = iconos_usuario.get(tipo_usuario, '👤')
        nombre = nombres_usuario.get(tipo_usuario, tipo_usuario.capitalize())
        
        self.label_usuario.setText(f"{icono} {nombre}\nSistema de Gestión")
    
    def cargar_opciones_menu(self, opciones):
        """Carga las opciones del menú en la interfaz"""
        self.opciones = opciones
        
        # Limpiar layout anterior si existe
        if self.widget_opciones.layout():
            while self.widget_opciones.layout().count():
                child = self.widget_opciones.layout().takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
        
        # Crear nuevo layout en grid
        layout_opciones = QGridLayout(self.widget_opciones)
        layout_opciones.setSpacing(15)
        layout_opciones.setContentsMargins(20, 20, 20, 20)
        
        # Crear botones para cada opción
        row = 0
        col = 0
        columnas_por_fila = 2
        
        for opcion in opciones:
            btn_opcion = self.crear_boton_opcion(opcion)
            layout_opciones.addWidget(btn_opcion, row, col)
            
            col += 1
            if col >= columnas_por_fila:
                col = 0
                row += 1
        
        # Agregar stretch al final
        layout_opciones.setRowStretch(row + 1, 1)
    
    def crear_boton_opcion(self, opcion):
        """Crea un botón para una opción del menú"""
        btn = QPushButton()
        btn.setFixedHeight(100)
        btn.setMinimumWidth(350)
        
        # Texto del botón
        texto = f"{opcion['nombre']}\n{opcion['descripcion']}"
        btn.setText(texto)
        btn.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        
        # Conectar acción
        btn.clicked.connect(lambda checked, accion=opcion['accion']: self.opcion_seleccionada.emit(accion))
        
        return btn
    
    def mostrar_mensaje_bienvenida(self):
        """Muestra un mensaje de bienvenida"""
        from PyQt6.QtWidgets import QMessageBox
        
        iconos_usuario = {
            'admin': '👨‍💼',
            'doctor': '👨‍⚕️',
            'recepcionista': '👩‍💼'
        }
        
        icono = iconos_usuario.get(self.tipo_usuario, '👤')
        
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("🎉 Bienvenido")
        msg.setText(f"¡Bienvenido al Sistema de Gestión Clínica Dental!\n\n{icono} Has iniciado sesión como {self.tipo_usuario.capitalize()}")
        msg.setStyleSheet(f"""
            QMessageBox {{
                background-color: {self.colors['surface']};
                font-family: Segoe UI, Arial, sans-serif;
                font-size: 14px;
            }}
            QMessageBox QPushButton {{
                background-color: {self.colors['accent']};
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                min-width: 80px;
                font-weight: bold;
            }}
            QMessageBox QPushButton:hover {{
                background-color: {self.colors['primary']};
            }}
        """)
        msg.exec()