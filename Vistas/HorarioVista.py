from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
                            QWidget, QLabel, QLineEdit, QPushButton, 
                            QTextEdit, QGroupBox, QFormLayout, QMessageBox,
                            QDialog, QDialogButtonBox, QInputDialog, QComboBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from datetime import datetime
from typing import List

class Doctor:
    def __init__(self, id_doctor: str, nombre: str, especialidad: str):
        self.id_doctor = id_doctor
        self.nombre = nombre
        self.especialidad = especialidad
    
    def __str__(self):
        return f"{self.nombre} ({self.especialidad})"

class Horario:
    def __init__(self, id_horario: str, dia: str, hora_inicio: str, hora_fin: str, doctor: Doctor):
        self.id_horario = id_horario
        self.dia = dia
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.doctor = doctor
        self.disponible = True

    def __str__(self):
        status = "✅ Disponible" if self.disponible else "❌ Ocupado"
        return (f"🆔 ID Horario: {self.id_horario}\n"
                f"📅 Día: {self.dia} | ⏰ {self.hora_inicio} - {self.hora_fin}\n"
                f"👨‍⚕️ Médico: {self.doctor}\n"
                f" {status}\n"
                )
    def horario_ocupado(self, otro_horario):
        if self.doctor.id_doctor != otro_horario.doctor.id_doctor or self.dia != otro_horario.dia:
            return False
        def hora_a_minutos(hora):
            h, m = map(int, hora.split(':'))
            return h * 60 + m
    
        inicio1 = hora_a_minutos(self.hora_inicio)
        fin1 = hora_a_minutos(self.hora_fin)
        inicio2 = hora_a_minutos(otro_horario.hora_inicio)
        fin2 = hora_a_minutos(otro_horario.hora_fin)

        return max (inicio1, inicio2) < min (fin1, fin2)

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
        
        #  seleccionar doctor
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
        self.btn_agregar.clicked.connect(self.agregar_horario)
        self.btn_agregar.setStyleSheet("background: #2ecc71;")
        
        self.btn_eliminar = QPushButton("🗑️ Eliminar")
        self.btn_eliminar.clicked.connect(self.eliminar_horario)
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
         
    def agregar_horario(self):
        dialog = AgregarHorarioDialog(self.doctores, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                datos = dialog.get_data()

    #validaciones
                if not all(datos.values()):
                    QMessageBox.warning(self, "Error", "Todos los campos son obligatorios")
                    return   
                datetime.strptime(datos['hora_inicio'], "%H:%M")
                datetime.strptime(datos['hora_fin'], "%H:%M")
        
                if any(h.id_horario == datos['id_horario'] for h in self.horarios):
                    QMessageBox.warning(self, "Error", "El ID de horario ya existe")
                    return
        
                nuevo_horario = Horario(**datos)
                for horario_existente in self.horarios:
                    if nuevo_horario.horario_ocupado(horario_existente):
                        QMessageBox.warning(self, "Error", "El horario ya está ocupado")
                        return
                self.horarios.append(nuevo_horario)
                self.actualizar_lista()
                QMessageBox.information(self, "Éxito", "Horario agregado correctamente")
            except ValueError as e:
                QMessageBox.warning(self, "Error", f"formato de hora invalido: {str(e)}")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error al agregar horario: {str(e)}")
    
    def eliminar_horario(self):
        """Elimina un horario existente"""
        if not self.horarios:
            QMessageBox.warning(self, "Error", "No hay horarios registrados")
            return
        
        items = [f"{h.id_horario} | {h.dia} {h.hora_inicio}-{h.hora_fin} (Dr. {h.doctor.nombre})" 
                for h in self.horarios]
        
        item, ok = QInputDialog.getItem(
            self, "Eliminar Horario", 
            "Seleccione un horario a eliminar:", items, 0, False
        )
        
        if ok and item:
            id_horario = item.split(" | ")[0]
            
            confirm = QMessageBox.question(
                self, "Confirmar",
                f"¿Eliminar el horario {id_horario}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if confirm == QMessageBox.StandardButton.Yes:
                self.horarios = [h for h in self.horarios if h.id_horario != id_horario]
                self.actualizar_lista()
                QMessageBox.information(self, "Éxito", "Horario eliminado")
    
    def actualizar_lista(self):
        self.resultados.clear()
        if not self.horarios:
            self.resultados.setPlainText("No hay horarios registrados")
            return
        # agrupar horarios por dia para q se vea ordenado
        horarios_por_dia = {}
        for horario in sorted(self.horarios, key=lambda h: h.dia):
            if horario.dia not in horarios_por_dia:
                horarios_por_dia[horario.dia] = []
            horarios_por_dia[horario.dia].append(horario)

        for dia, horarios in horarios_por_dia.items():
            self.resultados.append(f"\n📅 {dia.upper()}")
            self.resultados.append("━━━━━━━━━━━━━━━━━━━━━━━")
            for horario in sorted(horarios, key=lambda h: h.hora_inicio):
                self.resultados.append(str(horario))
#evidentemente son ejemplos de doctores vea, luego vemos los del sql 
def cargar_doctores():
    """Función de ejemplo para cargar doctores"""
    return [
        Doctor("D001", "Dra. Pérez", "Odontología"),
        Doctor("D002", "Dr. Gómez", "Ortodoncia"),
        Doctor("D003", "Dra. Martínez", "Cirugía Maxilofacial")
    ]

if __name__ == "__main__":
    app = QApplication([])
    
    doctores = cargar_doctores()
    
    window = HorarioWindow(doctores)
    window.show()
    app.exec()
