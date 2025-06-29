from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit, QPushButton,
    QTextEdit, QGroupBox, QFormLayout, QMessageBox, QComboBox, QDateTimeEdit, QInputDialog, QScrollArea
)
from PyQt6.QtCore import Qt, QDateTime
from PyQt6.QtGui import QFont
from datetime import datetime
from Vistas.DoctorVista import Doctor  

class Paciente:
    def __init__(self, nombre, apellido):
        self.nombre = nombre
        self.apellido = apellido
    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Cita:
    """
    Clase que representa una cita en la clínica dental.
    Contiene información sobre el paciente, el doctor, el horario y el estado de la cita.
    """
    def __init__(self, id_cita: str, paciente, doctor, hora_inicio: datetime, hora_fin: datetime, costo_cita: float):
        self.id_cita = id_cita                  # Identificador único de la cita
        self.paciente = paciente                # Paciente asociado a la cita
        self.doctor = doctor                    # Doctor asociado a la cita
        self.hora_inicio = hora_inicio          # Fecha y hora de inicio de la cita
        self.hora_fin = hora_fin                # Fecha y hora de fin de la cita
        self.costo_cita = costo_cita            # Costo de la cita
        self.estado = "Pendiente"               # Por defecto, la cita está pendiente

    def __str__(self):
        return (
            f"ID Cita: {self.id_cita}\n"
            f"Paciente: {self.paciente.nombre} {self.paciente.apellido}\n"
            f"Doctor: {self.doctor.nombre} {self.doctor.apellido}\n"
            f"Fecha y Hora Inicio: {self.hora_inicio.strftime('%d/%m/%Y %H:%M')}\n"
            f"Fecha y Hora Fin: {self.hora_fin.strftime('%d/%m/%Y %H:%M')}\n"
            f"Estado: {self.estado}\n"
            f"Costo: ${self.costo_cita:.2f}\n"
        )


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
        self.crear_btn.clicked.connect(self.crear_cita)
        self.cancelar_btn = QPushButton("❌ Cancelar Cita")
        self.cancelar_btn.clicked.connect(self.cancelar_cita)
        self.modificar_btn = QPushButton("✏️ Modificar Cita")
        self.modificar_btn.clicked.connect(self.modificar_cita)

        buttons_row1.addWidget(self.crear_btn)
        buttons_row1.addWidget(self.cancelar_btn)
        buttons_row1.addWidget(self.modificar_btn)

        # Segunda fila de botones
        buttons_row2 = QHBoxLayout()
        self.confirmar_btn = QPushButton("✅ Confirmar Asistencia")
        self.confirmar_btn.clicked.connect(self.confirmar_asistencia)
        self.monto_btn = QPushButton("💲 Calcular Monto a Pagar")
        self.monto_btn.clicked.connect(self.calcular_monto)

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

    def crear_cita(self):
        """Crea una nueva cita verificando disponibilidad de la Cita"""
        self.resultado_text.clear()
        id_cita = self.id_edit.text().strip()
        paciente_idx = self.paciente_combo.currentIndex()
        doctor_idx = self.doctor_combo.currentIndex()
        tratamiento_idx = self.tratamiento_combo.currentIndex()
        hora_inicio = self.fecha_inicio_edit.dateTime().toPyDateTime()
        hora_fin = self.fecha_fin_edit.dateTime().toPyDateTime()
        costo = self.costo_edit.text().strip()
        estado = self.estado_combo.currentText()

        if not id_cita or paciente_idx == -1 or doctor_idx == -1 or tratamiento_idx == -1 or not costo:
            QMessageBox.warning(self, "❌ Error", "Todos los campos son obligatorios.")
            return

        # Verificar disponibilidad del doctor
        doctor = self.doctores[doctor_idx]
        for cita in self.citas:
            if cita.doctor == doctor and not (hora_fin <= cita.hora_inicio or hora_inicio >= cita.hora_fin):
                QMessageBox.warning(self, "❌ Error", "El doctor no está disponible en ese horario.")
                return

        paciente = self.pacientes[paciente_idx]
        tratamiento = self.tratamientos[tratamiento_idx]
        nueva_cita = Cita(id_cita, paciente, doctor, hora_inicio, hora_fin, float(costo))
        nueva_cita.tratamiento = tratamiento  
        nueva_cita.estado = estado

        self.citas.append(nueva_cita)
        self.resultado_text.append(f"Cita creada:\n{nueva_cita}")
        QMessageBox.information(self, "✅ Éxito", "Cita creada exitosamente.")
        self.limpiar_campos()

    def cancelar_cita(self):
        """Cancela una cita por ID"""
        self.resultado_text.clear()
        id_cita, ok = QInputDialog.getText(self, "Cancelar Cita", "Ingrese el ID de la cita a cancelar:")
        if not ok or not id_cita.strip():
            return
        for cita in self.citas:
            if cita.id_cita == id_cita.strip():
                cita.estado = "Cancelada"
                self.resultado_text.append(f"Cita cancelada:\n{cita}")
                QMessageBox.information(self, "✅ Éxito", "Cita cancelada exitosamente.")
                return
        QMessageBox.warning(self, "❌ Error", "No se encontró la cita.")

    def modificar_cita(self):
        """Permite modificar fecha y hora de una cita"""
        self.resultado_text.clear()
        id_cita, ok = QInputDialog.getText(self, "Modificar Cita", "Ingrese el ID de la cita a modificar:")
        if not ok or not id_cita.strip():
            return
        for cita in self.citas:
            if cita.id_cita == id_cita.strip():
                # Cargar datos actuales
                self.id_edit.setText(cita.id_cita)
                self.fecha_inicio_edit.setDateTime(QDateTime(cita.hora_inicio))
                self.fecha_fin_edit.setDateTime(QDateTime(cita.hora_fin))
                # El usuario puede modificar y luego presionar "Crear Cita" para guardar cambios
                self.editando_cita = cita
                QMessageBox.information(self, "Modificar Cita", "Modifique los campos y presione 'Crear Cita' para guardar cambios.")
                return
        QMessageBox.warning(self, "❌ Error", "No se encontró la cita.")

    def confirmar_asistencia(self):
        """Confirma si se asistió a la cita"""
        self.resultado_text.clear()
        id_cita, ok = QInputDialog.getText(self, "Confirmar Asistencia", "Ingrese el ID de la cita:")
        if not ok or not id_cita.strip():
            return
        for cita in self.citas:
            if cita.id_cita == id_cita.strip():
                cita.estado = "Asistida"
                self.resultado_text.append(f"Asistencia confirmada:\n{cita}")
                QMessageBox.information(self, "✅ Éxito", "Asistencia confirmada.")
                return
        QMessageBox.warning(self, "❌ Error", "No se encontró la cita.")

    def calcular_monto(self):
        """Calcula el monto a pagar según el tipo de consulta y tratamiento"""
        self.resultado_text.clear()
        id_cita, ok = QInputDialog.getText(self, "Calcular Monto", "Ingrese el ID de la cita:")
        if not ok or not id_cita.strip():
            return
        for cita in self.citas:
            if cita.id_cita == id_cita.strip():
                costo_cita = cita.costo_cita
                costo_tratamiento = getattr(cita, 'tratamiento', {}).get('costo', 0)
                total = costo_cita + costo_tratamiento
                self.resultado_text.append(
                    f"Monto a pagar para la cita {cita.id_cita}:\n"
                    f"Consulta: ${costo_cita:.2f}\n"
                    f"Tratamiento: ${costo_tratamiento:.2f}\n"
                    f"Total: ${total:.2f}\n"
                )
                QMessageBox.information(self, "Monto a Pagar", f"Total a pagar: ${total:.2f}")
                return
        QMessageBox.warning(self, "❌ Error", "No se encontró la cita.")

    def limpiar_campos(self):
        self.id_edit.clear()
        self.fecha_inicio_edit.setDateTime(QDateTime.currentDateTime())
        self.fecha_fin_edit.setDateTime(QDateTime.currentDateTime())
        self.costo_edit.clear()
        self.estado_combo.setCurrentIndex(0)
        self.paciente_combo.setCurrentIndex(0)
        self.doctor_combo.setCurrentIndex(0)
        self.tratamiento_combo.setCurrentIndex(0)

def main():
    # Simulacion para pruebas
    doctores = [
        Doctor("Melisa", "Rivas", "12345678-9", "Cirujano Dentista", 12345678, "correo@gmail.com"), 
        Doctor("Carlos", "López", "98765432-1", "Ortodontista", 87654321, "coreo1@gmail.com")
        ]
    pacientes = [
        Paciente("Juan", "Pérez"), 
        Paciente("Ana", "Gómez")
        ]
    tratamientos = [{'descripcion': 'Limpieza', 'costo': 20.0}]
    app = QApplication([])
    window = CitaWindow(doctores, pacientes, tratamientos)
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
