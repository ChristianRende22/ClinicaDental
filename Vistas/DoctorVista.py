import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
                             QWidget, QLabel, QLineEdit, QPushButton, 
                             QTextEdit, QGroupBox, QFormLayout,
                             QDialog, QDialogButtonBox,
                             QScrollArea, QComboBox, QTimeEdit
                             )
from PyQt6.QtCore import Qt, QTime
from PyQt6.QtGui import QFont

from Controladores.DoctorControlador import ControladorDoctor

# class AgregarHorarioDialog(QDialog):
#     """
#     Diálogo para agregar un horario de atención del doctor.
#     Permite seleccionar el día de la semana y el rango de horas.
#     """
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setWindowTitle("⌚ Agregar Horario")        
#         self.setModal(True)
#         self.resize(450, 350)
#         self.setup_ui()
#         self.setup_styles()

#     def setup_ui(self):
#         """Configura la interfaz de usuario"""
#         # ComboBox para días de la semana
#         self.dia_combo = QComboBox()
#         self.dia_combo.addItems([
#             "Lunes", "Martes", "Miércoles", "Jueves", 
#             "Viernes", "Sábado", "Domingo"
#         ])
        
#         # TimeEdit para horas
#         self.hora_inicio_edit = QTimeEdit()
#         self.hora_inicio_edit.setTime(QTime(8, 0))  # Default 8:00 AM
#         self.hora_inicio_edit.setDisplayFormat("HH:mm")
        
#         self.hora_fin_edit = QTimeEdit()
#         self.hora_fin_edit.setTime(QTime(17, 0))  # Default 5:00 PM
#         self.hora_fin_edit.setDisplayFormat("HH:mm")

#         # Layout del formulario
#         layout = QFormLayout()
#         layout.addRow("🗓️ Día:", self.dia_combo)
#         layout.addRow("⏰ Hora Inicio:", self.hora_inicio_edit)
#         layout.addRow("⏳ Hora Fin:", self.hora_fin_edit)

#         # Botones
#         buttons = QDialogButtonBox(
#             QDialogButtonBox.StandardButton.Ok | 
#             QDialogButtonBox.StandardButton.Cancel
#         )
#         buttons.accepted.connect(self.accept)
#         buttons.rejected.connect(self.reject)
        
#         # Layout principal
#         main_layout = QVBoxLayout()
#         main_layout.addLayout(layout)
#         main_layout.addWidget(buttons)
#         self.setLayout(main_layout)

#     def setup_styles(self):
#         """Configura los estilos CSS"""
#         self.setStyleSheet("""
#             QDialog {
#                 background-color: #2b2b2b;
#                 font-family: 'Segoe UI';
#                 font-size: 14px;
#                 color: #ffffff;
#             }
            
#             QLabel {
#                 color: #ffffff;
#                 font-family: 'Segoe UI';
#                 font-size: 14px;
#                 font-weight: bold;
#             }
            
#             QComboBox, QTimeEdit {
#                 font-family: 'Segoe UI';
#                 font-size: 14px;
#                 border: 2px solid #756f9f;
#                 border-radius: 6px;
#                 padding: 8px;
#                 background-color: #3c3c3c;
#                 color: #ffffff;
#             }
            
#             QComboBox:focus, QTimeEdit:focus {
#                 border-color: #10b8b9;
#                 background-color: #404040;
#             }
            
#             QPushButton {
#                 font-family: 'Segoe UI';
#                 font-size: 14px;
#                 font-weight: bold;
#                 color: #ffffff;
#                 background-color: #756f9f;
#                 border: none;
#                 border-radius: 8px;
#                 padding: 10px 15px;
#             }
            
#             QPushButton:hover {
#                 background-color: #10b8b9;
#             }
#         """)

#     def get_horario_data(self):
#         """Devuelve los datos del horario ingresado"""
#         return {
#             'dia': self.dia_combo.currentText(),
#             'hora_inicio': self.hora_inicio_edit.time().toString("HH:mm"),
#             'hora_fin': self.hora_fin_edit.time().toString("HH:mm")
#         }

class DoctorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Doctores - Clínica Dental")
        self.setGeometry(100, 100, 800, 600)

        # Color scheme 
        self.colors = {
            'primary': '#130760',      # Dark blue-purple 
            'secondary': '#756f9f',    # Medium purple
            'accent': '#10b8b9',       # Teal
            'text_light': '#2b2b2b',   # Dark gray
            'text_dark': '#3c3c3c',      # Slightly lighter gray
            'background': '#f7f8fa',   # White text
            'surface': '#ffffff'     # Light gray text
        }

        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {self.colors['background']};
                font-family: 'Segoe UI';
                font-size: 14px;
                color: {self.colors['text_light']};
            }}

            QWidget {{
                background-color: {self.colors['background']};
            }}
            
            QLabel {{
                color: {self.colors['text_light']};
                background-color: {self.colors['surface']};
                font-family: 'Segoe UI';
                font-size: 14px;
            }}
            
            QGroupBox {{
                font-family: 'Segoe UI';
                font-size: 14px;
                font-weight: bold;
                color: {self.colors['text_light']};
                border: 2px solid {self.colors['secondary']};
                border-radius: 8px;
                margin: 10px 0px;
                padding-top: 15px;
                background-color: {self.colors['surface']};
            }}
            
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
                background-color: {self.colors['surface']};
                color: {self.colors['accent']};
            }}
            
            QLineEdit, QSpinBox, QDoubleSpinBox {{
                font-family: 'Segoe UI';
                font-size: 14px;
                border: 2px solid {self.colors['secondary']};
                border-radius: 6px;
                padding: 10px;
                background-color: {self.colors['surface']};
                color: {self.colors['text_light']};
                selection-background-color: {self.colors['accent']};
            }}
            
            QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {{
                border-color: {self.colors['accent']};
                background-color: {self.colors['surface']};
            }}
            
            QPushButton {{
                font-family: 'Segoe UI';
                font-size: 14px;
                font-weight: bold;
                color: {self.colors['surface']};
                background-color: {self.colors['secondary']};
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
                margin: 4px;
            }}
            
            QPushButton:hover {{
                background-color: {self.colors['accent']};
                
            }}
            
            QPushButton:pressed {{
                background-color: {self.colors['primary']};
            }}
            
            QTextEdit {{
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 13px;
                border: 2px solid {self.colors['secondary']};
                border-radius: 8px;
                background-color: {self.colors['surface']};
                color: {self.colors['text_dark']};
                padding: 15px;
                selection-background-color: {self.colors['accent']};
            }}
            
            QTextEdit:focus {{
                border-color: {self.colors['accent']};
            }}
            
            QComboBox {{
                font-family: 'Segoe UI';
                font-size: 14px;
                border: 2px solid {self.colors['secondary']};
                border-radius: 6px;
                padding: 10px;
                background-color: {self.colors['surface']};
                color: {self.colors['text_light']};
                selection-background-color: {self.colors['accent']};
            }}

            QComboBox:focus {{
                border-color: {self.colors['accent']};
                background-color: {self.colors['surface']};
            }}
            

            QComboBox QAbstractItemView {{
                background-color: {self.colors['surface']};
                color: {self.colors['text_dark']};
                border: 2px solid {self.colors['secondary']};
                border-radius: 6px;
                padding: 5px;
                selection-background-color: {self.colors['accent']};
                selection-color: white;
                outline: none;
            }}
            
            QComboBox QAbstractItemView::item {{
                padding: 8px;
                color: {self.colors['text_dark']};
                background-color: {self.colors['surface']};
                border: none;
            }}
            
            QComboBox QAbstractItemView::item:hover {{
                background-color: {self.colors['accent']};
                color: white;
            }}
            
            QComboBox QAbstractItemView::item:selected {{
                background-color: {self.colors['accent']};
                color: white;
            }}

            QDateTimeEdit {{
                font-family: 'Segoe UI';
                font-size: 14px;
                border: 2px solid {self.colors['secondary']};
                border-radius: 6px;
                padding: 10px;
                background-color: {self.colors['surface']};
                color: {self.colors['text_light']};
                selection-background-color: {self.colors['accent']};
            }}
            QDateTimeEdit:focus {{
                border-color: {self.colors['accent']};
                background-color: {self.colors['surface']};
            }}
        """)

        # PRIMERo: Crear la interfaz (sin conexiones)
        self.init_ui()

        # SEGUNDO: Crear el controlador
        self.controlador = ControladorDoctor(self)

        # TERCERO: Conectar los botones a las funciones del controlador
        self.conectar_botones()
    
    def init_ui(self):
        """Inicializa la interfaz de usuario del Doctor"""
        # Creamos el widget central real
        central_widget = QWidget()
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Creamos el scroll 
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(central_widget)
        self.setCentralWidget(scroll_area)

        # Título con estilo mejorado
        title = QLabel("🏥 Sistema de Gestión de Doctor")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setStyleSheet(f"""
            QLabel {{
                color: {self.colors['text_light']};
                background-color: {self.colors['surface']};
                border: 3px solid {self.colors['accent']};
                border-radius: 12px;
                padding: 20px;
                margin: 10px;
            }}
        """)
        main_layout.addWidget(title)
        
        # Información del paciente
        info_group = QGroupBox("Información del Doctor")
        info_layout = QFormLayout()
        
        self.dui_edit = QLineEdit()
        self.nombre_edit = QLineEdit()
        self.apellido_edit = QLineEdit()
        self.especialidad_edit = QLineEdit()
        self.telefono_edit = QLineEdit()
        self.correo_edit = QLineEdit()

        
        info_layout.addRow("DUI:", self.dui_edit)
        info_layout.addRow("Nombre:", self.nombre_edit)
        info_layout.addRow("Apellido:", self.apellido_edit)
        info_layout.addRow("Especialidad:", self.especialidad_edit)
        info_layout.addRow("Teléfono:", self.telefono_edit)
        info_layout.addRow("Correo:", self.correo_edit)
        
        info_group.setLayout(info_layout)
        main_layout.addWidget(info_group)
        
        # Botones de acción con iconos
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        # Primera fila de botones
        buttons_row1 = QHBoxLayout()
        buttons_row1.setSpacing(10)
        
        self.crear_btn = QPushButton("👤 Crear Doctor")
        self.agregar_horario_btn = QPushButton("🩺 Agregar Horario")
        self.ver_cita_btn = QPushButton("📅 Ver Citas")
        
        buttons_row1.addWidget(self.crear_btn)
        buttons_row1.addWidget(self.agregar_horario_btn)
        buttons_row1.addWidget(self.ver_cita_btn)
        
        # Segunda fila de botones
        buttons_row2 = QHBoxLayout()
        buttons_row2.setSpacing(10)
        
        self.mostrar_info_btn = QPushButton("ℹ️ Mostrar listado de doctores")
        self.suprimir_doctor_btn = QPushButton("📋 Suprimir Doctor")
        self.actualizar_info_doctor_btn = QPushButton("📚 Actualizar Info Doctor")
        
        buttons_row2.addWidget(self.mostrar_info_btn)
        buttons_row2.addWidget(self.suprimir_doctor_btn)
        buttons_row2.addWidget(self.actualizar_info_doctor_btn)
        
        # Tercer fila de botones 
        buttons_row3 = QHBoxLayout()
        buttons_row3.setSpacing(10)

        self.registrar_diagnostico_btn = QPushButton("📝 Registrar Diagnóstico")
        buttons_row3.addWidget(self.registrar_diagnostico_btn)

        # Layout vertical para las filas de botones
        buttons_container = QVBoxLayout()
        buttons_container.addLayout(buttons_row1)
        buttons_container.addLayout(buttons_row2)
        buttons_container.addLayout(buttons_row3)
        
        main_layout.addLayout(buttons_container)
        
        # Área de resultados con estilo mejorado y scroll bar
        resultado_label = QLabel("📊 Resultados:")
        resultado_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        resultado_label.setStyleSheet(f"color: {self.colors['accent']};")
        main_layout.addWidget(resultado_label)
        
        self.resultado_text = QTextEdit()
        self.resultado_text.setReadOnly(True)
        self.resultado_text.setFont(QFont("Consolas", 13))
        self.resultado_text.setPlaceholderText("Aquí aparecerán los resultados de las operaciones...")
        
        # Configurar scroll bars con estilo
        self.resultado_text.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.resultado_text.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Estilo mejorado para el área de texto y scroll bars
        self.resultado_text.setStyleSheet(f"""
            QTextEdit {{
                background-color: {self.colors['surface']};
                color: {self.colors['text_dark']};
                border: 2px solid {self.colors['secondary']};
                border-radius: 8px;
                padding: 15px;
            }}
            
            QScrollBar:vertical {{
                background-color: #3c3c3c;
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
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                border: none;
                background: none;
                height: 0px;
            }}
            
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: none;
            }}
            
            QScrollBar:horizontal {{
                background-color: #3c3c3c;
                height: 12px;
                border-radius: 6px;
                margin: 0px;
            }}
            
            QScrollBar::handle:horizontal {{
                background-color: {self.colors['secondary']};
                border-radius: 6px;
                min-width: 20px;
                margin: 2px;
            }}
            
            QScrollBar::handle:horizontal:hover {{
                background-color: {self.colors['accent']};
            }}
            
            QScrollBar::handle:horizontal:pressed {{
                background-color: {self.colors['primary']};
            }}
            
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                border: none;
                background: none;
                width: 0px;
            }}
            
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
                background: none;
            }}
        """)
        
        # Configurar el comportamiento del scroll
        self.resultado_text.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        self.resultado_text.setMinimumHeight(200)
        
        main_layout.addWidget(self.resultado_text)

    def conectar_botones(self):
        """Conecta los botones a las funciones del controlador"""
        self.crear_btn.clicked.connect(self.controlador.crear_doctor)
        self.agregar_horario_btn.clicked.connect(self.controlador.agregar_horario)
        self.ver_cita_btn.clicked.connect(self.controlador.ver_citas)
        self.mostrar_info_btn.clicked.connect(self.controlador.mostrar_info_doctor)
        self.suprimir_doctor_btn.clicked.connect(self.controlador.suprimir_doctor)
        self.actualizar_info_doctor_btn.clicked.connect(self.controlador.actualizar_info_doctor)
        # self.registrar_diagnostico_btn.clicked.connect(self.controlador.registrar_diagnostico)
    


def main():
    
    app = QApplication([])
    window = DoctorWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
