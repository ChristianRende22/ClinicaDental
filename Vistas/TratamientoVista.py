import sys
from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QDoubleSpinBox, 
    QSpinBox, QPushButton, QDialogButtonBox, QApplication
)

# ----------------------- Clases base -----------------------

class Paciente:
    def __init__(self, id_paciente, nombre, apellido, edad, genero, telefono, correo, direccion):
        self.id_paciente = id_paciente
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.genero = genero
        self.telefono = telefono
        self.correo = correo
        self.direccion = direccion

    def __str__(self):
        return f"{self.nombre} {self.apellido}, {self.edad} años"

class Doctor:
    def __init__(self, nombre, apellido):
        self.nombre = nombre
        self.apellido = apellido

    def __str__(self):
        return f"Dr. {self.nombre} {self.apellido}"

class Tratamiento:
    def __init__(self, id_tratamiento, descripcion, costo, fecha, estado, doctor, paciente):
        self.id_tratamiento = id_tratamiento
        self.descripcion = descripcion
        self.costo = costo
        self.fecha = fecha
        self.estado = estado
        self.doctor = doctor
        self.paciente = paciente

    def __str__(self):
        return (f"Tratamiento ID: {self.id_tratamiento} \n " 
                f"Descripción: '{self.descripcion}' \n "
                f"Costo: ${self.costo:,.2f} \n " 
                f"Fecha de realización: {self.fecha} \n " 
                f"Estado: '{self.estado}' \n "
                f"Doctor: {self.doctor} \n " 
                f"Paciente: {self.paciente.nombre} {self.paciente.apellido})")

# ----------------------- Ventana de Tratamiento -----------------------

class AgregarTratamientoDialog(QDialog):
    def __init__(self, paciente, parent=None):
        super().__init__(parent)
        self.paciente = paciente

        self.setWindowTitle("🩺 Agregar Tratamiento")
        self.resize(450, 370)
        
        # Updated styling to match the main application
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
        
        # Patient info label
        patient_label = QLabel(f"Paciente: {paciente.nombre} {paciente.apellido}")
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
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        main = QVBoxLayout()
        main.addLayout(form)
        main.addWidget(buttons)
        self.setLayout(main)

    def get_tratamiento(self):
        doctor = Doctor(self.doctor_nombre_edit.text(), self.doctor_apellido_edit.text())
        return Tratamiento(
            id_tratamiento=self.id_edit.text(),
            descripcion=self.descripcion_edit.toPlainText(),
            costo=self.costo_edit.value(),
            fecha=self.fecha_edit.text(),
            estado=self.estado_edit.text(),
            doctor=doctor,
            paciente=self.paciente
        )

# ----------------------- Prueba -----------------------

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    paciente_demo = Paciente(
        id_paciente=1,
        nombre="Laura",
        apellido="Pérez",
        edad=27,
        genero="Femenino",
        telefono="7012-3456",
        correo="laura.perez@example.com",
        direccion="Santa Tecla"
    )

    dialog = AgregarTratamientoDialog(paciente_demo)

    if dialog.exec():
        tratamiento = dialog.get_tratamiento()
        print("Tratamiento registrado:")
        print(tratamiento)

    sys.exit(app.exec())