from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from datetime import datetime
import os
import sys

# Agregar el directorio padre al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# ==========================================
# IMPORTACIONES: Clases del modelo y controladores (MVC CORRECTO)
# ==========================================

from Controladores.PacienteControlador import PacienteControlador
from Modelos.PacienteModelo import Paciente



# ==========================================
# CLASE PRINCIPAL: PacienteWindow
# PROPÓSITO: Ventana principal del sistema de gestión de pacientes
# ==========================================
class PacienteWindow(QMainWindow):
    def __init__(self, controlador=None):
        super().__init__()
        self.setWindowTitle("Gestión de Pacientes - Clínica Dental")
        self.setGeometry(100, 100, 900, 700)
        
        # Usar el controlador pasado o crear uno nuevo
        if controlador:
            self.controlador = controlador
            self.controlador.set_vista(self)  # Establecer referencia bidireccional
        else:
            self.controlador = PacienteControlador()
            self.controlador.set_vista(self)
        
        # Color scheme 
        self.colors = {
            'primary': '#130760',      # Dark blue-purple 
            'secondary': '#756f9f',    # Medium purple
            'accent': '#10b8b9',       # Teal
            'background': '#f7f8fa',   # Light background
            'surface': '#ffffff',      # White surface
            'text_light': '#2c3e50',   # Dark text for light backgrounds
            'text_dark': '#34495e'     # Darker text
        }

        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {self.colors['background']};
                font-family: Segoe UI, Arial, sans-serif;
                font-size: 14px;
                color: {self.colors['text_dark']};
            }}
            
            QWidget {{
                background-color: {self.colors['background']};
            }}
                
            QLabel {{
                color: {self.colors['text_light']};
                background-color: {self.colors['surface']};
                font-family: Segoe UI, Arial, sans-serif;
                font-size: 14px;
            }}
            
            QGroupBox {{
                font-family: Segoe UI, Arial, sans-serif;
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
            
            QLineEdit, QSpinBox, QDoubleSpinBox, QDateEdit {{
                font-family: Segoe UI, Arial, sans-serif;
                font-size: 14px;
                border: 2px solid {self.colors['secondary']};
                border-radius: 6px;
                padding: 10px;
                background-color: {self.colors['surface']};
                color: {self.colors['text_light']};
               
            }}
            
            QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QDateEdit:focus {{
                border-color: {self.colors['accent']};
                background-color: #ffffff;
            }}
            
            QDateEdit::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 25px;
                border-left: 1px solid {self.colors['secondary']};
                background-color: {self.colors['secondary']};
                border-radius: 3px;
            }}
            
            QDateEdit::drop-down:hover {{
                background-color: {self.colors['accent']};
            }}
            
            QDateEdit::down-arrow {{
                image: none;
                border: 2px solid {self.colors['text_light']};
                width: 6px;
                height: 6px;
                border-top: none;
                border-left: none;
                margin-top: -2px;
            }}
            
            QCalendarWidget {{
                background-color: #ffffff;
                color: #2c3e50;
                border: 3px solid #756f9f;
                border-radius: 12px;
                font-family: Segoe UI, Arial, sans-serif;
                font-size: 14px;
                padding: 10px;
                selection-background-color: #10b8b9;
                alternate-background-color: #f8f9fa;
            }}
            
            QCalendarWidget QWidget#qt_calendar_navigationbar {{
                background-color: #756f9f;
                color: #ffffff;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                padding: 5px;
            }}
            
            QCalendarWidget QToolButton {{
                background-color: #756f9f;
                color: #ffffff;
                border: none;
                border-radius: 6px;
                padding: 8px 12px;
                margin: 2px;
                font-weight: bold;
                font-size: 13px;
                min-width: 30px;
                min-height: 30px;
            }}
            
            QCalendarWidget QToolButton:hover {{
                background-color: #10b8b9;
            }}
            
            QCalendarWidget QToolButton:pressed {{
                background-color: #130760;
            }}
            
            QCalendarWidget QToolButton#qt_calendar_prevmonth {{
                qproperty-text: "◀";
                font-size: 16px;
                font-weight: bold;
            }}
            
            QCalendarWidget QToolButton#qt_calendar_nextmonth {{
                qproperty-text: "▶";
                font-size: 16px;
                font-weight: bold;
            }}
            
            QCalendarWidget QMenu {{
                background-color: #ffffff;
                color: #2c3e50;
                border: 2px solid #756f9f;
                border-radius: 8px;
                padding: 5px;
            }}
            
            QCalendarWidget QMenu::item {{
                background-color: transparent;
                padding: 8px 12px;
                border-radius: 4px;
            }}
            
            QCalendarWidget QMenu::item:selected {{
                background-color: #10b8b9;
                color: #ffffff;
            }}
            
            QCalendarWidget QSpinBox {{
                background-color: #ffffff;
                color: #2c3e50;
                border: 2px solid #756f9f;
                border-radius: 6px;
                padding: 6px;
                font-weight: bold;
                font-size: 13px;
                min-width: 80px;
                selection-background-color: #10b8b9;
            }}
            
            QCalendarWidget QSpinBox:focus {{
                border-color: #10b8b9;
                background-color: #f8f9fa;
            }}
            
            QCalendarWidget QSpinBox::up-button {{
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 20px;
                border-left: 1px solid #756f9f;
                background-color: #756f9f;
                border-top-right-radius: 4px;
            }}
            
            QCalendarWidget QSpinBox::up-button:hover {{
                background-color: #10b8b9;
            }}
            
            QCalendarWidget QSpinBox::down-button {{
                subcontrol-origin: border;
                subcontrol-position: bottom right;
                width: 20px;
                border-left: 1px solid #756f9f;
                background-color: #756f9f;
                border-bottom-right-radius: 4px;
            }}
            
            QCalendarWidget QSpinBox::down-button:hover {{
                background-color: #10b8b9;
            }}
            
            QCalendarWidget QSpinBox::up-arrow {{
                image: none;
                border: 2px solid #ffffff;
                width: 4px;
                height: 4px;
                border-bottom: none;
                border-right: none;
                margin: 2px;
            }}
            
            QCalendarWidget QSpinBox::down-arrow {{
                image: none;
                border: 2px solid #ffffff;
                width: 4px;
                height: 4px;
                border-top: none;
                border-left: none;
                margin: 2px;
            }}
            
            QCalendarWidget QAbstractItemView {{
                background-color: #ffffff;
                color: #2c3e50;
                selection-background-color: #10b8b9;
                selection-color: #ffffff;
                border: none;
                outline: none;
                gridline-color: #e1e8ed;
                font-size: 13px;
                font-weight: 500;
            }}
            
            QCalendarWidget QAbstractItemView:enabled {{
                color: #2c3e50;
                background-color: #ffffff;
            }}
            
            QCalendarWidget QAbstractItemView:disabled {{
                color: #bdc3c7;
                background-color: #f8f9fa;
            }}
            
            QCalendarWidget QAbstractItemView::item {{
                padding: 8px;
                border-radius: 6px;
                margin: 1px;
            }}
            
            QCalendarWidget QAbstractItemView::item:hover {{
                background-color: #e8f4fd;
                color: #2c3e50;
                border: 1px solid #10b8b9;
            }}
            
            QCalendarWidget QAbstractItemView::item:selected {{
                background-color: #10b8b9;
                color: #ffffff;
                font-weight: bold;
                border: 2px solid #0d9a9b;
            }}
            
            QCalendarWidget QHeaderView::section {{
                background-color: #756f9f;
                color: #ffffff;
                border: none;
                padding: 10px;
                font-weight: bold;
                font-size: 12px;
                border-radius: 4px;
                margin: 1px;
            }}
            
            QCalendarWidget QTableView {{
                gridline-color: #e1e8ed;
                background-color: #ffffff;
                alternate-background-color: #f8f9fa;
                border-radius: 8px;
            }}
            
            QCalendarWidget QTableView::item {{
                border: 1px solid transparent;
                padding: 6px;
            }}
            
            QCalendarWidget QTableView::item:hover {{
                background-color: #e8f4fd;
                border: 1px solid #10b8b9;
                border-radius: 4px;
            }}
            
            QCalendarWidget QTableView::item:selected {{
                background-color: #10b8b9;
                color: #ffffff;
                border: 2px solid #0d9a9b;
                border-radius: 4px;
                font-weight: bold;
            }}
            
            QPushButton {{
                font-family: Segoe UI, Arial, sans-serif;
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
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
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

        self.edad_edit = QDateEdit()
        self.edad_edit.setCalendarPopup(True)
        self.edad_edit.setDisplayFormat("dd/MM/yyyy")
        self.edad_edit.setDate(QDate.currentDate())
        # Conectar señal para actualizar el label del DUI cuando cambie la fecha
        self.edad_edit.dateChanged.connect(self.actualizar_label_dui)
        
        self.dui_edit = QLineEdit()
        self.telefono_edit = QLineEdit()
        self.correo_edit = QLineEdit()
        self.saldo_edit = QDoubleSpinBox()
        self.saldo_edit.setPrefix("$")
        self.saldo_edit.setMaximum(99999.99)
        
        info_layout.addRow("Nombre:", self.nombre_edit)
        info_layout.addRow("Apellido:", self.apellido_edit)
        info_layout.addRow("Fecha de Nacimiento:", self.edad_edit)
        
        # Crear el label del DUI que se actualizará dinámicamente
        self.dui_label = QLabel("DUI:")
        info_layout.addRow(self.dui_label, self.dui_edit)
        
        info_layout.addRow("Teléfono:", self.telefono_edit)
        info_layout.addRow("Correo:", self.correo_edit)
        info_layout.addRow("Saldo Pendiente:", self.saldo_edit)
        
        info_group.setLayout(info_layout)
        main_layout.addWidget(info_group)
        
        # ==========================================
        # GRUPO DE BÚSQUEDA DE PACIENTES
        # ==========================================
        busqueda_group = QGroupBox("🔍 Búsqueda de Pacientes")
        busqueda_layout = QFormLayout()
        
        # Campos de búsqueda
        self.buscar_nombre_edit = QLineEdit()
        self.buscar_nombre_edit.setPlaceholderText("Ingrese nombre para buscar...")
        self.buscar_nombre_edit.textChanged.connect(self.buscar_pacientes_por_nombre)
        
        self.buscar_apellido_edit = QLineEdit()
        self.buscar_apellido_edit.setPlaceholderText("Ingrese apellido para buscar...")
        self.buscar_apellido_edit.textChanged.connect(self.buscar_pacientes_por_nombre)
        
        # ComboBox para mostrar resultados de búsqueda
        self.pacientes_combo = QComboBox()
        self.pacientes_combo.setEditable(False)
        self.pacientes_combo.currentTextChanged.connect(self.seleccionar_paciente_desde_combo)
        
        # Estilo para el ComboBox
        self.pacientes_combo.setStyleSheet(f"""
            QComboBox {{
                font-family: Segoe UI, Arial, sans-serif;
                font-size: 14px;
                border: 2px solid {self.colors['secondary']};
                border-radius: 6px;
                padding: 10px;
                background-color: {self.colors['surface']};
                color: {self.colors['text_light']};
                min-height: 25px;
            }}
            
            QComboBox:focus {{
                border-color: {self.colors['accent']};
                background-color: #ffffff;
            }}
            
            QComboBox::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 30px;
                border-left: 2px solid {self.colors['secondary']};
                background-color: {self.colors['secondary']};
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
            }}
            
            QComboBox::drop-down:hover {{
                background-color: {self.colors['accent']};
            }}
            
            QComboBox::down-arrow {{
                image: none;
                border: 2px solid #ffffff;
                width: 6px;
                height: 6px;
                border-top: none;
                border-left: none;
                margin-top: -2px;
            }}
            
            QComboBox QAbstractItemView {{
                background-color: {self.colors['surface']};
                color: {self.colors['text_light']};
                border: 2px solid {self.colors['secondary']};
                border-radius: 6px;
                selection-background-color: {self.colors['accent']};
                selection-color: #ffffff;
                padding: 5px;
                font-size: 14px;
            }}
            
            QComboBox QAbstractItemView::item {{
                padding: 8px;
                border-radius: 4px;
                margin: 2px;
            }}
            
            QComboBox QAbstractItemView::item:hover {{
                background-color: #e8f4fd;
                color: {self.colors['text_light']};
            }}
            
            QComboBox QAbstractItemView::item:selected {{
                background-color: {self.colors['accent']};
                color: #ffffff;
            }}
        """)
        
        # Botón para limpiar búsqueda
        self.limpiar_busqueda_btn = QPushButton("🧹 Limpiar Búsqueda")
        self.limpiar_busqueda_btn.clicked.connect(self.limpiar_busqueda)
        self.limpiar_busqueda_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.colors['secondary']};
                font-size: 12px;
                padding: 8px 12px;
            }}
            QPushButton:hover {{
                background-color: {self.colors['accent']};
            }}
        """)
        
        busqueda_layout.addRow("🔤 Nombre:", self.buscar_nombre_edit)
        busqueda_layout.addRow("🔤 Apellido:", self.buscar_apellido_edit)
        busqueda_layout.addRow("📋 Pacientes Encontrados:", self.pacientes_combo)
        busqueda_layout.addRow("", self.limpiar_busqueda_btn)
        
        busqueda_group.setLayout(busqueda_layout)
        main_layout.addWidget(busqueda_group)
        
        # ==========================================
        # FIN GRUPO DE BÚSQUEDA
        # ==========================================
        
        # Botones de acción con iconos
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        # Primera fila de botones
        buttons_row1 = QHBoxLayout()
        buttons_row1.setSpacing(10)
        
        self.crear_btn = QPushButton("👤 Crear Paciente")
        self.crear_btn.clicked.connect(self.crear_paciente)
        
        # Solo botones relacionados con gestión básica de pacientes
        buttons_row1.addWidget(self.crear_btn)
        
        # Segunda fila de botones
        buttons_row2 = QHBoxLayout()
        buttons_row2.setSpacing(10)
        
        self.ver_info_basica_btn = QPushButton("📋 Ver Info Básica")
        self.ver_info_basica_btn.clicked.connect(self.ver_info_basica)
        
        self.mostrar_info_btn = QPushButton("ℹ️ Mostrar Info Paciente")
        self.mostrar_info_btn.clicked.connect(self.mostrar_info_paciente)
        
        # Botón para mostrar todos los pacientes
        self.mostrar_todos_btn = QPushButton("📚 Todos los Pacientes")
        self.mostrar_todos_btn.clicked.connect(self.mostrar_todos_pacientes)
        
        buttons_row2.addWidget(self.ver_info_basica_btn)
        buttons_row2.addWidget(self.mostrar_info_btn)
        buttons_row2.addWidget(self.mostrar_todos_btn)
        
        # Layout vertical para las filas de botones
        buttons_container = QVBoxLayout()
        buttons_container.addLayout(buttons_row1)
        buttons_container.addLayout(buttons_row2)

        main_layout.addLayout(buttons_container)
        
        # Área de resultados con estilo mejorado y scroll bar
        resultado_label = QLabel("📊 Resultados:")
        resultado_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        resultado_label.setStyleSheet(f"color: {self.colors['accent']};")
        main_layout.addWidget(resultado_label)
        
        self.resultado_text = QTextEdit()
        self.resultado_text.setReadOnly(True)
        self.resultado_text.setFont(QFont("Courier New", 12))
        self.resultado_text.setPlaceholderText("Aquí aparecerán los resultados de las operaciones...")
        
        # Configurar scroll bars con estilo
        self.resultado_text.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.resultado_text.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Estilo mejorado para el área de texto y scroll bars
        self.resultado_text.setStyleSheet(f"""
            QTextEdit {{
                background-color: #f7f8fa;
                color: #2c3e50;
                border: 2px solid {self.colors['secondary']};
                border-radius: 8px;
                padding: 15px;
            }}
            
            QScrollBar:vertical {{
                background-color: #e0e0e0;
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
                background-color: #e0e0e0;
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
        
        # Inicializar el ComboBox de búsqueda
        self.pacientes_combo.addItem("-- Seleccione un paciente --")
    
    def actualizar_interfaz(self):
        """Actualiza toda la interfaz con los datos actuales del controlador"""
        self.actualizar_lista_pacientes()
        if self.controlador.paciente_actual:
            self.cargar_datos_paciente_actual()
    
    def actualizar_lista_pacientes(self):
        """Actualiza el ComboBox con todos los pacientes"""
        self.pacientes_combo.clear()
        self.pacientes_combo.addItem("-- Seleccione un paciente --")
        
        for paciente in self.controlador.get_todos_los_pacientes():
            edad = paciente.calcular_edad()
            dui_info = f"DUI: {paciente.dui}" if paciente.tiene_dui() else "Sin DUI"
            texto_combo = f"#{paciente.id_paciente} - {paciente.nombre} {paciente.apellido} ({edad} años) - {dui_info}"
            self.pacientes_combo.addItem(texto_combo, paciente)
    
    def cargar_datos_paciente_actual(self):
        """Carga los datos del paciente actual en los campos de la vista"""
        paciente = self.controlador.paciente_actual
        if paciente:
            self.nombre_edit.setText(paciente.nombre)
            self.apellido_edit.setText(paciente.apellido)
            # Convertir datetime a QDate
            fecha_qt = QDate(paciente.fecha_nacimiento.year, 
                           paciente.fecha_nacimiento.month, 
                           paciente.fecha_nacimiento.day)
            self.edad_edit.setDate(fecha_qt)
            self.dui_edit.setText(paciente.dui)
            self.telefono_edit.setText(str(paciente.telefono))
            self.correo_edit.setText(paciente.correo)
            self.saldo_edit.setValue(paciente.saldo_pendiente)
    
    def mostrar_mensaje(self, titulo: str, mensaje: str, tipo: str = "info"):
        """Muestra un mensaje al usuario"""
        from PyQt6.QtWidgets import QMessageBox
        if tipo == "info":
            QMessageBox.information(self, titulo, mensaje)
        elif tipo == "warning":
            QMessageBox.warning(self, titulo, mensaje)
        elif tipo == "error":
            QMessageBox.critical(self, titulo, mensaje)
    
    def seleccionar_paciente_desde_combo(self, texto):
        """Selecciona un paciente desde el ComboBox"""
        current_index = self.pacientes_combo.currentIndex()
        if current_index > 0:  # Si no es "-- Seleccione un paciente --"
            paciente = self.pacientes_combo.itemData(current_index)
            if paciente:
                self.controlador.seleccionar_paciente(paciente)
                self.cargar_datos_paciente_actual()
    
    def buscar_pacientes_por_nombre(self):
        """Busca pacientes basado en los campos de búsqueda"""
        nombre = self.buscar_nombre_edit.text()
        apellido = self.buscar_apellido_edit.text()
        
        if nombre or apellido:
            pacientes_encontrados = self.controlador.buscar_pacientes_por_nombre_apellido(nombre, apellido)
            
            # Actualizar el ComboBox con los resultados
            self.pacientes_combo.clear()
            self.pacientes_combo.addItem("-- Seleccione un paciente --")
            
            for paciente in pacientes_encontrados:
                edad = paciente.calcular_edad()
                dui_info = f"DUI: {paciente.dui}" if paciente.tiene_dui() else "Sin DUI"
                texto_combo = f"#{paciente.id_paciente} - {paciente.nombre} {paciente.apellido} ({edad} años) - {dui_info}"
                self.pacientes_combo.addItem(texto_combo, paciente)
                
            self.resultado_text.setText(f"🔍 Búsqueda realizada: {len(pacientes_encontrados)} paciente(s) encontrado(s)")
        else:
            # Si no hay criterios de búsqueda, mostrar todos
            self.actualizar_lista_pacientes()
    
    def limpiar_busqueda(self):
        """Limpia los campos de búsqueda y muestra todos los pacientes"""
        self.buscar_nombre_edit.clear()
        self.buscar_apellido_edit.clear()
        self.actualizar_lista_pacientes()
        self.resultado_text.setText("🧹 Búsqueda limpiada - Mostrando todos los pacientes")
    
    def actualizar_label_dui(self):
        """Actualiza el label del DUI basado en la edad del paciente"""
        fecha_nacimiento = self.edad_edit.date().toPython()
        hoy = datetime.now().date()
        edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
        
        if edad >= 18:
            self.dui_label.setText("DUI (Obligatorio):")
            self.dui_edit.setStyleSheet(f"""
                border: 2px solid #e74c3c;
                background-color: #fff5f5;
            """)
        else:
            self.dui_label.setText("DUI (Opcional):")
            self.dui_edit.setStyleSheet("")  # Estilo normal
    
    def limpiar_campos(self):
        """Limpia todos los campos de entrada para agregar un nuevo paciente"""
        self.nombre_edit.clear()
        self.apellido_edit.clear()
        self.edad_edit.setDate(QDate.currentDate())
        self.dui_edit.clear()
        self.telefono_edit.clear()
        self.correo_edit.clear()
        self.saldo_edit.setValue(0.0)
        
        # Enfocar el primer campo para facilitar la entrada
        self.nombre_edit.setFocus()
    
    def crear_paciente(self):
        """Crea un nuevo paciente con los datos ingresados"""
        try:
            # Obtener valores directamente sin strip() para evitar errores
            nombre_raw = self.nombre_edit.text()
            apellido_raw = self.apellido_edit.text()
            
            # Limpiar manualmente si hay valor
            nombre = nombre_raw if isinstance(nombre_raw, str) else ""
            apellido = apellido_raw if isinstance(apellido_raw, str) else ""
            
            # Limpiar espacios manualmente sin strip()
            if nombre:
                nombre = nombre.replace("  ", " ")  # Remover espacios dobles
                if nombre.startswith(" "):
                    nombre = nombre[1:]  # Quitar espacio al inicio
                if nombre.endswith(" "):
                    nombre = nombre[:-1]  # Quitar espacio al final
            if apellido:
                apellido = apellido.replace("  ", " ")  # Remover espacios dobles
                if apellido.startswith(" "):
                    apellido = apellido[1:]  # Quitar espacio al inicio
                if apellido.endswith(" "):
                    apellido = apellido[:-1]  # Quitar espacio al final
            
            # Convertir QDate a datetime
            fecha_qdate = self.edad_edit.date()
            fecha_nacimiento = datetime(fecha_qdate.year(), fecha_qdate.month(), fecha_qdate.day())
            
            # Obtener otros valores de forma segura
            dui_raw = self.dui_edit.text()
            telefono_raw = self.telefono_edit.text()
            correo_raw = self.correo_edit.text()
            
            dui = dui_raw if isinstance(dui_raw, str) else ""
            telefono_str = telefono_raw if isinstance(telefono_raw, str) else ""
            correo = correo_raw if isinstance(correo_raw, str) else ""
            
            saldo_pendiente = self.saldo_edit.value()
            
            # Validación del teléfono - SIMPLIFICADO
            telefono = 0
            if telefono_str:
                # Simplemente convertir a entero si hay texto
                try:
                    telefono_limpio = ''.join(filter(str.isdigit, telefono_str))
                    if telefono_limpio:
                        telefono = int(telefono_limpio)
                except:
                    telefono = 0
            
            # Crear paciente usando el controlador (nuevo orden de parámetros)
            exito, mensaje = self.controlador.crear_paciente(
                nombre, apellido, fecha_nacimiento, telefono, correo, dui, saldo_pendiente
            )
            
            if exito:
                # Mostrar mensaje de éxito con información básica
                total_pacientes = len(self.controlador.pacientes_registrados)
                proximo_id = Paciente.get_next_id()
                
                QMessageBox.information(self, "✅ Éxito", 
                                      f"{mensaje}\n\n"
                                      f"📊 INFORMACIÓN DEL SISTEMA:\n"
                                      f"• Total de pacientes: {total_pacientes}\n"
                                      f"• Próximo ID disponible: {proximo_id}")
                
                # Mostrar información básica del paciente creado
                self.resultado_text.setText(f"✅ {mensaje}\n\n"
                                           f"📊 Pacientes registrados: {total_pacientes}\n"
                                           f"🆔 Próximo ID: {proximo_id}")
                
                # Limpiar campos automáticamente para el siguiente paciente
                self.limpiar_campos()
            else:
                QMessageBox.warning(self, "❌ Error", mensaje)
                
        except ValueError as e:
            QMessageBox.warning(self, "❌ Error", f"Error en el formato de los datos: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "❌ Error Inesperado", f"Ocurrió un error inesperado: {str(e)}")
            print(f"Error en crear_paciente: {e}")  # Para debug
    

    
    def _generar_resumen_todos_pacientes(self) -> str:
        """Genera un resumen básico de todos los pacientes (sin información médica)"""
        separador_principal = "=" * 80
        separador_paciente = "-" * 60
        
        pacientes = self.controlador.pacientes_registrados
        
        resumen = f"""
{separador_principal}
📚 RESUMEN DE PACIENTES REGISTRADOS - CLÍNICA DENTAL
{separador_principal}

📊 INFORMACIÓN GENERAL:
   ▪ Total de Pacientes Registrados: {len(pacientes)}
   ▪ Fecha de Consulta: {datetime.now().strftime('%d/%m/%Y - %H:%M:%S')}

{separador_principal}
"""
        
        # Mostrar cada paciente
        for i, paciente in enumerate(pacientes, 1):
            edad = paciente.calcular_edad()
            dui_label = "DUI del Responsable" if edad < 18 else "DUI"
            edad_info = f"{edad} años" + (" (Menor de edad)" if edad < 18 else "")
            dui_info = paciente.dui if paciente.tiene_dui() else "No registrado"
            
            resumen += f"""
{separador_paciente}
👤 PACIENTE #{i:02d}: {paciente.nombre} {paciente.apellido} (ID: #{paciente.id_paciente})
{separador_paciente}

📋 INFORMACIÓN PERSONAL:
   ▪ ID del Paciente: #{paciente.id_paciente}
   ▪ Nombre Completo: {paciente.nombre} {paciente.apellido}
   ▪ Edad: {edad_info}
   ▪ {dui_label}: {dui_info}
   ▪ Teléfono: {paciente.telefono}
   ▪ Correo: {paciente.correo if paciente.correo else 'No especificado'}
   ▪ Fecha de Registro: {paciente.fecha_registro}

💰 INFORMACIÓN FINANCIERA:
   ▪ Saldo Pendiente: ${paciente.saldo_pendiente:,.2f}
   ▪ Estado de Pago: {'🔴 Pendiente' if paciente.saldo_pendiente > 0 else '🟢 Al día'}

"""
        
        # Resumen estadístico básico
        total_pacientes = len(pacientes)
        total_saldos_pendientes = sum(p.saldo_pendiente for p in pacientes)
        pacientes_con_saldo = sum(1 for p in pacientes if p.saldo_pendiente > 0)
        
        resumen += f"""
{separador_principal}
📈 ESTADÍSTICAS BÁSICAS DE LA CLÍNICA
{separador_principal}

👥 PACIENTES:
   ▪ Total de Pacientes: {total_pacientes}
   ▪ Pacientes con Saldo Pendiente: {pacientes_con_saldo}
   ▪ Pacientes al Día: {total_pacientes - pacientes_con_saldo}
   
💰 FINANZAS BÁSICAS:
   ▪ Total Saldos Pendientes: ${total_saldos_pendientes:,.2f}

💡 NOTA: Esta vista muestra únicamente información básica de pacientes.
Para consultar historiales médicos, citas y tratamientos, 
utilice los módulos especializados correspondientes.

{separador_principal}
"""
        return resumen
    
    def ver_info_basica(self):
        """Muestra información básica del paciente seleccionado"""
        paciente_actual = self.controlador.paciente_actual
        if not paciente_actual:
            QMessageBox.warning(self, "❌ Error", "Debe crear o seleccionar un paciente primero")
            return
        
        # Generar información básica directamente
        edad = paciente_actual.calcular_edad()
        info_basica = f"""
📋 INFORMACIÓN BÁSICA DEL PACIENTE

🆔 ID: #{paciente_actual.id_paciente}
👤 Nombre: {paciente_actual.nombre} {paciente_actual.apellido}
🎂 Edad: {edad} años
📞 Teléfono: {paciente_actual.telefono}
📧 Correo: {paciente_actual.correo if paciente_actual.correo else 'No registrado'}
💰 Saldo pendiente: ${paciente_actual.saldo_pendiente:.2f}
"""
        self.resultado_text.setText(info_basica)

    def mostrar_todos_pacientes(self):
        """Muestra un resumen de todos los pacientes registrados (información básica únicamente)"""
        pacientes = self.controlador.pacientes_registrados
        if not pacientes:
            QMessageBox.information(self, "ℹ️ Información", 
                                  "No hay pacientes registrados en el sistema.")
            return
        
        resumen_completo = self._generar_resumen_todos_pacientes()
        self.resultado_text.setText(resumen_completo)
    
    def mostrar_info_paciente(self):
        """Muestra la información básica del paciente"""
        paciente_actual = self.controlador.paciente_actual
        if not paciente_actual:
            QMessageBox.warning(self, "❌ Error", "Debe crear un paciente primero")
            return
        
        self.resultado_text.setText(self._generar_info_completa())
    
    def _generar_info_completa(self):
        """Genera información completa del paciente actual"""
        paciente = self.controlador.paciente_actual
        if not paciente:
            return "No hay paciente seleccionado"
        
        # Usar el método del controlador para generar la información
        info_basica = self.controlador.generar_info_basica_paciente(paciente)
        info_financiera = self.controlador.generar_resumen_financiero(paciente)
        
        return f"""
{info_basica}

{info_financiera}
        """
    
    def actualizar_label_dui(self):
        """Actualiza el label del DUI basado en la edad del paciente (SOLO UI)"""
        try:
            fecha_qdate = self.edad_edit.date()
            fecha_nacimiento = datetime(fecha_qdate.year(), fecha_qdate.month(), fecha_qdate.day())
            
            # Calcular edad directamente en la vista para validación visual
            hoy = datetime.now()
            edad = hoy.year - fecha_nacimiento.year
            if hoy.month < fecha_nacimiento.month or (hoy.month == fecha_nacimiento.month and hoy.day < fecha_nacimiento.day):
                edad -= 1
            
            if edad < 18:
                self.dui_label.setText("📋 DUI del Responsable (Opcional):")
                self.dui_edit.setPlaceholderText("DUI del padre, madre o tutor legal (opcional)")
            else:
                self.dui_label.setText("📋 DUI (Opcional):")
                self.dui_edit.setPlaceholderText("Documento único de identidad (opcional)")
        except Exception:
            self.dui_label.setText("📋 DUI (Opcional):")
    
    # ==========================================
    # MÉTODOS DE BÚSQUEDA DE PACIENTES
    # ==========================================
    
    def buscar_pacientes_por_nombre(self):
        """Busca pacientes por nombre y/o apellido y actualiza el ComboBox"""
        nombre_busqueda = str(self.buscar_nombre_edit.text())
        apellido_busqueda = str(self.buscar_apellido_edit.text())
        
        # Limpiar espacios manualmente
        if nombre_busqueda.startswith(" "):
            nombre_busqueda = nombre_busqueda[1:]
        if nombre_busqueda.endswith(" "):
            nombre_busqueda = nombre_busqueda[:-1]
        if apellido_busqueda.startswith(" "):
            apellido_busqueda = apellido_busqueda[1:]
        if apellido_busqueda.endswith(" "):
            apellido_busqueda = apellido_busqueda[:-1]
        
        # Limpiar el ComboBox
        self.pacientes_combo.clear()
        self.pacientes_combo.addItem("-- Seleccione un paciente --")
        
        # Si no hay texto en ningún campo, no buscar
        if not nombre_busqueda and not apellido_busqueda:
            return
        
        # Usar el método del controlador para la búsqueda
        pacientes_encontrados = self.controlador.buscar_pacientes_por_nombre_apellido(
            nombre_busqueda, apellido_busqueda
        )
        
        # Agregar pacientes encontrados al ComboBox
        if pacientes_encontrados:
            for paciente in pacientes_encontrados:
                # Crear texto descriptivo con nombre completo, ID y edad
                edad = paciente.calcular_edad()
                dui_info = f"DUI: {paciente.dui}" if paciente.tiene_dui() else "Sin DUI"
                texto_combo = f"#{paciente.id_paciente} - {paciente.nombre} {paciente.apellido} ({edad} años) - {dui_info}"
                self.pacientes_combo.addItem(texto_combo, paciente)  # El segundo parámetro es el objeto paciente
            
            # Mostrar información adicional en el área de resultados
            self.mostrar_resultados_busqueda(pacientes_encontrados)
        else:
            self.pacientes_combo.addItem("❌ No se encontraron pacientes")
            self.resultado_text.setText("🔍 No se encontraron pacientes que coincidan con la búsqueda.")
    
    def mostrar_resultados_busqueda(self, pacientes_encontrados):
        """Muestra información detallada de los pacientes encontrados"""
        separador = "=" * 60
        info = f"""
{separador}
🔍 RESULTADOS DE BÚSQUEDA - {len(pacientes_encontrados)} PACIENTE(S) ENCONTRADO(S)
{separador}

"""
        
        for i, paciente in enumerate(pacientes_encontrados, 1):
            edad = paciente.calcular_edad()
            edad_info = f"{edad} años" + (" (Menor)" if edad < 18 else " (Mayor)")
            dui_info = paciente.dui if paciente.tiene_dui() else "No registrado"
            
            info += f"""
┌─ PACIENTE #{i:02d}
│ 🆔 ID: #{paciente.id_paciente}
│ 👤 Nombre: {paciente.nombre} {paciente.apellido}
│ 🎂 Edad: {edad_info}
│ 📋 DUI: {dui_info}
│ 📞 Teléfono: {paciente.telefono}
│ 💰 Saldo: ${paciente.saldo_pendiente:,.2f}
│ 📅 Registro: {paciente.fecha_registro}
└─────────────────────────────────────────────────
"""
        
        info += f"""
💡 INSTRUCCIONES:
• Seleccione un paciente del ComboBox de arriba para verlo como paciente actual
• Use el botón "🧹 Limpiar Búsqueda" para comenzar una nueva búsqueda

{separador}
"""
        
        self.resultado_text.setText(info)
    
    def seleccionar_paciente_desde_combo(self, texto_seleccionado):
        """Selecciona un paciente desde el ComboBox y lo establece como paciente actual"""
        if not texto_seleccionado or texto_seleccionado.startswith("--") or texto_seleccionado.startswith("❌"):
            return
        
        # Obtener el paciente asociado al item seleccionado
        indice_actual = self.pacientes_combo.currentIndex()
        if indice_actual > 0:  # Ignorar el primer item que es el placeholder
            paciente_seleccionado = self.pacientes_combo.itemData(indice_actual)
            
            if paciente_seleccionado:
                # Establecer como paciente actual
                self.controlador.paciente_actual = paciente_seleccionado
                
                # Mostrar mensaje de confirmación
                edad = self.controlador.calcular_edad(paciente_seleccionado.fecha_nacimiento)
                dui_info = f"DUI: {paciente_seleccionado.dui}" if paciente_seleccionado.tiene_dui() else "DUI: No registrado"
                
                QMessageBox.information(self, "✅ Paciente Seleccionado", 
                                      f"Paciente #{paciente_seleccionado.id_paciente}: {paciente_seleccionado.nombre} {paciente_seleccionado.apellido} "
                                      f"ha sido seleccionado como paciente actual.\n\n"
                                      f"ID: #{paciente_seleccionado.id_paciente}\n"
                                      f"Edad: {edad} años\n"
                                      f"{dui_info}\n\n"
                                      f"Ahora puede usar todas las funciones con este paciente.")
                
                # Mostrar información completa del paciente seleccionado
                self.resultado_text.setText(self._generar_info_completa())
    
    def limpiar_busqueda(self):
        """Limpia los campos de búsqueda y el ComboBox"""
        self.buscar_nombre_edit.clear()
        self.buscar_apellido_edit.clear()
        self.pacientes_combo.clear()
        self.pacientes_combo.addItem("-- Seleccione un paciente --")
        
        # Limpiar el área de resultados
        self.resultado_text.setText("🧹 Búsqueda limpiada. Ingrese nombre y/o apellido para buscar pacientes.")

def main():
    app = QApplication([])
    window = PacienteWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
