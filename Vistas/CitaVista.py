# Importaciones necesarias para no tener porblema con los path o importaciones de clase
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit, QPushButton,
    QTextEdit, QGroupBox, QFormLayout, QMessageBox, QComboBox, QDateTimeEdit, QInputDialog, QScrollArea,
    QDateEdit
)
from PyQt6.QtCore import Qt, QDateTime, QDate 
from PyQt6.QtGui import QFont, QIntValidator, QDoubleValidator
from Controladores.CitaControlador import ControladorCita



class CitaWindow(QMainWindow):
    def __init__(self, controlador = None):  
        super().__init__()
        self.setWindowTitle("Gestión de Citas - Clínica Dental")
        self.setGeometry(100, 100, 900, 700)    

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
            
            QDateEdit {{
                font-family: 'Segoe UI';
                font-size: 14px;
                border: 2px solid {self.colors['secondary']};
                border-radius: 6px;
                padding: 10px;
                background-color: {self.colors['surface']};
                color: {self.colors['text_light']};
                selection-background-color: {self.colors['accent']};
            }}
            
            QDateEdit:focus {{
                border-color: {self.colors['accent']};
                background-color: {self.colors['surface']};
            }}
            
            QDateEdit::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left: 1px solid {self.colors['secondary']};
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
                background-color: {self.colors['secondary']};
            }}
            
            QDateEdit::drop-down:hover {{
                background-color: {self.colors['accent']};
            }}
            
            QDateEdit::down-arrow {{
                image: none;
                border: 2px solid {self.colors['surface']};
                width: 6px;
                height: 6px;
                border-top: none;
                border-left: none;
                transform: rotate(45deg);
                margin-top: -2px;
            }}
            
            QCalendarWidget {{
                background-color: {self.colors['surface']};
                color: {self.colors['text_light']};
                border: 2px solid {self.colors['secondary']};
                border-radius: 8px;
            }}
            
            QCalendarWidget QToolButton {{
                background-color: {self.colors['secondary']};
                color: {self.colors['surface']};
                border: none;
                border-radius: 4px;
                padding: 5px;
                margin: 2px;
            }}
            
            QCalendarWidget QToolButton:hover {{
                background-color: {self.colors['accent']};
            }}
            
            QCalendarWidget QMenu {{
                background-color: {self.colors['surface']};
                color: {self.colors['text_light']};
                border: 1px solid {self.colors['secondary']};
            }}
            
            QCalendarWidget QSpinBox {{
                background-color: {self.colors['surface']};
                color: {self.colors['text_light']};
                border: 1px solid {self.colors['secondary']};
                border-radius: 4px;
                padding: 2px;
            }}
            
            QCalendarWidget QAbstractItemView:enabled {{
                background-color: {self.colors['surface']};
                color: {self.colors['text_light']};
                selection-background-color: {self.colors['accent']};
                selection-color: {self.colors['surface']};
            }}
            
            QCalendarWidget QAbstractItemView:disabled {{
                color: {self.colors['secondary']};
            }}
        """)

        # PRIMERO: Crear la interfaz
        self.init_ui()

        # SEGUNDO: Configurar el controlador
        if controlador:
            self.controlador = controlador
            self.controlador.vista = self
        else:
            self.controlador = ControladorCita()
            self.controlador.vista = self

        # TERCERO: Conectar botones
        self.conectar_botones()
        
        # CUARTO: Actualizar combos con datos
        if self.controlador:
            self.controlador.actualizar_vista()

    def validar_fecha_seleccionada(self, fecha):
        """Valida que la fecha seleccionada no sea en el pasado"""
        fecha_actual = QDate.currentDate()
        if fecha < fecha_actual:
            QMessageBox.warning(self, "❌ Fecha Inválida", 
                              "No se pueden seleccionar fechas pasadas.\n"
                              "Por favor seleccione una fecha actual o futura.")
            # Restaurar a la fecha actual si se selecciona una fecha pasada
            self.fecha_edit.setDate(fecha_actual)

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

        # ====================================
        # FORMS PARA CREAR Y MODIFICAR CITAS
        # ====================================

        info_group = QGroupBox("Información de la Cita")
        info_layout = QFormLayout()

        self.id_edit = QLineEdit()
        id_validator = QIntValidator(0, 99999999)
        self.id_edit.setValidator(id_validator)

        self.paciente_combo = QComboBox()
        self.doctor_combo = QComboBox()
        self.tratamiento_combo = QComboBox()

        # Calendario popup
        self.fecha_edit = QDateEdit(QDate.currentDate())
        self.fecha_edit.setDisplayFormat("dd/MM/yyyy")
        self.fecha_edit.setCalendarPopup(True)  
        
        # Establecer fecha mínima como hoy (no permite fechas pasadas)
        self.fecha_edit.setMinimumDate(QDate.currentDate())
        
        # Conectar señal para validación en tiempo real
        self.fecha_edit.dateChanged.connect(self.validar_fecha_seleccionada)
        
        self.inicio_edit = QDateTimeEdit(QDateTime.currentDateTime())
        self.inicio_edit.setDisplayFormat("HH:mm")
        self.fin_edit = QDateTimeEdit(QDateTime.currentDateTime())
        self.fin_edit.setDisplayFormat("HH:mm")
        
        self.costo_edit = QLineEdit()
        costo_validator = QDoubleValidator(0.0, 999999.99, 2)
        costo_validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.costo_edit.setValidator(costo_validator)

        self.estado_combo = QComboBox()
        self.estado_combo.addItems(["Pendiente", "Confirmada", "Cancelada", "Asistida", "Ausente"])

        # info_layout.addRow("ID Cita:", self.id_edit)
        info_layout.addRow("Paciente:", self.paciente_combo)
        info_layout.addRow("Doctor:", self.doctor_combo)
        info_layout.addRow("Tratamiento:", self.tratamiento_combo)
        info_layout.addRow("Fecha:", self.fecha_edit)
        info_layout.addRow("Hora Inicio:", self.inicio_edit)
        info_layout.addRow("Hora Fin:", self.fin_edit)
        info_layout.addRow("Costo:", self.costo_edit)
        info_layout.addRow("Estado:", self.estado_combo)

        info_group.setLayout(info_layout)
        main_layout.addWidget(info_group)

        # ====================================
        # BOTONES DE ACCION
        # ====================================
        
        # Primera fila de botones
        buttons_row1 = QHBoxLayout()
        self.crear_btn = QPushButton("➕ Crear Cita")
        self.cancelar_btn = QPushButton("❌ Cancelar Cita")
        self.modificar_btn = QPushButton("✏ Modificar Cita")

        buttons_row1.addWidget(self.crear_btn)
        buttons_row1.addWidget(self.cancelar_btn)
        buttons_row1.addWidget(self.modificar_btn)

        # Segunda fila de botones
        buttons_row2 = QHBoxLayout()
        self.confirmar_btn = QPushButton("✅ Confirmar Asistencia")
        self.monto_btn = QPushButton("💲 Calcular Monto a Pagar")

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
        
        self.resultado_text.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        self.resultado_text.setMinimumHeight(200)
        
        main_layout.addWidget(self.resultado_text)

        # Scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(central_widget)
        self.setCentralWidget(scroll_area)

    def cargar_datos_cita_actual(self):
        """Carga los datos de la cita actual en los campos del formulario"""
        cita = self.controlador.cita

        if cita:
            self.id_edit.setText(str(cita.id_cita))
            self.paciente_combo.setCurrentText(f"{cita.paciente.nombre} {cita.paciente.apellido}")
            self.doctor_combo.setCurrentText(f"{cita.doctor.nombre} {cita.doctor.apellido}")
            self.fecha_edit.setDate(cita.fecha)
            self.inicio_edit.setTime(cita.hora_inicio.time())
            self.fin_edit.setTime(cita.hora_fin.time())
            self.costo_edit.setText(f"{cita.costo_cita:.2f}")
            self.estado_combo.setCurrentText(cita.estado)
            self.tratamiento_combo.setCurrentText(cita.tratamiento.descripcion if cita.tratamiento else "")


    def conectar_botones(self):
        """Conecta los botones con los métodos del controlador"""
        self.crear_btn.clicked.connect(self.controlador.crear_cita)
        self.cancelar_btn.clicked.connect(self.controlador.cancelar_cita)
        self.modificar_btn.clicked.connect(self.controlador.modificar_cita)
        self.confirmar_btn.clicked.connect(self.controlador.confirmar_asistencia)
        self.monto_btn.clicked.connect(self.controlador.calcular_monto)

    def actualizar_combos(self, doctores, pacientes, tratamientos):
        """Método para que el controlador actualice los combos"""
        print(f"Actualizando combos - Pacientes: {len(pacientes)}, Doctores: {len(doctores)}, Tratamientos: {len(tratamientos)}")  # Debug
        
        # Limpiar combos
        self.paciente_combo.clear()
        self.doctor_combo.clear()
        self.tratamiento_combo.clear()
        
        # Agregar opción vacía al inicio
        self.paciente_combo.addItem("-- Seleccionar Paciente --")
        self.doctor_combo.addItem("-- Seleccionar Doctor --")
        self.tratamiento_combo.addItem("-- Seleccionar Tratamiento --")
        
        # Cargar pacientes
        for i, paciente in enumerate(pacientes):
            texto = f"{paciente.nombre} {paciente.apellido}"
            if hasattr(paciente, 'telefono') and paciente.telefono:
                texto += f" - Tel: {paciente.telefono}"
            self.paciente_combo.addItem(texto)
            print(f"Agregando paciente {i+1}: {texto}")  # Debug
        
        # Cargar doctores
        for i, doctor in enumerate(doctores):
            texto = f"Dr. {doctor.nombre} {doctor.apellido}"
            if hasattr(doctor, 'especialidad') and doctor.especialidad:
                texto += f" - {doctor.especialidad}"
            self.doctor_combo.addItem(texto)
            print(f"Agregando doctor {i+1}: {texto}")  # Debug
        
        # Cargar tratamientos - CORREGIDO
        for i, tratamiento in enumerate(tratamientos):
            texto = f"{tratamiento.descripcion}"  # CORREGIDO: usar descripcion
            if hasattr(tratamiento, 'costo') and tratamiento.costo:
                texto += f" - ${tratamiento.costo:.2f}"
            self.tratamiento_combo.addItem(texto)
            print(f"Agregando tratamiento {i+1}: {texto}")  # Debug
        
        print(f"Combos actualizados - Pacientes: {self.paciente_combo.count()}, Doctores: {self.doctor_combo.count()}, Tratamientos: {self.tratamiento_combo.count()}")
