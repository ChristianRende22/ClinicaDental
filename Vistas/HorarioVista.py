from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout,
                               QWidget, QLabel, QLineEdit, QPushButton, 
                               QTextEdit, QGroupBox, QFormLayout, QDialog, 
                               QDialogButtonBox, QInputDialog, QComboBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QMessageBox
from typing import List
from modelo import Doctor, Horario

class AgregarHorarioDialog(QDialog):
    def __init__(self, doctores: List[Doctor], parent=None):
        super().__init__(parent)
        self.doctores = doctores
        self.setWindowTitle("➕ Agregar Horario")
        self.setModal(True)
        self.resize(500, 400)
        
        self.setStyleSheet("""
            QDialog { background: #2b2b2b; color: white; font-family: 'Segoe UI'; }
            QLabel { color: #10b8b9; font-weight: bold; }
            QLineEdit, QComboBox {
                background: #3c3c3c; color: white; border: 2px solid #756f9f;
                border-radius: 6px; padding: 8px;
            }
            QPushButton {
                background: #756f9f; color: white; padding: 10px 15px;
                border-radius: 8px; min-width: 120px;
            }
            QPushButton:hover { background: #10b8b9; }
        """)

        layout = QFormLayout()
        
        # form
        self.id_edit = QLineEdit()
        self.dia_edit = QLineEdit()
        self.hora_inicio_edit = QLineEdit()
        self.hora_fin_edit = QLineEdit()
        
        # seleccionar doctor
        self.doctor_combo = QComboBox()
        for doctor in self.doctores:
            self.doctor_combo.addItem(f"{doctor.id_doctor} - {doctor.nombre}", doctor)
        
        layout.addRow(" ID Horario:", self.id_edit)
        layout.addRow("🗓️ Día:", self.dia_edit)
        layout.addRow("⏰ Hora Inicio (HH:MM):", self.hora_inicio_edit)
        layout.addRow("⏳ Hora Fin (HH:MM):", self.hora_fin_edit)
        layout.addRow("👨‍⚕️ Médico:", self.doctor_combo)
        
        # botones
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addWidget(buttons)
        self.setLayout(main_layout)
    
    def get_data(self):
        return {
            'id_horario': self.id_edit.text().strip(),
            'dia': self.dia_edit.text().strip(),
            'hora_inicio': self.hora_inicio_edit.text().strip(),
            'hora_fin': self.hora_fin_edit.text().strip(),
            'doctor': self.doctor_combo.currentData()
        }

class HorarioWindow(QMainWindow):
    def __init__(self, doctores: List[Doctor]):
        super().__init__()
        self.doctores = doctores
        self.horarios: List[Horario] = []
        
        self.setWindowTitle("🕒 Gestión de horarios")
        self.setGeometry(100, 100, 900, 700)
        
        self.configurar_ui()
        
    def configurar_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        titulo = QLabel("🕒 Gestión de horarios médicos")
        titulo.setStyleSheet("font-size: 24px; font-weight: bold; color: #10b8b9;")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)
        
        # botones
        btn_container = QHBoxLayout()
        
        self.btn_agregar = QPushButton("➕ Agregar")
        self.btn_agregar.setStyleSheet("background: #2ecc71;")
        
        self.btn_eliminar = QPushButton("🗑️ Eliminar")
        self.btn_eliminar.setStyleSheet("background: #e74c3c; color: white;")
        
        btn_container.addWidget(self.btn_agregar)
        btn_container.addWidget(self.btn_eliminar)
        layout.addLayout(btn_container)
        # lista de horarios
        self.resultados = QTextEdit()
        self.resultados.setReadOnly(True)
        self.resultados.setStyleSheet("""
            QTextEdit {
                background: #1e1e1e;
                color: #f0f0f0;
                border: 2px solid #756f9f;
                border-radius: 8px;
                font-family: 'Consolas';
                font-size: 13px;
            }
        """)
        layout.addWidget(QLabel("📋 Horarios Registrados:"))
        layout.addWidget(self.resultados)

    def mostrar_mensaje(self, titulo: str, mensaje: str):
        QMessageBox.information(self, titulo, mensaje)

    def mostrar_error(self, titulo: str, mensaje: str):
        QMessageBox.warning(self, titulo, mensaje)

    def actualizar_lista(self, horarios: List[Horario]):
        self.resultados.clear()
        if not horarios:
            self.resultados.setPlainText("No hay horarios registrados")
            return
        # agrupar horarios por dia para que se vea ordenado
        horarios_por_dia = {}
        for horario in sorted(horarios, key=lambda h: h.dia):
            if horario.dia not in horarios_por_dia:
                horarios_por_dia[horario.dia] = []
            horarios_por_dia[horario.dia].append(horario)

        for dia, horarios in horarios_por_dia.items():
            self.resultados.append(f"\n📅 {dia.upper()}")
            self.resultados.append("━━━━━━━━━━━━━━━━━━━━━━━")
            for horario in sorted(horarios, key=lambda h: h.hora_inicio):
                self.resultados.append(str(horario))
