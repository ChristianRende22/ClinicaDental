import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QVBoxLayout, QLabel, QLineEdit, 
    QTextEdit, QComboBox, QPushButton, QDateEdit,
    QDialogButtonBox, QApplication, QHBoxLayout, QCalendarWidget,
    QMessageBox
)
from PyQt6.QtCore import QDate

from Controladores.TratamientoControlador import TratamientoControlador
from Modelos.PacienteModelo import Paciente

class AgregarTratamientoDialog(QDialog):
    def __init__(self, paciente):
        super().__init__()
        self.paciente = paciente  
        self.controlador = TratamientoControlador(self)

        self.setWindowTitle("🩺 Agregar Tratamiento")
        self.resize(500, 500)
        
        self.setStyleSheet("""
            QDialog { 
                background-color: #f7f8fa; 
                color: #2c2c2c; 
                font: 14px 'Segoe UI'; 
            }
            QLabel { 
                font-weight: bold; 
                color: #2c2c2c;
            }
            QLineEdit, QTextEdit, QComboBox, QDateEdit {
                background: white; 
                color: #2c2c2c; 
                border: 2px solid #756f9f;
                border-radius: 6px; 
                padding: 6px;
                font-size: 14px;
            }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QDateEdit:focus {
                border-color: #10b8b9;
                background-color: #fdfcf8;
            }
            QPushButton {
                background: #756f9f; 
                color: white; 
                padding: 8px 15px;
                border-radius: 8px; 
                font-weight: bold;
                border: none;
            }
            QPushButton:hover { 
                background: #10b8b9; 
            }
            
            QPushButton:hover { 
                background: #10b8b9; 
            }

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
                transform: rotate(45deg);
            }}
            
            QCalendarWidget {{
                background-color: #ffffff;
                color: #2c3e50;
                border: 3px solid #756f9f;
                border-radius: 12px;
                font-family: 'Segoe UI';
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
                transform: scale(1.05);
            }}
            
            QCalendarWidget QToolButton:pressed {{
                background-color: #130760;
                transform: scale(0.95);
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
                transform: rotate(45deg);
            }}
            
            QCalendarWidget QSpinBox::down-arrow {{
                image: none;
                border: 2px solid #ffffff;
                width: 4px;
                height: 4px;
                border-top: none;
                border-left: none;
                margin: 2px;
                transform: rotate(45deg);
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
        """)

        form = QFormLayout()
        
        patient_label = QLabel(f"Paciente: {self.paciente.nombre} {self.paciente.apellido}")
        patient_label.setStyleSheet("color: #10b8b9; font-weight: bold; font-size: 16px;")
        form.addRow(patient_label)

        # Tratamientos comunes (combo)
        self.tratamientos = {
            "Limpieza dental": 100.00,
            "Extracción simple": 150.00,
            "Obturación (empaste)": 200.00,
            "Endodoncia": 500.00,
            "Profilaxis dental": 120.00,
            "Blanqueamiento dental": 700.00,
            "Corona dental": 1000.00,
            "Implante dental": 2500.00,
            "Ortodoncia": 3000.00,
            "Consulta general": 80.00
        }
        self.tratamiento_combo = QComboBox()
        self.tratamiento_combo.addItems(self.tratamientos.keys())
        self.tratamiento_combo.currentIndexChanged.connect(self.actualizar_costo)
        form.addRow("Tratamiento:", self.tratamiento_combo)

        # Costo, solo lectura
        self.costo_edit = QLineEdit()
        self.costo_edit.setReadOnly(True)
        self.costo_edit.setText(f"${self.tratamientos[self.tratamiento_combo.currentText()]:.2f}")
        form.addRow("Costo:", self.costo_edit)

        # Descripción
        self.descripcion_edit = QTextEdit()
        self.descripcion_edit.setMaximumHeight(80)
        form.addRow("Descripción:", self.descripcion_edit)

        # Fecha con calendario
        self.fecha_edit = QDateEdit()
        self.fecha_edit.setCalendarPopup(True)
        self.fecha_edit.setDisplayFormat("dd/MM/yyyy")
        self.fecha_edit.setDate(QDate.currentDate())
        form.addRow("Fecha:", self.fecha_edit)

        # Estado (enum)
        self.estado_combo = QComboBox()
        self.estado_combo.addItems(['Pendiente', 'En_Progreso', 'Finalizado'])
        form.addRow("Estado:", self.estado_combo)

        # Doctor: carnet + botón verificar + label nombre
        self.doctor_carnet_edit = QLineEdit()
        self.doctor_carnet_edit.setPlaceholderText("Ingrese carnet de doctor")
        self.verificar_doctor_btn = QPushButton("Verificar Doctor")
        self.verificar_doctor_btn.clicked.connect(self.verificar_doctor)

        self.doctor_nombre_label = QLabel("Nombre Doctor: ---")

        hbox_doctor = QVBoxLayout()
        hbox_doctor_inner = QHBoxLayout()
        hbox_doctor_inner.addWidget(self.doctor_carnet_edit)
        hbox_doctor_inner.addWidget(self.verificar_doctor_btn)
        hbox_doctor.addLayout(hbox_doctor_inner)
        hbox_doctor.addWidget(self.doctor_nombre_label)

        form.addRow("Carnet Doctor:", hbox_doctor)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.on_accepted)
        buttons.rejected.connect(self.reject)

        main = QVBoxLayout()
        main.addLayout(form)
        main.addWidget(buttons)
        self.setLayout(main)

    def actualizar_costo(self):
        tratamiento = self.tratamiento_combo.currentText()
        costo = self.tratamientos.get(tratamiento, 0)
        self.costo_edit.setText(f"${costo:.2f}")

    def verificar_doctor(self):
        carnet = self.doctor_carnet_edit.text().strip()
        self.controlador.verificar_doctor(carnet)
        
    def mostrar_mensaje(self, titulo, mensaje):
        QMessageBox.warning(self, titulo, mensaje)
        
    def mostrar_nombre_doctor(self, texto):
        self.doctor_nombre_label.setText(texto)
        
    def preguntar_registro_doctor(self):
        respuesta = QMessageBox.question(self, "Doctor no existe", "El doctor no existe. ¿Desea registrar uno nuevo?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        return respuesta == QMessageBox.StandardButton.Yes

    def abrir_registro_doctor(self):
        QMessageBox.information(self, "Registro Doctor", "Aquí abriría la ventana para registrar un doctor.")

    def on_accepted(self):
        
        tratamiento = self.tratamiento_combo.currentText()
        costo_text = self.costo_edit.text().replace("$", "")
        try:
            costo = float(costo_text)
        except ValueError:
            costo = 0
            
        fecha = self.fecha_edit.date()
        estado = self.estado_combo.currentText()
        carnet_doctor = self.doctor_carnet_edit.text().strip()
        self.verificar_doctor()
        nombre_doctor = self.doctor_nombre_label.text()
        
        # Validar datos llamando al controlador
        if not self.controlador.validar_datos(tratamiento, costo, fecha, estado, carnet_doctor, nombre_doctor):
            return
        
        tratamiento_obj = self.controlador.crear_tratamiento(
            id_tratamiento=None,  # Manejar el autoincremento
            descripcion=self.descripcion_edit.toPlainText(),
            costo=costo,
            fecha=fecha.toString("yyyy-MM-dd"),
            estado=estado,
            doctor_nombre=nombre_doctor.replace("Nombre Doctor: ", ""),
            doctor_apellido="",  # Por simplicidad, no capturamos apellido aquí
            paciente=self.paciente
        )
            
        print("Tratamiento registrado con datos:")
        print(f"Tratamiento: {tratamiento}")
        print(f"Costo: {costo}")
        print(f"Descripción: {self.descripcion_edit.toPlainText()}")
        print(f"Fecha: {fecha.toString('dd/MM/yyyy')}")
        print(f"Estado: {estado}")
        print(f"Carnet Doctor: {carnet_doctor}")
        print(nombre_doctor)

        self.accept()
        
def main():
    paciente = Paciente(
        nombre="Ana",
        apellido="Gómez",
        fecha_nacimiento="21/05/1990", 
        dui="12345678-9",
        telefono=12345678,
        correo="ana@gmail.com"
    )
    
    app = QApplication([])
    window = AgregarTratamientoDialog(paciente)  
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
