import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
    QWidget, QLabel, QLineEdit, QPushButton,
    QTextEdit, QFormLayout, QMessageBox,
    QDialog, QDialogButtonBox, QInputDialog, QComboBox
)
from PyQt6.QtCore import Qt
from typing import List
from Controladores.HorarioControlador import HorarioController
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
            self.doctor_combo.addItem(f"{doctor.nombre} {doctor.apellido}", doctor) 
        
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
            'doctor': self.doctor_combo.currentData() # Esto devuelve el objeto Doctor
        }

class HorarioView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🕒 Gestión de horarios")
        self.setGeometry(100, 100, 900, 700)
        
        # Color scheme 
        self.colors = {
            'primary': '#130760',      # Dark blue-purple 
            'secondary': '#756f9f',    # Medium purple
            'accent': '#10b8b9',       # Teal
            'background': '#f7f8fa',   # cambio
            'surface': "#fffdfd",      # cambio
            'text_light': "#000000",   # White text
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
            
            QDateTimeEdit {{ # Aunque no se usa directamente en Horario, se mantiene por consistencia.
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
        # 1.crear la interfaz (sin conexiones)
        self.configurar_ui()
        # 2. crear el controlador, pasandose a sí misma
        self.controlador = HorarioController(self)
        # 3. conectar los botones después de crear el controlador
        self.conectar_botones()
    
    def configurar_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        # Titulo
        titulo = QLabel("🕒 Gestión de horarios médicos")
        titulo.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {self.colors['accent']};")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)
        # Botones
        btn_container = QHBoxLayout()
        self.btn_agregar = QPushButton("➕ Agregar Horario") 
        self.btn_eliminar = QPushButton("🗑️ Eliminar Horario") 
        btn_container.addWidget(self.btn_agregar)
        btn_container.addWidget(self.btn_eliminar)
        layout.addLayout(btn_container)
        # Lista de horarios
        self.resultados = QTextEdit()
        self.resultados.setReadOnly(True)
        self.resultados.setStyleSheet(f"""
            QTextEdit {{
                background: {self.colors['surface']};
                color: {self.colors['text_dark']};
                border: 2px solid {self.colors['secondary']};
                border-radius: 8px;
                font-family: 'Consolas';
                font-size: 13px;
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
        layout.addWidget(QLabel("📋 Horarios Registrados:"))
        layout.addWidget(self.resultados)
    
    def conectar_botones(self):
        """Conecta los botones con los métodos del controlador."""
        self.btn_agregar.clicked.connect(self.controlador.agregar_horario)
        self.btn_eliminar.clicked.connect(self.controlador.eliminar_horario)
    
    def actualizar_combos(self, doctores: List[Doctor]):
        """Método para que el controlador actualice los combos.
        En este caso, el combo de doctores está en el diálogo, pero este método es para consistencia."""
        pass 
    
    def mostrar_dialogo_agregar(self, doctores: List[Doctor]):
        """Muestra el diálogo para agregar horario y retorna los datos."""
        dialog = AgregarHorarioDialog(doctores, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            return dialog.get_data()
        return None
    
    def mostrar_dialogo_eliminar(self, horarios_info: List[str]):
        """Muestra el diálogo para eliminar horario y retorna el ID seleccionado."""
        if not horarios_info:
            QMessageBox.information(self, "ℹ️ Información", "No hay horarios registrados para eliminar.")
            return None
        item, ok = QInputDialog.getItem(
            self, "Eliminar Horario", 
            "Seleccione un horario a eliminar:", horarios_info, 0, False)
        
        if ok and item:
            id_horario = item.split(" | ")[0] # Extrae el ID del string
            
            confirm = QMessageBox.question(
                self, "Confirmar Eliminación", 
                f"¿Está seguro que desea eliminar el horario con ID: {id_horario}?", 
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if confirm == QMessageBox.StandardButton.Yes:
                return id_horario
        return None
    
    def actualizar_lista_horarios(self, horarios_por_dia: dict):
        """Actualiza la lista de horarios en la interfaz."""
        self.resultados.clear()
        
        if not horarios_por_dia:
            self.resultados.setPlainText("No hay horarios registrados.")
            return
        
        for dia, horarios in horarios_por_dia.items():
            self.resultados.append(f"\n📅 {dia.upper()}")
            self.resultados.append("━━━━━━━━━━━━━━━━━━━━━━━")
            for horario in sorted(horarios, key=lambda h: h.hora_inicio):
                self.resultados.append(str(horario))
    
    def obtener_info_horarios_para_eliminar(self, horarios):
        """Genera la lista de información de horarios para el diálogo de eliminación."""
        return [f"{h.id_horario} | {h.dia} {h.hora_inicio}-{h.hora_fin} (Dr. {h.doctor.nombre} {h.doctor.apellido})"
                for h in horarios]

def main():
    app = QApplication(sys.argv)
    window = HorarioView()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
