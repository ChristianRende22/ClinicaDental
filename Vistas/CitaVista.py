# Importaciones necesarias para no tener porblema con los path o importaciones de clase
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit, QPushButton,
    QTextEdit, QGroupBox, QFormLayout, QMessageBox, QComboBox, QDateTimeEdit, QInputDialog, QScrollArea
)
from PyQt6.QtCore import Qt, QDateTime
from PyQt6.QtGui import QFont
from Controladores.CitaControlador import ControladorCita
from Controladores.DoctorControlador import Doctor
from Controladores.PacienteControlador import Paciente

class CitaWindow(QMainWindow):
    def __init__(self, doctores, pacientes, tratamientos):
        super().__init__()
        self.setWindowTitle("Gestión de Citas - Clínica Dental")
        self.setGeometry(100, 100, 900, 700)
        
        # Color scheme 
        self.colors = {
            'primary': '#130760',      # Dark blue-purple 
            'secondary': '#756f9f',    # Medium purple
            'accent': '#10b8b9',       # Teal
            'background': '#2b2b2b',   # Dark gray
            'surface': '#3c3c3c',      # Slightly lighter gray
            'text_light': '#ffffff',   # White text
            'text_dark': '#e0e0e0'     # Light gray text
        }

        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {self.colors['background']};
                font-family: 'Segoe UI';
                font-size: 14px;
                color: {self.colors['text_light']};
            }}
            
            QLabel {{
                color: {self.colors['text_light']};
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
                background-color: #404040;
            }}
            
            QPushButton {{
                font-family: 'Segoe UI';
                font-size: 14px;
                font-weight: bold;
                color: {self.colors['text_light']};
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
                background-color: #404040;
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
                background-color: #404040;
            }}
        """)

        self.controlador = ControladorCita(self)
        self.doctores = doctores
        self.pacientes = pacientes
        self.tratamientos = tratamientos
        self.citas = []

        self.editando_cita = None

        self.init_ui()

    def init_ui(self):
        """ Inicializa la interfaz de usuario de las Citas """
        # Creamos el widget central
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Título
        title = QLabel("🏥 Sistema de Gestión de Citas")
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

        # Información de la cita
        info_group = QGroupBox("Información de la Cita")
        info_layout = QFormLayout()

        self.id_edit = QLineEdit()
        self.paciente_combo = QComboBox()
        self.paciente_combo.addItems([f"{p.nombre} {p.apellido}" for p in self.pacientes])
        self.doctor_combo = QComboBox()

        for doctor in self.doctores:
            self.doctor_combo.addItem(str(doctor), doctor)  
        
        self.tratamiento_combo = QComboBox()
        self.tratamiento_combo.addItems([t['descripcion'] for t in self.tratamientos])

        self.fecha_inicio_edit = QDateTimeEdit(QDateTime.currentDateTime())
        self.fecha_inicio_edit.setDisplayFormat("dd/MM/yyyy HH:mm")
        self.fecha_fin_edit = QDateTimeEdit(QDateTime.currentDateTime())
        self.fecha_fin_edit.setDisplayFormat("dd/MM/yyyy HH:mm")
        self.costo_edit = QLineEdit()
        self.estado_combo = QComboBox()
        self.estado_combo.addItems(["Pendiente", "Confirmada", "Cancelada", "Asistida", "No asistió"])

        info_layout.addRow("ID Cita:", self.id_edit)
        info_layout.addRow("Paciente:", self.paciente_combo)
        info_layout.addRow("Doctor:", self.doctor_combo)
        info_layout.addRow("Tratamiento:", self.tratamiento_combo)
        info_layout.addRow("Fecha y Hora Inicio:", self.fecha_inicio_edit)
        info_layout.addRow("Fecha y Hora Fin:", self.fecha_fin_edit)
        info_layout.addRow("Costo:", self.costo_edit)
        info_layout.addRow("Estado:", self.estado_combo)

        info_group.setLayout(info_layout)
        main_layout.addWidget(info_group)

        # Botones
        # Primera fila de botones
        buttons_row1 = QHBoxLayout()
        self.crear_btn = QPushButton("➕ Crear Cita")
        self.crear_btn.clicked.connect(self.controlador.crear_cita)
        self.cancelar_btn = QPushButton("❌ Cancelar Cita")
        self.cancelar_btn.clicked.connect(self.controlador.cancelar_cita)
        self.modificar_btn = QPushButton("✏️ Modificar Cita")
        self.modificar_btn.clicked.connect(self.controlador.modificar_cita)

        buttons_row1.addWidget(self.crear_btn)
        buttons_row1.addWidget(self.cancelar_btn)
        buttons_row1.addWidget(self.modificar_btn)

        # Segunda fila de botones
        buttons_row2 = QHBoxLayout()
        self.confirmar_btn = QPushButton("✅ Confirmar Asistencia")
        self.confirmar_btn.clicked.connect(self.controlador.confirmar_asistencia)
        self.monto_btn = QPushButton("💲 Calcular Monto a Pagar")
        self.monto_btn.clicked.connect(self.controlador.calcular_monto)

        buttons_row2.addWidget(self.confirmar_btn)
        buttons_row2.addWidget(self.monto_btn)

        main_layout.addLayout(buttons_row1)
        main_layout.addLayout(buttons_row2)

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
                background-color: #1e1e1e;
                color: #d4d4d4;
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

        # Creamos el Scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(central_widget)
        self.setCentralWidget(scroll_area)


def main():
    # Simulacion para pruebas
    doctores = [
        Doctor("Melisa", "Rivas", "12345678-9", "Cirujano Dentista", 12345678, "correo@gmail.com"), 
        Doctor("Carlos", "López", "98765432-1", "Ortodontista", 87654321, "coreo1@gmail.com")
        ]
    pacientes = [
        Paciente("Juan", "Pérez", "06-12-05", "12345678-9", 12345567, "correo@gmail.com"), 
        Paciente("Ana", "Gomex", "07-31-07", "12345678-0", 12345678, "correo1@gmail.com")
        ]
    tratamientos = [{'descripcion': 'Limpieza', 'costo': 20.0}]
    app = QApplication([])
    window = CitaWindow(doctores, pacientes, tratamientos)
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
