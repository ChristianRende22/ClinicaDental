import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
                             QWidget, QLabel, QLineEdit, QPushButton, 
                             QTextEdit, QGroupBox, QFormLayout, QMessageBox,
                             QComboBox, QScrollArea, QSizePolicy) 
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QDoubleValidator 
from datetime import datetime
from typing import List, Dict, Any

class FacturacionView(QMainWindow):  
    crear_factura_signal = pyqtSignal(dict)
    mostrar_facturas_signal = pyqtSignal()
    limpiar_campos_signal = pyqtSignal()
    actualizar_datos_signal = pyqtSignal()  # Nueva señal para actualizar datos

    def __init__(self):
        super().__init__()
    
        self.colors = {
            'primary': '#130760',      # Dark blue-purple 
            'secondary': '#756f9f',    # Medium purple
            'accent': '#10b8b9',       # Teal
            'text_light': '#2b2b2b',   # Dark gray
            'text_dark': '#3c3c3c',    # Slightly lighter gray
            'background': '#f7f8fa',   # Light background
            'surface': '#ffffff'       # White surface
        }


        self.setWindowTitle("Gestión de Facturas - Clínica Dental") 
        self.setGeometry(100, 100, 1000, 750)
        
        self.setup_styles()  
        self.init_ui()      
        self.conectar_botones() 
            

    def setup_styles(self):
        """Configura los estilos de la aplicación"""
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
            
            QLineEdit, QComboBox {{
                font-family: 'Segoe UI';
                font-size: 14px;
                border: 2px solid {self.colors['secondary']};
                border-radius: 6px;
                padding: 10px;
                background-color: {self.colors['surface']};
                color: #000000;
                selection-background-color: {self.colors['accent']};
            }}
            
            QComboBox {{
                color: #000000;
                background-color: #ffffff;
                border: 2px solid {self.colors['secondary']};
                padding: 8px 12px;
                font-size: 14px;
                font-weight: normal;
                min-height: 30px;
                height: 45px;
                min-width: 300px;
                width: 400px;
            }}
            
            QComboBox QAbstractItemView {{
                color: #000000;
                background-color: #ffffff;
                border: 1px solid {self.colors['secondary']};
                selection-background-color: {self.colors['accent']};
                selection-color: #ffffff;
                font-size: 14px;
                min-width: 350px;
            }}
            
            QComboBox QAbstractItemView::item {{
                color: #000000;
                background-color: #ffffff;
                padding: 10px 8px;
                border: none;
                min-height: 25px;
                font-size: 14px;
            }}
            
            QComboBox QAbstractItemView::item:selected {{
                color: #ffffff;
                background-color: {self.colors['accent']};
            }}
            
            QComboBox::drop-down {{
                border: none;
                background-color: {self.colors['secondary']};
                width: 20px;
                border-radius: 4px;
            }}
            
            QComboBox::down-arrow {{
                image: none;
                border: 2px solid {self.colors['surface']};
                width: 6px;
                height: 6px;
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
                min-width: 120px;
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
                line-height: 1.4;
            }}
            
            QScrollArea {{
                border: none;
                background-color: {self.colors['background']};
            }}
        """)

    def init_ui(self):
        """Inicializa la interfaz de usuario"""
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Título principal
        title = QLabel("🧾 Sistema de Gestión de Facturas")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {self.colors['primary']}; margin: 10px;")
        main_layout.addWidget(title)
        
        # Crear formulario
        self.create_form_group(main_layout)
        
        # Crear botones
        self.create_buttons(main_layout)
        
        # Crear área de resultados
        self.create_results_area(main_layout)

        # ScrollArea para el contenido
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(central_widget)
        self.setCentralWidget(scroll_area)
    
    def create_form_group(self, main_layout):
        """Crea el grupo de formulario para datos de facturación"""
        form_group = QGroupBox("📋 Datos de Facturación")
        form_layout = QFormLayout()
        form_layout.setVerticalSpacing(20)
        form_layout.setHorizontalSpacing(20)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        
        # Campo para número de factura (solo el número)
        self.numero_factura_edit = QLineEdit()
        self.numero_factura_edit.setPlaceholderText("Ej: 5, 10, 25...")
        self.numero_factura_edit.setMinimumHeight(35)
        self.numero_factura_edit.setMinimumWidth(150)
        self.numero_factura_edit.setMaximumWidth(200)
        self.numero_factura_edit.setStyleSheet("""
            QLineEdit {
                padding: 8px 12px;
                border: 2px solid #ddd;
                border-radius: 5px;
                background-color: white;
                color: #000000;
                font-size: 14px;
                font-weight: normal;
            }
            QLineEdit:focus {
                border-color: #5e81ac;
            }
        """)
        
        # Campo ID Factura completo (automático - solo lectura)
        self.id_factura_edit = QLineEdit()
        self.id_factura_edit.setPlaceholderText("Se generará automáticamente...")
        self.id_factura_edit.setMinimumHeight(35)
        self.id_factura_edit.setMinimumWidth(350)
        self.id_factura_edit.setReadOnly(True)
        self.id_factura_edit.setStyleSheet("""
            QLineEdit {
                background-color: #f8f9fa;
                color: #495057;
                font-style: italic;
                padding: 8px 12px;
                border: 2px solid #e9ecef;
                border-radius: 5px;
                font-size: 14px;
            }
        """)
        
        # Conectar evento para actualizar automáticamente
        self.numero_factura_edit.textChanged.connect(self.actualizar_id_factura)

        # ComboBox para pacientes
        self.paciente_combo = QComboBox()
        self.paciente_combo.setMinimumHeight(40)
        self.paciente_combo.setMinimumWidth(300)
        self.paciente_combo.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.paciente_combo.setStyleSheet("""
            QComboBox {
                padding: 8px 12px;
                border: 2px solid #ddd;
                border-radius: 5px;
                background-color: white;
                color: #000000;
                font-size: 14px;
                font-weight: normal;
                height: 40px;
                min-width: 300px;
            }
            QComboBox:focus {
                border-color: #5e81ac;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 25px;
                border-left: 1px solid #ddd;
                background-color: #f0f0f0;
            }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: #000000;
                selection-background-color: #e3f2fd;
                selection-color: #000000;
                border: 1px solid #ddd;
                font-size: 14px;
                min-width: 300px;
            }
            QComboBox QAbstractItemView::item {
                padding: 8px 12px;
                min-height: 25px;
                color: #000000;
                background-color: white;
            }
            QComboBox QAbstractItemView::item:selected {
                background-color: #e3f2fd;
                color: #000000;
            }
        """)
        
        # ComboBox para tratamientos
        self.tratamiento_combo = QComboBox()
        self.tratamiento_combo.setMinimumHeight(40)
        self.tratamiento_combo.setMinimumWidth(300)
        self.tratamiento_combo.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.tratamiento_combo.setStyleSheet("""
            QComboBox {
                padding: 8px 12px;
                border: 2px solid #ddd;
                border-radius: 5px;
                background-color: white;
                color: #000000;
                font-size: 14px;
                font-weight: normal;
                height: 40px;
                min-width: 300px;
            }
            QComboBox:focus {
                border-color: #5e81ac;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 25px;
                border-left: 1px solid #ddd;
                background-color: #f0f0f0;
            }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: #000000;
                selection-background-color: #e3f2fd;
                selection-color: #000000;
                border: 1px solid #ddd;
                font-size: 14px;
                min-width: 300px;
            }
            QComboBox QAbstractItemView::item {
                padding: 8px 12px;
                min-height: 25px;
                color: #000000;
                background-color: white;
            }
            QComboBox QAbstractItemView::item:selected {
                background-color: #e3f2fd;
                color: #000000;
            }
        """)
        
        # Agregar campos al formulario
        form_layout.addRow("🔢 Número de Factura:", self.numero_factura_edit)
        form_layout.addRow("🆔 ID Completo (Auto):", self.id_factura_edit)
        form_layout.addRow("👤 Paciente:", self.paciente_combo)
        form_layout.addRow("🦷 Tratamiento:", self.tratamiento_combo)
        
        form_group.setLayout(form_layout)
        main_layout.addWidget(form_group)
    
    def create_buttons(self, main_layout):
        """Crea los botones de acción"""
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        self.crear_btn = QPushButton("➕ Crear Factura")
        self.mostrar_btn = QPushButton("📋 Mostrar Facturas")
        self.limpiar_btn = QPushButton("🗑️ Limpiar Campos")
        self.actualizar_btn = QPushButton("🔄 Actualizar Datos")
        
        buttons_layout.addWidget(self.crear_btn)
        buttons_layout.addWidget(self.mostrar_btn)
        buttons_layout.addWidget(self.limpiar_btn)
        buttons_layout.addWidget(self.actualizar_btn)
        
        main_layout.addLayout(buttons_layout)
    
    def create_results_area(self, main_layout):
        """Crea el área de resultados"""
        resultado_label = QLabel("📊 Resultados:")
        resultado_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        resultado_label.setStyleSheet(f"color: {self.colors['primary']};")
        main_layout.addWidget(resultado_label)

        self.resultado_text = QTextEdit()
        self.resultado_text.setReadOnly(True)
        self.resultado_text.setMinimumHeight(250)
        self.resultado_text.setPlaceholderText("Los resultados aparecerán aquí...")
        main_layout.addWidget(self.resultado_text)
    
    def conectar_botones(self):
        """Conecta los botones con sus funciones"""
        self.crear_btn.clicked.connect(self.on_crear_factura)
        self.mostrar_btn.clicked.connect(self.on_mostrar_facturas)
        self.limpiar_btn.clicked.connect(self.on_limpiar_campos)
        self.actualizar_btn.clicked.connect(self.on_actualizar_datos)

    def on_actualizar_datos(self):
        """Manejador para el botón de actualizar datos"""
        # Esta señal la definiremos ahora
        self.actualizar_datos_signal.emit()
    
    def cargar_pacientes(self, pacientes):
        """Carga la lista de pacientes en el ComboBox"""
        self.paciente_combo.clear()
        self.paciente_combo.addItem("Seleccione un paciente", None)
        
        for paciente in pacientes:
            texto = f"{paciente.nombre} {paciente.apellido} - {paciente.dui}"
            self.paciente_combo.addItem(texto, paciente)

    def cargar_tratamientos(self, tratamientos):
        """Carga la lista de tratamientos en el ComboBox"""
        self.tratamiento_combo.clear()
        self.tratamiento_combo.addItem("Seleccione un tratamiento", None)
        
        for tratamiento in tratamientos:
            texto = f"{tratamiento.descripcion} - ${tratamiento.costo:.2f}"
            self.tratamiento_combo.addItem(texto, tratamiento)

    def on_crear_factura(self):
        """Manejador para el botón de crear factura"""
        print("🖱️ [DEBUG] Botón 'Crear Factura' clickeado")
        datos = self.get_datos_formulario()
        print(f"📋 [DEBUG] Datos obtenidos del formulario: {datos}")
        
        if datos:
            print("📤 [DEBUG] Emitiendo señal crear_factura_signal")
            self.crear_factura_signal.emit(datos)
            print("✅ [DEBUG] Señal emitida correctamente")
        else:
            print("❌ [DEBUG] No se obtuvieron datos del formulario")

    def on_mostrar_facturas(self):
        """Manejador para el botón de mostrar facturas"""
        self.mostrar_facturas_signal.emit()

    def on_limpiar_campos(self):
        """Manejador para el botón de limpiar campos"""
        self.limpiar_campos_signal.emit()

    def on_actualizar_datos(self):
        """Manejador para el botón de actualizar datos"""
        self.actualizar_datos_signal.emit()

    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        self.numero_factura_edit.clear()
        self.id_factura_edit.clear()
        self.paciente_combo.setCurrentIndex(0)
        self.tratamiento_combo.setCurrentIndex(0)

    def mostrar_mensaje(self, tipo, titulo, mensaje):
        """Muestra un mensaje al usuario"""
        if tipo == "success":
            QMessageBox.information(self, titulo, mensaje)
        elif tipo == "error":
            QMessageBox.critical(self, titulo, mensaje)
        elif tipo == "info":
            QMessageBox.information(self, titulo, mensaje)

    def actualizar_resultado(self, texto, limpiar=False):
        """Actualiza el área de resultados"""
        if limpiar:
            self.resultado_text.clear()
        self.resultado_text.append(texto)

    def agregar_factura_resultado(self, texto_factura):
        """Agrega una factura al área de resultados"""
        self.resultado_text.append(texto_factura)
        self.resultado_text.append("\n")

    def actualizar_id_factura(self):
        """Genera automáticamente el ID completo cuando cambia el número"""
        numero = self.numero_factura_edit.text().strip()
        
        if numero.isdigit():
            # Generar timestamp actual
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            
            # Crear ID completo
            id_completo = f"FAC-{numero}-{timestamp}"
            
            # Mostrar en el campo de solo lectura
            self.id_factura_edit.setText(id_completo)
            
            print(f"🆔 [AUTO] Número: {numero} → ID: {id_completo}")
        else:
            # Si no es un número válido, limpiar el campo
            self.id_factura_edit.setText("")
            if numero:  # Solo mostrar mensaje si hay texto
                print(f"⚠️ [AUTO] '{numero}' no es un número válido")

    def get_datos_formulario(self):
        """Obtiene los datos del formulario"""
        print("📋 [DEBUG] Obteniendo datos del formulario...")
        
        id_factura = self.id_factura_edit.text().strip()
        print(f"🆔 [DEBUG] ID Factura: '{id_factura}'")
        
        paciente = self.paciente_combo.currentData()
        print(f"👤 [DEBUG] Paciente seleccionado: {paciente}")
        
        tratamiento = self.tratamiento_combo.currentData()
        print(f"🦷 [DEBUG] Tratamiento seleccionado: {tratamiento}")
        
        datos = {
            'id_factura': id_factura,
            'paciente': paciente,
            'tratamiento': tratamiento
        }
        
        print(f"📦 [DEBUG] Datos preparados: {datos}")
        return datos