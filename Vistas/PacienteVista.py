
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QLabel, QLineEdit, QSpinBox, QPushButton, 
                             QTextEdit, QGroupBox, QFormLayout, QMessageBox,
                             QListWidget, QDialog, QDialogButtonBox, QDoubleSpinBox,
                             QScrollArea, QScrollBar)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from datetime import datetime
from typing import List
import re

# Clases auxiliares (Lo puse para que no se pierda el contexto)
class Doctor:
    def __init__(self, nombre: str, apellido: str):
        self.nombre = nombre
        self.apellido = apellido

class Tratamiento:
    def __init__(self, id_tratamiento: str, descripcion: str, costo: float, 
                 fecha_realizacion: str, estado: str, doctor: Doctor):
        self.id_tratamiento = id_tratamiento
        self.descripcion = descripcion
        self.costo = costo
        self.fecha_realizacion = fecha_realizacion
        self.estado = estado
        self.doctor = doctor

class Cita:
    def __init__(self, id_cita: str, hora_inicio: str, hora_fin: str, 
                 costo_cita: float, estado: str, doctor: Doctor):
        self.id_cita = id_cita
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.costo_cita = costo_cita
        self.estado = estado
        self.doctor = doctor

class AgregarTratamientoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🩺 Agregar Tratamiento")
        self.setModal(True)
        self.resize(450, 350)
        
       
        self.setStyleSheet(f"""
            QDialog {{
                background-color: #2b2b2b;
                font-family: 'Segoe UI';
                font-size: 14px;
                color: #ffffff;
            }}
            
            QLabel {{
                color: #ffffff;
                font-family: 'Segoe UI';
                font-size: 14px;
                font-weight: bold;
            }}
            
            QLineEdit, QTextEdit, QDoubleSpinBox {{
                font-family: 'Segoe UI';
                font-size: 14px;
                border: 2px solid #756f9f;
                border-radius: 6px;
                padding: 8px;
                background-color: #3c3c3c;
                color: #ffffff;
            }}
            
            QLineEdit:focus, QTextEdit:focus, QDoubleSpinBox:focus {{
                border-color: #10b8b9;
                background-color: #404040;
            }}
            
            QPushButton {{
                font-family: 'Segoe UI';
                font-size: 14px;
                font-weight: bold;
                color: #ffffff;
                background-color: #756f9f;
                border: none;
                border-radius: 8px;
                padding: 10px 15px;
            }}
            
            QPushButton:hover {{
                background-color: #10b8b9;
            }}
        """)
        
        layout = QFormLayout()
        
        self.id_edit = QLineEdit()
        self.descripcion_edit = QTextEdit()
        self.descripcion_edit.setMaximumHeight(80)
        self.costo_edit = QDoubleSpinBox()
        self.costo_edit.setMaximum(99999.99)
        self.costo_edit.setPrefix("$")
        self.fecha_edit = QLineEdit()
        self.fecha_edit.setPlaceholderText("DD/MM/YYYY")
        self.estado_edit = QLineEdit()
        self.doctor_nombre_edit = QLineEdit()
        self.doctor_apellido_edit = QLineEdit()
        
        layout.addRow("ID Tratamiento:", self.id_edit)
        layout.addRow("Descripción:", self.descripcion_edit)
        layout.addRow("Costo:", self.costo_edit)
        layout.addRow("Fecha:", self.fecha_edit)
        layout.addRow("Estado:", self.estado_edit)
        layout.addRow("Nombre Doctor:", self.doctor_nombre_edit)
        layout.addRow("Apellido Doctor:", self.doctor_apellido_edit)
        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | 
                                 QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addWidget(buttons)
        self.setLayout(main_layout)
    
    def get_tratamiento(self):
        doctor = Doctor(self.doctor_nombre_edit.text(), self.doctor_apellido_edit.text())
        return Tratamiento(
            self.id_edit.text(),
            self.descripcion_edit.toPlainText(),
            self.costo_edit.value(),
            self.fecha_edit.text(),
            self.estado_edit.text(),
            doctor
        )

class AgregarCitaDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("📅 Agregar Cita")
        self.setModal(True)
        self.resize(450, 300)
        
      
        self.setStyleSheet(f"""
            QDialog {{
                background-color: #2b2b2b;
                font-family: 'Segoe UI';
                font-size: 14px;
                color: #ffffff;
            }}
            
            QLabel {{
                color: #ffffff;
                font-family: 'Segoe UI';
                font-size: 14px;
                font-weight: bold;
            }}
            
            QLineEdit, QDoubleSpinBox {{
                font-family: 'Segoe UI';
                font-size: 14px;
                border: 2px solid #756f9f;
                border-radius: 6px;
                padding: 8px;
                background-color: #3c3c3c;
                color: #ffffff;
            }}
            
            QLineEdit:focus, QDoubleSpinBox:focus {{
                border-color: #10b8b9;
                background-color: #404040;
            }}
            
            QPushButton {{
                font-family: 'Segoe UI';
                font-size: 14px;
                font-weight: bold;
                color: #ffffff;
                background-color: #756f9f;
                border: none;
                border-radius: 8px;
                padding: 10px 15px;
            }}
            
            QPushButton:hover {{
                background-color: #10b8b9;
            }}
        """)
        
        layout = QFormLayout()
        
        self.id_edit = QLineEdit()
        self.hora_inicio_edit = QLineEdit()
        self.hora_inicio_edit.setPlaceholderText("DD/MM/YYYY HH:MM")
        self.hora_fin_edit = QLineEdit()
        self.hora_fin_edit.setPlaceholderText("DD/MM/YYYY HH:MM")
        self.costo_edit = QDoubleSpinBox()
        self.costo_edit.setMaximum(99999.99)
        self.costo_edit.setPrefix("$")
        self.estado_edit = QLineEdit()
        self.doctor_nombre_edit = QLineEdit()
        self.doctor_apellido_edit = QLineEdit()
        
        layout.addRow("ID Cita:", self.id_edit)
        layout.addRow("Hora Inicio:", self.hora_inicio_edit)
        layout.addRow("Hora Fin:", self.hora_fin_edit)
        layout.addRow("Costo:", self.costo_edit)
        layout.addRow("Estado:", self.estado_edit)
        layout.addRow("Nombre Doctor:", self.doctor_nombre_edit)
        layout.addRow("Apellido Doctor:", self.doctor_apellido_edit)
        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | 
                                 QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addWidget(buttons)
        self.setLayout(main_layout)
    
    def get_cita(self):
        doctor = Doctor(self.doctor_nombre_edit.text(), self.doctor_apellido_edit.text())
        return Cita(
            self.id_edit.text(),
            self.hora_inicio_edit.text(),
            self.hora_fin_edit.text(),
            self.costo_edit.value(),
            self.estado_edit.text(),
            doctor
        )

# CLASE PACIENTE
class Paciente:
    def __init__(self, nombre, apellido, fecha_nacimiento, dui, telefono, correo):
        self.nombre = nombre
        self.apellido = apellido
        self.fecha_nacimiento = fecha_nacimiento  # Cambiado a fecha de nacimiento
        self.dui = dui
        self.telefono = telefono
        self.correo = correo

class PacienteWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Pacientes - Clínica Dental")
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
        """)
        
        
        # Atributos del paciente actual
        # CREAR LA CLASE PACIENTE
        self.nombre = ""
        self.apellido = ""
        self.edad = 0 # CAMBIAR A FECHA DE NACIMIENTO PARA HACER COHERENCIA CON LA BASE DE DATOS
        self.dui = "" 
        self.telefono = 0
        self.correo = ""
        self.historial_medico: List[Tratamiento] = [] #QUERY
        self.citas: List[Cita] = [] # QUERY
        self.saldo_pendiente = 0.0 # POR MEDIO DEL JOIN DE TRATAMIENTO SE HACE LA CONSULTA PARA CALCULAR EL SALDO PENDIENTE
        
        # Nueva lista para almacenar todos los pacientes registrados
        self.pacientes_registrados = [] # INSERT INTO pacientes (nombre, apellido, edad, dui, telefono, correo, saldo_pendiente, fecha_registro)
        
        self.init_ui()
    
    def init_ui(self):
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
        title = QLabel("🏥 Sistema de Gestión de Pacientes")
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
        info_group = QGroupBox("Información del Paciente")
        info_layout = QFormLayout()
        
        self.nombre_edit = QLineEdit()
        self.apellido_edit = QLineEdit()
        self.edad_edit = QSpinBox()
        self.edad_edit.setRange(0, 120)
        self.dui_edit = QLineEdit()
        self.telefono_edit = QLineEdit()
        self.correo_edit = QLineEdit()
        self.saldo_edit = QDoubleSpinBox()
        self.saldo_edit.setPrefix("$")
        self.saldo_edit.setMaximum(99999.99)
        
        info_layout.addRow("Nombre:", self.nombre_edit)
        info_layout.addRow("Apellido:", self.apellido_edit)
        info_layout.addRow("Edad:", self.edad_edit)
        info_layout.addRow("DUI:", self.dui_edit)
        info_layout.addRow("Teléfono:", self.telefono_edit)
        info_layout.addRow("Correo:", self.correo_edit)
        info_layout.addRow("Saldo Pendiente:", self.saldo_edit)
        
        info_group.setLayout(info_layout)
        main_layout.addWidget(info_group)
        
        # Botones de acción con iconos
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        # Primera fila de botones
        buttons_row1 = QHBoxLayout()
        buttons_row1.setSpacing(10)
        
        self.crear_btn = QPushButton("👤 Crear Paciente")
        self.crear_btn.clicked.connect(self.crear_paciente)
        self.crear_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.colors['accent']};
                min-height: 45px;
            }}
            QPushButton:hover {{
                background-color: {self.colors['secondary']};
            }}
        """)
        
        self.agregar_tratamiento_btn = QPushButton("🩺 Agregar Tratamiento")
        self.agregar_tratamiento_btn.clicked.connect(self.agregar_tratamiento)
        
        self.agregar_cita_btn = QPushButton("📅 Agregar Cita")
        self.agregar_cita_btn.clicked.connect(self.agregar_cita)
        
        buttons_row1.addWidget(self.crear_btn)
        buttons_row1.addWidget(self.agregar_tratamiento_btn)
        buttons_row1.addWidget(self.agregar_cita_btn)
        
        # Segunda fila de botones
        buttons_row2 = QHBoxLayout()
        buttons_row2.setSpacing(10)
        
        self.consultar_historial_btn = QPushButton("📋 Consultar Historial")
        self.consultar_historial_btn.clicked.connect(self.consultar_historial)
        
        self.mostrar_info_btn = QPushButton("ℹ️ Mostrar Info Paciente")
        self.mostrar_info_btn.clicked.connect(self.mostrar_info_paciente)
        
        # Botón para mostrar todos los historiales
        self.mostrar_todos_btn = QPushButton("📚 Todos los Historiales")
        self.mostrar_todos_btn.clicked.connect(self.mostrar_todos_historiales)
        self.mostrar_todos_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #9b59b6;
                min-height: 45px;
            }}
            QPushButton:hover {{
                background-color: #8e44ad;
            }}
        """)
        
        buttons_row2.addWidget(self.consultar_historial_btn)
        buttons_row2.addWidget(self.mostrar_info_btn)
        buttons_row2.addWidget(self.mostrar_todos_btn)
        
        # Layout vertical para las filas de botones
        buttons_container = QVBoxLayout()
        buttons_container.addLayout(buttons_row1)
        buttons_container.addLayout(buttons_row2)
        
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
    
    def validar_email(self, email: str) -> bool:
        """Valida el formato del email"""
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(patron, email) is not None
    
    def validar_dui(self, dui: str) -> bool:
        """Valida el formato del DUI (########-#)"""
        patron = r'^\d{8}-\d{1}$'
        return re.match(patron, dui) is not None
    
    def validar_telefono(self, telefono: str) -> bool:
        """Valida que el teléfono tenga al menos 8 dígitos"""
        return telefono.isdigit() and len(telefono) >= 8
    
    def limpiar_campos(self):
        """Limpia todos los campos de entrada para agregar un nuevo paciente"""
        self.nombre_edit.clear()
        self.apellido_edit.clear()
        self.edad_edit.setValue(0)
        self.dui_edit.clear()
        self.telefono_edit.clear()
        self.correo_edit.clear()
        self.saldo_edit.setValue(0.0)
        
        # Enfocar el primer campo para facilitar la entrada
        self.nombre_edit.setFocus()
    
    def crear_paciente(self):
        """Crea un nuevo paciente con los datos ingresados"""
        try:
            nombre = self.nombre_edit.text().strip().title()
            apellido = self.apellido_edit.text().strip().title()
            edad = self.edad_edit.value()
            dui = self.dui_edit.text().strip()
            telefono_str = self.telefono_edit.text().strip()
            correo = self.correo_edit.text().strip().lower()
            saldo_pendiente = self.saldo_edit.value()
            
            # Validaciones básicas
            if not all([nombre, apellido, dui]):
                QMessageBox.warning(self, "❌ Error", "Nombre, Apellido y DUI son campos obligatorios")
                return
            
            # Validación DUI
            if not self.validar_dui(dui):
                QMessageBox.warning(self, "❌ Error de Formato", 
                                  "El DUI debe tener el formato: 12345678-9")
                return
            
            # Verificar si ya existe un paciente con el mismo DUI
            for paciente in self.pacientes_registrados:
                if paciente['dui'] == dui:
                    QMessageBox.warning(self, "❌ Error", 
                                      f"Ya existe un paciente registrado con el DUI: {dui}")
                    return
            
            # Validación teléfono
            if telefono_str and not self.validar_telefono(telefono_str):
                QMessageBox.warning(self, "❌ Error de Formato", 
                                  "El teléfono debe contener al menos 8 dígitos")
                return
            
            telefono = int(telefono_str) if telefono_str else 0
            
            # Validación email
            if correo and not self.validar_email(correo):
                QMessageBox.warning(self, "❌ Error de Formato", 
                                  "El email no tiene un formato válido")
                return
            
            # Validación edad
            if edad <= 0:
                QMessageBox.warning(self, "❌ Error", "La edad debe ser mayor a 0")
                return
            
            # Crear datos del nuevo paciente
            nuevo_paciente = {
                'nombre': nombre,
                'apellido': apellido,
                'edad': edad,
                'dui': dui,
                'telefono': telefono,
                'correo': correo,
                'saldo_pendiente': saldo_pendiente,
                'historial_medico': [],
                'citas': [],
                'fecha_registro': datetime.now().strftime('%d/%m/%Y - %H:%M:%S')
            }
            
            # Agregar a la lista de pacientes registrados
            self.pacientes_registrados.append(nuevo_paciente)
            
            # Establecer como paciente actual
            self.nombre = nombre
            self.apellido = apellido
            self.edad = edad
            self.dui = dui
            self.telefono = telefono
            self.correo = correo
            self.saldo_pendiente = saldo_pendiente
            self.historial_medico = []
            self.citas = []
            
            # Mostrar mensaje de éxito
            QMessageBox.information(self, "✅ Éxito", 
                                  f"Paciente {nombre} {apellido} creado exitosamente.\n\n"
                                  f"Total de pacientes registrados: {len(self.pacientes_registrados)}")
            
            # Mostrar información del paciente creado
            self.resultado_text.setText(self._generar_info_completa())
            
            # Limpiar campos automáticamente para el siguiente paciente
            self.limpiar_campos()
            
        except ValueError as e:
            QMessageBox.warning(self, "❌ Error", f"Error en el formato de los datos: {str(e)}")
    
    def mostrar_todos_historiales(self):
        """Muestra todos los historiales de los pacientes registrados"""
        if not self.pacientes_registrados:
            QMessageBox.information(self, "ℹ️ Información", 
                                  "No hay pacientes registrados en el sistema.")
            return
        
        historial_completo = self._generar_historial_todos_pacientes()
        self.resultado_text.setText(historial_completo)
    
    def _generar_historial_todos_pacientes(self) -> str:
        """Genera el historial de todos los pacientes registrados"""
        separador_principal = "=" * 80
        separador_paciente = "-" * 60
        
        historial = f"""
{separador_principal}
🏥 HISTORIALES MÉDICOS COMPLETOS - CLÍNICA DENTAL
{separador_principal}

📊 RESUMEN GENERAL:
   ▪ Total de Pacientes Registrados: {len(self.pacientes_registrados)}
   ▪ Fecha de Consulta: {datetime.now().strftime('%d/%m/%Y - %H:%M:%S')}

{separador_principal}
"""
        
        # Mostrar cada paciente
        for i, paciente in enumerate(self.pacientes_registrados, 1):
            total_tratamientos = sum(t.costo for t in paciente['historial_medico'])
            total_citas = sum(c.costo_cita for c in paciente['citas'])
            
            historial += f"""
{separador_paciente}
👤 PACIENTE #{i:02d}: {paciente['nombre']} {paciente['apellido']}
{separador_paciente}

📋 INFORMACIÓN PERSONAL:
   ▪ Nombre Completo: {paciente['nombre']} {paciente['apellido']}
   ▪ Edad: {paciente['edad']} años
   ▪ DUI: {paciente['dui']}
   ▪ Teléfono: {self._formatear_telefono_static(paciente['telefono'])}
   ▪ Correo: {paciente['correo'] if paciente['correo'] else 'No especificado'}
   ▪ Fecha de Registro: {paciente['fecha_registro']}

💰 INFORMACIÓN FINANCIERA:
   ▪ Saldo Pendiente: ${paciente['saldo_pendiente']:,.2f}
   ▪ Total Tratamientos: ${total_tratamientos:,.2f}
   ▪ Total Citas: ${total_citas:,.2f}
   ▪ Balance Total: ${(total_tratamientos + total_citas + paciente['saldo_pendiente']):,.2f}

🩺 TRATAMIENTOS ({len(paciente['historial_medico'])}):
"""
            
            if not paciente['historial_medico']:
                historial += "   📝 No hay tratamientos registrados.\n"
            else:
                for j, tratamiento in enumerate(paciente['historial_medico'], 1):
                    estado_icon = self._get_estado_icon(tratamiento.estado)
                    historial += f"""   {j}. {tratamiento.descripcion}
      💵 ${tratamiento.costo:,.2f} | 📅 {tratamiento.fecha_realizacion}
      {estado_icon} {tratamiento.estado} | 👨‍⚕️ Dr. {tratamiento.doctor.nombre} {tratamiento.doctor.apellido}
"""
            
            historial += f"""
📅 CITAS ({len(paciente['citas'])}):
"""
            
            if not paciente['citas']:
                historial += "   📝 No hay citas programadas.\n"
            else:
                for j, cita in enumerate(paciente['citas'], 1):
                    estado_icon = self._get_estado_icon(cita.estado)
                    historial += f"""   {j}. ID: {cita.id_cita}
      ⏰ {cita.hora_inicio} - {cita.hora_fin}
      💵 ${cita.costo_cita:,.2f} | {estado_icon} {cita.estado}
      👨‍⚕️ Dr. {cita.doctor.nombre} {cita.doctor.apellido}
"""
            
            historial += "\n"
        
        # Resumen general
        total_pacientes = len(self.pacientes_registrados)
        total_tratamientos_general = sum(len(p['historial_medico']) for p in self.pacientes_registrados)
        total_citas_general = sum(len(p['citas']) for p in self.pacientes_registrados)
        total_dinero_tratamientos = sum(sum(t.costo for t in p['historial_medico']) for p in self.pacientes_registrados)
        total_dinero_citas = sum(sum(c.costo_cita for c in p['citas']) for p in self.pacientes_registrados)
        total_saldos_pendientes = sum(p['saldo_pendiente'] for p in self.pacientes_registrados)
        
        historial += f"""
{separador_principal}
📈 ESTADÍSTICAS GENERALES DE LA CLÍNICA
{separador_principal}

👥 PACIENTES:
   ▪ Total de Pacientes: {total_pacientes}
   
🩺 TRATAMIENTOS:
   ▪ Total de Tratamientos: {total_tratamientos_general}
   ▪ Ingresos por Tratamientos: ${total_dinero_tratamientos:,.2f}
   
📅 CITAS:
   ▪ Total de Citas: {total_citas_general}
   ▪ Ingresos por Citas: ${total_dinero_citas:,.2f}
   
💰 FINANCIERO:
   ▪ Saldos Pendientes: ${total_saldos_pendientes:,.2f}
   ▪ Ingresos Totales: ${(total_dinero_tratamientos + total_dinero_citas):,.2f}
   ▪ Balance General: ${(total_dinero_tratamientos + total_dinero_citas + total_saldos_pendientes):,.2f}

{separador_principal}
"""
        return historial
    
    def _formatear_telefono_static(self, telefono: int) -> str:
        """Formatea el número de teléfono para mejor presentación (versión estática)"""
        if telefono == 0:
            return "No especificado"
        
        telefono_str = str(telefono)
        if len(telefono_str) == 8:
            return f"{telefono_str[:4]}-{telefono_str[4:]}"
        elif len(telefono_str) >= 8:
            return f"+503 {telefono_str[-8:-4]}-{telefono_str[-4:]}"
        return telefono_str
    
    def agregar_tratamiento(self):
        """Abre un diálogo para agregar un tratamiento"""
        if not self.nombre:
            QMessageBox.warning(self, "❌ Error", "Debe crear un paciente primero")
            return
        
        dialog = AgregarTratamientoDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            tratamiento = dialog.get_tratamiento()
            self.historial_medico.append(tratamiento)
            
            # Actualizar también en la lista de pacientes registrados
            for paciente in self.pacientes_registrados:
                if paciente['dui'] == self.dui:
                    paciente['historial_medico'].append(tratamiento)
                    break
            
            QMessageBox.information(self, "✅ Éxito", "Tratamiento agregado exitosamente")
    
    def agregar_cita(self):
        """Abre un diálogo para agregar una cita"""
        if not self.nombre:
            QMessageBox.warning(self, "❌ Error", "Debe crear un paciente primero")
            return
        
        dialog = AgregarCitaDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            cita = dialog.get_cita()
            self.citas.append(cita)
            
            # Actualizar también en la lista de pacientes registrados
            for paciente in self.pacientes_registrados:
                if paciente['dui'] == self.dui:
                    paciente['citas'].append(cita)
                    break
            
            QMessageBox.information(self, "✅ Éxito", "Cita agregada exitosamente")
    
    def consultar_historial(self):
        """Consulta y muestra el historial médico del paciente"""
        if not self.nombre:
            QMessageBox.warning(self, "❌ Error", "Debe crear un paciente primero")
            return
        
        historial = self._generar_historial_detallado()
        self.resultado_text.setText(historial)
    
    def mostrar_info_paciente(self):
        """Muestra la información básica del paciente"""
        if not self.nombre:
            QMessageBox.warning(self, "❌ Error", "Debe crear un paciente primero")
            return
        
        self.resultado_text.setText(self._generar_info_completa())
    
    def _generar_info_completa(self) -> str:
        """Genera la información completa del paciente con formato mejorado"""
        separador = "=" * 60
        info = f"""
{separador}
🏥 INFORMACIÓN DEL PACIENTE - CLÍNICA DENTAL
{separador}

👤 DATOS PERSONALES:
   ▪ Nombre Completo: {self.nombre} {self.apellido}
   ▪ Edad: {self.edad} años
   ▪ DUI: {self.dui}
   ▪ Teléfono: {self._formatear_telefono()}
   ▪ Correo Electrónico: {self.correo if self.correo else 'No especificado'}

💰 INFORMACIÓN FINANCIERA:
   ▪ Saldo Pendiente: ${self.saldo_pendiente:,.2f}
   ▪ Estado: {'🔴 Pendiente de pago' if self.saldo_pendiente > 0 else '🟢 Al día'}

📊 RESUMEN MÉDICO:
   ▪ Tratamientos Realizados: {len(self.historial_medico)}
   ▪ Citas Agendadas: {len(self.citas)}
   ▪ Costo Total Tratamientos: ${self._calcular_total_tratamientos():,.2f}
   ▪ Costo Total Citas: ${self._calcular_total_citas():,.2f}

⏰ Última Actualización: {datetime.now().strftime('%d/%m/%Y - %H:%M:%S')}
{separador}
"""
        return info
    
    def _generar_historial_detallado(self) -> str:
        """Genera el historial médico detallado con formato mejorado"""
        separador_principal = "=" * 60
        separador_seccion = "-" * 40
        
        historial = f"""
{separador_principal}
📋 HISTORIAL MÉDICO COMPLETO
{separador_principal}

👤 Paciente: {self.nombre} {self.apellido}
📅 Fecha de Consulta: {datetime.now().strftime('%d/%m/%Y - %H:%M:%S')}

{separador_seccion}
🩺 TRATAMIENTOS REALIZADOS ({len(self.historial_medico)})
{separador_seccion}
"""
        
        if not self.historial_medico:
            historial += "\n   📝 No hay tratamientos registrados en el historial.\n"
        else:
            for i, tratamiento in enumerate(self.historial_medico, 1):
                estado_icon = self._get_estado_icon(tratamiento.estado)
                historial += f"""
   ┌─ Tratamiento #{i:02d}
   │ 🆔 ID: {tratamiento.id_tratamiento}
   │ 📄 Descripción: {tratamiento.descripcion}
   │ 💵 Costo: ${tratamiento.costo:,.2f}
   │ 📅 Fecha: {tratamiento.fecha_realizacion}
   │ {estado_icon} Estado: {tratamiento.estado}
   │ 👨‍⚕️ Doctor: Dr. {tratamiento.doctor.nombre} {tratamiento.doctor.apellido}
   └─────────────────────────────────────────────────
"""
        
        historial += f"""
{separador_seccion}
📅 CITAS PROGRAMADAS ({len(self.citas)})
{separador_seccion}
"""
        
        if not self.citas:
            historial += "\n   📝 No hay citas programadas.\n"
        else:
            for i, cita in enumerate(self.citas, 1):
                estado_icon = self._get_estado_icon(cita.estado)
                historial += f"""
   ┌─ Cita #{i:02d}
   │ 🆔 ID: {cita.id_cita}
   │ ⏰ Inicio: {cita.hora_inicio}
   │ ⏰ Fin: {cita.hora_fin}
   │ 💵 Costo: ${cita.costo_cita:,.2f}
   │ {estado_icon} Estado: {cita.estado}
   │ 👨‍⚕️ Doctor: Dr. {cita.doctor.nombre} {cita.doctor.apellido}
   └─────────────────────────────────────────────────
"""
        
        # Resumen financiero
        total_tratamientos = self._calcular_total_tratamientos()
        total_citas = self._calcular_total_citas()
        total_general = total_tratamientos + total_citas
        
        historial += f"""
{separador_seccion}
💰 RESUMEN FINANCIERO
{separador_seccion}

   📊 Estadísticas:
   ▪ Total de Tratamientos: {len(self.historial_medico)} - ${total_tratamientos:,.2f}
   ▪ Total de Citas: {len(self.citas)} - ${total_citas:,.2f}
   ▪ Subtotal General: ${total_general:,.2f}
   ▪ Saldo Pendiente: ${self.saldo_pendiente:,.2f}
   
   💳 Balance Final: ${(total_general + self.saldo_pendiente):,.2f}

{separador_principal}
"""
        return historial
    
    def _formatear_telefono(self) -> str:
        """Formatea el número de teléfono para mejor presentación"""
        if self.telefono == 0:
            return "No especificado"
        
        telefono_str = str(self.telefono)
        if len(telefono_str) == 8:
            return f"{telefono_str[:4]}-{telefono_str[4:]}"
        elif len(telefono_str) >= 8:
            return f"+503 {telefono_str[-8:-4]}-{telefono_str[-4:]}"
        return telefono_str
    
    def _get_estado_icon(self, estado: str) -> str:
        """Devuelve un icono basado en el estado"""
        estado_lower = estado.lower()
        if 'completado' in estado_lower or 'finalizado' in estado_lower:
            return "✅"
        elif 'pendiente' in estado_lower or 'programado' in estado_lower:
            return "⏳"
        elif 'cancelado' in estado_lower:
            return "❌"
        elif 'en proceso' in estado_lower or 'activo' in estado_lower:
            return "🔄"
        else:
            return "📋"
    
    def _calcular_total_tratamientos(self) -> float:
        """Calcula el costo total de todos los tratamientos"""
        return sum(tratamiento.costo for tratamiento in self.historial_medico)
    
    def _calcular_total_citas(self) -> float:
        """Calcula el costo total de todas las citas"""
        return sum(cita.costo_cita for cita in self.citas)
    
    def __str__(self):
        """Representación en cadena del paciente con formato mejorado"""
        return self._generar_info_completa()

def main():
    app = QApplication([])
    window = PacienteWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
