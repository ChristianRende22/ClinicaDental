from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
                             QWidget, QLabel, QLineEdit, QPushButton, 
                             QTextEdit, QGroupBox, QFormLayout, QMessageBox,
                             QScrollArea, QComboBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from datetime import datetime
from typing import List

class Paciente:
    def __init__(self, nombre: str, apellido: str, dui: str, edad: int = 0):
        self.nombre = nombre
        self.apellido = apellido
        self.dui = dui
        self.edad = edad

class Factura:
    def __init__(self, id_factura: str, paciente: Paciente, 
                 servicios: List[str], montos: List[float], fecha_emision: datetime, 
                 estado_pago: str):
        self.id_factura = id_factura
        self.paciente = paciente
        self.servicios = servicios
        self.montos = montos
        self.monto_total = sum(montos)
        self.fecha_emision = fecha_emision
        self.estado_pago = estado_pago

    def __str__(self):
        servicios_str = "\n".join(f"   - {servicio}: ${monto:.2f}" 
                                 for servicio, monto in zip(self.servicios, self.montos))
        return (f"🧾 Factura ID: {self.id_factura}\n"
                f"📅 Fecha: {self.fecha_emision.strftime('%d/%m/%Y')}\n"
                f"👤 Paciente: {self.paciente.nombre} {self.paciente.apellido}\n"
                f"📋 DUI: {self.paciente.dui}\n"
                f"🩺 Servicios:\n{servicios_str}\n"
                f"💰 Estado: {self.estado_pago}\n"
                f"💵 Total: ${self.monto_total:.2f}\n"
                f"{'='*30}")

