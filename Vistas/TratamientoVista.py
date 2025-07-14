import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QVBoxLayout, QLabel, QLineEdit, 
    QTextEdit, QComboBox, QPushButton, QDateEdit,
    QDialogButtonBox, QHBoxLayout, QMessageBox
)
from PyQt6.QtCore import QDate

from Vistas.DoctorVista import DoctorWindow
from Controladores.DoctorControlador import ControladorDoctor

class AgregarTratamientoDialog(QDialog):
    def __init__(self, controlador=None):
        super().__init__()
        self.controlador = controlador

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
        """)

        form = QFormLayout()
        
        tratamiento_label = QLabel(f"Ingresa los datos: ")
        tratamiento_label.setStyleSheet("color: #10b8b9; font-weight: bold; font-size: 16px;")
        form.addRow(tratamiento_label)

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
        self.estado_combo.addItems(['Pendiente', 'En Progreso', 'Finalizado'])
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
        if self.controlador:
            resultado = self.controlador.verificar_doctor(carnet)
            return resultado is not None
        return False
        
    def mostrar_mensaje(self, titulo, mensaje):
        QMessageBox.warning(self, titulo, mensaje)
        
    def mostrar_nombre_doctor(self, texto):
        self.doctor_nombre_label.setText(texto)
        
    def preguntar_registro_doctor(self):
        respuesta = QMessageBox.question(self, "Doctor no existe", "El doctor no existe. ¿Desea registrar uno nuevo?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        return respuesta == QMessageBox.StandardButton.Yes

    def abrir_registro_doctor(self):
        self.registro_doctor_window = DoctorWindow()
        self.controlador_doctor = ControladorDoctor(self.registro_doctor_window)
        self.registro_doctor_window.show()

    def on_accepted(self):
        descripcion = self.descripcion_edit.toPlainText()
        costo_text = self.costo_edit.text().replace("$", "")
        try:
            costo = float(costo_text)
        except ValueError:
            costo = 0

        fecha = self.fecha_edit.date()
        estado = self.estado_combo.currentText()
        carnet_doctor = self.doctor_carnet_edit.text().strip()

        if not self.verificar_doctor():
            self.mostrar_mensaje("Error", "Doctor no válido o no registrado.")
            return

        if not self.controlador.validar_datos(descripcion, costo, fecha, estado, carnet_doctor):
            return

        fecha_str = fecha.toString("yyyy-MM-dd") + " 00:00:00"

        id_tratamiento = self.controlador.guardar_tratamiento(
            descripcion=descripcion,
            costo=costo,
            fecha=fecha_str,
            estado=estado,
            carnet_doctor=carnet_doctor
        )

        if id_tratamiento:
            self.mostrar_mensaje("Éxito", f"Tratamiento registrado con ID: {id_tratamiento}")
            self.accept()
        else:
            self.mostrar_mensaje("Error", "No se pudo registrar el tratamiento.")
