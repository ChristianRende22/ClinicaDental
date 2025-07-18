import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QLineEdit, QPushButton, QMessageBox, QFrame, QScrollArea)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

class LoginVista(QWidget):
    # Señal que se emite cuando el login es exitoso
    login_exitoso = pyqtSignal(str)  # Emite el tipo de usuario
    
    def __init__(self):
        super().__init__()
        # Esquema de colores consistente con PacienteVista
        self.colors = {
            'primary': '#130760',
            'secondary': '#756f9f',
            'accent': '#10b8b9',
            'background': '#f7f8fa',
            'surface': '#ffffff',
            'text_light': '#2c3e50',
            'text_dark': '#34495e'
        }
        self.inicializar_ui()
    
    def inicializar_ui(self):
        """Inicializa la interfaz de usuario"""
        self.setWindowTitle("🏥 Sistema de Gestión Clínica Dental - Login")

        self.setFixedSize(500, 600)
        self.centrar_ventana()
        self.configurar_estilo()
        self.crear_widgets()
        self.conectar_eventos()
    
    def centrar_ventana(self):
        """Centra la ventana en la pantalla"""
        from PyQt6.QtGui import QScreen
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        window_geometry = self.frameGeometry()
        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())
    
    def configurar_estilo(self):
        """Configura el estilo de la ventana con el esquema de colores de la clínica"""
        self.setStyleSheet(f"""
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
                font-size: 14px;
            }}
            
            QLineEdit {{
                font-family: Segoe UI, Arial, sans-serif;
                font-size: 18px;
                border: 2px solid {self.colors['secondary']};
                border-radius: 10px;
                padding: 18px;
                background-color: {self.colors['surface']};
                color: {self.colors['text_light']};
                selection-background-color: {self.colors['accent']};
                min-height: 25px;
            }}
            
            QLineEdit:focus {{
                border-color: {self.colors['accent']};
                background-color: #ffffff;
            }}
            
            QLineEdit::placeholder {{
                color: #bdc3c7;
                font-style: italic;
            }}
            
            QPushButton {{
                font-family: Segoe UI, Arial, sans-serif;
                font-size: 18px;
                font-weight: bold;
                color: #ffffff;
                background-color: {self.colors['accent']};
                border: none;
                border-radius: 10px;
                padding: 18px 30px;
                min-height: 30px;
            }}
            
            QPushButton:hover {{
                background-color: {self.colors['primary']};
            }}
            
            QPushButton:pressed {{
                background-color: {self.colors['secondary']};
            }}
            
            QFrame {{
                background-color: {self.colors['surface']};
                border: 2px solid {self.colors['secondary']};
                border-radius: 15px;
                padding: 25px;
            }}
            
            QMessageBox {{
                background-color: {self.colors['surface']};
                font-family: Segoe UI, Arial, sans-serif;
            }}
            
            QMessageBox QPushButton {{
                min-width: 80px;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
            }}
            
            QScrollArea {{
                border: none;
                background-color: {self.colors['background']};
            }}
            
            QScrollBar:vertical {{
                background-color: {self.colors['surface']};
                width: 12px;
                border-radius: 6px;
                margin: 0px;
            }}
            
            QScrollBar::handle:vertical {{
                background-color: {self.colors['secondary']};
                border-radius: 6px;
                min-height: 20px;
                margin: 2px;
            }}
            
            QScrollBar::handle:vertical:hover {{
                background-color: {self.colors['accent']};
            }}
            
            QScrollBar::handle:vertical:pressed {{
                background-color: {self.colors['primary']};
            }}
            
            QScrollBar::add-line:vertical {{
                background: none;
                height: 0px;
            }}
            
            QScrollBar::sub-line:vertical {{
                background: none;
                height: 0px;
            }}
            
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: none;
            }}
        """)
    
    def crear_widgets(self):
        """Crea y organiza los widgets de la interfaz"""
        # Crear el widget principal que contendrá todo el contenido
        widget_contenido = QWidget()
        
        layout_principal = QVBoxLayout(widget_contenido)
        layout_principal.setSpacing(30)
        layout_principal.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_principal.setContentsMargins(35, 35, 35, 35)
        
        # Título de la aplicación
        titulo = QLabel("🏥 Clínica Dental")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setFont(QFont("Segoe UI", 32, QFont.Weight.Bold))
        titulo.setStyleSheet(f"""
            QLabel {{
                color: {self.colors['primary']};
                background-color: {self.colors['surface']};
                border: 3px solid {self.colors['accent']};
                border-radius: 15px;
                padding: 25px;
                margin: 10px;
            }}
        """)
        
        subtitulo = QLabel("Sistema de Gestión Integral")
        subtitulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitulo.setFont(QFont("Segoe UI", 16))
        subtitulo.setStyleSheet(f"""
            QLabel {{
                color: {self.colors['secondary']};
                margin-bottom: 20px;
                font-style: italic;
            }}
        """)
        
        # Frame para el formulario de login
        frame_login = QFrame()
        frame_login.setFrameStyle(QFrame.Shape.StyledPanel)
        
        layout_frame = QVBoxLayout(frame_login)
        layout_frame.setSpacing(30)
        layout_frame.setContentsMargins(40, 40, 40, 40)
        
        # Campo de usuario
        label_usuario = QLabel("👤 Usuario:")
        label_usuario.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        label_usuario.setStyleSheet(f"color: {self.colors['text_light']};")
        self.input_usuario = QLineEdit()
        self.input_usuario.setPlaceholderText("Ingrese su nombre de usuario")
        
        # Campo de contraseña
        label_password = QLabel("🔒 Contraseña:")
        label_password.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        label_password.setStyleSheet(f"color: {self.colors['text_light']};")
        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Ingrese su contraseña")
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
        
        # Botón de login
        self.btn_login = QPushButton("🚀 Iniciar Sesión")
        self.btn_login.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        
        # Agregar widgets al frame
        layout_frame.addWidget(label_usuario)
        layout_frame.addWidget(self.input_usuario)
        layout_frame.addWidget(label_password)
        layout_frame.addWidget(self.input_password)
        layout_frame.addWidget(self.btn_login)
        
        # Información de usuarios de prueba
        info_label = QLabel("📋 Usuarios de prueba:\n• 👨‍💼 admin / 123456 (Administrador)\n• 👨‍⚕️ doctor / doctor123 (Doctor)\n• 👩‍💼 recepcionista / recep123 (Recepcionista)")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_label.setFont(QFont("Segoe UI", 11))
        info_label.setStyleSheet(f"""
            QLabel {{
                color: {self.colors['text_light']}; 
                font-size: 12px; 
                background-color: {self.colors['surface']}; 
                border: 2px solid {self.colors['secondary']}; 
                border-radius: 10px; 
                padding: 15px;
                margin: 15px;
                line-height: 1.5;
            }}
        """)
        
        # Agregar todo al layout principal del widget de contenido
        layout_principal.addWidget(titulo)
        layout_principal.addWidget(subtitulo)
        layout_principal.addWidget(frame_login)
        layout_principal.addWidget(info_label)
        
        # Crear el scroll area y configurarlo
        scroll_area = QScrollArea()
        scroll_area.setWidget(widget_contenido)
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Layout principal de la ventana
        layout_ventana = QVBoxLayout()
        layout_ventana.setContentsMargins(0, 0, 0, 0)
        layout_ventana.addWidget(scroll_area)
        
        self.setLayout(layout_ventana)
    
    def conectar_eventos(self):
        """Conecta los eventos de los widgets"""
        self.btn_login.clicked.connect(self.intentar_login)
        self.input_password.returnPressed.connect(self.intentar_login)
        self.input_usuario.returnPressed.connect(self.input_password.setFocus)
    
    def intentar_login(self):
        """Emite la señal para intentar hacer login"""
        usuario = self.input_usuario.text().strip()
        password = self.input_password.text().strip()
        
        if not usuario or not password:
            self.mostrar_error("Por favor, complete todos los campos")
            return
        
        # Emitir señal con las credenciales para que el controlador las valide
        self.validar_credenciales(usuario, password)
    
    def validar_credenciales(self, usuario, password):
        """Método que será conectado al controlador"""
        pass  # Este método será sobrescrito por el controlador
    
    def mostrar_error(self, mensaje):
        """Muestra un mensaje de error"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("⚠️ Error de Login")
        msg.setText(mensaje)
        msg.setStyleSheet(f"""
            QMessageBox {{
                background-color: {self.colors['surface']};
                font-family: Segoe UI, Arial, sans-serif;
                font-size: 14px;
            }}
            QMessageBox QPushButton {{
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                min-width: 80px;
                font-weight: bold;
            }}
            QMessageBox QPushButton:hover {{
                background-color: #c0392b;
            }}
        """)
        msg.exec()
    
    def mostrar_exito(self, tipo_usuario):
        """Muestra mensaje de éxito y emite señal"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("✅ Login Exitoso")
        msg.setText(f"¡Bienvenido, {tipo_usuario.capitalize()}! 🎉")
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
        
        # Emitir señal de login exitoso
        self.login_exitoso.emit(tipo_usuario)
    
    def limpiar_campos(self):
        """Limpia los campos de entrada"""
        self.input_usuario.clear()
        self.input_password.clear()
        self.input_usuario.setFocus()