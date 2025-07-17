import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QGridLayout, QSpacerItem, QSizePolicy)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

class MenuVista(QWidget):
    # Señales para cada módulo
    ir_a_pacientes = pyqtSignal()
    ir_a_doctores = pyqtSignal()
    ir_a_citas = pyqtSignal()
    ir_a_tratamientos = pyqtSignal()
    ir_a_horarios = pyqtSignal()
    ir_a_facturas = pyqtSignal()
    cerrar_sesion = pyqtSignal()
    
    def __init__(self, tipo_usuario="admin"):
        super().__init__()
        self.tipo_usuario = tipo_usuario
        self.inicializar_ui()
    
    def inicializar_ui(self):
        """Inicializa la interfaz de usuario"""
        self.setWindowTitle("Sistema de Gestión Clínica Dental")
        self.setFixedSize(900, 600)
        self.centrar_ventana()
        self.configurar_estilo()
        self.crear_widgets()
    
    def centrar_ventana(self):
        """Centra la ventana en la pantalla"""
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        window_geometry = self.frameGeometry()
        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())
    
    def configurar_estilo(self):
        """Configura el estilo simple y limpio"""
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            
            QLabel {
                color: #333;
                background-color: transparent;
            }
            
            QPushButton {
                background-color: white;
                color: #333;
                border: 2px solid #130760;
                border-radius: 8px;
                padding: 15px;
                font-size: 14px;
                font-weight: bold;
                min-height: 50px;
            }
            
            QPushButton:hover {
                background-color: #130760;
                color: white;
            }
            
            QPushButton:pressed {
                background-color: #0d0540;
            }
        """)
    
    def crear_widgets(self):
        """Crea los widgets principales"""
        layout_principal = QVBoxLayout()
        layout_principal.setSpacing(30)
        layout_principal.setContentsMargins(40, 40, 40, 40)
        
        # Header simple
        self.crear_header(layout_principal)
        
        # Espaciador
        layout_principal.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        
        # Grid de botones
        grid_layout = QGridLayout()
        grid_layout.setSpacing(20)
        self.crear_botones_servicios(grid_layout)
        layout_principal.addLayout(grid_layout)
        
        # Espaciador
        layout_principal.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        # Botón cerrar sesión
        self.crear_boton_cerrar_sesion(layout_principal)
        
        self.setLayout(layout_principal)
    
    def crear_header(self, layout_principal):
        """Crea el header simple"""
        header_layout = QHBoxLayout()
        
        # Título
        titulo = QLabel("🏥 Clínica Dental")
        titulo.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        titulo.setStyleSheet("color: #130760; margin-bottom: 10px;")
        
        # Usuario
        usuario_label = QLabel(f"Usuario: {self.tipo_usuario.capitalize()}")
        usuario_label.setFont(QFont("Segoe UI", 14))
        usuario_label.setStyleSheet("color: #666;")
        usuario_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        header_layout.addWidget(titulo)
        header_layout.addStretch()
        header_layout.addWidget(usuario_label)
        
        layout_principal.addLayout(header_layout)
    
    def crear_botones_servicios(self, grid_layout):
        """Crea los botones de servicios simples"""
        servicios = [
            ("👥 Pacientes", self.ir_a_pacientes),
            ("👨‍⚕️ Doctores", self.ir_a_doctores),
            ("📅 Citas", self.ir_a_citas),
            ("🦷 Tratamientos", self.ir_a_tratamientos),
            ("⏰ Horarios", self.ir_a_horarios),
            ("💰 Facturas", self.ir_a_facturas),
        ]
        
        for i, (texto, signal) in enumerate(servicios):
            btn = QPushButton(texto)
            btn.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
            btn.clicked.connect(signal.emit)
            
            row = i // 3
            col = i % 3
            grid_layout.addWidget(btn, row, col)
    
    def crear_boton_cerrar_sesion(self, layout_principal):
        """Crea el botón de cerrar sesión"""
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        btn_cerrar = QPushButton("Cerrar Sesión")
        btn_cerrar.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        btn_cerrar.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 12px;
                font-weight: bold;
                min-height: 30px;
                max-width: 120px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        btn_cerrar.clicked.connect(self.cerrar_sesion.emit)
        
        btn_layout.addWidget(btn_cerrar)
        layout_principal.addLayout(btn_layout)
    
    def actualizar_usuario(self, tipo_usuario):
        """Actualiza el tipo de usuario"""
        self.tipo_usuario = tipo_usuario
