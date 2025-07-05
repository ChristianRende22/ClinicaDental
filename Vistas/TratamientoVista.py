import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QVBoxLayout, QLabel, QLineEdit, 
    QTextEdit, QComboBox, QPushButton, QDateEdit,
    QDialogButtonBox, QApplication, QHBoxLayout, QCalendarWidget
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
        self.resize(600, 700)
        
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
            
                        QCalendarWidget {
                background-color: #f7f8fa;
                color: #2c3e50;
            }

            QCalendarWidget QMenu {
                background-color: #ffffff;
                color: #2c3e50;
            }

            QCalendarWidget QSpinBox {
                background-color: #ffffff;
                color: #2c3e50;
            }

            QCalendarWidget QAbstractItemView {
                background-color: #ffffff;
                color: #2c3e50;
            }

            QCalendarWidget QAbstractItemView:enabled {
                color: #2c3e50;
                background-color: #ffffff;
            }

            QCalendarWidget QAbstractItemView:disabled {
                color: #999999;
            }

            QCalendarWidget QWidget {
                alternate-background-color: #f7f8fa;
            }

            QCalendarWidget QTableView {
                gridline-color: #e0e0e0;
                background-color: #ffffff;
            }
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
        self.fecha_edit = QCalendarWidget()
        self.fecha_edit.setSelectedDate(QDate.currentDate())
        self.fecha_edit.setGridVisible(True)
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
        if not carnet:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Validación", "Ingrese el carnet del doctor.")
            return
        
        # Simulación búsqueda en BD
        doctores_simulados = {
            "DOC123": "Juan Pérez",
            "DOC456": "María López",
            "DOC789": "Carlos Gómez"
        }

        nombre = doctores_simulados.get(carnet)
        if nombre:
            self.doctor_nombre_label.setText(f"Nombre Doctor: {nombre}")
        else:
            self.doctor_nombre_label.setText("Doctor no encontrado, debe registrarlo.")
            from PyQt6.QtWidgets import QMessageBox
            respuesta = QMessageBox.question(
                self, "Doctor no existe",
                "El doctor no existe. ¿Desea registrar uno nuevo?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if respuesta == QMessageBox.StandardButton.Yes:
                self.abrir_registro_doctor()

    def abrir_registro_doctor(self):
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.information(self, "Registro Doctor", "Aquí abriría la ventana para registrar un doctor.")

    def on_accepted(self):
        from PyQt6.QtWidgets import QMessageBox

        # Validar fecha
        fecha_str = self.fecha_edit.selectedDate().toString("dd/MM/yyyy")
        if not fecha_str:
            QMessageBox.warning(self, "Validación", "Debe seleccionar una fecha válida.")
            return

        # Aquí, por ahora, solo imprime los datos y acepta la ventana
        print("Tratamiento registrado con datos:")
        print(f"Tratamiento: {self.tratamiento_combo.currentText()}")
        print(f"Costo: {self.costo_edit.text()}")
        print(f"Descripción: {self.descripcion_edit.toPlainText()}")
        print(f"Fecha: {fecha_str}")
        print(f"Estado: {self.estado_combo.currentText()}")
        print(f"Carnet Doctor: {self.doctor_carnet_edit.text()}")
        print(f"{self.doctor_nombre_label.text()}")

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
