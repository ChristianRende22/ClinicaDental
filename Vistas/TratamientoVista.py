import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QVBoxLayout, QLabel, QLineEdit, 
    QTextEdit, QDoubleSpinBox, QDialogButtonBox, QApplication
    )

from Controladores.TratamientoControlador import TratamientoControlador
from Modelos.TratamientoModelo import Paciente

class AgregarTratamientoDialog(QDialog):
    def __init__(self, paciente):
        super().__init__()
        self.paciente = paciente  
        self.controlador = TratamientoControlador(self)

        self.setWindowTitle("🩺 Agregar Tratamiento")
        self.resize(450, 370)
        
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
            QLineEdit, QTextEdit, QDoubleSpinBox {
                background: white; 
                color: #2c2c2c; 
                border: 2px solid #756f9f;
                border-radius: 6px; 
                padding: 8px;
            }
            QLineEdit:focus, QTextEdit:focus, QDoubleSpinBox:focus {
                border-color: #10b8b9;
                background-color: #fdfcf8;
            }
            QPushButton {
                background: #756f9f; 
                color: white; 
                padding: 10px 15px;
                border-radius: 8px; 
                font-weight: bold;
                border: none;
            }
            QPushButton:hover { 
                background: #10b8b9; 
            }
        """)

        form = QFormLayout()
        
        patient_label = QLabel(f"Paciente: {self.paciente.nombre} {self.paciente.apellido}")
        patient_label.setStyleSheet("color: #10b8b9; font-weight: bold; font-size: 16px;")
        form.addRow(patient_label)

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

        form.addRow("ID Tratamiento:", self.id_edit)
        form.addRow("Descripción:", self.descripcion_edit)
        form.addRow("Costo:", self.costo_edit)
        form.addRow("Fecha:", self.fecha_edit)
        form.addRow("Estado:", self.estado_edit)
        form.addRow("Nombre Doctor:", self.doctor_nombre_edit)
        form.addRow("Apellido Doctor:", self.doctor_apellido_edit)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.on_accepted)
        buttons.rejected.connect(self.reject)

        main = QVBoxLayout()
        main.addLayout(form)
        main.addWidget(buttons)
        self.setLayout(main)

    def on_accepted(self):
        tratamiento = self.controlador.crear_tratamiento(
            id_tratamiento=self.id_edit.text(),
            descripcion=self.descripcion_edit.toPlainText(),
            costo=self.costo_edit.value(),
            fecha=self.fecha_edit.text(),
            estado=self.estado_edit.text(),
            doctor_nombre=self.doctor_nombre_edit.text(),
            doctor_apellido=self.doctor_apellido_edit.text(),
            paciente=self.paciente
        )
        print("Tratamiento registrado:")
        print(tratamiento)
        self.accept()

def main():
    app = QApplication([])

    paciente = Paciente(
        id_paciente="001",
        nombre="Ana",
        apellido="Gómez",
        edad=30,
        genero="Femenino",
        telefono="123456789",
        correo="ana@gmail.com",
        direccion="Calle Falsa 123"
    )    

    window = AgregarTratamientoDialog(paciente)  # Pasar el paciente como parámetro
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
