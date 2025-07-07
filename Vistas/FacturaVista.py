import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
                             QWidget, QLabel, QLineEdit, QPushButton, 
                             QTextEdit, QGroupBox, QFormLayout, QMessageBox,
                             QComboBox, QScrollArea) 
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QDoubleValidator 
from datetime import datetime
from typing import List, Dict, Any

class FacturacionView(QMainWindow):  
    crear_factura_signal = pyqtSignal(dict)
    mostrar_facturas_signal = pyqtSignal()
    limpiar_campos_signal = pyqtSignal()
    
    def __init__(self):
        super().__init__()

        self.colors = {
            'primary': '#130760',      # Dark blue-purple 
            'secondary': '#756f9f',    # Medium purple
            'accent': '#10b8b9',       # Teal
            'text_light': '#2b2b2b',   # Dark gray
            'text_dark': '#3c3c3c',    # Slightly lighter gray
            'background': '#f7f8fa',   # White text
            'surface': '#ffffff'       # Light gray text
        }

        self.setWindowTitle("Gestión de Facturas - Clínica Dental") 
        self.setGeometry(100, 100, 900, 700)
        
        self.setup_styles()  # Configurar estilos
        self.init_ui()       # Inicializar la interfaz
        self.conectar_botones()  # Conectar los botones

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
        """)

    def init_ui(self):
        """Inicializa la interfaz de usuario"""
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Título
        title = QLabel("🧾 Sistema de Gestión de Facturas")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        main_layout.addWidget(title)
        
        # Formulario
        self.create_form_group(main_layout)
        # Botones de acción
        self.create_buttons(main_layout)
        # Área de resultados
        self.create_results_area(main_layout)

        # Creamos el ScrollArea para envolver todo el contenido principal
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(central_widget)
        self.setCentralWidget(scroll_area)
    
    def create_form_group(self, main_layout):
        # Grupo formulario
        form_group = QGroupBox("Datos de Facturación")
        form_layout = QFormLayout()
        
        # Campos del formulario
        self.id_factura_edit = QLineEdit()
        self.id_factura_edit.setPlaceholderText("Ej: FAC-001")
        
        self.fecha_edit = QLineEdit(datetime.now().strftime('%d/%m/%Y'))
        self.fecha_edit.setPlaceholderText("DD/MM/YYYY")
        
        self.servicio_edit = QLineEdit()
        self.servicio_edit.setPlaceholderText("Ej: Limpieza dental, extracción molar, radiografía")
        
        self.monto_edit = QLineEdit()
        self.monto_edit.setPlaceholderText("Ej: 50.00, 120.00, 30.00 (en el mismo orden)")
        costo_validator = QDoubleValidator(0.0, 999999.99, 2)
        self.monto_edit.setValidator(costo_validator)
        
        self.paciente_combo = QComboBox()
        self.estado_pago_combo = QComboBox()
        self.estado_pago_combo.addItems(["Pendiente", "Pagado", "Cancelado"])
        
        form_layout.addRow("🆔 ID Factura:", self.id_factura_edit)
        form_layout.addRow("👤 Paciente:", self.paciente_combo)
        form_layout.addRow("📅 Fecha:", self.fecha_edit)
        form_layout.addRow("🩺 Servicio:", self.servicio_edit)
        form_layout.addRow("💵 Monto ($):", self.monto_edit)
        form_layout.addRow("💰 Estado Pago:", self.estado_pago_combo)
        
        form_group.setLayout(form_layout)
        main_layout.addWidget(form_group)
    
    def create_buttons(self, main_layout):
        # Botones de acción
        buttons_layout = QHBoxLayout()
        
        self.crear_btn = QPushButton("➕ Crear Factura")
        self.mostrar_btn = QPushButton("📋 Mostrar Facturas")
        self.limpiar_btn = QPushButton("🗑️ Limpiar")
        
        buttons_layout.addWidget(self.crear_btn)
        buttons_layout.addWidget(self.mostrar_btn)
        buttons_layout.addWidget(self.limpiar_btn)
        main_layout.addLayout(buttons_layout)
    
    def create_results_area(self, main_layout):
        # Resultados
        resultado_label = QLabel("📊 Resultados:")
        resultado_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        main_layout.addWidget(resultado_label)

        self.resultado_text = QTextEdit()
        self.resultado_text.setReadOnly(True)
        main_layout.addWidget(self.resultado_text)
    
    def conectar_botones(self):
        # Conecta las señales de los botones
        self.crear_btn.clicked.connect(self.on_crear_factura)
        self.mostrar_btn.clicked.connect(self.on_mostrar_facturas)
        self.limpiar_btn.clicked.connect(self.on_limpiar_campos)
    
    def cargar_pacientes(self, pacientes):
        # Carga la lista de pacientes en el ComboBox
        self.paciente_combo.clear()
        if pacientes:
            for paciente in pacientes:
                self.paciente_combo.addItem(f"{paciente.nombre} {paciente.apellido}", paciente)
        else:
            self.paciente_combo.addItem("No hay pacientes disponibles", None)
    
    def obtener_datos_formulario(self) -> Dict[str, Any]:
        # Obtiene los datos del formulario
        return {
            'id_factura': self.id_factura_edit.text().strip(),
            'paciente': self.paciente_combo.currentData(),
            'fecha': self.fecha_edit.text().strip(),
            'servicios': self.servicio_edit.text().strip(),
            'montos': self.monto_edit.text().strip(),
            'estado_pago': self.estado_pago_combo.currentText()
        }
    
    def limpiar_formulario(self):
        # Limpiar campos
        self.id_factura_edit.clear()
        self.fecha_edit.setText(datetime.now().strftime('%d/%m/%Y'))
        self.servicio_edit.clear()
        self.monto_edit.clear()
        self.estado_pago_combo.setCurrentIndex(0)
        self.resultado_text.clear()
    
    def mostrar_mensaje(self, tipo: str, titulo: str, mensaje: str):
        # Mensaje al usuario
        if tipo == "error":
            QMessageBox.warning(self, titulo, mensaje)
        elif tipo == "info":
            QMessageBox.information(self, titulo, mensaje)
        elif tipo == "success":
            QMessageBox.information(self, titulo, mensaje)
    
    def agregar_factura_resultado(self, factura_str: str):
        # Agrega una factura al área de resultados
        self.resultado_text.append(factura_str)
        self.resultado_text.append("\n")
    
    def actualizar_resultado(self, texto: str, limpiar: bool = False):
        # Actualiza el área de resultados
        if limpiar:
            self.resultado_text.clear()
        self.resultado_text.append(texto)
    
    # Métodos para manejar eventos (conectados a las señales)
    def on_crear_factura(self):
        # Evento de crear factura
        datos = self.obtener_datos_formulario()
        self.crear_factura_signal.emit(datos)
    
    def on_mostrar_facturas(self):
        # Evento de mostrar facturas
        self.mostrar_facturas_signal.emit()
    
    def on_limpiar_campos(self):
        # Evento de limpiar campos
        self.limpiar_campos_signal.emit()

# Función principal para ejecutar la aplicación
def main():
    app = QApplication(sys.argv)
    view = FacturacionView()
    from Controladores.FacturaControlador import FacturacionController
    controller = FacturacionController(view)
    view.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
