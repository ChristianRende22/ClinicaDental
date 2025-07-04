from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
                             QWidget, QLabel, QLineEdit, QPushButton, 
                             QTextEdit, QGroupBox, QFormLayout, QMessageBox,
                             QScrollArea, QComboBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from datetime import datetime
from typing import List, Dict, Any
class FacturacionView(QMainWindow):  
  
    # señales para comunicacion con el controlador
    crear_factura_signal = pyqtSignal(dict)
    mostrar_facturas_signal = pyqtSignal()
    limpiar_campos_signal = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.colors = {
            'primary': '#130760',      
            'secondary': '#756f9f',   
            'accent': '#10b8b9',       
            'background': '#2b2b2b',   
            'surface': '#3c3c3c',      
            'text_light': '#ffffff',   
            'text_dark': '#e0e0e0'     
        }
        self.init_ui()
        self.setup_styles()
        self.conectar_signals()
    
    def init_ui(self):
        """Inicializa la interfaz de usuario"""
        self.setWindowTitle("Gestión de facturas")
        self.setGeometry(100, 100, 900, 700)
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)

        # Titulo
        title = QLabel("🧾 Sistema de facturación dental")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"color: {self.colors['accent']}; padding: 20px;")
        main_layout.addWidget(title)
        
        # Formulario
        self.create_form_group(main_layout)
        # Botones de accion
        self.create_buttons(main_layout)
        # area de resultados
        self.create_results_area(main_layout)
        self.setCentralWidget(central_widget)
    
    def create_form_group(self, main_layout):
        # grupo formulario
        form_group = QGroupBox("Datos de facturación")
        form_layout = QFormLayout()
        form_layout.setVerticalSpacing(12)
        
        # campos del formulario
        self.id_factura_edit = QLineEdit()
        self.id_factura_edit.setPlaceholderText("Ej: FAC-001")
        
        self.fecha_edit = QLineEdit(datetime.now().strftime('%d/%m/%Y'))
        self.fecha_edit.setPlaceholderText("DD/MM/YYYY")
        
        self.servicio_edit = QLineEdit()
        self.servicio_edit.setPlaceholderText("Ej: Limpieza dental, extracción molar, radiografía")
        
        self.monto_edit = QLineEdit()
        self.monto_edit.setPlaceholderText("Ej: 50.00, 120.00, 30.00 (en el mismo orden)")
        
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
        #botones accion 
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        self.crear_btn = QPushButton("➕ Crear Factura")
        self.mostrar_btn = QPushButton("📋 Mostrar Facturas")
        self.limpiar_btn = QPushButton("🗑️ Limpiar")
        
        buttons_layout.addWidget(self.crear_btn)
        buttons_layout.addWidget(self.mostrar_btn)
        buttons_layout.addWidget(self.limpiar_btn)
        main_layout.addLayout(buttons_layout)
    
    def create_results_area(self, main_layout):
        #resultados
        resultado_group = QGroupBox("📊 Resultados")
        resultado_layout = QVBoxLayout()
        
        self.resultado_text = QTextEdit()
        self.resultado_text.setReadOnly(True)
        self.resultado_text.setPlaceholderText("Aquí aparecerán las facturas creadas...")
        
        resultado_layout.addWidget(self.resultado_text)
        resultado_group.setLayout(resultado_layout)
        main_layout.addWidget(resultado_group)
    
    def conectar_signals(self):
        #conecta las señales de los botones
        self.crear_btn.clicked.connect(self.on_crear_factura)
        self.mostrar_btn.clicked.connect(self.on_mostrar_facturas)
        self.limpiar_btn.clicked.connect(self.on_limpiar_campos)
    
    def setup_styles(self):
        #configura los estilos de la aplicación
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {self.colors['background']};
                color: {self.colors['text_light']};
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
            QLabel {{
                color: {self.colors['accent']};
                font-weight: bold;
                font-size: 12px;
            }}
            QLineEdit, QComboBox {{
                background-color: {self.colors['surface']};
                color: {self.colors['text_light']};
                border: 2px solid {self.colors['secondary']};
                border-radius: 5px;
                padding: 8px;
                font-size: 11px;
            }}
            QLineEdit:focus, QComboBox:focus {{
                border-color: {self.colors['accent']};
            }}
            QPushButton {{
                background-color: {self.colors['secondary']};
                color: white;
                padding: 10px 15px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 11px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {self.colors['accent']};
                transform: translateY(-2px);
            }}
            QPushButton:pressed {{
                background-color: {self.colors['primary']};
            }}
            QGroupBox {{
                color: {self.colors['text_light']};
                font-weight: bold;
                font-size: 13px;
                border: 2px solid {self.colors['secondary']};
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }}
            QGroupBox::title {{
                color: {self.colors['accent']};
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px;
            }}
            QTextEdit {{
                background-color: {self.colors['surface']};
                color: {self.colors['text_light']};
                border: 2px solid {self.colors['secondary']};
                border-radius: 5px;
                padding: 10px;
                font-family: 'Courier New', monospace;
                font-size: 10px;
            }}
        """)
    
    def cargar_pacientes(self, pacientes):
        #carga la lista de pacientes en el ComboBox
        self.paciente_combo.clear()
        if pacientes:
            for paciente in pacientes:
                self.paciente_combo.addItem(
                    f"{paciente.nombre} {paciente.apellido} - {paciente.dui}", 
                    paciente
                )
        else:
            self.paciente_combo.addItem("No hay pacientes disponibles", None)
    
    def obtener_datos_formulario(self) -> Dict[str, Any]:
        #obtiene los datos del formulario
        return {
            'id_factura': self.id_factura_edit.text().strip(),
            'paciente': self.paciente_combo.currentData(),
            'fecha': self.fecha_edit.text().strip(),
            'servicios': self.servicio_edit.text().strip(),
            'montos': self.monto_edit.text().strip(),
            'estado_pago': self.estado_pago_combo.currentText()
        }
    
    def limpiar_formulario(self):
        #limpiar campos
        self.id_factura_edit.clear()
        self.fecha_edit.setText(datetime.now().strftime('%d/%m/%Y'))
        self.servicio_edit.clear()
        self.monto_edit.clear()
        self.estado_pago_combo.setCurrentIndex(0)
        self.resultado_text.clear()
    
    def mostrar_mensaje(self, tipo: str, titulo: str, mensaje: str):
      #mensuaje al usuario
        if tipo == "error":
            QMessageBox.warning(self, titulo, mensaje)
        elif tipo == "info":
            QMessageBox.information(self, titulo, mensaje)
        elif tipo == "success":
            QMessageBox.information(self, titulo, mensaje)
    
    def actualizar_resultado(self, texto: str, limpiar: bool = False):
        #axtualizar"
        if limpiar:
            self.resultado_text.clear()
        self.resultado_text.append(texto)
    
    def agregar_factura_resultado(self, factura_str: str):
        #agrega una factura al area de resultados
        self.resultado_text.append(factura_str)
        self.resultado_text.append("\n")
    
    # metodos para manejar eventos 
    def on_crear_factura(self):
        # evento de crear factura
        datos = self.obtener_datos_formulario()
        self.crear_factura_signal.emit(datos)
    
    def on_mostrar_facturas(self):
        # evento de mostrar facturas
        self.mostrar_facturas_signal.emit()
    
    def on_limpiar_campos(self):
        #evento de limpiar campos
        self.limpiar_campos_signal.emit()

if __name__ == "__main__":
    app = QApplication([])
    ventana = FacturacionView()
    ventana.show()
    app.exec()