class FacturaWindow(QMainWindow):
    def __init__(self, pacientes: List[Paciente]):
        super().__init__()
        self.setWindowTitle("Gestión de facturas")
        self.setGeometry(100, 100, 900, 700)
        self.colors = {
            'primary': '#130760',      
            'secondary': '#756f9f',   
            'accent': '#10b8b9',       
            'background': '#2b2b2b',   
            'surface': '#3c3c3c',      
            'text_light': '#ffffff',   
            'text_dark': '#e0e0e0'     
        }

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

        self.facturas: List[Factura] = []  # lista de facturas
        self.pacientes = pacientes  # lista de pacientes existentes
        self.init_ui()
    
    def init_ui(self):
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)

        # titulo
        title = QLabel("🧾 Sistema de facturación dental")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"color: {self.colors['accent']}; padding: 20px;")
        main_layout.addWidget(title)
        
        # form
        form_group = QGroupBox("Datos de facturación")
        form_layout = QFormLayout()
        form_layout.setVerticalSpacing(12)
        
        self.id_factura_edit = QLineEdit()
        self.id_factura_edit.setPlaceholderText("Ej: FAC-001")
        
        self.fecha_edit = QLineEdit(datetime.now().strftime('%d/%m/%Y'))
        self.fecha_edit.setPlaceholderText("DD/MM/YYYY")
        #aqui ponemos ejemplos de algunos servicios 
        self.servicio_edit = QLineEdit()
        self.servicio_edit.setPlaceholderText("Ej: Limpieza dental, extracción molar, radiografía")
        
        # indicamos como poner los precios de los servicios por , 
        self.monto_edit = QLineEdit()
        self.monto_edit.setPlaceholderText("Ej: 50.00, 120.00, 30.00 (en el mismo orden)")
        
        # elegimos un paciente de los hipoteticamente creados 
        self.paciente_combo = QComboBox()
        if self.pacientes:
            for paciente in self.pacientes:
                self.paciente_combo.addItem(
                    f"{paciente.nombre} {paciente.apellido} - {paciente.dui}", 
                    paciente
                )
        else:
            self.paciente_combo.addItem("No hay pacientes disponibles", None)
        
        # pago
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
        
        # Botones de acción
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        self.crear_btn = QPushButton("➕ Crear Factura")
        self.crear_btn.clicked.connect(self.crear_factura)
        
        self.mostrar_btn = QPushButton("📋 Mostrar Facturas")
        self.mostrar_btn.clicked.connect(self.mostrar_facturas)
        
        self.limpiar_btn = QPushButton("🗑️ Limpiar")
        self.limpiar_btn.clicked.connect(self.limpiar_campos)
        
        buttons_layout.addWidget(self.crear_btn)
        buttons_layout.addWidget(self.mostrar_btn)
        buttons_layout.addWidget(self.limpiar_btn)
        main_layout.addLayout(buttons_layout)
        
        # resultados
        resultado_group = QGroupBox("📊 Resultados")
        resultado_layout = QVBoxLayout()
        
        self.resultado_text = QTextEdit()
        self.resultado_text.setReadOnly(True)
        self.resultado_text.setPlaceholderText("Aquí aparecerán las facturas creadas...")
        
        resultado_layout.addWidget(self.resultado_text)
        resultado_group.setLayout(resultado_layout)
        main_layout.addWidget(resultado_group)
        
        self.setCentralWidget(central_widget)

    def crear_factura(self):
        id_factura = self.id_factura_edit.text().strip()
        paciente = self.paciente_combo.currentData()
        fecha_str = self.fecha_edit.text().strip()
        servicios_str = self.servicio_edit.text().strip()
        montos_str = self.monto_edit.text().strip()
        estado_pago = self.estado_pago_combo.currentText()
        
        # validaciones
        if not id_factura:
            QMessageBox.warning(self, "⚠️ Error", "El ID de factura es obligatorio")
            return
            
        if paciente is None:
            QMessageBox.warning(self, "⚠️ Error", "Debe seleccionar un paciente")
            return
            
        if not servicios_str:
            QMessageBox.warning(self, "⚠️ Error", "La descripción del servicio es obligatoria")
            return
            
        # ver si ya hay una con el mismo ID
        if any(f.id_factura == id_factura for f in self.facturas):
            QMessageBox.warning(self, "⚠️ Error", "Ya existe una factura con este ID")
            return
            
        try:
            fecha = datetime.strptime(fecha_str, '%d/%m/%Y')
        except ValueError:
            QMessageBox.warning(self, "⚠️ Error", "Formato de fecha inválido (DD/MM/YYYY)")
            return
        
        #  servicios y $
        try:
            servicios = [s.strip() for s in servicios_str.split(',') if s.strip()]
            
            if montos_str:
                montos = [float(m.strip()) for m in montos_str.split(',') if m.strip()]
            else:
                montos = [0.0] * len(servicios)
            
            # ver que haya la misma cantidad 
            if len(servicios) != len(montos):
                QMessageBox.warning(self, "⚠️ Error", 
                                   f"Número de servicios ({len(servicios)}) no coincide con número de montos ({len(montos)})")
                return
            
            # que sean numeros positivos
            if any(m <= 0 for m in montos):
                QMessageBox.warning(self, "⚠️ Error", "Todos los montos deben ser mayores a 0")
                return
                
        except ValueError:
            QMessageBox.warning(self, "⚠️ Error", "Los montos deben ser números válidos separados por comas")
            return
        
        nueva_factura = Factura(
            id_factura=id_factura,
            paciente=paciente,
            servicios=servicios,
            montos=montos,
            fecha_emision=fecha,
            estado_pago=estado_pago
        )
        
        self.facturas.append(nueva_factura)
        QMessageBox.information(self, "✅ Éxito", 
                               f"Factura '{id_factura}' creada correctamente\n"
                               f"Servicios: {len(servicios)}\n"
                               f"Total: ${nueva_factura.monto_total:.2f}")
        
        #aqui  mostramos la factura
        self.resultado_text.append(str(nueva_factura))
        self.resultado_text.append("\n")

    def mostrar_facturas(self):
        self.resultado_text.clear()
        if not self.facturas:
            QMessageBox.information(self, "ℹ️ Información", "No hay facturas registradas")
            self.resultado_text.append("📋 No hay facturas registradas en el sistema.")
            return
            
        self.resultado_text.append(f"📊 RESUMEN DE FACTURAS ({len(self.facturas)} total)\n")
        self.resultado_text.append("="*60 + "\n")
        
        total_general = 0
        for i, factura in enumerate(self.facturas, 1):
            self.resultado_text.append(f"FACTURA #{i}")
            self.resultado_text.append(str(factura))
            self.resultado_text.append("\n")
            total_general += factura.monto_total
            
        self.resultado_text.append("="*60)
        self.resultado_text.append(f"TOTAL GENERAL: ${total_general:.2f}")

    def limpiar_campos(self):
        self.id_factura_edit.clear()
        self.fecha_edit.setText(datetime.now().strftime('%d/%m/%Y'))
        self.servicio_edit.clear()
        self.monto_edit.clear()
        self.estado_pago_combo.setCurrentIndex(0)
        self.resultado_text.clear()

def main():
    app = QApplication([])
    
    # igual aqui creamos pacientes hipoteticos y luego al sql
    pacientes = [
        Paciente(nombre="Laura", apellido="Pérez", dui="12345678-9", edad=27),
        Paciente(nombre="Juan", apellido="Gómez", dui="87654321-0", edad=30),
        Paciente(nombre="María", apellido="González", dui="11111111-1", edad=35),
        Paciente(nombre="Carlos", apellido="Rodríguez", dui="22222222-2", edad=42)
    ]
    
    window = FacturaWindow(pacientes)
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
