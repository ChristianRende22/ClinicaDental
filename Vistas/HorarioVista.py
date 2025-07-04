from PyQt6.QtWidgets import (QApplication,QMainWindow, QVBoxLayout, QHBoxLayout,
                            QWidget, QLabel, QLineEdit, QPushButton, 
                            QTextEdit, QFormLayout, QMessageBox,
                            QDialog, QDialogButtonBox, QInputDialog, QComboBox)
from PyQt6.QtCore import Qt
from typing import List
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Modelos.DoctorModelo import Doctor

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

        self.configurar_ui()
    
    def configurar_ui(self):
        layout = QFormLayout()  
        # Campos del formulario
        self.id_edit = QLineEdit()
        self.dia_edit = QLineEdit()
        self.hora_inicio_edit = QLineEdit()
        self.hora_fin_edit = QLineEdit()
        # ComboBox para seleccionar doctor
        self.doctor_combo = QComboBox()
        for doctor in self.doctores:
            self.doctor_combo.addItem(f"{doctor.id_doctor} - {doctor.nombre}", doctor) 
        layout.addRow("🆔 ID Horario:", self.id_edit)
        layout.addRow("🗓️ Día:", self.dia_edit)
        layout.addRow("⏰ Hora Inicio (HH:MM):", self.hora_inicio_edit)
        layout.addRow("⏳ Hora Fin (HH:MM):", self.hora_fin_edit)
        layout.addRow("👨‍⚕️ Médico:", self.doctor_combo)
        
        # Botones
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



class HorarioView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🕒 Gestión de horarios")
        self.setGeometry(100, 100, 900, 700)
        self.configurar_ui()
        
        # Referencias a los controladores (se estableceran desde el controlador)
        self.controlador = None
    
    def configurar_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Titulo
        titulo = QLabel("🕒 Gestión de horarios médicos")
        titulo.setStyleSheet("font-size: 24px; font-weight: bold; color: #10b8b9;")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)
        
        # Botones
        btn_container = QHBoxLayout()
        
        self.btn_agregar = QPushButton("➕ Agregar")
        self.btn_agregar.setStyleSheet("background: #2ecc71;")
        
        self.btn_eliminar = QPushButton("🗑️ Eliminar")
        self.btn_eliminar.setStyleSheet("background: #e74c3c; color: white;")
        
        btn_container.addWidget(self.btn_agregar)
        btn_container.addWidget(self.btn_eliminar)
        layout.addLayout(btn_container)
        
        # Lista de horarios
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
    
    def conectar_controlador(self, controlador):
        #Conecta los botones con el controlador
        self.controlador = controlador
        self.btn_agregar.clicked.connect(self.controlador.agregar_horario)
        self.btn_eliminar.clicked.connect(self.controlador.eliminar_horario)
    
    def mostrar_dialogo_agregar(self, doctores: List[Doctor]):
        #Muestra el dialogo para agregar horario
        dialog = AgregarHorarioDialog(doctores, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            return dialog.get_data()
        return None
    
    def mostrar_dialogo_eliminar(self, horarios_info: List[str]):
        #Muestra el dialogo para eliminar horario
        if not horarios_info:
            self.mostrar_mensaje("Error", "No hay horarios registrados")
            return None
        item, ok = QInputDialog.getItem(
            self, "Eliminar Horario", 
            "Seleccione un horario a eliminar:", horarios_info, 0, False)
        if ok and item:
            id_horario = item.split(" | ")[0]
            
            confirm = QMessageBox.question(
                self, "Confirmar",
                f"¿Eliminar el horario {id_horario}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            
            if confirm == QMessageBox.StandardButton.Yes:
                return id_horario
        
        return None
    
    def actualizar_lista_horarios(self, horarios_por_dia: dict):
        #Actualiza la lista de horarios en la interfaz
        self.resultados.clear()
        
        if not horarios_por_dia:
            self.resultados.setPlainText("No hay horarios registrados")
            return
        
        for dia, horarios in horarios_por_dia.items():
            self.resultados.append(f"\n📅 {dia.upper()}")
            self.resultados.append("━━━━━━━━━━━━━━━━━━━━━━━")
            for horario in sorted(horarios, key=lambda h: h.hora_inicio):
                self.resultados.append(str(horario))
    
    def mostrar_mensaje(self, titulo: str, mensaje: str, tipo: str = "info"):
        #Muestra un mensaje al usuario
        if tipo == "error":
            QMessageBox.warning(self, titulo, mensaje)
        elif tipo == "success":
            QMessageBox.information(self, titulo, mensaje)
        else:
            QMessageBox.information(self, titulo, mensaje)
    
    def obtener_info_horarios_para_eliminar(self, horarios):
        #Genera la lista de información de horarios para el diálogo de eliminación
        return [f"{h.id_horario} | {h.dia} {h.hora_inicio}-{h.hora_fin} (Dr. {h.doctor.nombre})" 
                for h in horarios]
if __name__ == "__main__":
    app = QApplication(sys.argv)
    vista = HorarioView()
    vista.show()
    sys.exit(app.exec())